---
name: burry-cash
description: Apply the FIN 439 Burry cash-conversion and liabilities screen to annual SEC facts and write a skeptical Lab 19 business memo.
---

From the course repository run `python .agents/skills/burry-cash/scripts/screen.py COST`. Replace COST with the requested ticker. Saved SEC sources support COST, NVDA and JPM; append `--live` only for a fresh download. The bundled wrapper uses Lab19/panel.py so the panel reads identical facts; Lab 18 remains intact.

Checks in code: Operating cash flow at least net income every year; latest liabilities/year-end equity no more than two. Missing inputs or nonpositive equity yield not known. A screen failure is not an accusation of fraud.

Select five annual 10-K USD periods by actual fiscal end, use the latest filing for the same period and only the course XBRL tags/fallbacks. Preserve source tags, dates, accessions and gaps. Do not estimate absent facts. Annual flows must match fiscal starts and ends; equity is year-end equity. No price data, valuation, trading, paid keys or installation of FAskills.

Read the computed report, then write a separate simulated Burry business memo using only printed numbers. Give a verdict and a limiting condition. Save under Lab19/memos, validate with `panel.flags`, and manually check year/metric associations. The numeric guard cannot establish qualitative truth. This perspective is an interpretation, not an independent verification or the investor's actual opinion.

Reference philosophy: https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md. Read for context; apply the course's narrower checks. For the Cathie threshold probe append `--threshold 5` and explain any retained threshold.
