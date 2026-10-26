import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL_SCRIPT = ROOT / 'scripts/install.py'


class InstallBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.tmp_home_dir = tempfile.TemporaryDirectory(prefix='george-test-home-')
        self.home = Path(self.tmp_home_dir.name).resolve()
        self.env = dict(os.environ)
        self.env['HOME'] = str(self.home)

    def tearDown(self):
        self.tmp_home_dir.cleanup()

    def run_install(self, *args, root=None):
        cmd = [sys.executable, str(INSTALL_SCRIPT)]
        if root is not None:
            cmd.extend(['--root', str(root)])
        cmd.extend(args)
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=self.env,
        )
        try:
            data = json.loads(proc.stdout) if proc.stdout else {}
        except json.JSONDecodeError:
            data = {}
        return proc.returncode, data, proc.stderr

    def test_fresh_install_preview_and_apply(self):
        # 1. Preview mode (no flags)
        code, data, _ = self.run_install()
        self.assertEqual(code, 0)
        self.assertFalse(data.get('applied'))
        plan = data.get('plan', [])
        # 11 skills * 4 hosts = 44 skill links + 1 OMP command = 45 links
        self.assertEqual(len(plan), 45)

        hosts = [x['host'] for x in plan]
        self.assertEqual(hosts.count('shared'), 11)
        self.assertEqual(hosts.count('codex'), 11)
        self.assertEqual(hosts.count('cursor'), 11)
        self.assertEqual(hosts.count('antigravity'), 11)
        self.assertEqual(hosts.count('omp'), 1)

        for item in plan:
            self.assertEqual(item['action'], 'link')

        # In preview, nothing should exist on disk yet
        omp_target = self.home / '.omp/agent/commands/george-mode.md'
        self.assertFalse(omp_target.exists() or omp_target.is_symlink())
        self.assertFalse((self.home / '.agents/skills').exists())

        # 2. Apply mode
        code, data, _ = self.run_install('--apply')
        self.assertEqual(code, 0)
        self.assertTrue(data.get('applied'))

        # Check all 44 skill targets are valid directory symlinks
        for host, subdir in [('shared', '.agents/skills'), ('codex', '.codex/skills'), ('cursor', '.cursor/skills'), ('antigravity', '.gemini/config/skills')]:
            base = self.home / subdir
            self.assertTrue(base.is_dir())
            for skill_dir in (ROOT / 'skills').iterdir():
                if not (skill_dir / 'SKILL.md').is_file():
                    continue
                dest = base / skill_dir.name
                self.assertTrue(dest.is_symlink(), f"Target {dest} should be a symlink")
                self.assertTrue(dest.is_dir(), f"Target {dest} should point to a directory")
                self.assertEqual(dest.resolve(), skill_dir.resolve())

        # Check OMP command link is a valid file symlink
        self.assertTrue(omp_target.is_symlink())
        self.assertTrue(omp_target.is_file())
        self.assertFalse(omp_target.is_dir())
        self.assertEqual(omp_target.resolve(), (ROOT / 'commands/omp/george-mode.md').resolve())

    def test_idempotent_reinstall(self):
        # Initial install
        code, _, _ = self.run_install('--apply')
        self.assertEqual(code, 0)

        # Re-apply
        code, data, _ = self.run_install('--apply')
        self.assertEqual(code, 0)
        plan = data.get('plan', [])
        self.assertEqual(len(plan), 45)
        for item in plan:
            self.assertEqual(item['action'], 'already-linked')

        # Symlinks should still be valid
        omp_target = self.home / '.omp/agent/commands/george-mode.md'
        self.assertTrue(omp_target.is_symlink())
        self.assertEqual(omp_target.resolve(), (ROOT / 'commands/omp/george-mode.md').resolve())

    def test_remove_only_own_links_and_preserves_foreign_and_broken(self):
        code, _, _ = self.run_install('--apply')
        self.assertEqual(code, 0)

        # Plant foreign artifacts
        foreign_skill_dir = self.home / '.agents/skills/foreign-skill'
        foreign_skill_dir.mkdir(parents=True, exist_ok=True)
        (foreign_skill_dir / 'SKILL.md').write_text('# Foreign')

        foreign_cmd_file = self.home / '.omp/agent/commands/other-cmd.md'
        foreign_cmd_file.parent.mkdir(parents=True, exist_ok=True)
        foreign_cmd_file.write_text('# Other command')

        foreign_symlink = self.home / '.codex/skills/foreign-link'
        foreign_symlink.symlink_to(foreign_skill_dir, target_is_directory=True)

        broken_foreign_link = self.home / '.cursor/skills/broken-foreign-link'
        broken_foreign_link.symlink_to(Path('/tmp/non_existent_foreign_target_xyz'), target_is_directory=True)

        # Remove own links
        code, data, _ = self.run_install('--remove', '--apply')
        self.assertEqual(code, 0)

        # George-mode skill links and OMP command link must be removed
        for subdir in ('.agents/skills', '.codex/skills', '.cursor/skills', '.gemini/config/skills'):
            for skill_dir in (ROOT / 'skills').iterdir():
                if not (skill_dir / 'SKILL.md').is_file():
                    continue
                dest = self.home / subdir / skill_dir.name
                self.assertFalse(dest.exists() or dest.is_symlink(), f"Link {dest} should have been unlinked")

        omp_target = self.home / '.omp/agent/commands/george-mode.md'
        self.assertFalse(omp_target.exists() or omp_target.is_symlink())

        # Foreign files, symlinks, and broken symlinks MUST remain intact
        self.assertTrue(foreign_skill_dir.is_dir())
        self.assertTrue((foreign_skill_dir / 'SKILL.md').is_file())
        self.assertTrue(foreign_cmd_file.is_file())
        self.assertTrue(foreign_symlink.is_symlink())
        self.assertTrue(broken_foreign_link.is_symlink())

    def test_conflict_blocks_globally_without_partial_install(self):
        # Scenario A: Conflict on OMP command target
        omp_target = self.home / '.omp/agent/commands/george-mode.md'
        omp_target.parent.mkdir(parents=True, exist_ok=True)
        omp_target.write_text('# Pre-existing foreign command file')

        code, data, _ = self.run_install('--apply')
        self.assertEqual(code, 2)
        self.assertEqual(data.get('status'), 'blocked-by-existing-path')

        # Global all-or-nothing check: NO skill links should have been created
        for subdir in ('.agents/skills', '.codex/skills', '.cursor/skills', '.gemini/config/skills'):
            base = self.home / subdir
            if base.exists():
                self.assertEqual(list(base.iterdir()), [])

        # Foreign file was not overwritten
        self.assertEqual(omp_target.read_text(), '# Pre-existing foreign command file')

        # Scenario B: Conflict on a skill target
        omp_target.unlink()
        conflict_skill = self.home / '.agents/skills/george-mode'
        conflict_skill.parent.mkdir(parents=True, exist_ok=True)
        conflict_skill.write_text('foreign skill content')

        code, data, _ = self.run_install('--apply')
        self.assertEqual(code, 2)
        self.assertEqual(data.get('status'), 'blocked-by-existing-path')

        # OMP command link was NOT created
        self.assertFalse(omp_target.exists() or omp_target.is_symlink())

    def test_source_missing_fails_closed(self):
        with tempfile.TemporaryDirectory(prefix='mock-repo-') as mock_repo:
            mock_root = Path(mock_repo)
            # Create a mock skills dir
            mock_skill = mock_root / 'skills/mock-skill'
            mock_skill.mkdir(parents=True, exist_ok=True)
            (mock_skill / 'SKILL.md').write_text('# Mock')
            # But do NOT create commands/omp/george-mode.md

            code, data, _ = self.run_install('--apply', root=mock_root)
            self.assertEqual(code, 1)
            self.assertEqual(data.get('status'), 'source-missing')

            # Ensure nothing was installed in HOME
            omp_target = self.home / '.omp/agent/commands/george-mode.md'
            self.assertFalse(omp_target.exists() or omp_target.is_symlink())
            for subdir in ('.agents/skills', '.codex/skills', '.cursor/skills', '.gemini/config/skills'):
                base = self.home / subdir
                if base.exists():
                    self.assertEqual(list(base.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
