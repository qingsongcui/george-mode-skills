import os
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from linkcheck import check_links, check_navigation, resolve_target, lexical_join


class NavigationAndSymlinkTests(unittest.TestCase):
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

    def check(self, md, check_nested=False):
        return check_links(md, self.skill, host_roots=(self.host,), check_nested=check_nested)

    def test_external_symlink_target_exists_but_body_has_dead_link_fails(self):
        """External symlink target exists, but dead links in its body must be caught and fail."""
        outside_file = self.root / 'outside' / 'usage.md'
        outside_file.parent.mkdir(parents=True)
        outside_file.write_text('see [missing](dead_link.md)\n')

        symlink_file = self.skill / 'references' / '使用与验收.md'
        symlink_file.symlink_to(outside_file)

        errors = self.check(symlink_file)
        self.assertTrue(
            any(e.startswith('missing reference:') and 'dead_link.md' in e for e in errors),
            'Expected dead link inside symlink body to fail, got: %s' % errors
        )

    def test_symlink_resolves_links_relative_to_access_path(self):
        """Links in a symlinked file resolve relative to its access path, not target realpath."""
        outside_file = self.root / 'outside' / 'usage.md'
        outside_file.parent.mkdir(parents=True)
        # hosts.md exists in self.skill/references/hosts.md, but NOT in outside/hosts.md
        outside_file.write_text('see [hosts](hosts.md)\n')

        symlink_file = self.skill / 'references' / '使用与验收.md'
        symlink_file.symlink_to(outside_file)

        errors = self.check(symlink_file)
        self.assertEqual(errors, [], 'Expected access path resolution to find references/hosts.md')

    def test_correct_internal_and_sibling_navigation_passes(self):
        """Correct internal (../SKILL.md) and sibling (../../george-investigate/SKILL.md) links pass."""
        sibling = self.root / 'src' / 'george-investigate'
        sibling.mkdir(parents=True)
        (sibling / 'SKILL.md').write_text('# investigate\n')

        page = self.skill / 'references' / '使用与验收.md'
        page.write_text(
            '# usage\n'
            '- [self](../SKILL.md)\n'
            '- [investigate](../../george-investigate/SKILL.md)\n'
            '- [hosts](hosts.md)\n'
        )

        errors = self.check(page)
        self.assertEqual(errors, [])

    def test_host_lexical_escape_from_symlink_is_rejected(self):
        """Climbing out of host skills root via relative navigation is rejected."""
        page = self.skill / 'references' / 'bad.md'
        page.write_text('see [outside](../../../../escape.md)\n')

        errors = self.check(page)
        self.assertTrue(any(e.startswith('host-lexical-escape:') for e in errors), errors)

    def test_nested_dead_link_detection(self):
        """Transitive navigation detects dead links in linked secondary documents."""
        page_a = self.skill / 'references' / 'a.md'
        page_b = self.skill / 'references' / 'b.md'

        page_a.write_text('see [b](b.md)\n')
        page_b.write_text('see [missing](nonexistent.md)\n')

        errors = check_navigation(page_a, self.skill, host_roots=(self.host,))
        self.assertTrue(
            any(e.startswith('missing reference:') and 'nonexistent.md' in e for e in errors),
            'Expected nested dead link in b.md to be caught, got: %s' % errors
        )

    def test_navigation_cycle_does_not_loop_infinitely(self):
        """Cyclic navigation (A -> B -> A) terminates cleanly without infinite recursion."""
        page_a = self.skill / 'references' / 'a.md'
        page_b = self.skill / 'references' / 'b.md'

        page_a.write_text('see [b](b.md)\n')
        page_b.write_text('see [a](a.md)\n')

        # Should terminate cleanly with 0 errors
        errors = check_navigation(page_a, self.skill, host_roots=(self.host,))
        self.assertEqual(errors, [])

    def test_symlink_loop_is_safely_reported_without_crashing(self):
        """A filesystem symlink cycle is handled safely without raising unhandled exception."""
        loop_a = self.skill / 'references' / 'loop_a.md'
        loop_b = self.skill / 'references' / 'loop_b.md'
        loop_a.symlink_to(loop_b)
        loop_b.symlink_to(loop_a)

        errors = self.check(loop_a)
        self.assertTrue(
            any('symlink loop detected' in e or 'broken symlink' in e for e in errors),
            'Expected symlink loop error, got: %s' % errors
        )

    def test_broken_symlink_is_safely_reported(self):
        """A broken symlink (pointing to non-existent target) is reported cleanly."""
        broken = self.skill / 'references' / 'broken.md'
        broken.symlink_to(self.root / 'does_not_exist.md')

        errors = self.check(broken)
        self.assertTrue(
            any('broken symlink' in e or 'missing reference' in e for e in errors),
            'Expected broken symlink error, got: %s' % errors
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
