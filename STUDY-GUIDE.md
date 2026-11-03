# Labs 16–18 — what to understand

## The connecting idea

A useful answer needs a chain of evidence: source → information available at the time → explicit calculation → bounded judgment. Lab 16 establishes the timing rules on a small table. Lab 17 applies the timing question to real economic data. Lab 18 separates repeatable computations from the model's interpretation.

## Lab 16: two dates and one honest information set

**Observation date:** the period a value measures. **Publication date:** when it became available. **Revision:** a replacement published later for that same observation period. The historical answer uses the latest revision published by the cutoff, not the earliest value and not today's value.

AAA February was initially 104, then revised to 103 before March 31. January was 101. The knowable change is 103/101−1 = 1.98%. March's 109 was published April 10 and cannot be used for a March 31 decision; using it creates the 5.83% naive signal. A backtest with that future information has look-ahead bias.

A provenance gate says when a value was knowable, not whether it is sensible. The exercise's strange bond prices need a separate sanity check. For its one-year zero, yield = 100/price−1. A price above 100 yields a negative number; the exercise treats that as an anomaly, although negative yields exist in real markets.

**Self-check:** Why is “remove all revisions” wrong? Because the revision published before the decision was part of the information set. Why does a fixed publication lag fail to repair today's data? It cannot reconstruct earlier values replaced by revisions.

## Lab 17: today's history versus history as it looked then

FRED returns the series as published today. ALFRED returns a historical vintage. An honest comparison needs two source downloads, not today's data sliced at an earlier measurement date. Missing days are not zeros. Revisions are differences on matching observation dates; later observations are dates absent because the vintage stopped earlier. These are different effects.

PAYEMS is the deliberate leak detector: December 2024 was 159,536 in the January 15, 2025 vintage and 158,316 in the saved current file. A zero revised count in this case would be a warning to inspect whether the app fetched today's file twice.

A data card states source, measure, units, frequency, release timing, revision behavior and download date. A claim of “clean data” does not establish any of those. DGS10 is a daily annualized yield quoted in percent; it is not an ETF total return. A date-level vintage also does not establish that you could trade on its contents that morning.

**Self-check:** Can a daily series have publication lag? Yes; measuring a rate on a day is distinct from publishing it. Can zero revisions prove future corrections are impossible? No; it describes the comparison you actually made.

## Lab 18: a skill constrains the workflow, not all judgment

A skill folder contains a `SKILL.md` with a name and description, plus any scripts it needs. Metadata tells the model when to use it; the full instructions describe the task. The bundled script is the quantitative authority. The model interprets the printed results and must preserve gaps.

SEC companyfacts mixes annual and quarterly forms, durations, instants and comparative years. Filter to 10-K, USD, annual flows and matching fiscal periods. Label years by actual fiscal-year end, not simply the `fy` field of a later filing repeating comparative data. Costco's 53-week year is still a fiscal year. Use permitted fallback tags only and record which was selected.

**Course formulas:** ROE = net income/year-end equity. Owner earnings = operating cash flow−capital spending. These are classroom definitions; a richer owner-earnings analysis would distinguish maintenance from growth investment, which this assignment does not estimate.

**Course checks:** ROE at least 15% every year; owner earnings positive every year; final owner earnings greater than initial owner earnings. “Grew first-to-last” does not mean “grew every year”: COST passes despite the decline from 6,745 to 6,629.

**Missingness:** source fact absent → `not found`; dependent check cannot be computed → `not known`. Nonpositive equity also makes the ROE uninterpretable under the lab's rule. JPM's missing capex does not mean zero capex, and a bank's cash-flow categories limit this screen's usefulness.

**Judgment:** a passing screen supports a limited business-quality argument. It does not establish a durable moat, trustworthy managers, intrinsic value, or a good purchase price. There is no price data in this lab. The simulated Buffett memo is a model judgment, not Buffett speaking.

**Self-check:** Would the numeric flag catch copying a valid 2024 number into a 2025 claim? Not necessarily: the number exists, but the association is wrong. Would identical facts guarantee identical prose/verdicts? No: code fixes the arithmetic; the model still judges.

## A concise explanation you should be able to give

“I preserve what the source actually supplied, choose records using explicit timing and period rules, and compute the financial checks in code. Missing facts stay missing. The AI memo may interpret those printed facts, but it cannot supply new numbers or turn a limited business screen into a valuation conclusion.”
