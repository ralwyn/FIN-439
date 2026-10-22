"""FIN 439 portfolio lab: shared risk engine, selectable demo and free data."""
import hashlib
import importlib
import io
import json
from pathlib import Path
import pandas as pd
import streamlit as st
import portfolio as p
# The class requires saved engine input edits to appear after browser refresh.
importlib.reload(p)
from market_data import fetch_monthly_prices

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Scholarship Capital | FIN 439', page_icon='📊', layout='wide')
st.markdown('''<style>
.block-container{padding-top:2rem;max-width:1450px}
[data-testid="stMetric"]{background:rgba(98,153,177,.09);border:1px solid rgba(98,153,177,.22);padding:16px;border-radius:12px}
[data-testid="stSidebar"]{border-right:1px solid rgba(98,153,177,.2)}
h1{letter-spacing:-.04em}div.stButton>button{border-radius:9px}
</style>''', unsafe_allow_html=True)
st.caption('FIN 439  /  PORTFOLIO RESEARCH WORKBENCH')
st.title('Scholarship Capital')
st.caption('Built with AI help, a learning demonstration, not investment advice.')

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_prices(text):
    return fetch_monthly_prices(text)

with st.sidebar:
    st.header('Choose your universe')
    mode = st.selectbox('Data source', ['Meridian training', 'Scholarship fund demo',
                                       'Enter ETF tickers', 'Upload CSV'])
    csv_text = None
    provenance = None
    if mode == 'Scholarship fund demo':
        csv_text = (ROOT / 'prices.csv').read_text()
        provenance = {'source': 'Yahoo Finance via yfinance', 'downloaded': '2026-10-22',
                      'field': 'Adj Close', 'price_rows': 60,
                      'note': 'Saved five-year history; October 2021–September 2026.'}
    elif mode == 'Enter ETF tickers':
        with st.form('ticker-form'):
            tickers = st.text_input('Which ETFs do you want to explore?', value='BIL, IEF, QQQ, SPY',
                                   help='Three to six tickers. You choose the universe; no automatic substitutions.')
            fetch = st.form_submit_button('Fetch free price history', type='primary')
        st.caption('Yahoo Finance through yfinance. No API key or paid account. '
                   'Five years of completed monthly adjusted closes.')
        if fetch:
            try:
                with st.spinner('Fetching and checking every ticker…'):
                    prices, record = fetch_prices(tickers)
                st.session_state['market_download'] = (prices, record)
            except Exception as error:
                # Clear old history so a failed request cannot masquerade as the new universe.
                st.session_state.pop('market_download', None)
                st.error(f'Download failed: {error}')
        saved = st.session_state.get('market_download')
        if saved:
            csv_text, provenance = saved
            st.success('Loaded: ' + ', '.join(provenance['tickers']))
    elif mode == 'Upload CSV':
        upload = st.file_uploader('Upload prices.csv', type=['csv'])
        if upload:
            csv_text = upload.getvalue().decode('utf-8-sig')
            provenance = {'source': 'User-uploaded CSV', 'filename': upload.name,
                          'note': 'Verify source and adjusted-close definitions before use.'}
    st.divider()
    st.header('Mandate')
    objective = st.number_input('Objective return (%)', value=6.5, step=0.1,
                               key=f'{mode}-objective') / 100
    reserve_minimum = st.number_input('Reserve minimum (%)', min_value=0.0,
        max_value=100.0, value=3.0 if mode == 'Meridian training' else 10.0,
        step=1.0, key=f'{mode}-reserve-min') / 100
    last_36 = st.checkbox('Last 36 monthly returns', value=False, disabled=csv_text is None,
                          key=f'{mode}-last36')
    st.caption('5-point allocation grid · long-only · fully invested')

if mode in ('Enter ETF tickers', 'Upload CSV') and csv_text is None:
    st.info('Enter your ETFs and fetch history, or choose the scholarship demo to explore immediately.')
    st.stop()

try:
    if csv_text is None:
        names = p.SLEEVES
        loaded = {'returns': p.EXPECTED_RETURNS, 'volatilities': p.VOLATILITIES,
                  'correlations': p.CORRELATIONS}
        current = loaded
        source_id = 'meridian'
        defaults = p.RESERVE_ELIGIBLE
        st.subheader('Meridian · training case')
        st.write('Use the published course inputs to check your engine before exploring market history.')
        st.caption('Course-authored annual values; CPI 2.5% is a labelled estimate.')
    else:
        loaded = p.estimate_from_csv(io.StringIO(csv_text))
        current = p.estimate_from_csv(io.StringIO(csv_text), last_36=last_36)
        names = loaded['names']
        source_id = hashlib.sha256(csv_text.encode()).hexdigest()[:12]
        defaults = [name.upper() == 'BIL' for name in names]
        st.subheader('Campus Opportunity Scholarship Fund' if mode == 'Scholarship fund demo'
                     else 'Your ETF research universe')
        st.write(' → '.join(names))
        st.caption(f"Historical estimates · {current['months']} monthly returns · "
                   f"{current['first_return_date']} through {current['last_return_date']} · "
                   'mean × 12, sample standard deviation × √12; not compounded growth or forecasts.')
        if mode == 'Scholarship fund demo':
            st.caption('Fictional $1m fund · 10-year horizon · $40,000 annual scholarship budget · BIL reserve sleeve')
        if 'SPY' in names and 'QQQ' in names:
            st.info('SPY and QQQ share many large U.S. stocks. Two ticker symbols do not necessarily '
                    'provide two independent sources of risk; inspect their correlation below.')
    context = f'{source_id}-{bool(last_36)}'
    edited_returns, eligible = [], []
    with st.expander('Assumptions & reserve eligibility', expanded=True):
        st.caption('Change a return estimate to test it. Reserve eligibility is a mandate choice; '
                   'it is not inferred from a low historical volatility.')
        def reset_returns():
            for i in range(len(names)):
                st.session_state[f'{context}-return-{i}'] = float(current['returns'][i] * 100)
        stress_index = names.index('VT') if 'VT' in names else len(names) - 1
        def stress_return():
            key = f'{context}-return-{stress_index}'
            st.session_state[key] = float(current['returns'][stress_index] * 100 - 1)
        buttons = st.columns(2)
        buttons[0].button(f"Stress {names[stress_index]}: 1 point below window estimate", on_click=stress_return)
        buttons[1].button('Restore window estimates', on_click=reset_returns)
        for i, name in enumerate(names):
            a, b, c = st.columns([3, 2, 2])
            a.write(name)
            return_key = f'{context}-return-{i}'
            if return_key not in st.session_state:
                st.session_state[return_key] = float(current['returns'][i] * 100)
            edited_returns.append(b.number_input(f'{name} expected return (%)',
                value=None, step=.1, format='%.2f', key=return_key) / 100)
            eligible.append(c.checkbox(f'{name} reserve-eligible', value=bool(defaults[i]),
                                       key=f'{source_id}-reserve-{i}'))
    if not any(eligible) and reserve_minimum > 0:
        st.warning('No reserve-eligible ETF is selected. Select the assets allowed by your mandate, '
                   'or set the minimum to 0 only if your mandate has no reserve rule.')
    baseline = p.search_portfolio(loaded['returns'], loaded['volatilities'],
        loaded['correlations'], objective, eligible, reserve_minimum)
    answer = p.search_portfolio(edited_returns, current['volatilities'],
        current['correlations'], objective, eligible, reserve_minimum)
    change = p.largest_weight_change(baseline, answer)
    if answer:
        cols = st.columns(4)
        cols[0].metric('Expected annual return', f"{answer['return']:.2%}")
        cols[1].metric('Annual volatility', f"{answer['volatility']:.2%}")
        cols[2].metric('Eligible reserves', f"{answer['reserve']:.2%}")
        cols[3].metric('Largest weight change', 'N/A' if change is None else f'{change:.2f} pp')
        st.success('A grid mix meets the return target and reserve rule under the current estimates.')
    else:
        st.warning('no mix meets the objective')
        st.caption('No grid allocation meets both rules. The target has not been lowered.')
    overview, history, sources = st.tabs(['Allocation & stability', 'History & correlations', 'Sources & export'])
    with overview:
        st.subheader('What changes when assumptions change?')
        rows = [{'Asset': name,
                 'As loaded (%)': None if baseline is None else baseline['weights'][i] * 100,
                 'Current (%)': None if answer is None else answer['weights'][i] * 100}
                for i, name in enumerate(names)]
        frame = pd.DataFrame(rows).set_index('Asset')
        if answer or baseline:
            st.bar_chart(frame, color=['#7596a8', '#37c9ad'], horizontal=True, height=250, stack=False)
        st.dataframe(frame.style.format('{:.2f}', na_rep='No mix'), width='stretch')
        c1, c2 = st.columns(2)
        for column, title, result in ((c1, 'As loaded · original full history', baseline),
                                       (c2, 'Current · selected window and edits', answer)):
            with column:
                st.markdown(f'**{title}**')
                if result:
                    st.write(f"Return **{result['return']:.2%}** · Volatility **{result['volatility']:.2%}** · "
                             f"Reserves **{result['reserve']:.2%}**")
                else:
                    st.write('no mix meets the objective')
        st.caption('Both columns use the current objective and reserve rules. The left keeps all-history '
                   'estimates; the right uses your selected window and return edits. Lowest risk on a '
                   '5-point grid does not establish a suitable investment recommendation.')
        if change is not None:
            st.write(f'**{change:.2f} percentage points** is the largest allocation movement from the loaded answer.')
    with history:
        if csv_text:
            prices = pd.read_csv(io.StringIO(csv_text), index_col=0, parse_dates=True)
            st.subheader('How each ETF’s adjusted price evolved')
            st.caption('Each series starts at 100. Historical adjusted-price growth for each individual ETF; '
                       'not a backtest of the optimized allocation.')
            st.line_chart(prices.div(prices.iloc[0]).mul(100), height=300)
        else:
            st.info('Meridian uses supplied course values. Choose market data to see history.')
        st.subheader('Correlation · selected estimation window')
        corr = pd.DataFrame(current['correlations'], index=names, columns=names)
        st.dataframe(corr.style.format('{:.2f}'), width='stretch')
        st.caption('Historical correlations can change, particularly during stress.')
    with sources:
        if provenance:
            st.json(provenance)
            st.download_button('Download checked monthly prices', csv_text, 'prices.csv', 'text/csv')
        else:
            st.write('Source: FIN 439 Lab 14 course-authored training values.')
        snapshot = {'universe': names, 'objective': objective, 'reserve_minimum': reserve_minimum,
            'reserve_eligible': eligible, 'last_36': last_36, 'edited_expected_returns': edited_returns,
            'annual_volatilities': current['volatilities'], 'correlations': current['correlations'],
            'baseline': baseline, 'current': answer, 'largest_change_pp': change, 'source': provenance}
        st.download_button('Export this scenario', json.dumps(snapshot, indent=2), 'portfolio-scenario.json', 'application/json')
        st.caption('Yahoo Finance access is through an unofficial open-source client and can be rate-limited '
                   'or unavailable. Fetches are cached for one hour; the recorded download time is shown above. '
                   'Incomplete current months are excluded. Missing history is rejected; nothing is forward-filled.')
except (ValueError, UnicodeError, TypeError) as error:
    st.error(f'Input error: {error}')
    st.stop()
