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
    required += ['LICENSE', 'NOTICE.md', 'NOTICE.zh.md', 'README.md', 'README.zh.md', 'docs/glossary.md',
                 'skills/george-mode/SKILL.en.md']
    required += ['theory/' + name for name in
                 ['00_开始使用.md', '00_开始使用.en.md', '01_反身实践私典_理论全本.md',
                  '01_反身实践私典_理论全本.en.md', '02_闭环运行手册.md', '03_AI协作指令.md',
                  '04_闭环记录工作簿_空白模板.xlsx', '04_闭环记录工作簿_空白模板.en.xlsx',
                  '06_字段与编号规范.md', '07_理论来源与修订说明.md']]
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
