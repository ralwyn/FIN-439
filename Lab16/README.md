# Lab 16 — Provenance Gate

Catch-up build dated November 3, 2026. Built with AI assistance. The training table is fictional; outputs are computed from its rows, not typed in as answers.

## Run and evidence

From this folder: `python asof.py`, `python asof.py --date 2026-04-15`, and `python verify_lab16.py`. Standard library only. `results.txt` is the executed default output; `later-date-results.txt` records the April 15 probe; `validation.txt` records the checks.

## What the filter proves

The four rules run in the assigned order: quarantine a blank ticker, remove exact duplicates, remove future publications, then retain the latest available revision for each ticker/month. Original row numbers survive so each exclusion has an audit trail. Duplicate identity excludes the row identifier itself.

| Step | Original row IDs removed |
|---|---|
| Missing ticker | 11 |
| Exact duplicate | 7 |
| Published after March 31 | 3, 8, 10 |
| Older revision | 2 |
| Kept | 1, 4, 5, 6, 9, 12 |

| Fund | Knowable return | Naive return |
|---|---:|---:|
| AAA | +1.98% | +5.83% |
| BBB | −1.02% | −5.15% |
| CCC | +0.91% | +1.82% |

AAA is 103/101−1 as known on March 31. The naive calculation uses the March price published April 10 and returns 109/103−1. The 3.85 percentage-point difference is information unavailable on the decision date. Keeping the earlier February price of 104 is also wrong: the March 25 revision was already knowable. On April 15 all three knowable signals equal their naive comparisons.

## Sanity check — worked study solution

These calculations are provided as AI-assisted study work, not a claim that the student's required by-hand exercise has occurred. Yield = 100/price−1.

| Row | Price | Yield | Classroom sanity issue |
|---|---:|---:|---|
| 1 | 101 | −0.99% | Negative yield |
| 4 | 103 | −2.91% | Negative yield |
| 5 | 98 | +2.04% | None in the exercise |
| 6 | 97 | +3.09% | None in the exercise |
| 9 | 110 | −9.09% | Negative yield; CCC priced above AAA and BBB |
| 12 | 111 | −9.91% | Negative yield; CCC priced above AAA and BBB |

A proposed fifth rule quarantines prices above face value in this exercise and credit-order violations within the same month/maturity. These are the lab's planted anomalies; negative yields can occur in actual markets, so the classroom rule is not a universal finance law. Provenance alone establishes timing, not economic validity.

## Explain the revision code

`latest_vintages` builds a dictionary keyed by ticker and measured month. For each surviving row, it reads the existing candidate. A newer publication replaces the candidate; an older one does not. Equally dated conflicting values stop the run rather than choosing silently. After future publications have been removed, the dictionary therefore contains only the newest vintage actually available by the cutoff. The signal uses the immediately preceding calendar month; a missing month produces an unknown result rather than a mislabeled monthly return.

Practice question: why must future publications be removed before selecting the latest vintage? If the future revision wins first, it can displace the earlier value that the decision maker really had.

## Reflection draft for student review

The future-publication rule removes the biggest source of look-ahead information, while the revision rule is essential to recover the correct February AAA value. A naive backtest would attribute later releases and revisions to an earlier decision. A financial sanity gate is still needed after the timing gate.

## Completion status

Code, known-answer validation, later-date probe and study notes are complete. The student reports on November 3 that the professor waived in-person attendance and partner work because of career fairs. Partner activities are therefore not outstanding. Personal review of the code, by-hand calculations and explanations remains useful preparation; no partner participation is claimed. GitHub publication is separate from Brightspace checkout and late-work acceptance.
