#!/usr/bin/env python3
"""Run a project-authored verification contract and keep evidence after cleanup."""
import argparse
import hashlib
import json
import os
import signal
import subprocess
import time
from pathlib import Path


def run(spec, output):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    cwd = Path(spec['cwd']).resolve()
    phases = ('launch', 'doctor', 'drive', 'evidence', 'cleanup')
    for phase in phases:
        step = spec.get(phase)
        if not isinstance(step, dict) or not isinstance(step.get('argv'), list) or not step['argv']:
            raise ValueError('every phase needs an explicit argv: ' + phase)
        if any(not isinstance(x, str) for x in step['argv']):
            raise ValueError('argv values must be strings')
    if not spec.get('version') or not spec.get('artifacts'):
        raise ValueError('version and required artifacts are mandatory')
    results = []
    started = time.time()

    def execute(phase):
        step = spec[phase]
        record = {'phase': phase, 'argv': step['argv'], 'started_at': time.time()}
        try:
            p = subprocess.Popen(step['argv'], cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True, start_new_session=True)
            try:
                out, err = p.communicate(timeout=step.get('timeout_seconds', 60))
                record.update(exit_code=p.returncode, timed_out=False)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid, signal.SIGKILL)
                out, err = p.communicate()
                record.update(exit_code=p.returncode, timed_out=True)
            (output / (phase + '.stdout.txt')).write_text(out)
            (output / (phase + '.stderr.txt')).write_text(err)
            record['pass'] = (not record['timed_out'] and record['exit_code'] == step.get('expected_exit', 0)
                              and all(x in out for x in step.get('stdout_contains', []))
                              and all(x not in out + err for x in step.get('must_not_contain', [])))
        except OSError as exc:
            record.update(error=str(exc), **{'pass': False})
        record['finished_at'] = time.time()
        results.append(record)
        return record['pass']

    before_cleanup = {}
    try:
        for phase in phases[:-1]:
            if not execute(phase):
                break
        for relative in spec['artifacts']:
            path = (cwd / relative).resolve()
            before_cleanup[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    finally:
        execute('cleanup')
    artifacts = []
    for path, digest in before_cleanup.items():
        p = Path(path)
        current = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        artifacts.append({'path': path, 'sha256': current, 'preserved': digest is not None and current == digest})
    passed = len(results) == 5 and all(x['pass'] for x in results) and all(x['preserved'] for x in artifacts)
    report = {'version': spec['version'], 'started_at': started, 'finished_at': time.time(),
              'pass': passed, 'steps': results, 'artifacts': artifacts,
              'scope': 'Contract execution; behavioral adequacy and correct target require reviewer inspection.'}
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('contract', type=Path)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    result = run(json.loads(args.contract.read_text()), args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(not result['pass'])
