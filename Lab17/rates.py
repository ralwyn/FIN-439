"""FRED/ALFRED downloads and comparisons; no API keys or inferred vintages."""
from datetime import date, datetime, timezone
from io import StringIO
import re
import requests
import pandas as pd

SERIES = {"BAA": "Moody's Baa corporate bond yield", "FEDFUNDS": "Federal funds rate",
          "DGS10": "10-year Treasury yield", "MORTGAGE30US": "30-year mortgage rate"}


def validate_id(series):
    series = series.strip().upper()
    if not re.fullmatch(r"[A-Z0-9_]{1,40}", series):
        raise ValueError("Use a FRED series ID containing letters, digits or underscores.")
    return series


def parse_csv(text):
    raw = pd.read_csv(StringIO(text), na_values=["."])
    if raw.shape[1] != 2 or raw.columns[0] not in ("DATE", "observation_date"):
        raise ValueError("The source did not return a two-column FRED CSV.")
    raw.columns = ["date", "value"]
    raw["date"] = pd.to_datetime(raw["date"], errors="raise")
    raw["value"] = pd.to_numeric(raw["value"], errors="raise")
    if raw["date"].duplicated().any():
        raise ValueError("Source returned duplicate observation dates.")
    return raw.dropna(subset=["value"]).set_index("date").sort_index()["value"]


def fetch_csv(url):
    response = requests.get(url, timeout=40)
    response.raise_for_status()
    values = parse_csv(response.text)
    return values, {"url": url, "downloaded_at": datetime.now(timezone.utc).isoformat()}


def today_url(series):
    return f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={validate_id(series)}"


def vintage_url(series, asof):
    vintage = date.fromisoformat(str(asof))
    if vintage > date.today():
        raise ValueError("An as-known-on date cannot be in the future.")
    return f"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={validate_id(series)}&vintage_date={vintage}"


def compare(series, current, vintage):
    last_old = vintage.index.max() if len(vintage) else None
    last_now = current.index.max() if len(current) else None
    common = current.index.intersection(vintage.index)
    revised = (current.loc[common] - vintage.loc[common]).abs() > 1e-9
    return {"Series": series, "FRED page": f"https://fred.stlouisfed.org/series/{series}",
            "Last measured then": last_old.date().isoformat() if last_old is not None else None,
            "Value then": float(vintage.loc[last_old]) if last_old is not None else None,
            "Last measured today": last_now.date().isoformat() if last_now is not None else None,
            "Value today": float(current.loc[last_now]) if last_now is not None else None,
            "Later observations": int((current.index > last_old).sum()) if last_old is not None else len(current),
            "Revised common dates": int(revised.sum()),
            "Common dates": len(common),
            "Previously present, absent today": len(vintage.index.difference(current.index))}
