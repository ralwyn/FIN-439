from pathlib import Path
import json
import pandas as pd
import streamlit as st
import panel

HERE = Path(__file__).resolve().parent


def main():
    st.set_page_config(page_title='Legend Investor Panel', layout='wide')
    st.title('Legend Investor Panel')
    st.caption('SEC EDGAR data · Learning demonstration, not investment advice.')
    ticker = st.sidebar.selectbox('Company', ['COST', 'NVDA', 'JPM'])
    threshold = st.sidebar.select_slider('Cathie Wood revenue growth threshold (%)', [5, 15], value=15)
    st.sidebar.caption('Keep 15% as the default growth hurdle. 5% is the required sensitivity probe.')
    r = panel.build(ticker, threshold)
    st.subheader(ticker+' · '+r['company'])
    st.caption('Saved SEC download: '+r['source']['downloaded_at']+' · Latest annual 10-K facts; not a historical trading signal.')
    rows = []
    for row in r['rows']:
        rows.append({'FY end': row['fiscal_year_end'],
                     **{k.replace('_',' ').title(): panel.base.money(v['value']) for k,v in row['facts'].items()},
                     'ROE %': 'not known' if row['roe_percent'] is None else f"{row['roe_percent']:.1f}",
                     'Owner earnings': panel.base.money(row['owner_earnings']),
                     'Liabilities / equity': 'not known' if row['liabilities_to_equity'] is None else f"{row['liabilities_to_equity']:.2f}",
                     'R&D / revenue %': 'not found' if row['rd_percent'] is None else f"{row['rd_percent']:.2f}"})
    st.caption('Amounts in USD millions; percentages and ratios labeled separately.')
    st.dataframe(pd.DataFrame(rows), hide_index=True)
    st.line_chart(pd.DataFrame([{'FY end':x['fiscal_year_end'], 'Net income': x['facts']['net_income']['value']/1e6 if x['facts']['net_income']['value'] is not None else None,
                                'Owner earnings': x['owner_earnings']/1e6 if x['owner_earnings'] is not None else None} for x in r['rows']]).set_index('FY end'))
    st.metric('Revenue CAGR, first to last fiscal year', 'not known' if r['growth_percent'] is None else f"{r['growth_percent']:.2f}%")
    table = [{'Investor':i,'Check':c,'Result':v} for i,cs in r['panel'].items() for c,v in cs.items()]
    st.dataframe(pd.DataFrame(table), hide_index=True)
    for col, investor in zip(st.columns(3), panel.INVESTORS):
        with col:
            st.subheader(investor)
            checks = r['panel'][investor]
            verdict = 'Screen passes; further research' if all(v=='pass' for v in checks.values()) else ('Does not pass the full screen' if 'fail' in checks.values() else 'Insufficient evidence')
            st.write(verdict)
            path = HERE/'memos'/f"{ticker}-{investor.lower().replace(' ','-')}.md"
            memo = path.read_text() if path.exists() else 'No saved memo for these facts.'
            meta = path.with_suffix('.json')
            if meta.exists() and json.loads(meta.read_text()).get('fingerprint') != panel.fingerprint(r):
                st.info('Threshold or facts changed. Saved memo uses the default 15% threshold; use the live checks above.')
            text = st.text_area(investor+' memo', memo, height=290, key=f'{ticker}-{investor}')
            st.markdown(text)
            issues = panel.flags(text,r)
            if issues:
                st.error('Unprinted numbers: '+', '.join(x['number'] for x in issues))
            else:
                st.success('No unprinted numeric tokens.')
            if investor == 'Cathie Wood':
                st.caption('Threshold retained: 15%, to preserve the course growth-screen design. The 5% probe changes the growth check, not missing R&D.')
    st.caption('The numeric guard checks printed-token presence, not correct year/metric association or qualitative truth. Personas share evidence; agreement is not independent verification. No stock price or valuation is used.')
    with st.expander('Computed report and XBRL provenance'):
        st.markdown(panel.printed(r))
    st.download_button('Download panel report', panel.printed(r), f'{ticker}-panel.md')


if __name__ == '__main__':
    main()
