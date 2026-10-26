#!/usr/bin/env python3
"""Verify a standalone George release using only the standard library."""
import hashlib
import json
from pathlib import Path


def verify(root):
    root = Path(root).resolve()
    errors = []
    try:
        entries = json.loads((root / 'PACKAGE-MANIFEST.json').read_text())
        if not isinstance(entries, dict) or not entries:
            return ['manifest must be a nonempty object']
    except (OSError, ValueError) as exc:
        return ['manifest unavailable: ' + str(exc)]
    required = ['scripts/install.py', 'scripts/verify_package.py', 'skills/george-mode/SKILL.md']
    required += ['skills/george-mode/references/' + name for name in
                 ['decision-loop.md', 'verify-before-deliver.md', 'theory.md']]
    required += ['skills/george-orchestrate/adapters/' + host + '.md' for host in ['codex', 'cursor', 'omp', 'grok', 'antigravity']]
    for name in required:
        if name not in entries:
            errors.append('required file absent from manifest: ' + name)
    for name, digest in entries.items():
        path = root / name
        if Path(name).is_absolute() or not path.resolve().is_relative_to(root):
            errors.append('path escapes package: ' + name)
            continue
        try:
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                errors.append('hash mismatch: ' + name)
        except OSError:
            errors.append('missing file: ' + name)
    return errors


if __name__ == '__main__':
    failures = verify(Path(__file__).resolve().parents[1])
    print(json.dumps({'passed': not failures, 'errors': failures,
                      'scope': 'package integrity, not host runtime'}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(failures))
