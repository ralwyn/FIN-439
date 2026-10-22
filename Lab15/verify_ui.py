"""Streamlit smoke and interaction checks: python verify_ui.py."""
from pathlib import Path
from streamlit.testing.v1 import AppTest

app = AppTest.from_file(str(Path(__file__).with_name('app.py'))).run(timeout=30)
assert not app.exception, [e.message for e in app.exception]
assert [m.value for m in app.metric] == ['6.51%', '9.44%', '20.00%', '0.00 pp']
next(n for n in app.number_input if n.label == 'Global equity index fund expected return (%)').set_value(7).run(timeout=30)
assert not app.exception
assert [m.value for m in app.metric] == ['6.53%', '12.94%', '10.00%', '25.00 pp']
print('PASS: Meridian original and equity-return stress match published app results.')
app.selectbox[0].select('Scholarship fund demo').run(timeout=30)
assert not app.exception
assert [m.value for m in app.metric] == ['6.61%', '6.05%', '60.00%', '0.00 pp']
next(c for c in app.checkbox if c.label == 'Last 36 monthly returns').check().run(timeout=30)
assert not app.exception
assert [m.value for m in app.metric] == ['6.75%', '1.79%', '85.00%', '25.00 pp']
print('PASS: scholarship full-history and last-36 app results match engine results.')
next(c for c in app.checkbox if c.label == 'Last 36 monthly returns').uncheck().run(timeout=30)
next(b for b in app.button if b.label.startswith('Stress VT:')).click().run(timeout=30)
assert not app.exception
assert [m.value for m in app.metric] == ['6.53%', '6.79%', '55.00%', '5.00 pp']
next(b for b in app.button if b.label == 'Restore window estimates').click().run(timeout=30)
assert not app.exception
assert app.metric[0].value == '6.61%'
print('PASS: VT attack and restore controls work.')
next(n for n in app.number_input if n.label == 'Objective return (%)').set_value(100).run(timeout=30)
assert not app.exception and any(w.value == 'no mix meets the objective' for w in app.warning)
print('PASS: infeasible objective is reported without changing the target.')
app.selectbox[0].select('Enter ETF tickers').run(timeout=30)
assert not app.exception and app.text_input[0].value == 'BIL, IEF, QQQ, SPY'
print('PASS: direct ETF entry form renders. Actual Yahoo fetch was separately verified in the browser.')
