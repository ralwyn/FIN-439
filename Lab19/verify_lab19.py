import unittest
import panel

class PanelChecks(unittest.TestCase):
    def test_cost_known_answers(self):
        r=panel.build('COST')
        self.assertEqual([round(x['liabilities_to_equity'],2) for x in r['rows']],[2.11,1.75,1.96,1.64,1.49])
        self.assertAlmostEqual(r['growth_percent'],7.51,places=2)
        self.assertEqual(list(r['panel']['Buffett'].values()),['pass']*3)
        self.assertEqual(list(r['panel']['Cathie Wood'].values()),['fail','not known'])
        self.assertEqual(list(r['panel']['Burry'].values()),['pass','pass'])
    def test_probe(self):
        self.assertEqual(list(panel.build('COST',5)['panel']['Cathie Wood'].values()),['pass','not known'])
    def test_missing_and_equity(self):
        r=panel.build('NVDA')
        r['rows'][-1]['facts']['equity']['value']=0
        r['rows'][-1]['facts']['research_and_development']['value']=None
        panel.add_checks(r)
        self.assertEqual(list(r['panel']['Burry'].values())[-1],'not known')
        self.assertEqual(list(r['panel']['Cathie Wood'].values())[-1],'not known')
    def test_boundary(self):
        r=panel.build('COST')
        for row in r['rows']:row['facts']['operating_cash_flow']['value']=row['facts']['net_income']['value']
        r['rows'][-1]['facts']['liabilities']['value']=2*r['rows'][-1]['facts']['equity']['value']
        panel.add_checks(r)
        self.assertEqual(list(r['panel']['Burry'].values()),['pass','pass'])
        r['rows'][0]['facts']['operating_cash_flow']['value']=None
        panel.add_checks(r)
        self.assertEqual(list(r['panel']['Burry'].values())[0],'not known')
    def test_nvda(self):
        r=panel.build('NVDA')
        self.assertEqual(list(r['panel']['Buffett'].values()),['pass']*3)
        self.assertEqual(list(r['panel']['Cathie Wood'].values()),['pass','pass'])
        self.assertEqual(list(r['panel']['Burry'].values()),['fail','pass'])
    def test_memos_and_probe(self):
        for ticker in ['COST','NVDA','JPM']:
            r=panel.build(ticker)
            for investor in panel.INVESTORS:
                path=panel.HERE/'memos'/f"{ticker}-{investor.lower().replace(' ','-')}.md"
                self.assertTrue(path.exists(),path.name)
                self.assertEqual(panel.flags(path.read_text(),r),[],path.name)
                self.assertTrue(panel.flags('Unsupported ROE 987.654321%.',r))
    def test_jpm_gaps(self):
        r=panel.build('JPM')
        self.assertTrue(all(x['owner_earnings'] is None for x in r['rows']))
        self.assertEqual(list(r['panel']['Buffett'].values())[1:],['not known','not known'])

if __name__=='__main__':unittest.main(verbosity=2)
