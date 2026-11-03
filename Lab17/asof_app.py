"""Run: python -m streamlit run asof_app.py"""
from datetime import date
import pandas as pd
import streamlit as st
from rates import SERIES, fetch_csv, today_url, vintage_url, validate_id, compare


@st.cache_data(ttl=3600, show_spinner=False)
def download_today(series, download_day):
    # download_day prevents yesterday's cache from masquerading as today's download.
    return fetch_csv(today_url(series))


@st.cache_data(ttl=3600, show_spinner=False)
def download_asof(series, asof, download_day):
    return fetch_csv(vintage_url(series, asof))


def main():
    st.set_page_config(page_title="Point-in-Time Rates Audit", layout="wide")
    st.title("Point-in-Time Rates Audit")
    st.caption("Data from FRED and ALFRED, Federal Reserve Bank of St. Louis; "
               f"downloaded {date.today():%Y-%m-%d}. Built with AI help, a learning demonstration, not investment advice.")
    selected = st.sidebar.multiselect("Series", list(SERIES), default=list(SERIES),
                                      format_func=lambda s: f"{s} — {SERIES[s]}")
    extra = st.sidebar.text_input("Add a FRED series ID", help="For example PAYEMS or DGS10")
    start = st.sidebar.date_input("Chart start", value=date(2020, 1, 1), min_value=date(1900, 1, 1))
    asof = st.sidebar.date_input("As known on", value=date.today(), min_value=date(1776, 7, 4), max_value=date.today())
    if st.sidebar.button("Refresh downloads"):
        st.cache_data.clear()
    if extra.strip():
        try:
            added = validate_id(extra)
            if added not in selected:
                selected.append(added)
        except ValueError as exc:
            st.error(str(exc))
    st.info("Charts show today's history. The table uses a separate historical vintage. "
            "Counts cover the full downloaded history; the chart start changes only the charts.")
    summaries = []
    provenance = []
    for series in selected:
        st.subheader(f"{series} · {SERIES.get(series, 'Additional series')}")
        try:
            with st.spinner(f"Downloading {series}…"):
                current, current_meta = download_today(series, date.today().isoformat())
                vintage, vintage_meta = download_asof(series, asof.isoformat(), date.today().isoformat())
            summary = compare(series, current, vintage)
            summaries.append(summary)
            st.line_chart(current.loc[str(start):].rename("Today's published value"))
            st.caption(f"Last measured date known on {asof}: {summary['Last measured then'] or 'none'}")
            provenance.extend([{"series": series, "kind": "today", **current_meta},
                               {"series": series, "kind": "vintage", **vintage_meta}])
        except Exception as exc:
            st.error(f"{series}: {exc}")
    st.subheader("What was knowable?")
    if summaries:
        frame = pd.DataFrame(summaries)
        st.dataframe(frame, hide_index=True, column_config={"FRED page": st.column_config.LinkColumn("FRED source")})
        st.download_button("Download audit table", frame.to_csv(index=False), "rates-audit.csv", "text/csv")
    else:
        st.warning("Select at least one valid series to see an audit.")
    with st.expander("Download provenance"):
        st.json(provenance)
    st.caption("A vintage is a date-level information set, not proof that a value was available before an intraday trade.")


if __name__ == "__main__":
    main()
