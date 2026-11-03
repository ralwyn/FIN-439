from pathlib import Path
from datetime import date
from unittest.mock import patch
import sys,json,gzip
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'Lab17'))
sys.path.insert(0,str(ROOT/'.agents/skills/buffett-business/scripts'))
import streamlit as st
import requests
import edgar_facts
from urllib.parse import urlparse,parse_qs
results=[]
class Response:
 def __init__(self,text):self.text=text
 def raise_for_status(self):pass

def source_get(url,**kwargs):
 q=parse_qs(urlparse(url).query);s=q['id'][0];v=q.get('vintage_date',['today'])[0]
 if s not in ['BAA','FEDFUNDS','DGS10','MORTGAGE30US','PAYEMS']:raise requests.HTTPError('404 invalid series (test fixture)')
 if v==date.today().isoformat():v='today'
 p=ROOT/'Lab17/evidence'/f'{s}-{v}.csv'
 if not p.exists():raise ValueError('No recorded fixture for '+str(p))
 return Response(p.read_text())

def no_exception(app):
 assert len(app.exception)==0,[x.message for x in app.exception]

with patch('requests.get',side_effect=source_get):
 st.cache_data.clear()
 a=AppTest.from_file(str(ROOT/'Lab17/asof_app.py'),default_timeout=30).run();no_exception(a)
 assert len(a.dataframe)==1 and len(a.dataframe[0].value)==4
 a.sidebar.date_input[1].set_value(date(2026,10,5)).run();no_exception(a)
 table=a.dataframe[0].value
 assert table['Value then'].tolist()==[6.47,3.75,5.28,7.28]
 a.sidebar.text_input[0].set_value('INVALID_ID').run();no_exception(a)
 assert len(a.error)==1 and len(a.dataframe[0].value)==4
 a.sidebar.multiselect[0].set_value([])
 a.sidebar.text_input[0].set_value('PAYEMS')
 a.sidebar.date_input[1].set_value(date(2025,1,15)).run();no_exception(a)
 assert a.dataframe[0].value.iloc[0]['Value then']==159536
 assert a.dataframe[0].value.iloc[0]['Revised common dates']==381
 results.append('Lab17: four charts/table; historical date; invalid-ID isolation; PAYEMS revision probe passed using recorded HTTP fixtures.')

def fixture_company(ticker,cache):
 p=ROOT/'Lab18/evidence'
 if ticker not in ['COST','JPM']:raise ValueError('Unknown ticker (test fixture)')
 return json.loads(gzip.decompress((p/f'{ticker}-companyfacts.json.gz').read_bytes())),json.loads((p/f'{ticker}-source.json').read_text())
with patch.object(edgar_facts,'fetch_company',side_effect=fixture_company):
 st.cache_data.clear()
 a=AppTest.from_file(str(ROOT/'Lab18/buffett_app.py'),default_timeout=30).run();no_exception(a)
 assert a.dataframe[1].value['Result'].tolist()==['pass']*3
 a.sidebar.radio[0].set_value('Saved verified download').run();no_exception(a)
 a.text_area[0].set_value(a.text_area[0].value+'\nFabricated ROE: 40.0%.').run();no_exception(a)
 assert any('40.0%' in e.value for e in a.error)
 a.sidebar.text_input[0].set_value('JPM').run();no_exception(a)
 assert a.dataframe[1].value['Result'].tolist()==['fail','not known','not known']
 assert a.dataframe[0].value['Owner earnings'].tolist()==['not found']*5
 a.sidebar.text_input[0].set_value('../bad').run();no_exception(a)
 assert any('Invalid ticker' in e.value for e in a.error)
 results.append('Lab18: COST checks/memo; saved replay; 40.0% warning; JPM honest gaps; invalid ticker passed.')
print('\n'.join(results))
(ROOT/'app-validation.txt').write_text('AppTest widget validation; recorded HTTP fixtures, not live network calls.\n'+'\n'.join(results)+'\n')
