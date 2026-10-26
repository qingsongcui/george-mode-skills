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
    'grok.md': '5999bbea11cef347638b99be2d9bff18ec9f227d70c6b35e0d1ecbef06c679aa',
}


class AntigravityAdapterIsolationTests(unittest.TestCase):
    def test_existing_four_adapters_unchanged(self):
        for name, digest in FROZEN.items():
            path = ADAPTERS / name
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest, name)

    def test_antigravity_adapter_exists_and_is_antigravity_native(self):
        text = (ADAPTERS / 'antigravity.md').read_text()
        self.assertIn('invoke_subagent', text)
        self.assertIn('define_subagent', text)
        self.assertIn('send_message', text)
        self.assertIn('manage_subagents', text)
        self.assertIn('0.3.5', text)
        self.assertIn('不修改 `adapters/codex.md`', text)
        self.assertIn('禁止打开 `codex.md`', text)
        self.assertIn('TypeName: "self"', text)
        self.assertIn('TypeName: "research"', text)
        self.assertIn('Reactive Wakeup', text)

    def test_shared_entries_route_to_antigravity_and_install_gemini_config_skills(self):
        skill = (ROOT / 'skills/george-mode/SKILL.md').read_text()
        orch = (ROOT / 'skills/george-orchestrate/SKILL.md').read_text()
        hosts = (ROOT / 'skills/george-mode/references/hosts.md').read_text()
        install = (ROOT / 'scripts/install.py').read_text()
        linkcheck = (ROOT / 'scripts/linkcheck.py').read_text()
        self.assertIn('adapters/antigravity.md', skill)
        self.assertIn('adapters/antigravity.md', orch)
        self.assertIn('Antigravity', hosts)
        self.assertIn("home / '.gemini/config/skills'", install)
        self.assertIn("Path.home() / '.gemini/config/skills'", linkcheck)

    def test_capability_schema_keeps_empty_catalogs(self):
        schema = json.loads((ADAPTERS / 'antigravity-capability.schema.json').read_text())
        self.assertEqual(schema['properties']['models']['default'], [])
        self.assertEqual(schema['properties']['types']['default'], [])
        self.assertEqual(schema['properties']['tool']['properties']['name']['const'], 'invoke_subagent')
        self.assertEqual(schema['properties']['tool']['properties']['follow_up']['const'], 'send_message')
        self.assertEqual(schema['properties']['tool']['properties']['manage']['const'], 'manage_subagents')
        self.assertEqual(schema['properties']['depth']['properties']['max_nesting']['const'], 1)


if __name__ == '__main__':
    unittest.main()
