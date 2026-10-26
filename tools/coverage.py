#!/usr/bin/env python3
"""Report structural outcome/question coverage; it does NOT measure competence."""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
from pathlib import Path
import yaml


def report(root: Path) -> dict:
    outcomes = {}
    for f in sorted((root / 'knowledge').glob('**/unit.yaml')):
        data = yaml.safe_load(f.read_text(encoding='utf-8'))
        for outcome in data['outcomes']:
            outcomes[outcome['id']] = {'unit': data['id'], 'statement': outcome['statement']}
    counts = defaultdict(int)
    for f in sorted((root / 'assessments').glob('**/questions.yaml')):
        data = yaml.safe_load(f.read_text(encoding='utf-8'))
        for item in data['items']:
            if item['status'] != 'deprecated':
                counts[item['outcome_id']] += 1
    missing = sorted(k for k in outcomes if counts[k] == 0)
    return {
        'outcomes': len(outcomes),
        'covered_outcomes': len(outcomes) - len(missing),
        'uncovered_outcome_ids': missing,
        'question_counts': {k: counts[k] for k in sorted(outcomes)}
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    data = report(args.root.resolve())
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"Question coverage: {data['covered_outcomes']}/{data['outcomes']} outcomes have >=1 non-deprecated item")
        for item in data['uncovered_outcome_ids']:
            print(f'  GAP {item}')
        print('CAUTION: this is structural coverage only; it says nothing about question quality or learning.')
