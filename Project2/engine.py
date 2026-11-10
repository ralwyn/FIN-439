"""Scholarship mandate comparisons and point-in-time risk monitor. No fitted backtest."""
from datetime import date, timedelta
import csv
import hashlib
import json
import math
from pathlib import Path
import portfolio_math as p

HERE = Path(__file__).resolve().parent
TICKERS = ['BIL','IEF','LQD','VT']
REFERENCE = [.6,0,0,.4]


def estimates(last36=False):
    result = p.estimate_from_csv(HERE/'data/prices.csv',last36)
    if result['names'] != TICKERS:
        raise ValueError('Expected BIL / IEF / LQD / VT in the saved price file.')
    return result


def point_in_time_signal(lag_business_days=1, decision_date='2026-11-10', threshold_bps=25):
    if lag_business_days < 1:
        raise ValueError('Use at least one weekday after the source download; holiday calendar still requires review.')
    values = []
    for vintage in ['2026-10-05','2026-10-31']:
        path = HERE/'data'/f'DGS10-{vintage}.csv'
        meta = json.loads(path.with_suffix('.csv.meta.json').read_text())
        if hashlib.sha256(path.read_bytes()).hexdigest() != meta['sha256']:
            raise ValueError('Vintage file failed its source hash check.')
        with path.open() as f:
            rows = list(csv.reader(f))
        valid = [(date.fromisoformat(r[0]),float(r[1])) for r in rows[1:] if len(r)>1 and r[1] not in ['.','']]
        measured, value = max(valid)
        cutoff = date.fromisoformat(vintage)
        if measured > cutoff:
            raise ValueError('Observation occurs after its vintage cutoff.')
        available = max(cutoff, date.fromisoformat(meta['downloaded_at'][:10]))
        for _ in range(lag_business_days):
            available += timedelta(days=1)
            while available.weekday() >= 5:
                available += timedelta(days=1)
        values.append({'vintage':vintage,'observation':measured.isoformat(),'yield_percent':value,
                       'downloaded_at':meta['downloaded_at'],'available_no_earlier_than':available.isoformat(),
                       'url':meta['url']})
    cutoff_day = date.fromisoformat(decision_date)
    fresh = (cutoff_day-date.fromisoformat(values[-1]['observation'])).days <= 15
    admission = all(x['available_no_earlier_than'] <= decision_date for x in values) and fresh
    # DGS10 is in percentage points: multiplying the change by 100 gives basis points.
    change_bps = (values[-1]['yield_percent']-values[0]['yield_percent'])*100
    return {'decision_date':decision_date,'sources':values,'change_bps':change_bps,
            'threshold_bps':threshold_bps,'admitted':admission,'fresh_within_15_calendar_days':fresh,
            'state': 'quarantine' if not admission else ('rate-rise alert' if change_bps >= threshold_bps else 'no rate-rise alert'),
            'rule':'A rise of at least 25 basis points between the two archived vintage endpoints triggers committee review; no automatic trading.',
            'purpose':'Governance/rate-risk monitor, not a validated return predictor or backtest.'}


def evaluate(weights, estimate, objective=.065, reserve=.1, cost_bps=10, cap=1.0):
    p.validate_weights(weights,4)
    if not all(math.isfinite(x) for x in [objective,reserve,cost_bps,cap]) or not 0<=reserve<=1 or not 0<cap<=1 or cost_bps<0:
        raise ValueError('Invalid objective, reserve, cost or concentration input.')
    cov = p.covariance_matrix(estimate['volatilities'], estimate['correlations'])
    gross = p.portfolio_return(weights, estimate['returns'])
    turnover = sum(abs(a-b) for a,b in zip(weights,REFERENCE))/2
    cost = cost_bps/10000*turnover
    net = gross-cost
    failures=[]
    if net < objective-1e-12: failures.append('Net modeled return below target')
    if weights[0] < reserve-1e-12: failures.append('BIL below reserve floor')
    if max(weights)>cap+1e-12: failures.append('ETF concentration above limit')
    return {'weights':weights,'gross_return':gross,'cost_drag':cost,'net_return':net,
            'volatility':p.portfolio_volatility(weights,cov),'reserve':weights[0],
            'turnover':turnover,'verdict':'FAIL' if failures else 'PASS','failed_rules':failures}


def compare(objective=.065,reserve=.1,cost_bps=10,cap=1,last36=False,vt_shock_pp=0):
    e=estimates(last36)
    e['returns'][3] += vt_shock_pp/100
    best=None
    for w in p.weight_grid(4):
        result=evaluate(w,e,objective,reserve,cost_bps,cap)
        if result['verdict']=='PASS' and (best is None or result['volatility']<best['volatility']-1e-12):
            best=result
    candidates={'Equal weight':p.equal_weights(4),
                'Inverse volatility':p.inverse_volatility_weights(e['volatilities']),
                'Policy benchmark (40% LQD / 60% VT)':[0,0,.4,.6]}
    results={name:evaluate(w,e,objective,reserve,cost_bps,cap) for name,w in candidates.items()}
    results['Constrained portfolio']=best
    return {'inputs':{'objective':objective,'reserve_minimum':reserve,'cost_bps':cost_bps,
                      'concentration_cap':cap,'window':'Last 36' if last36 else 'All 59 returns',
                      'vt_shock_percentage_points':vt_shock_pp},'estimates':e,'portfolios':results,
            'decision':'PAUSE — no feasible mix' if best is None else 'RESEARCH PILOT — committee review required'}


def stress_suite():
    scenarios={'Base':{}, 'VT estimate minus 1 percentage point':{'vt_shock_pp':-1},
               'Last 36 returns':{'last36':True}, 'Trading cost 100 bps':{'cost_bps':100},
               'Last 36 with 100 bps cost':{'last36':True,'cost_bps':100},
               'Reserve floor 90%':{'reserve':.9}, 'ETF concentration cap 50%':{'cap':.5}}
    return {name:compare(**kwargs) for name,kwargs in scenarios.items()}


def main():
    result={'base':compare(),'signal':point_in_time_signal(),'stresses':stress_suite()}
    (HERE/'evidence/executed-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
