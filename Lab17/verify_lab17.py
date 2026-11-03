"""Recorded-source checks: known answers, revisions, missing days and errors."""
from pathlib import Path
import unittest
import pandas as pd
from rates import parse_csv, compare

EVIDENCE = Path(__file__).resolve().parent / "evidence"


def saved(series, vintage="today"):
    return parse_csv((EVIDENCE/f"{series}-{vintage}.csv").read_text())


class RateTests(unittest.TestCase):
    def test_four_known_answers(self):
        for series, end, value in [("BAA", "2026-09-01", 6.47), ("FEDFUNDS", "2026-09-01", 3.75),
                                   ("DGS10", "2026-10-02", 5.28), ("MORTGAGE30US", "2026-10-01", 7.28)]:
            result = compare(series, saved(series), saved(series, "2026-10-05"))
            self.assertEqual(result["Last measured then"], end)
            self.assertEqual(result["Value then"], value)

    def test_payroll_revision(self):
        current, old = saved("PAYEMS"), saved("PAYEMS", "2025-01-15")
        self.assertEqual(old.loc["2024-12-01"], 159536)
        self.assertLess(current.loc["2024-12-01"], old.loc["2024-12-01"])
        self.assertGreater(compare("PAYEMS", current, old)["Revised common dates"], 0)

    def test_month_end_project_series(self):
        r = compare("DGS10", saved("DGS10"), saved("DGS10", "2026-10-31"))
        self.assertEqual(r["Last measured then"], "2026-10-29")
        self.assertEqual(r["Value then"], 4.98)
        self.assertEqual(r["Last measured today"], "2026-10-30")
        self.assertEqual(r["Later observations"], 1)
        self.assertEqual(r["Revised common dates"], 0)

    def test_missing_days_not_zero(self):
        r = parse_csv("observation_date,DGS10\n2026-01-01,.\n2026-01-02,4.2\n")
        self.assertEqual(len(r), 1)
        self.assertEqual(float(r.iloc[0]), 4.2)

    def test_duplicates_and_html_rejected(self):
        for text in ["<html>error</html>", "observation_date,X\n2026-01-01,1\n2026-01-01,2\n"]:
            with self.assertRaises(ValueError):
                parse_csv(text)

    def test_empty_vintage(self):
        r = compare("DGS10", saved("DGS10"), pd.Series([], index=pd.DatetimeIndex([]), dtype=float))
        self.assertIsNone(r["Last measured then"])
        self.assertEqual(r["Common dates"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
