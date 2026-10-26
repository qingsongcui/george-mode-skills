import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj
plan = module('plan_check', ROOT/'skills/george-orchestrate/tools/check_plan.py')
package = module('package_check', ROOT/'scripts/verify_package.py')

class Contracts(unittest.TestCase):
    def template(self):
        return json.loads((ROOT/'skills/george-orchestrate/templates/plan.json').read_text())
    def test_unfilled_template_rejected(self):
        self.assertTrue(plan.validate(self.template()))
    def test_outside_write_rejected(self):
        p=self.template(); p['project_root']='/tmp/project'; p['units'][0]['files']=['../other/private.py']
        self.assertTrue(plan.validate(p))
    def test_malformed_unit_returns_error(self):
        p=self.template(); p['project_root']='/tmp/project'; p['units']=[42]
        self.assertTrue(plan.validate(p))
    def test_filled_plan_accepted(self):
        p=self.template(); p['project_root']='/tmp/project'
        self.assertEqual(plan.validate(p),[])
    def test_manifest_cannot_hide_missing_theory(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'PACKAGE-MANIFEST.json').write_text('{"README.md":"fake"}')
            self.assertTrue(any('decision-loop.md' in e for e in package.verify(d)))
    def test_manifest_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'PACKAGE-MANIFEST.json').write_text('{"../outside":"fake"}')
            self.assertTrue(any('escapes' in e for e in package.verify(d)))
