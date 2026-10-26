import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = ROOT / 'skills/george-orchestrate/adapters'
FROZEN = {
    'codex.md': '67801cc4cb1c30f8a9adf4ee1f6f126b209a822831b3d60c0321ddb162bb2f7d',
    'cursor.md': '522a1ebf62619125c5dda8fc92deb5d356e8e328e2228e2728c44a1284426a85',
    'omp.md': '899b545d52a61ac10f20f54bb8a1449fdce53d73ed79dbfdea3f39589d4f1926',
}


class GrokAdapterIsolationTests(unittest.TestCase):
    def test_existing_adapters_unchanged(self):
        for name, digest in FROZEN.items():
            path = ADAPTERS / name
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest, name)

    def test_grok_adapter_exists_and_is_grok_native(self):
        text = (ADAPTERS / 'grok.md').read_text()
        self.assertIn('spawn_subagent', text)
        self.assertIn('0.3.4', text)
        self.assertIn('不修改 `adapters/codex.md`', text)
        self.assertIn('禁止打开 `codex.md`', text)
        self.assertIn('general-purpose', text)
        self.assertIn('explore', text)
        self.assertIn('resume_from', text)
        self.assertIn('深度', text)

    def test_shared_entries_route_to_grok_without_install_host(self):
        skill = (ROOT / 'skills/george-mode/SKILL.md').read_text()
        orch = (ROOT / 'skills/george-orchestrate/SKILL.md').read_text()
        hosts = (ROOT / 'skills/george-mode/references/hosts.md').read_text()
        install = (ROOT / 'scripts/install.py').read_text()
        self.assertIn('adapters/grok.md', skill)
        self.assertIn('adapters/grok.md', orch)
        self.assertIn('Grok CLI', hosts)
        self.assertIn("home / '.agents/skills'", install)
        self.assertNotIn('.grok/skills', install)

    def test_capability_schema_keeps_empty_catalogs(self):
        schema = json.loads((ADAPTERS / 'grok-capability.schema.json').read_text())
        self.assertEqual(schema['properties']['models']['default'], [])
        self.assertEqual(schema['properties']['types']['default'], [])
        self.assertEqual(schema['properties']['tool']['properties']['name']['const'], 'spawn_subagent')
        self.assertEqual(schema['properties']['depth']['properties']['max_nesting']['const'], 1)


if __name__ == '__main__':
    unittest.main()
