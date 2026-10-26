#!/usr/bin/env python3
"""Install George skill and command links; never replace an existing foreign path."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_plan(root=ROOT, home=None, remove=False):
    root = Path(root).resolve()
    if home is None:
        home = Path.home()
    else:
        home = Path(home).resolve()

    skill_targets = {
        'shared': home / '.agents/skills',
        'codex': home / '.codex/skills',
        'cursor': home / '.cursor/skills',
        'antigravity': home / '.gemini/config/skills',
    }
    omp_command_target = home / '.omp/agent/commands/george-mode.md'
    omp_command_source = root / 'commands/omp/george-mode.md'

    plan = []

    def evaluate_entry(host, source, dest):
        same = dest.is_symlink() and dest.resolve() == source.resolve()
        exists = dest.exists() or dest.is_symlink()
        if remove:
            state = 'remove' if same else 'leave'
        elif not source.exists():
            state = 'source-missing'
        elif same:
            state = 'already-linked'
        elif exists:
            state = 'conflict'
        else:
            state = 'link'
        return {'host': host, 'source': str(source), 'target': str(dest), 'action': state}

    skills_dir = root / 'skills'
    if not skills_dir.is_dir():
        for host, base in skill_targets.items():
            plan.append({
                'host': host,
                'source': str(skills_dir),
                'target': str(base),
                'action': 'source-missing' if not remove else 'leave',
            })
    else:
        for host, base in skill_targets.items():
            for source in sorted(skills_dir.iterdir()):
                if not (source / 'SKILL.md').is_file():
                    continue
                dest = base / source.name
                plan.append(evaluate_entry(host, source, dest))

    plan.append(evaluate_entry('omp', omp_command_source, omp_command_target))
    return plan


def apply_plan(plan):
    for x in plan:
        dest = Path(x['target'])
        if x['action'] == 'link':
            dest.parent.mkdir(parents=True, exist_ok=True)
            source = Path(x['source'])
            dest.symlink_to(source, target_is_directory=source.is_dir())
        elif x['action'] == 'remove':
            dest.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Apply planned link or remove operations')
    parser.add_argument('--remove', action='store_true', help='Remove only links pointing to this source repository')
    parser.add_argument('--root', type=Path, default=ROOT, help='Override repository root')
    parser.add_argument('--home', type=Path, default=None, help='Override home directory')
    args = parser.parse_args()

    plan = build_plan(root=args.root, home=args.home, remove=args.remove)

    if any(x['action'] == 'source-missing' for x in plan):
        print(json.dumps({'status': 'source-missing', 'plan': plan}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    if any(x['action'] == 'conflict' for x in plan):
        print(json.dumps({'status': 'blocked-by-existing-path', 'plan': plan}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    if args.apply:
        apply_plan(plan)

    print(json.dumps({'applied': args.apply, 'plan': plan}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
