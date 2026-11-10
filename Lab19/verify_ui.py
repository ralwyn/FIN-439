from pathlib import Path
from streamlit.testing.v1 import AppTest

app=AppTest.from_file(str(Path(__file__).with_name('app.py'))).run(timeout=30)
assert not app.exception,[x.message for x in app.exception]
assert app.metric[0].value=='7.51%'
assert len(app.text_area)==3 and len(app.success)==3
app.select_slider[0].set_value(5).run(timeout=30)
assert not app.exception
app.selectbox[0].set_value('NVDA').run(timeout=30)
assert not app.exception and app.metric[0].value=='68.30%'
for index in range(3):
    old=app.text_area[index].value
    app.text_area[index].set_value(old+' Unsupported ROE 987.654321%.').run(timeout=30)
    assert any('987.654321%' in x.value for x in app.error)
    app.text_area[index].set_value(old).run(timeout=30)
app.selectbox[0].set_value('JPM').run(timeout=30)
assert not app.exception and len(app.success)==3
print('PASS: COST, threshold probe, NVDA, unprinted-number flag in all three memos, JPM gaps.')
