"""Lab 16: auditable point-in-time filter. Standard library only."""
from datetime import date
import argparse
import json

DECISION_DATE = "2026-03-31"
# Original row numbers are evidence identifiers, not part of duplicate identity.
TABLE = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]


def latest_vintages(rows):
    """Keep one latest publication per ticker/month; flag conflicting ties."""
    chosen = {}
    for row in rows:
        key = row[1:3]
        old = chosen.get(key)
        if old and row[3] == old[3] and row[4] != old[4]:
            raise ValueError(f"Conflicting same-day publications: {old[0]}, {row[0]}")
        if old is None or row[3] > old[3]:
            chosen[key] = row
    return sorted(chosen.values())


def filter_asof(table, decision_date):
    cutoff = date.fromisoformat(decision_date)
    rows = list(table)
    funnel = []

    def remove(label, predicate):
        nonlocal rows
        removed = [r[0] for r in rows if predicate(r)]
        rows = [r for r in rows if r[0] not in removed]
        funnel.append({"rule": label, "removed": removed, "count": len(removed)})

    remove("Quarantine: no ticker", lambda r: not r[1].strip())
    seen, duplicate_ids = set(), set()
    for r in rows:
        if r[1:] in seen:
            duplicate_ids.add(r[0])
        seen.add(r[1:])
    remove("Exact duplicate", lambda r: r[0] in duplicate_ids)
    clean = rows[:]
    remove("Published after decision date", lambda r: date.fromisoformat(r[3]) > cutoff)
    panel = latest_vintages(rows)
    selected = {r[0] for r in panel}
    remove("Older vintage replaced", lambda r: r[0] not in selected)
    return funnel, panel, latest_vintages(clean)


def signals(panel):
    result = {}
    for ticker in sorted({r[1] for r in panel}):
        history = sorted((r for r in panel if r[1] == ticker), key=lambda r: r[2])
        latest = history[-1]
        y, m = map(int, latest[2].split("-"))
        previous_month = f"{y - (m == 1):04d}-{12 if m == 1 else m - 1:02d}"
        previous = next((r for r in history if r[2] == previous_month), None)
        value = None if previous is None or previous[4] == 0 else (latest[4] / previous[4] - 1) * 100
        result[ticker] = {"month": latest[2], "percent": value}
    return result


def audit(decision_date=DECISION_DATE):
    funnel, panel, naive = filter_asof(TABLE, decision_date)
    return {"decision_date": decision_date, "funnel": funnel, "panel": panel,
            "asof": signals(panel), "naive": signals(naive)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=DECISION_DATE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = audit(args.date)
    if args.json:
        print(json.dumps(result, indent=2))
        return
    print(f"Decision date: {args.date}; input rows: {len(TABLE)}")
    for step in result["funnel"]:
        print(f"{step['rule']}: {step['count']} removed, rows {step['removed']}")
    print("\nAs-of panel: row | ticker | measured | published | price | yield")
    for r in result["panel"]:
        print(f"{r[0]:2} | {r[1]} | {r[2]} | {r[3]} | {r[4]:.1f} | {(100/r[4]-1)*100:+.2f}%")
    for ticker in result["asof"]:
        parts = []
        for mode in ("asof", "naive"):
            s = result[mode][ticker]
            value = "not known" if s["percent"] is None else f"{s['percent']:+.2f}%"
            parts.append(f"{mode}: {value} ({s['month']})")
        print(ticker, " | ".join(parts))


if __name__ == "__main__":
    main()
