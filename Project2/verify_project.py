import math
import unittest
import engine

class ProjectChecks(unittest.TestCase):
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
