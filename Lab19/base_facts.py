"""Compute Lab 18 facts from SEC companyfacts; standard library only.

Live: python edgar_facts.py COST --out Lab18/evidence
Replay: add --facts-file Lab18/evidence/COST-companyfacts.json.gz
SEC_USER_AGENT must identify the caller and contact email for live requests.
"""
import argparse
from datetime import date, datetime, timezone
from decimal import Decimal
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
from urllib.request import Request, urlopen

FIELDS = {
    "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"),
    "net_income": ("NetIncomeLoss",),
    "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",),
    "capital_spending": ("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"),
    "equity": ("StockholdersEquity",),
}
FLOWS = {"revenue", "net_income", "operating_cash_flow", "capital_spending"}
NUMBER = re.compile(r"(?<![\d.])[-+−]?(?:(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+)(?:[eE][-+]?\d+)?(?:[ \t]*%)?(?!\d|\.\d|[eE][-+]?\d|%)")


def user_agent():
    explicit = os.environ.get("SEC_USER_AGENT", "")
    if explicit:
        value = explicit
    else:
        # Use the user's already configured identity without publishing their email in code.
        def config(key):
            try:
                env = {**os.environ, "DEVELOPER_DIR": "/Library/Developer/CommandLineTools"}
                return subprocess.check_output(["git", "config", key], env=env, text=True).strip()
            except (OSError, subprocess.CalledProcessError):
                return ""
        value = f"{config('user.name')} {config('user.email')}"
    if "@" not in value or not value.split():
        raise ValueError("Set SEC_USER_AGENT to your name and contact email for SEC requests.")
    return value


def download_json(url, cache):
    cache = Path(cache)
    if cache.exists() and time.time() - cache.stat().st_mtime < 86400:
        return json.loads(cache.read_text()), json.loads(cache.with_suffix(".meta.json").read_text())
    request = Request(url, headers={"User-Agent": user_agent(), "Accept-Encoding": "identity"})
    with urlopen(request, timeout=45) as response:
        payload = response.read()
    data = json.loads(payload)
    meta = {"url": url, "downloaded_at": datetime.now(timezone.utc).isoformat(),
            "sha256": hashlib.sha256(payload).hexdigest()}
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(payload)
    cache.with_suffix(".meta.json").write_text(json.dumps(meta, indent=2))
    time.sleep(.25)  # Sequential requests, well below SEC's published limit.
    return data, meta


def validate_ticker(ticker):
    ticker = ticker.upper().strip()
    if not re.fullmatch(r"[A-Z0-9.-]{1,15}", ticker):
        raise ValueError("Invalid ticker.")
    return ticker


def fetch_company(ticker, cache):
    ticker = validate_ticker(ticker)
    listing, _ = download_json("https://www.sec.gov/files/company_tickers.json", Path(cache)/"tickers.json")
    match = next((r for r in listing.values() if r["ticker"] == ticker), None)
    if match is None:
        raise ValueError(f"Ticker {ticker} was not found in the SEC listing.")
    cik = int(match["cik_str"])
    return download_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json", Path(cache)/f"{ticker}.json")


def annual(record):
    if record.get("form") != "10-K" or not record.get("start"):
        return False
    days = (date.fromisoformat(record["end"]) - date.fromisoformat(record["start"])).days + 1
    # Calendar and 52/53-week fiscal years; reject quarters and year-to-date fragments.
    return 330 <= days <= 400


def records(facts, tag, is_flow):
    return [r for r in facts.get(tag, {}).get("units", {}).get("USD", [])
            if r.get("form") == "10-K" and (annual(r) if is_flow else not r.get("start"))]


def latest_record(candidates):
    if not candidates:
        return None
    latest = max(r["filed"] for r in candidates)
    candidates = [r for r in candidates if r["filed"] == latest]
    if len({r["val"] for r in candidates}) > 1:
        raise ValueError("Conflicting values in equally recent filings; inspect source contexts.")
    return max(candidates, key=lambda r: r.get("accn", ""))


def select_fact(facts, field, end, start):
    for tag in FIELDS[field]:
        candidates = [r for r in records(facts, tag, field in FLOWS)
                      if r["end"] == end and (field not in FLOWS or r["start"] == start)]
        chosen = latest_record(candidates)
        if chosen is not None:
            return {"value": chosen["val"], "tag": "us-gaap:" + tag, "units": "USD",
                    "start": chosen.get("start"), "end": end, "filed": chosen["filed"],
                    "accession": chosen["accn"]}
    return {"value": None, "tag": None, "status": "not found",
            "attempted_tags": ["us-gaap:" + t for t in FIELDS[field]]}


def make_row(facts, end, start):
    row = {"fiscal_year_end": end, "fiscal_year_start": start,
           "facts": {f: select_fact(facts, f, end, start) for f in FIELDS}}
    v = {k: f["value"] for k, f in row["facts"].items()}
    row["roe_percent"] = None if v["net_income"] is None or v["equity"] is None or v["equity"] <= 0 else v["net_income"] / v["equity"] * 100
    row["owner_earnings"] = None if v["operating_cash_flow"] is None or v["capital_spending"] is None else v["operating_cash_flow"] - v["capital_spending"]
    return row


def checks(rows):
    def all_years(values, predicate):
        if len(values) != 5 or any(v is None for v in values):
            return "not known"
        return "pass" if all(predicate(v) for v in values) else "fail"
    roe = [r["roe_percent"] for r in rows]
    oe = [r["owner_earnings"] for r in rows]
    growth = "not known" if len(oe) != 5 or oe[0] is None or oe[-1] is None else ("pass" if oe[-1] > oe[0] else "fail")
    return {"ROE at least 15% every year": all_years(roe, lambda x: x >= 15),
            "Owner earnings positive every year": all_years(oe, lambda x: x > 0),
            "Owner earnings grew first to last": growth}


def build_report(data, ticker, source):
    facts = data.get("facts", {}).get("us-gaap", {})
    anchors = records(facts, "NetIncomeLoss", True)
    ends = sorted({r["end"] for r in anchors})[-5:]
    if not ends:
        raise ValueError("No annual USD NetIncomeLoss facts from 10-K filings found.")
    rows = []
    for end in ends:
        anchor = latest_record([r for r in anchors if r["end"] == end])
        rows.append(make_row(facts, end, anchor["start"]))
    return {"ticker": ticker, "company": data["entityName"], "source": source,
            "basis": "Latest available 10-K facts, not a historical as-of screen",
            "rows": rows, "checks": checks(rows)}


def money(value):
    return "not found" if value is None else f"{value / 1_000_000:,.0f}"


def facts_fingerprint(report):
    payload = {k: report[k] for k in ("ticker", "company", "rows", "checks")}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def report_text(report):
    lines = [f"# {report['ticker']} · {report['company']}", "", report["basis"],
             "Source: SEC EDGAR; 10-K only. USD millions, except ROE (%).",
             f"Downloaded: {report['source'].get('downloaded_at', 'unknown')}", "",
             "| Fiscal year end | Revenue | Net income | Operating cash flow | Capital spending | Equity | Liabilities | R&D | ROE % | Owner earnings |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in report["rows"]:
        amounts = [money(r["facts"][f]["value"]) for f in FIELDS]
        roe = "not known" if r["roe_percent"] is None else f"{r['roe_percent']:.1f}"
        lines.append("| " + " | ".join([r["fiscal_year_end"], *amounts, roe, money(r["owner_earnings"])]) + " |")
    lines += ["", "ROE = net income / year-end equity; owner earnings = operating cash flow - capital spending.",
              "The owner-earnings formula is the course proxy, not an estimate of maintenance capital spending.", ""]
    lines += [f"- {name}: **{verdict}**" for name, verdict in report["checks"].items()]
    lines += ["", "## XBRL provenance", "",
              "| Fiscal year end | Field | Tag | USD value | Period start | Filed | Accession |",
              "|---|---|---|---:|---|---|---|"]
    for r in report["rows"]:
        for field, f in r["facts"].items():
            lines.append("| " + " | ".join([r["fiscal_year_end"], field, f.get("tag") or "not found",
                str(f["value"]) if f["value"] is not None else "not found", f.get("start") or "instant",
                f.get("filed", "not found"), f.get("accession", "not found")]) + " |")
    lines += ["", "Derived tags: ROE uses us-gaap:NetIncomeLoss / us-gaap:StockholdersEquity; "
              "owner earnings uses the operating-cash-flow tag minus the selected capital-spending tag.",
              "Missing source facts remain not found; checks with missing inputs remain not known."]
    return "\n".join(lines) + "\n"


def normalize_number(token):
    # Percent is part of identity: 40 USD is not evidence for 40% ROE.
    percent = token.endswith("%")
    return (Decimal(token.rstrip("%").strip().replace(",", "").replace("−", "-")), percent)


def unprinted_numbers(memo, printed):
    tokens = NUMBER.findall(printed)
    allowed = {normalize_number(t) for t in tokens}
    # Table ROE values omit the % symbol because the column carries its units.
    for line in printed.splitlines():
        if line.startswith("| ") and re.match(r"\| \d{4}-\d{2}-\d{2} \|", line) and len(line.split("|")) == 10:
            roe = line.split("|")[7].strip()
            if roe != "not known":
                allowed.add(normalize_number(roe + "%"))
    return [{"number": m.group(), "start": m.start(), "end": m.end()}
            for m in NUMBER.finditer(memo) if normalize_number(m.group()) not in allowed]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker")
    parser.add_argument("--out", type=Path, default=Path("Lab18/evidence"))
    parser.add_argument("--facts-file", type=Path)
    parser.add_argument("--source-meta", type=Path)
    args = parser.parse_args()
    ticker = validate_ticker(args.ticker)
    if args.facts_file:
        raw = gzip.decompress(args.facts_file.read_bytes()) if args.facts_file.suffix == ".gz" else args.facts_file.read_bytes()
        data = json.loads(raw)
        source = json.loads(args.source_meta.read_text()) if args.source_meta else {"mode": "provided file", "sha256": hashlib.sha256(raw).hexdigest()}
    else:
        data, source = fetch_company(ticker, args.out / "cache")
    report = build_report(data, ticker, source)
    args.out.mkdir(parents=True, exist_ok=True)
    text = report_text(report)
    (args.out/f"{ticker}-facts.json").write_text(json.dumps(report, indent=2) + "\n")
    (args.out/f"{ticker}-printed.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
