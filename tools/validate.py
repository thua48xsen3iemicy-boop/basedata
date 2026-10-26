#!/usr/bin/env python3
"""Bounded, deterministic repository validator. Not a factual/standards auditor."""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path, PurePosixPath
import sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def main(root: Path) -> int:
    failures = []
    units, outcomes, questions, orders = {}, {}, {}, {}

    def error(path, message):
        failures.append(f"{path.relative_to(root) if path.is_relative_to(root) else path}: {message}")

    def load(path):
        try:
            with path.open(encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as exc:
            error(path, f'YAML read failure: {exc}')
            return None

    def check_schema(path, data, name):
        if data is None:
            return False
        schema = json.loads((root / 'contracts' / name).read_text(encoding='utf-8'))
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            error(root / 'contracts' / name, f'invalid schema: {exc}')
            return False
        errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda x: str(x.path))
        for e in errors:
            error(path, f'schema: {".".join(str(x) for x in e.path)}: {e.message}')
        return not errors

    for file in sorted((root/'knowledge').glob('**/unit.yaml')):
        data = load(file)
        if not check_schema(file, data, 'unit.schema.json'): continue
        uid = data['id']
        if uid in units: error(file, f'duplicate unit ID {uid}')
        units[uid] = (file, data)
        for relative_name in ('content_file', 'misconceptions_file','sources_file'):
            sub = file.parent/data[relative_name]
            if not sub.is_file(): error(file, f'missing {relative_name}: {sub}')
        for outcome in data['outcomes']:
            oid = outcome['id']
            if oid in outcomes: error(file, f'duplicate outcome ID {oid}')
            outcomes[oid] = uid
        if data['status'] in ('expert_approved','published'):
            error(file, 'human approval/published requires a separate, implemented approval audit gate (not present in starter)')
        sources = file.parent / data['sources_file']
        if sources.is_file():
            evidence = load(sources)
            if not isinstance(evidence,list) or not evidence:
                error(sources, 'at least one source entry required')
            elif any(not isinstance(s,dict) or not s.get('id') or not str(s.get('url','')).startswith('https://') for s in evidence):
                error(sources, 'source entries must have id and https URL')

    for uid,(file,data) in units.items():
        for pre in data['prerequisites']:
            if pre not in units: error(file, f'missing prerequisite ID {pre}')
            elif pre == uid: error(file, f'unit cannot be its own prerequisite')

    # Detect indirect prerequisite cycles.
    state = {}
    def visit(uid, stack):
        if state.get(uid) == 1:
            error(units[uid][0], 'prerequisite cycle: ' + ' -> '.join(stack+[uid])); return
        if state.get(uid) == 2: return
        state[uid] = 1
        for pre in units[uid][1]['prerequisites']:
            if pre in units: visit(pre, stack+[uid])
        state[uid] = 2
    for uid in units: visit(uid,[])

    for file in sorted((root/'assessments').glob('**/questions.yaml')):
        data = load(file)
        if not check_schema(file, data, 'assessment.schema.json'): continue
        uid = data['unit_id']
        if uid not in units: error(file,f'unknown unit_id {uid}')
        for item in data['items']:
            qid = item['id']; oid = item['outcome_id']
            if qid in questions: error(file,f'duplicate question ID {qid}')
            questions[qid] = True
            if oid not in outcomes: error(file, f'{qid}: unknown outcome {oid}')
            elif outcomes[oid] != uid: error(file, f'{qid}: outcome {oid} belongs to another unit')
            if item['correct_option'] not in item['options']:
                error(file, f'{qid}: correct_option not in options')
            if len(set(item['options'].values())) != len(item['options']):
                error(file, f'{qid}: duplicated option text')
            if item['status'] in ('expert_approved','published'):
                error(file, f'{qid}: human approval gate not implemented')

    for file in sorted((root/'learning-paths').glob('*.yaml')):
        data=load(file)
        if not check_schema(file,data,'path.schema.json'): continue
        for uid in data['unit_ids']:
            if uid not in units: error(file, f'unknown unit {uid}')
        for oid in data['required_outcome_ids']:
            if oid not in outcomes: error(file, f'unknown outcome {oid}')
            elif outcomes[oid] not in data['unit_ids']: error(file, f'{oid} not in selected units')
        if data['status'] in ('expert_approved','published'): error(file,'human approval gate not implemented')

    for file in sorted((root/'curricula').glob('**/*.yaml')):
        data=load(file)
        if not check_schema(file,data,'curriculum.schema.json'):continue
        if data['hours_total'] != sum(m['hours'] for m in data['modules']):
            error(file,'hours_total is not equal to sum of modules[].hours')
        mids=[m['id'] for m in data['modules']]
        if len(mids)!=len(set(mids)): error(file,'duplicate module IDs')
        for mod in data['modules']:
            for oid in mod['outcome_ids']:
                if oid not in outcomes:error(file,f'module {mod["id"]}: unknown outcome {oid}')
        if data['status'] in ('expert_approved','published'): error(file,'human approval gate not implemented')

    # Work orders and compact role-to-role handoffs.
    # These checks are structural; they cannot prove agents in other branches
    # aren't concurrently writing the same file.
    def valid_relative_path(value):
        if not isinstance(value, str) or not value or '\\' in value or value.startswith('/'):
            return False
        components = PurePosixPath(value).parts
        return bool(components) and all(part not in ('.', '..') for part in value.split('/'))

    for file in sorted((root/'work/orders').glob('*/order.yaml')):
        data = load(file)
        if not check_schema(file, data, 'work-order.schema.json'):
            continue
        oid = data['id']
        if oid in orders: error(file, f'duplicate work order ID {oid}')
        if file.parent.name != oid: error(file, f'work order directory does not match ID {oid}')
        orders[oid] = (file, data)
        for path in data['scope']['allowed_paths']:
            if not valid_relative_path(path):
                error(file, f'unsafe allowed_path {path!r}')
        if data.get('model_tier') == 'human' and data['role'] == 'validator':
            # This is allowed; do not bind real assignments to a guessed model policy.
            pass

    for oid, (file, data) in orders.items():
        for dep in data.get('depends_on', []):
            if dep not in orders: error(file, f'unknown work order dependency {dep}')
            if dep == oid: error(file, 'work order depends on itself')

    task_state = {}
    def visit_order(oid, stack):
        if task_state.get(oid) == 1:
            error(orders[oid][0], 'work order dependency cycle: ' + ' -> '.join(stack + [oid]))
            return
        if task_state.get(oid) == 2: return
        task_state[oid] = 1
        for dep in orders[oid][1].get('depends_on', []):
            if dep in orders: visit_order(dep, stack + [oid])
        task_state[oid] = 2
    for oid in orders: visit_order(oid, [])

    for file in sorted((root/'work/handoffs').glob('*/*.yaml')):
        data = load(file)
        if not check_schema(file, data, 'handoff.schema.json'):
            continue
        oid, role = data['task_id'], data['role']
        if file.parent.name != oid or file.stem != role:
            error(file, 'handoff directory/filename must match task_id/role')
        if oid not in orders:
            error(file, f'handoff references unknown work order {oid}')
            continue
        if role != orders[oid][1]['role']:
            # Later roles are allowed when tasks are explicitly reassigned;
            # a work order role describes the initial executor, not all reviewers.
            if role not in ('machine_reviewer', 'validator', 'human_expert', 'release_manager'):
                error(file, f'handoff role {role} differs from assigned role')
        allowed = orders[oid][1]['scope']['allowed_paths']
        for path in data['changed_paths']:
            if not valid_relative_path(path):
                error(file, f'unsafe changed_path {path!r}')
            elif not any(path == a.rstrip('/') or path.startswith(a.rstrip('/') + '/')
                         for a in allowed):
                error(file, f'changed_path outside work order scope: {path}')

    if failures:
        print(f'FAIL: {len(failures)} issue(s)')
        for e in failures:print(' - '+e)
        return 1
    print(f'PASS: {len(units)} units, {len(outcomes)} outcomes, {len(questions)} questions, {len(orders)} work orders; structural references and hours valid')
    print('NOTE: factual correctness, source license, normative compliance, and human approval NOT validated')
    return 0

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=ROOT)
    args=parser.parse_args()
    sys.exit(main(args.root.resolve()))
