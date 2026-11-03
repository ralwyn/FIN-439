"""Known answer, fiscal selection, honest gaps and numeric-guard tests."""
from pathlib import Path
import gzip,json,sys,unittest,copy
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.agents/skills/buffett-business/scripts'))
from edgar_facts import build_report,report_text,unprinted_numbers,annual,make_row,select_fact,checks,latest_record

def replay(t):
 p=ROOT/'Lab18/evidence'
 return build_report(json.loads(gzip.decompress((p/f'{t}-companyfacts.json.gz').read_bytes())),t,json.loads((p/f'{t}-source.json').read_text()))

class FactsTests(unittest.TestCase):
 def test_cost_known_answer(self):
  r=replay('COST')
  expected=[('2022-08-28',226954,5844,7392,3891,20642,28.3,3501),('2023-09-03',242290,6292,11068,4323,25058,25.1,6745),('2024-09-01',254453,7367,11339,4710,23622,31.2,6629),('2025-08-31',275235,8099,13335,5498,29164,27.8,7837),('2026-08-30',303154,9226,15817,6435,35803,25.8,9382)]
  for row,e in zip(r['rows'],expected,strict=True):
   actual=(row['fiscal_year_end'],*[row['facts'][k]['value']/1e6 for k in ['revenue','net_income','operating_cash_flow','capital_spending','equity']],round(row['roe_percent'],1),row['owner_earnings']/1e6)
   self.assertEqual(actual,e)
  self.assertEqual(list(r['checks'].values()),['pass']*3)
 def test_jpm_gaps(self):
  r=replay('JPM')
  self.assertTrue(all(x['facts']['capital_spending']['value'] is None and x['owner_earnings'] is None for x in r['rows']))
  self.assertEqual(list(r['checks'].values()),['fail','not known','not known'])
 def test_full_year_not_filing_label(self):
  self.assertTrue(annual({'form':'10-K','start':'2022-08-29','end':'2023-09-03'}))
  self.assertFalse(annual({'form':'10-K','start':'2023-06-01','end':'2023-09-03'}))
  self.assertFalse(annual({'form':'10-Q','start':'2022-08-29','end':'2023-09-03'}))
 def test_fallback_and_latest(self):
  def fact(val,filed):return {'form':'10-K','start':'2025-01-01','end':'2025-12-31','filed':filed,'accn':'example','val':val,'fy':2026}
  facts={'Revenues':{'units':{'USD':[fact(10,'2026-02-01'),fact(12,'2027-02-01')]}}}
  self.assertEqual(select_fact(facts,'revenue','2025-12-31','2025-01-01')['value'],12)
  facts['RevenueFromContractWithCustomerExcludingAssessedTax']={'units':{'USD':[fact(11,'2026-02-01')]}}
  self.assertEqual(select_fact(facts,'revenue','2025-12-31','2025-01-01')['value'],11)
 def test_nonpositive_equity(self):
  for v in [0,-10]:
   f={'StockholdersEquity':{'units':{'USD':[{'form':'10-K','end':'2025-12-31','val':v,'filed':'2026-02-01','accn':'test'}]}}}
   self.assertIsNone(make_row(f,'2025-12-31','2025-01-01')['roe_percent'])
 def test_missing_year(self):
  self.assertEqual(set(checks(replay('COST')['rows'][:-1]).values()),{'not known'})
 def test_ambiguous_same_day(self):
  with self.assertRaises(ValueError):latest_record([{'filed':'2026-01-01','val':1},{'filed':'2026-01-01','val':2}])
 def test_memo_guard(self):
  report=report_text(replay('COST'))
  self.assertEqual(unprinted_numbers('ROE was 28.30%; owner earnings were $3,501 million.',report),[])
  self.assertEqual([x['number'] for x in unprinted_numbers('ROE was 40.0%.',report)],['40.0%'])
  self.assertTrue(unprinted_numbers('ROE was 3501%.',report))
 def test_saved_memos(self):
  for t in ['COST','JPM']:
   self.assertEqual(unprinted_numbers((ROOT/f'Lab18/memos/{t}.md').read_text(),report_text(replay(t))),[])
 def test_numeric_formats_and_years(self):
  report=report_text(replay('COST'))
  self.assertEqual([x['number'] for x in unprinted_numbers('FY2099, .12345%, 4e1%, −40.0%.',report)],['2099','.12345%','4e1%','−40.0%'])
  self.assertEqual(unprinted_numbers('FY2022 had ROE of 28.30 %.',report),[])
 def test_growth_uses_endpoints(self):
  rows=copy.deepcopy(replay('COST')['rows']);rows[2]['owner_earnings']=None
  self.assertEqual(list(checks(rows).values()),['pass','not known','pass'])
if __name__=='__main__':unittest.main(verbosity=2)
