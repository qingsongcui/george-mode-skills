#!/usr/bin/env python3
"""Bound the bundled read-only GitHub watcher, including stuck child commands."""
import argparse
import os
import signal
import subprocess
from pathlib import Path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--deadline', type=float, default=55)
    args, forwarded = parser.parse_known_args()
    if args.deadline <= 0:
        parser.error('deadline must be positive')
    entry = Path(__file__).parent / 'pstack/watch-pr/watch-pr'
    process = subprocess.Popen(['bun', str(entry), *forwarded], start_new_session=True)
    try:
        code = process.wait(timeout=args.deadline)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()
        print('{"kind":"WRAPPER_TIMEOUT","terminal":true,"exitCode":5}', flush=True)
        code = 5
    raise SystemExit(code)
