#!/usr/bin/env python3
"""Check plan contracts, dependencies and conflicting ownership, not behavior."""
import argparse
import json
from pathlib import Path


def validate(plan):
    errors = []
    if not isinstance(plan, dict) or not isinstance(plan.get('units'), list) or not plan['units']:
        return ['plan requires a nonempty units list']
    if plan.get('mode') not in ('plan-only', 'execute'):
        errors.append('mode must be explicit: plan-only or execute')
    root = plan.get('project_root')
    if not isinstance(root, str) or not Path(root).is_absolute():
        return errors + ['project_root must be an absolute path']
    if 'REPLACE_WITH_' in root:
        return errors + ['project_root template is not filled']
    root = Path(root).resolve()
    units = plan['units']
    if any(not isinstance(u, dict) for u in units):
        return errors + ['units must be objects']
    ids = [u.get('id') for u in units]
    if any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
        return errors + ['unit IDs must be unique nonempty strings']
    by_id = dict(zip(ids, units))
    for u in units:
        for key in ('owner', 'deliverable', 'acceptance', 'rollback', 'playbook'):
            if not isinstance(u.get(key), str) or not u[key].strip():
                errors.append(f'{u["id"]}: missing {key}')
        if not isinstance(u.get('files'), list) or not u['files']:
            errors.append(f'{u["id"]}: missing owned paths')
        elif any(not isinstance(p, str) or not p.strip() or any(c in p for c in '*?[') for p in u['files']):
            errors.append(f'{u["id"]}: owned paths must be explicit nonempty paths without globs')
        if isinstance(u.get('files'), list):
            for owned in u['files']:
                if isinstance(owned, str) and not (root / owned).resolve().is_relative_to(root):
                    errors.append(f'{u["id"]}: owned path outside project_root: {owned}')
        deps = u.get('depends_on')
        if not isinstance(deps, list) or any(not isinstance(d, str) or d not in by_id for d in deps):
            errors.append(f'{u["id"]}: invalid dependencies')
        checks = u.get('checks', {})
        if not isinstance(checks, dict) or set(checks) - {'unit', 'live', 'perf'}:
            errors.append(f'{u["id"]}: checks must use unit/live/perf')
            continue
        for level in ('unit', 'live', 'perf'):
            c = checks.get(level, {})
            if not isinstance(c, dict):
                errors.append(f'{u["id"]}: invalid {level} check')
                continue
            if c.get('applicable') is False:
                if not c.get('reason'):
                    errors.append(f'{u["id"]}: {level} needs exclusion reason')
            elif c.get('applicable') is not True or not all(c.get(k) for k in ('method', 'pass_when', 'evidence')):
                errors.append(f'{u["id"]}: {level} needs method, predicate and evidence')
        if not any(c.get('applicable') is True for c in checks.values() if isinstance(c, dict)):
            errors.append(f'{u["id"]}: no verification')
    if errors:
        return errors
    visiting, visited, ancestors = set(), set(), {}

    def visit(identity):
        if identity in visiting:
            raise ValueError('dependency cycle at ' + identity)
        if identity in visited:
            return ancestors[identity]
        visiting.add(identity)
        deps = set()
        for dep in by_id[identity]['depends_on']:
            deps.add(dep)
            deps.update(visit(dep))
        visiting.remove(identity)
        visited.add(identity)
        ancestors[identity] = deps
        return deps

    try:
        for identity in ids:
            visit(identity)
    except ValueError as exc:
        return [str(exc)]
    for i, a in enumerate(units):
        for b in units[i+1:]:
            ordered = a['id'] in ancestors[b['id']] or b['id'] in ancestors[a['id']]
            for p in a['files']:
                for q in b['files']:
                    pp, qq = (root / p).resolve(), (root / q).resolve()
                    overlap = pp == qq or pp in qq.parents or qq in pp.parents
                    if overlap and not ordered:
                        errors.append(f'{a["id"]}/{b["id"]}: unordered shared write path {p} / {q}')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    problems = validate(json.loads(args.plan.read_text()))
    print(json.dumps({'pass': not problems, 'errors': problems, 'scope': 'structure only'}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(problems))
