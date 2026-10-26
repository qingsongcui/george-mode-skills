"""Check skill markdown links against real files and host lexical roots.

Cursor Read collapses `..` without following the install directory symlink.
A link that climbs out of `~/.cursor/skills/` therefore 404s even when the
real source file exists. Codex and OMP use the same install layout, so the
same relative-link contract keeps all three hosts working.
"""
import os
import re
from pathlib import Path

HOST_SKILL_ROOTS = (
    Path.home() / '.cursor/skills',
    Path.home() / '.codex/skills',
    Path.home() / '.agents/skills',
    Path.home() / '.gemini/config/skills',
)


def lexical_join(base, rel):
    return Path(os.path.normpath(os.path.join(str(base), rel)))


def resolve_target(md_file, target):
    if target.startswith('/'):
        return Path(target)
    # Always resolve target relative to the file's access path (its parent directory)
    return md_file.parent / target


def check_links(md_file, skill_dir, host_roots=HOST_SKILL_ROOTS, check_nested=False, seen=None):
    """Check links in md_file for existence and host lexical boundary containment.

    If md_file is a symlink, links are resolved relative to its access path.
    If check_nested is True, recursively inspects linked local markdown files
    while tracking visited files in `seen` to prevent infinite cycle loops.
    """
    errors = []
    try:
        rel = md_file.relative_to(skill_dir)
    except ValueError:
        # File might be outside skill_dir (e.g. sibling skill target in nested check)
        rel = Path(md_file.name)

    if md_file.is_symlink():
        try:
            target_res = md_file.resolve()
            if not target_res.exists():
                errors.append('broken symlink: %s' % md_file)
                return errors
        except (RuntimeError, OSError) as e:
            errors.append('symlink loop detected: %s (%s)' % (md_file, e))
            return errors

    try:
        text = md_file.read_text()
    except (FileNotFoundError, OSError) as e:
        return ['unreadable file: %s (%s)' % (md_file, e)]

    for link in re.findall(r'\]\(([^)]+)\)', text):
        if '://' in link or link.startswith(('#', 'mailto:')):
            continue
        target = link.split('#')[0]
        if not target:
            continue
        real = resolve_target(md_file, target)
        try:
            exists = real.exists()
        except (RuntimeError, OSError):
            exists = False

        if not exists:
            errors.append('missing reference: %s:%s' % (md_file, link))
        elif real.is_symlink():
            try:
                real.resolve()
            except (RuntimeError, OSError) as e:
                errors.append('symlink cycle: %s:%s (%s)' % (md_file, link, e))

        if target.startswith('/'):
            continue

        for host_root in host_roots:
            advertised = host_root / skill_dir.name / rel
            collapsed = lexical_join(advertised.parent, target)
            try:
                collapsed.relative_to(host_root)
            except ValueError:
                errors.append(
                    'host-lexical-escape: %s:%s -> %s' % (md_file, link, collapsed)
                )

        if check_nested and exists and real.is_file() and real.suffix == '.md':
            if seen is None:
                seen = set()
            try:
                visit_key = str(real.resolve())
            except (RuntimeError, OSError):
                visit_key = str(real)
            if visit_key not in seen:
                seen.add(visit_key)
                # Determine skill directory for nested file if applicable
                nested_skill = skill_dir
                try:
                    real.relative_to(skill_dir)
                except ValueError:
                    if skill_dir.parent and skill_dir.parent in real.parents:
                        for p in real.parents:
                            if p.parent == skill_dir.parent:
                                nested_skill = p
                                break
                errors.extend(
                    check_links(real, nested_skill, host_roots=host_roots, check_nested=True, seen=seen)
                )

    return errors


def check_navigation(entry_file, skill_dir, host_roots=HOST_SKILL_ROOTS, seen=None):
    """Check navigation links from entry_file transitively, detecting nested dead links and avoiding loops."""
    if seen is None:
        seen = set()
    try:
        visit_key = str(entry_file.resolve())
    except (RuntimeError, OSError):
        visit_key = str(entry_file)
    seen.add(visit_key)
    return check_links(entry_file, skill_dir, host_roots=host_roots, check_nested=True, seen=seen)
