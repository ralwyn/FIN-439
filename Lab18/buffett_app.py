"""Run from the repository: python -m streamlit run Lab18/buffett_app.py"""
from pathlib import Path
import gzip
import json
import sys
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".agents/skills/buffett-business/scripts"))
from edgar_facts import (build_report, fetch_company, report_text, unprinted_numbers,
                         facts_fingerprint, validate_ticker, FIELDS)


@st.cache_data(ttl=3600, show_spinner=False)
def live_report(ticker):
    data, source = fetch_company(ticker, ROOT / "Lab18/cache")
    return build_report(data, ticker, source)


def saved_report(ticker):
    evidence = ROOT / "Lab18/evidence"
    source = json.loads((evidence / f"{ticker}-source.json").read_text())
    raw = gzip.decompress((evidence / f"{ticker}-companyfacts.json.gz").read_bytes())
    return build_report(json.loads(raw), ticker, source)


def main():
    st.set_page_config(page_title="Buffett Business Screen", layout="wide")
    st.title("Buffett Business Screen")
    st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
    ticker = st.sidebar.text_input("Ticker", "COST").strip().upper()
    mode = st.sidebar.radio("Data source", ["Live SEC", "Saved verified download"])
    try:
        ticker = validate_ticker(ticker)
    except ValueError as exc:
        st.error(str(exc))
        return
    if st.sidebar.button("Refresh SEC data"):
        live_report.clear()
        for p in (ROOT/"Lab18/cache").glob(f"{ticker}.*"):
            # Invalidate cache age without deleting a user's saved evidence.
            import os
            os.utime(p, (0, 0))
    try:
        with st.spinner("Selecting annual SEC facts…"):
            report = live_report(ticker) if mode == "Live SEC" else saved_report(ticker)
    except Exception as exc:
        st.error(f"Unable to load {ticker}: {exc}")
        st.info("Live downloads need a SEC User-Agent with your name and email. Saved downloads are available for COST and JPM.")
        return
    st.subheader(f"{ticker} · {report['company']}")
    st.caption(f"{mode}. Downloaded: {report['source'].get('downloaded_at', 'unknown')}")
    st.info("Latest available annual filings. This screen judges the business from a limited set of facts; "
            "it does not assess stock valuation or reproduce a historical investment information set.")
    table = []
    for row in report["rows"]:
        table.append({"Fiscal year end": row["fiscal_year_end"],
                      **{f.replace("_", " ").title(): "not found" if row["facts"][f]["value"] is None else f"{row['facts'][f]['value']/1e6:,.0f}" for f in FIELDS},
                      "ROE %": "not known" if row["roe_percent"] is None else f"{row['roe_percent']:.1f}",
                      "Owner earnings": "not found" if row["owner_earnings"] is None else f"{row['owner_earnings']/1e6:,.0f}"})
    chart = pd.DataFrame([{"Fiscal year end": r["fiscal_year_end"],
                           "Owner earnings": None if r["owner_earnings"] is None else r["owner_earnings"]/1e6,
                           "Net income": None if r["facts"]["net_income"]["value"] is None else r["facts"]["net_income"]["value"]/1e6}
                          for r in report["rows"]]).set_index("Fiscal year end")
    st.line_chart(chart, y_label="USD millions")
    st.caption("Missing owner earnings remain gaps in the chart. USD millions, except ROE.")
    st.dataframe(pd.DataFrame(table), hide_index=True)
    st.dataframe(pd.DataFrame([{"Check": k, "Result": v} for k, v in report["checks"].items()]), hide_index=True)
    printed = report_text(report)
    st.download_button("Download computed report", printed, f"{ticker}-printed.md", "text/markdown")
    st.download_button("Download facts and provenance", json.dumps(report, indent=2), f"{ticker}-facts.json", "application/json")
    with st.expander("XBRL tags, selected filing dates, accessions and formulas"):
        st.markdown(printed)
    st.subheader("AI judgment · simulated Buffett perspective")
    memo_path = ROOT / "Lab18/memos" / f"{ticker}.md"
    memo = memo_path.read_text() if memo_path.exists() else ""
    meta_path = memo_path.with_name(f"{ticker}-meta.json")
    if memo:
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
        if meta.get("facts_fingerprint") != facts_fingerprint(report):
            st.warning("This saved memo is not bound to the current selected facts. Run the skill again before relying on it.")
    else:
        st.warning("No memo has been generated for this ticker. Invoke $buffett-business in Codex, then rerun the app, or paste its memo below.")
    edited = st.text_area("Memo (editable for the unsupported-number probe)", memo, height=260, key=f"memo-{ticker}-{mode}")
    st.markdown(edited.replace("$", r"\$"))
    flags = unprinted_numbers(edited, printed)
    if flags:
        st.error("Unprinted numbers: " + ", ".join(x["number"] for x in flags))
        st.dataframe(pd.DataFrame(flags), hide_index=True)
    elif edited.strip():
        st.success("Every numeric token appears in the computed report.")
    st.caption("The guard compares numeric tokens, including percentages. It cannot prove that a supported number "
               "belongs to the right year or metric, or that a qualitative claim is supported. Review those associations.")
    st.download_button("Download memo text", edited, f"{ticker}-memo.md", "text/markdown")


if __name__ == "__main__":
    main()
