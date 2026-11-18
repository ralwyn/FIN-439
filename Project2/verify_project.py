import math
import unittest
import engine

class ProjectChecks(unittest.TestCase):
    def test_manual_two_asset_reconciliation(self):
        # Fixed hand-derived answers, not outputs copied from the engine.
        corr=[[1,.25,0,0],[.25,1,0,0],[0,0,1,0],[0,0,0,1]]
        e={'returns':[.04,.08,.03,.10], 'volatilities':[.10,.20,.15,.25], 'correlations':corr}
        r=engine.evaluate([.5,.5,0,0],e,objective=.055,reserve=.1,cost_bps=10)
        self.assertAlmostEqual(r['gross_return'],.06)
        self.assertAlmostEqual(r['turnover'],.5)
        self.assertAlmostEqual(r['cost_drag'],.0005)
        self.assertAlmostEqual(r['net_return'],.0595)
        self.assertAlmostEqual(r['volatility'],math.sqrt(.015))
        self.assertEqual(r['verdict'],'PASS')
        r2=engine.evaluate([.2,0,0,.8],e,objective=.085,reserve=.25,cost_bps=100)
        self.assertAlmostEqual(r2['gross_return'],.088)
        self.assertAlmostEqual(r2['turnover'],.4)
        self.assertAlmostEqual(r2['cost_drag'],.004)
        self.assertAlmostEqual(r2['net_return'],.084)
        self.assertAlmostEqual(r2['volatility'],math.sqrt(.0404))
        self.assertEqual(r2['failed_rules'],['Net modeled return below target','BIL below reserve floor'])

    def test_training_known_answers(self):
        p=engine.p
        c=p.covariance_matrix(p.VOLATILITIES,p.CORRELATIONS)
        self.assertAlmostEqual(p.portfolio_variance([0,0,.4,.6],c),.010944)
    def test_saved_own_universe(self):
        r=engine.compare(cost_bps=0)['portfolios']['Constrained portfolio']
        self.assertEqual(r['weights'],[.6,0,0,.4])
        self.assertAlmostEqual(r['net_return'],.0661,places=4)
        e=engine.compare(last36=True,cost_bps=0)['portfolios']['Constrained portfolio']
        self.assertEqual(e['weights'],[.85,0,0,.15])
    def test_cost_and_verdict(self):
        e=engine.estimates()
        a=engine.evaluate([.55,0,0,.45],e,cost_bps=100)
        self.assertAlmostEqual(a['turnover'],.05)
        self.assertAlmostEqual(a['gross_return']-a['net_return'],.0005)
        self.assertEqual(engine.evaluate([0,0,.4,.6],e)['verdict'],'FAIL')
        self.assertIn('BIL below reserve floor',engine.evaluate([0,0,.4,.6],e)['failed_rules'])
    def test_infeasible(self):
        self.assertIsNone(engine.compare(reserve=.9)['portfolios']['Constrained portfolio'])
    def test_constraints(self):
        r=engine.compare(cap=.5)['portfolios']['Constrained portfolio']
        self.assertIsNotNone(r)
        self.assertLessEqual(max(r['weights']),.5)
        self.assertGreaterEqual(r['reserve'],.1)
    def test_timing_gate(self):
        r=engine.point_in_time_signal()
        self.assertTrue(r['admitted'])
        self.assertAlmostEqual(r['change_bps'],-30)
        self.assertFalse(engine.point_in_time_signal(decision_date='2026-10-31')['admitted'])
        self.assertEqual(r['sources'][-1]['observation'],'2026-10-29')
    def test_invalid_input(self):
        with self.assertRaises(ValueError):engine.point_in_time_signal(0)
        with self.assertRaises(ValueError):engine.compare(cost_bps=-1)
    def test_exhaustive_minimum(self):
        e=engine.estimates();best=engine.compare()['portfolios']['Constrained portfolio']
        feasible=[engine.evaluate(w,e) for w in engine.p.weight_grid(4)]
        feasible=[r for r in feasible if r['verdict']=='PASS']
        self.assertAlmostEqual(best['volatility'],min(r['volatility'] for r in feasible))

if __name__=='__main__':unittest.main(verbosity=2)
