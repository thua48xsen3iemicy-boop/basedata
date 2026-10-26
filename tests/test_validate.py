"""Smoke and regression checks for the example repo contracts."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import yaml

BASE = Path(__file__).resolve().parents[1]

class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)/'repo'
        shutil.copytree(BASE, self.repo, ignore=shutil.ignore_patterns('__pycache__', '.git'))

    def run_validator(self):
        return subprocess.run([sys.executable, 'tools/validate.py', '--root', str(self.repo)],cwd=self.repo,text=True,capture_output=True)

    def change_yaml(self, name, change):
        path = self.repo/name
        obj = yaml.safe_load(path.read_text(encoding='utf-8'))
        change(obj)
        path.write_text(yaml.safe_dump(obj,sort_keys=False,allow_unicode=True),encoding='utf-8')

    def test_example_passes(self):
        p=self.run_validator()
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

    def test_missing_prerequisite_fails(self):
        self.change_yaml('knowledge/networking/ipv4/cidr/unit.yaml',lambda d:d['prerequisites'].append('NET.UNKNOWN'))
        p=self.run_validator()
        self.assertNotEqual(p.returncode,0)
        self.assertIn('missing prerequisite',p.stdout)

    def test_wrong_answer_key_fails(self):
        self.change_yaml('assessments/networking/ipv4/cidr/questions.yaml',lambda d:d['items'][0].update(correct_option='Z'))
        p=self.run_validator()
        self.assertNotEqual(p.returncode,0)
        self.assertIn('correct_option not in options',p.stdout)

    def test_hours_mismatch_fails(self):
        self.change_yaml('curricula/examples/example-plan.yaml',lambda d:d.update(hours_total=22))
        p=self.run_validator()
        self.assertNotEqual(p.returncode,0)
        self.assertIn('hours_total is not equal',p.stdout)

    def test_approval_without_audit_fails(self):
        self.change_yaml('knowledge/networking/ipv4/cidr/unit.yaml',lambda d:d.update(status='published'))
        p=self.run_validator()
        self.assertNotEqual(p.returncode,0)
        self.assertIn('human approval',p.stdout)


    def test_unknown_handoff_task_fails(self):
        self.change_yaml('work/handoffs/TASK-DEMO-001/author.yaml', lambda d: d.update(task_id='TASK-UNKNOWN'))
        p = self.run_validator()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('handoff directory/filename must match', p.stdout)

    def test_handoff_scope_violation_fails(self):
        self.change_yaml('work/handoffs/TASK-DEMO-001/author.yaml', lambda d: d.update(changed_paths=['knowledge/linux/']))
        p = self.run_validator()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('outside work order scope', p.stdout)

    def test_handoff_missing_required_fields_fails(self):
        self.change_yaml('work/handoffs/TASK-DEMO-001/author.yaml', lambda d: d.pop('checks_run'))
        p = self.run_validator()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('checks_run', p.stdout)

    def test_work_order_unknown_dependency_fails(self):
        self.change_yaml('work/orders/TASK-DEMO-001/order.yaml', lambda d: d.update(depends_on=['TASK-NO-SUCH']))
        p = self.run_validator()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('unknown work order dependency', p.stdout)

    def test_work_order_unsafe_write_path_fails(self):
        self.change_yaml('work/orders/TASK-DEMO-001/order.yaml', lambda d: d['scope'].update(allowed_paths=['../outside']))
        p = self.run_validator()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('unsafe allowed_path', p.stdout)

    def test_coverage_reports_missing_items(self):
        p = subprocess.run([sys.executable, 'tools/coverage.py', '--json', '--root', str(self.repo)],
                           cwd=self.repo, text=True, capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        import json
        data = json.loads(p.stdout)
        self.assertEqual(data['outcomes'], 4)
        self.assertEqual(data['covered_outcomes'], 1)
        self.assertIn('LO.NET.IPV4.MASK.01', data['uncovered_outcome_ids'])

if __name__=='__main__':
    unittest.main()
