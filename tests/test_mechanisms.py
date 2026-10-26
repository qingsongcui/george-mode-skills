import copy,importlib.util,json,sys,tempfile,unittest,sqlite3
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
R=Path(__file__).resolve().parents[1]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,R/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
state=load('state','skills/george-orchestrate/tools/state.py')
plan=load('plan','skills/george-orchestrate/tools/check_plan.py')
runner=load('runner','skills/george-verify/scripts/run_verification.py')
class StateTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.d=Path(self.tmp.name);self.db=self.d/'state.sqlite';self.e=self.d/'result.txt';self.e.write_text('actual output');self.call('init');self.unit()
 def tearDown(self):self.tmp.cleanup()
 def call(self,a,**d):return state.operate(self.db,a,d)
 def unit(self,version='h1',owner='writer',**kw):return self.call('unit.put',id='a',owner=owner,version=version,scope='src/a',state='code-ready',**kw)
 def record(self,**kw):
  d=dict(unit='a',version='h1',verifier='reader',level='independent-real-surface',evidence=str(self.e),observed_at='2026-10-23T12:00:00+08:00');d.update(kw);return self.call('verdict.record',**d)
 def test_scope_change_invalidates_same_version(self):
  self.record();self.call('unit.put',id='a',owner='writer',version='h1',scope='src/a and src/b',state='code-ready');self.assertFalse(self.call('verdict.check',unit='a')['verified'])
 def test_read_does_not_wait_for_writer_lock(self):
  with sqlite3.connect(str(self.db)) as db:
   db.execute('BEGIN IMMEDIATE');self.assertEqual(len(self.call('status')['facts']['unit']),1);db.rollback()
 def test_new_version_cannot_use_old_green(self):
  self.record();self.assertTrue(self.call('verdict.check',unit='a')['verified']);self.unit('h2');self.assertFalse(self.call('verdict.check',unit='a')['verified'])
 def test_changed_or_missing_evidence_is_not_verified(self):
  self.record();self.e.write_text('replaced');self.assertFalse(self.call('verdict.check',unit='a')['verified']);self.e.unlink();self.assertFalse(self.call('verdict.check',unit='a')['verified'])
 def test_owner_cannot_claim_independent_verdict(self):
  with self.assertRaises(ValueError):self.record(verifier='writer')
 def test_static_does_not_satisfy_real_surface(self):
  self.record(level='static');self.assertFalse(self.call('verdict.check',unit='a')['verified'])
 def test_later_failure_invalidates_prior_success(self):
  self.record();self.record(level='failed');self.assertFalse(self.call('verdict.check',unit='a')['verified'])
 def test_stale_record_rejected(self):
  with self.assertRaises(ValueError):self.record(version='h0')
 def test_owner_transfer_requires_stopped_handoff(self):
  with self.assertRaises(ValueError):self.unit(owner='other')
  self.assertEqual(self.unit(owner='other',handoff='previous-owner-stopped')['owner'],'other')
 def test_read_crash_recovery_and_idempotent_delivery(self):
  d=dict(id='m1',unit='a',sender='writer',report='path/to/report');self.call('inbox.push',**d);self.call('inbox.push',**d)
  first=self.call('inbox.read');self.assertEqual(len(first),1);self.assertEqual(self.call('inbox.read'),first)
  self.call('inbox.ack',id='m1',evidence=str(self.e));self.assertEqual(self.call('inbox.read'),[])
  self.assertEqual(len(self.call('status')['facts']['inbox']),1)
 def test_message_key_conflict_rejected(self):
  self.call('inbox.push',id='x',unit='a',sender='w',report='a')
  with self.assertRaises(ValueError):self.call('inbox.push',id='x',unit='a',sender='w',report='b')
 def test_default_does_not_resolve_gate(self):
  g=self.call('gate.put',id='publish',question='publish?',suggested_default='yes');self.assertEqual(g['state'],'open')
  with self.assertRaises(ValueError):self.call('gate.resolve',id='publish',answer='yes')
 def test_frontier_content_and_order(self):
  item=dict(id='a',parent=None,version='h1',source='forge',observed_at='now')
  a=self.call('frontier.set',items=[item]);item['observed_at']='later';b=self.call('frontier.set',items=[item]);self.assertEqual(a['generation'],b['generation'])
  item['version']='h2';c=self.call('frontier.set',items=[item]);self.assertEqual(c['generation'],b['generation']+1)
  item['parent']='missing'
  with self.assertRaises(ValueError):self.call('frontier.set',items=[item])
 def test_same_count_different_content_is_detected(self):
  a=self.call('status')['content_sha256'];self.unit('h2');self.assertNotEqual(a,self.call('status')['content_sha256'])
 def test_concurrent_messages_not_lost(self):
  def add(i):return self.call('inbox.push',id='msg'+str(i),unit='a',sender='w',report=str(i))
  with ThreadPoolExecutor(max_workers=5) as pool:list(pool.map(add,range(20)))
  self.assertEqual(len(self.call('inbox.read')),20)
class PlanTests(unittest.TestCase):
 def setUp(self):self.p=json.loads((R/'skills/george-orchestrate/templates/plan.json').read_text());self.p['project_root']='/tmp/george-plan-test'
 def two(self):
  b=copy.deepcopy(self.p['units'][0]);b.update(id='b',owner='b-owner',files=['src/b']);self.p['units'].append(b)
 def test_unknown_check_cannot_fake_coverage(self):
  self.p['units'][0]['checks']={k:dict(applicable=False,reason='n/a') for k in ['unit','live','perf']};self.p['units'][0]['checks']['fake']={'applicable':True};self.assertTrue(plan.validate(self.p))
 def test_absolute_alias_overlap(self):
  self.two();self.p['units'][1]['files']=['/tmp/george-plan-test/src/feature-a'];self.assertTrue(plan.validate(self.p))
 def test_parent_path_alias_overlap(self):
  self.two();self.p['units'][1]['files']=['src/b/../feature-a'];self.assertTrue(plan.validate(self.p))
 def test_good_plan(self):self.assertEqual(plan.validate(self.p),[])
 def test_cycle_rejected(self):
  self.two();self.p['units'][0]['depends_on']=['b'];self.p['units'][1]['depends_on']=['feature-a'];self.assertIn('cycle',' '.join(plan.validate(self.p)))
 def test_shared_paths_require_order(self):
  self.two();self.p['units'][1]['files']=['src/feature-a/inside.py'];self.assertTrue(plan.validate(self.p));self.p['units'][1]['depends_on']=['feature-a'];self.assertEqual(plan.validate(self.p),[])
 def test_unjustified_omission_rejected(self):
  self.p['units'][0]['checks']['perf'].pop('reason');self.assertTrue(plan.validate(self.p))
 def test_all_checks_omitted_rejected(self):
  self.p['units'][0]['checks']={k:dict(applicable=False,reason='n/a') for k in ['unit','live','perf']};self.assertTrue(plan.validate(self.p))
class RunnerTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.d=Path(self.tmp.name)
  def command(code):return dict(argv=[sys.executable,'-c',code],timeout_seconds=2)
  self.spec=dict(cwd=str(self.d),version='h1',artifacts=['evidence.json'])
  self.spec.update({k:command('print("OK")') for k in ['launch','doctor','drive','evidence']})
  self.spec['evidence']=command('from pathlib import Path;Path("evidence.json").write_text("observed")')
  self.spec['cleanup']=command('from pathlib import Path;Path("cleaned").write_text("yes")')
 def tearDown(self):self.tmp.cleanup()
 def runit(self):return runner.run(self.spec,self.d/'output')
 def test_full_contract_preserves_evidence(self):self.assertTrue(self.runit()['pass']);self.assertTrue((self.d/'cleaned').exists())
 def test_deleted_evidence_is_failure(self):
  self.spec['cleanup']['argv'][-1]='from pathlib import Path;Path("evidence.json").unlink()';self.assertFalse(self.runit()['pass'])
 def test_failed_launch_still_cleans(self):
  self.spec['launch']['argv'][-1]='raise SystemExit(4)';self.assertFalse(self.runit()['pass']);self.assertTrue((self.d/'cleaned').exists())
 def test_zero_exit_with_wrong_body_fails(self):
  self.spec['drive']['stdout_contains']=['actual-expected-result'];self.assertFalse(self.runit()['pass'])
 def test_timeout_still_cleans(self):
  self.spec['drive']['argv'][-1]='import time;time.sleep(10)';self.spec['drive']['timeout_seconds']=0.05;self.assertFalse(self.runit()['pass']);self.assertTrue((self.d/'cleaned').exists())
if __name__=='__main__':unittest.main(verbosity=2)
