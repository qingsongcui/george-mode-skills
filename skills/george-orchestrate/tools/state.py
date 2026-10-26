#!/usr/bin/env python3
"""Local orchestration facts. Never starts agents or performs forge writes."""
import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def required(data, key):
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(key + ' must be a nonempty string')
    return value


def evidence(data):
    path = Path(required(data, 'evidence')).expanduser()
    if not path.is_absolute() or not path.is_file():
        raise ValueError('evidence must be an existing absolute file')
    return str(path), hashlib.sha256(path.read_bytes()).hexdigest()


def operate(db_path, action, data):
    db_path = Path(db_path)
    if action != 'init' and not db_path.exists():
        raise ValueError('store missing; init first')
    if action == 'init':
        db_path.parent.mkdir(parents=True, exist_ok=True)
    readonly = action in ('status', 'inbox.read', 'verdict.check')
    location = db_path.resolve().as_uri() + '?mode=ro' if readonly else str(db_path)
    with sqlite3.connect(location, timeout=10, uri=readonly) as db:
        db.row_factory = sqlite3.Row
        if readonly:
            db.execute('BEGIN')
        else:
            db.execute('PRAGMA journal_mode=WAL')
            db.execute('BEGIN IMMEDIATE')
            db.execute('CREATE TABLE IF NOT EXISTS facts(kind TEXT, id TEXT, body TEXT, PRIMARY KEY(kind,id))')
            db.execute('CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY, at TEXT, action TEXT, body TEXT)')

        def get(kind, identity):
            row = db.execute('SELECT body FROM facts WHERE kind=? AND id=?', (kind, identity)).fetchone()
            return json.loads(row['body']) if row else None

        def put(kind, identity, body):
            db.execute('INSERT OR REPLACE INTO facts VALUES(?,?,?)', (kind, identity, encoded(body)))
            return body

        def rows(kind):
            return [json.loads(row['body']) for row in db.execute('SELECT body FROM facts WHERE kind=? ORDER BY id', (kind,))]

        if action == 'init':
            result = {'store': str(db_path.resolve())}
        elif action == 'unit.put':
            identity, owner = required(data, 'id'), required(data, 'owner')
            version, scope = required(data, 'version'), required(data, 'scope')
            state = data.get('state', 'pending')
            if state not in ('pending', 'running', 'code-ready', 'blocked'):
                raise ValueError('unit state must be pending/running/code-ready/blocked; verification is derived')
            old = get('unit', identity)
            if old and old['owner'] != owner and data.get('handoff') != 'previous-owner-stopped':
                raise ValueError('owner replacement requires confirmed stopped-owner handoff')
            result = put('unit', identity, dict(id=identity, owner=owner, version=version, scope=scope, state=state))
        elif action == 'verdict.record':
            identity = required(data, 'unit')
            unit = get('unit', identity)
            if not unit:
                raise ValueError('unit missing')
            if required(data, 'version') != unit['version']:
                raise ValueError('stale version')
            verifier = required(data, 'verifier')
            level = required(data, 'level')
            if level not in ('static', 'unit', 'real-surface', 'independent-real-surface', 'blocked', 'failed'):
                raise ValueError('unsupported verification level')
            if level == 'independent-real-surface' and verifier == unit['owner']:
                raise ValueError('owner cannot self-certify independent verification')
            path, digest = evidence(data)
            key = encoded([identity, unit['version'], unit['scope']])
            result = put('verdict', key, dict(unit=identity, version=unit['version'], scope=unit['scope'], verifier=verifier, level=level,
                         evidence=path, sha256=digest, observed_at=required(data, 'observed_at')))
        elif action == 'verdict.check':
            unit = get('unit', required(data, 'unit'))
            if not unit:
                raise ValueError('unit missing')
            current = []
            for row in rows('verdict'):
                if row['unit'] != unit['id'] or row['version'] != unit['version'] or row.get('scope') != unit['scope']:
                    continue
                p = Path(row['evidence'])
                row['evidence_intact'] = p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == row['sha256']
                current.append(row)
            level = data.get('required_level', 'independent-real-surface')
            if level not in ('static', 'unit', 'real-surface', 'independent-real-surface'):
                raise ValueError('unsupported required level')
            result = {'unit': unit, 'current_verdicts': current,
                      'verified': any(row['level'] == level and row['evidence_intact'] for row in current),
                      'note': 'Exact requested evidence level only. Not external permission or proof of truthful authorship.'}
        elif action == 'inbox.push':
            identity = required(data, 'id')
            body = dict(id=identity, unit=required(data, 'unit'), sender=required(data, 'sender'),
                        report=required(data, 'report'), state='pending')
            if not get('unit', body['unit']):
                raise ValueError('unit missing')
            old = get('inbox', identity)
            if old and any(old[k] != body[k] for k in ('unit', 'sender', 'report')):
                raise ValueError('idempotency key reused for different message')
            result = old or put('inbox', identity, body)
        elif action == 'inbox.read':
            result = [row for row in rows('inbox') if row['state'] == 'pending']
        elif action == 'inbox.ack':
            identity = required(data, 'id')
            item = get('inbox', identity)
            if not item:
                raise ValueError('message missing')
            path, digest = evidence(data)
            item.update(state='acked', receipt=path, receipt_sha256=digest)
            result = put('inbox', identity, item)
        elif action == 'gate.put':
            identity = required(data, 'id')
            result = put('gate', identity, dict(id=identity, question=required(data, 'question'),
                         suggested_default=data.get('suggested_default'), state='open'))
        elif action == 'gate.resolve':
            identity = required(data, 'id')
            gate = get('gate', identity)
            if not gate:
                raise ValueError('gate missing')
            gate.update(state='resolved', answer=required(data, 'answer'), source=required(data, 'source'))
            result = put('gate', identity, gate)
        elif action == 'frontier.set':
            items = data.get('items')
            if not isinstance(items, list):
                raise ValueError('items must be a list')
            seen = set()
            for item in items:
                identity = required(item, 'id')
                if identity in seen:
                    raise ValueError('duplicate frontier item')
                parent = item.get('parent')
                if parent is not None and parent not in seen:
                    raise ValueError('frontier must be ordered with parent before child')
                required(item, 'version')
                required(item, 'source')
                required(item, 'observed_at')
                seen.add(identity)
            # Observation timestamps are freshness facts, not topology changes.
            topology = [{k: item.get(k) for k in ('id', 'parent', 'version')} for item in items]
            digest = hashlib.sha256(encoded(topology).encode()).hexdigest()
            old = get('frontier', 'current') or {'generation': 0, 'digest': None}
            result = put('frontier', 'current', dict(items=items, digest=digest,
                         generation=old['generation'] + int(old['digest'] != digest)))
        elif action == 'standing.add':
            result = put('standing', required(data, 'id'), dict(id=data['id'], instruction=required(data, 'instruction'),
                         source=required(data, 'source')))
        elif action == 'status':
            facts = {kind: rows(kind) for kind in ('unit', 'verdict', 'inbox', 'gate', 'frontier', 'standing')}
            result = {'facts': facts, 'content_sha256': hashlib.sha256(encoded(facts).encode()).hexdigest(),
                      'event_count': db.execute('SELECT COUNT(*) FROM events').fetchone()[0]}
        else:
            raise ValueError('unknown action')
        if action not in ('status', 'inbox.read', 'verdict.check'):
            db.execute('INSERT INTO events(at,action,body) VALUES(?,?,?)',
                       (datetime.now(timezone.utc).isoformat(), action, encoded(result)))
        db.commit()
        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', required=True, help='SQLite file owned by this task')
    parser.add_argument('action')
    parser.add_argument('--input', type=Path, help='JSON request file; no shell interpolation required')
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text()) if args.input else {}
        result = operate(args.store, args.action, payload)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.action == 'verdict.check' and not result['verified']:
            raise SystemExit(1)
    except (ValueError, OSError, sqlite3.Error) as exc:
        parser.exit(1, str(exc) + '\n')
