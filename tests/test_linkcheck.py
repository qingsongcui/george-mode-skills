import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from linkcheck import check_links


class LinkCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.skill = self.root / 'src' / 'george-mode'
        self.skill.mkdir(parents=True)
        (self.skill / 'references').mkdir()
        (self.skill / 'references' / 'hosts.md').write_text('# hosts\n')
        (self.skill / 'SKILL.md').write_text('# skill\n')
        self.host = self.root / 'fake-host' / 'skills'

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, md, text):
        md.write_text(text)
        return check_links(md, self.skill, host_roots=(self.host,))

    def test_in_skill_relative_link_is_ok(self):
        errors = self.check(
            self.skill / 'SKILL.md',
            'see [hosts](references/hosts.md)\n',
        )
        self.assertEqual(errors, [])

    def test_sibling_skill_link_is_ok(self):
        other = self.root / 'src' / 'george-evaluate'
        other.mkdir()
        (other / 'SKILL.md').write_text('# eval\n')
        play = self.skill / 'playbooks'
        play.mkdir()
        errors = self.check(
            play / 'x.md',
            'see [eval](../../george-evaluate/SKILL.md)\n',
        )
        self.assertEqual(errors, [])

    def test_climb_out_of_host_skills_root_is_rejected(self):
        (self.root / 'src' / '使用与验收.md').write_text('# usage\n')
        errors = self.check(
            self.skill / 'SKILL.md',
            'see [usage](../../使用与验收.md)\n',
        )
        self.assertTrue(any(e.startswith('host-lexical-escape:') for e in errors), errors)

    def test_in_skill_symlink_to_outside_target_is_ok(self):
        dest = self.root / 'src' / '使用与验收.md'
        dest.write_text('# usage\n')
        (self.skill / 'references' / '使用与验收.md').symlink_to(dest)
        errors = self.check(
            self.skill / 'SKILL.md',
            'see [usage](references/使用与验收.md)\n',
        )
        self.assertEqual(errors, [])

    def test_missing_file_is_rejected(self):
        errors = self.check(
            self.skill / 'SKILL.md',
            'see [missing](references/nope.md)\n',
        )
        self.assertTrue(any(e.startswith('missing reference:') for e in errors), errors)


if __name__ == '__main__':
    unittest.main(verbosity=2)
