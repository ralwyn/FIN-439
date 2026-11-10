from pathlib import Path
import json
import pandas as pd
import streamlit as st
import engine

HERE=Path(__file__).resolve().parent


def frame(result):
    rows=[]
    for name,r in result['portfolios'].items():
        if r is None:
            rows.append({'Portfolio':name,'Verdict':'NO FEASIBLE MIX','Failed rules':'No grid allocation satisfies the target and limits'})
        else:
            rows.append({'Portfolio':name,**{t:f'{w:.0%}' for t,w in zip(engine.TICKERS,r['weights'])},
                         'Gross estimate':f"{r['gross_return']:.2%}",'Cost drag':f"{r['cost_drag']:.3%}",
                         'Net estimate':f"{r['net_return']:.2%}",'Volatility':f"{r['volatility']:.2%}",
                         'BIL reserve':f"{r['reserve']:.0%}",'One-way turnover':f"{r['turnover']:.1%}",
                         'Verdict':r['verdict'],'Failed rules':'; '.join(r['failed_rules']) or 'None'})
    return pd.DataFrame(rows)


def main():
    st.set_page_config(page_title='Scholarship Fund · Project 2',layout='wide')
    st.title('Campus Opportunity Scholarship Fund')
    st.caption('Investment management workbench · Education, not investment advice.')
    st.sidebar.header('Mandate and stress controls')
    objective=st.sidebar.slider('Net modeled return target (%)',0.,15.,6.5,.1)
    reserve=st.sidebar.slider('Minimum BIL reserve (%)',0,100,10,5)
    cost=st.sidebar.slider('Trading cost (bps per one-way turnover)',0,200,10,10)
    cap=st.sidebar.slider('Maximum weight in any ETF (%)',25,100,100,5)
    window=st.sidebar.radio('Estimation window',['All 59 returns','Last 36'])
    shock=st.sidebar.slider('VT expected-return change (percentage points)',-5.,5.,0.,.5)
    result=engine.compare(objective/100,reserve/100,cost,cap/100,window=='Last 36',shock)
    overview, signal_tab, audit, evidence, panel_tab=st.tabs(['Portfolio decision','Point-in-time signal','Stress audit','Documents','Investor panel'])
    with overview:
        st.write('Fictional 1 million USD fund · 40,000 USD annual scholarships · 10+ year horizon · Annual rebalancing · BIL / IEF / LQD / VT')
        st.info(result['decision'])
        current=result['portfolios']['Constrained portfolio']
        if current:
            a,b,c=st.columns(3)
            a.metric('Net modeled return',f"{current['net_return']:.2%}")
            b.metric('Estimated volatility',f"{current['volatility']:.2%}")
            c.metric('BIL reserve',f"{current['reserve']:.0%}")
        display=frame(result)
        st.dataframe(display,hide_index=True,width='stretch')
        st.caption('PASS covers fully invested long-only weights, modeled net target, reserve and ETF cap. It does not establish suitability, realized return or protection from losses.')
        st.subheader('Allocation comparison')
        chart={name:dict(zip(engine.TICKERS,r['weights'])) for name,r in result['portfolios'].items() if r}
        st.bar_chart(pd.DataFrame(chart).T,stack=True)
        st.subheader('What the committee can authorize')
        st.write('A paper research pilot only. The saved full-history starting mix is 60% BIL / 40% VT. The documented estimate stress moves toward 55% BIL / 45% VT; the alternate window moves to 85% BIL / 15% VT. These are scenario bounds, not a client allocation approval.')
        st.warning('Pause adoption if allocation sensitivity exceeds 10 percentage points, reserves fail, the net target is infeasible, or source timing cannot be verified. The saved window comparison already triggers review.')
        st.caption('Prices: October 2021–September 2026; downloaded October 22. Arithmetic annualized historical estimates are not rolling-five-year compound forecasts. Cost drag models one annual rebalance from an assumed 60% BIL / 40% VT reference, not actual client holdings. ETF expenses are embedded in adjusted-price history; tax, market impact and advisor fees are not modeled.')
        st.download_button('Download this scenario',json.dumps(result,indent=2),'scholarship-scenario.json')
    with signal_tab:
        st.subheader('Treasury-rate risk monitor · DGS10')
        decision=st.date_input('Information cutoff',value=__import__('datetime').date(2026,11,10))
        lag=st.slider('Weekdays after source download',1,5,1)
        signal=engine.point_in_time_signal(lag,decision.isoformat())
        st.metric('Change between archived vintage endpoints',f"{signal['change_bps']:.1f} basis points")
        st.info(signal['state'].upper())
        st.dataframe(pd.DataFrame(signal['sources']),hide_index=True)
        st.write(signal['rule'])
        st.caption('Rule designed November 10. Historical snapshots illustrate availability; no return-prediction or realized backtest claim. Weekday lag is conservative, but holidays and the exact execution clock need review before any real trade. Current revised history never substitutes for archived vintages.')
        st.markdown((HERE/'docs/data-card.md').read_text())
    with audit:
        st.subheader('Fixed saved stress suite')
        st.caption('Independent of sidebar changes; all scenarios use the documented base inputs except the named perturbation.')
        saved=json.loads((HERE/'evidence/executed-results.json').read_text())
        rows=[]
        for name,x in saved['stresses'].items():
            r=x['portfolios']['Constrained portfolio']
            rows.append({'Scenario':name,'Weights BIL / IEF / LQD / VT': 'infeasible' if r is None else ' / '.join(f'{w:.0%}' for w in r['weights']),
                         'Net estimate':'—' if r is None else f"{r['net_return']:.2%}",
                         'Volatility':'—' if r is None else f"{r['volatility']:.2%}",'Decision':x['decision']})
        st.dataframe(pd.DataFrame(rows),hide_index=True)
        st.markdown((HERE/'docs/committee-challenge.md').read_text())
    with evidence:
        for label,filename in [('Decision memo','decision-memo.md'),('Mandate','mandate.md'),('Validation','validation-and-ai-use.md'),('Cold run','cold-run.md'),('Must-fix list','must-fix.md')]:
            with st.expander(label):st.markdown((HERE/'docs'/filename).read_text())
    with panel_tab:
        st.subheader('Lab 19 · NVIDIA, largest holding in VT')
        path=HERE/'data/NVDA-panel.json'
        if path.exists():
            r=json.loads(path.read_text())
            st.dataframe(pd.DataFrame([{'Investor':i,'Check':c,'Result':v} for i,checks in r['panel'].items() for c,v in checks.items()]),hide_index=True)
            st.write('Buffett and Cathie Wood screens pass; Burry flags cash-flow conversion. The panel supports research questions, not a change in ETF weights or a stock purchase.')
        st.link_button('Open full Lab 19 app','http://127.0.0.1:8519')
        st.caption('Launch Lab19/Start-Lab19.command if the panel server is not already running.')


if __name__=='__main__':main()
