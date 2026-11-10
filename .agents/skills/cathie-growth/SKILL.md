---
name: cathie-growth
description: Apply the FIN 439 Cathie Wood growth and R&D screen to annual SEC facts and write a bounded Lab 19 business memo.
---

From the course repository run `python .agents/skills/cathie-growth/scripts/screen.py COST`. Replace COST with the requested ticker. Saved SEC sources support COST, NVDA and JPM; append `--live` only for a fresh download. The bundled wrapper uses Lab19/panel.py so the panel reads identical facts; Lab 18 remains intact.

Checks in code: Revenue CAGR (last / first)^(1/4)-1 at least 15%; latest R&D/revenue at least 5%. Missing inputs yield not known. Probe 5% growth but retain 15% by default. Revenue growth and R&D do not prove innovation or an investment opportunity.

Select five annual 10-K USD periods by actual fiscal end, use the latest filing for the same period and only the course XBRL tags/fallbacks. Preserve source tags, dates, accessions and gaps. Do not estimate absent facts. Annual flows must match fiscal starts and ends; equity is year-end equity. No price data, valuation, trading, paid keys or installation of FAskills.

Read the computed report, then write a separate simulated Cathie Wood business memo using only printed numbers. Give a verdict and a limiting condition. Save under Lab19/memos, validate with `panel.flags`, and manually check year/metric associations. The numeric guard cannot establish qualitative truth. This perspective is an interpretation, not an independent verification or the investor's actual opinion.

Reference philosophy: https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/cathie_wood.md. Read for context; apply the course's narrower checks. For the Cathie threshold probe append `--threshold 5` and explain any retained threshold.
