from pathlib import Path
import datetime
from streamlit.testing.v1 import AppTest

app=AppTest.from_file(str(Path(__file__).with_name('app.py'))).run(timeout=30)
assert not app.exception,[x.message for x in app.exception]
assert any('RESEARCH PILOT' in x.value for x in app.info)
next(x for x in app.slider if x.label=='Minimum BIL reserve (%)').set_value(90).run(timeout=30)
assert not app.exception,[x.message for x in app.exception]
assert any('PAUSE' in x.value for x in app.info)
next(x for x in app.slider if x.label=='Minimum BIL reserve (%)').set_value(10).run(timeout=30)
assert not app.exception
next(x for x in app.date_input if x.label=='Information cutoff').set_value(datetime.date(2026,10,31)).run(timeout=30)
assert any('QUARANTINE' in x.value for x in app.info)
next(x for x in app.date_input if x.label=='Information cutoff').set_value(datetime.date(2026,11,10)).run(timeout=30)
next(x for x in app.radio if x.label=='Estimation window').set_value('Last 36').run(timeout=30)
assert not app.exception
next(x for x in app.slider if x.label=='Trading cost (bps per one-way turnover)').set_value(100).run(timeout=30)
assert not app.exception
print('PASS: portfolio app, infeasible reserve verdict, timing quarantine, alternate window and cost controls.')
