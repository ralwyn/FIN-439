"""Known-answer, boundary and missing-month checks, independent of presentation."""
import unittest
from asof import audit, filter_asof, signals


class ProvenanceTests(unittest.TestCase):
    def test_known_answer(self):
        r = audit()
        self.assertEqual([s["removed"] for s in r["funnel"]], [[11], [7], [3, 8, 10], [2]])
        self.assertEqual([x[0] for x in r["panel"]], [1, 4, 5, 6, 9, 12])
        for t, a, n in [("AAA", 1.98, 5.83), ("BBB", -1.02, -5.15), ("CCC", .91, 1.82)]:
            self.assertEqual(round(r["asof"][t]["percent"], 2), a)
            self.assertEqual(round(r["naive"][t]["percent"], 2), n)

    def test_later_date(self):
        r = audit("2026-04-15")
        self.assertEqual(r["asof"], r["naive"])

    def test_publication_boundary(self):
        self.assertEqual(audit("2026-03-24")["panel"][1][0], 2)
        self.assertEqual(audit("2026-03-25")["panel"][1][0], 4)

    def test_missing_previous_month(self):
        self.assertIsNone(signals([(1, "X", "2026-01", "2026-02-01", 1),
                                   (2, "X", "2026-03", "2026-04-01", 2)])["X"]["percent"])

    def test_conflicting_same_day(self):
        with self.assertRaises(ValueError):
            filter_asof([(1, "X", "2026-01", "2026-02-01", 1),
                         (2, "X", "2026-01", "2026-02-01", 2)], "2026-03-01")


if __name__ == "__main__":
    unittest.main(verbosity=2)
