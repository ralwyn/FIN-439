# Validation record

The engine shares the existing Lab 15 financial functions. New comparisons evaluate fully invested long-only grid weights against net modeled target, BIL floor and ETF concentration. Known-answer training covariance, saved scholarship allocations, cost arithmetic, infeasibility, concentration, timing-gate rejection, invalid inputs and exhaustive minimum-risk selection are checked by verify_project.py. Executed results and logs are in evidence/.

Data: preserved adjusted prices and archived ALFRED downloads with SHA-256 metadata. Price definitions, transformations, exclusions, the CSV hash and source limitations are recorded in [price source record](../data/price-sources.md). Price history can be retrospectively adjusted; no historical predictive backtest is claimed. The point-in-time rule uses archived vintage values and actual download time, not today's data truncated to an earlier date.

Highest-risk counterexample: alternate estimation window moves twenty-five percentage points, failing the proposed stability condition. Source → prices.csv; calculation → estimate_from_csv; test → saved last-thirty-six stress; decision effect → paper pilot only, defer adoption.

## Changed-input evidence

Reserve minimum: 10% → 90%; target 6.5%; all other base inputs fixed. The saved prediction anticipated infeasibility, and the run returned no feasible mix. Decision effect: pause, retain the target and ask the committee to reconcile constraints. Prediction was committed as 2cebc22 and pushed through GitHub Desktop before this run. Snapshot hash/time are in evidence/prediction-snapshot.json. This prediction was AI-assisted and does not satisfy the required human-authored AI-off prediction. The later student prediction and test are documented below. See [AI checkout](ai-checkout.md).

The zero-cost base result follows unchanged reference weights. Nonzero-turnover scenarios test the actual cost formula. No trading, capital deployment, false attendance, personal recording or Brightspace submission is claimed. Detailed tool use and outstanding personal items are in [AI checkout](ai-checkout.md).

## Student's 25% reserve test

The student's 10% → 25% reserve-floor prediction was committed and pushed before the run. The portfolio remained 60% BIL / 40% VT with no change in modeled return or volatility; the floor did not bind. The prediction, inputs, results, diagnosis, and decision effect are in the [complete record](reserve-25-result.md). The student subsequently confirmed the prediction was their own; the AI-off condition has not been separately confirmed.

## Further reconciliation after Project 1 feedback

Two independently specified synthetic examples check return, covariance, turnover, costs and simultaneous rule failures against the portfolio engine. The input values and hand calculations are in [independent reconciliation](independent-reconciliation.md); both pass in `verify_project.py`. These do not substitute for the instructor-requested Week 3 DCF and ABG multi-statement reconciliations, which have not been established for this portfolio application. A student-operated cold run and actual timestamped video transcripts remain outstanding.
