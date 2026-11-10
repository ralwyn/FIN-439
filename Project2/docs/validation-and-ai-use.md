# Validation record

The engine shares the existing Lab 15 financial functions. New comparisons evaluate fully invested long-only grid weights against net modeled target, BIL floor and ETF concentration. Known-answer training covariance, saved scholarship allocations, cost arithmetic, infeasibility, concentration, timing-gate rejection, invalid inputs and exhaustive minimum-risk selection are checked by verify_project.py. Executed results and logs are in evidence/.

Data: preserved adjusted prices and archived ALFRED downloads with SHA-256 metadata. Price history can be retrospectively adjusted; no historical predictive backtest is claimed. The point-in-time rule uses archived vintage values and actual download time, not today's data truncated to an earlier date.

Highest-risk counterexample: alternate estimation window moves twenty-five percentage points, failing the proposed stability condition. Source → prices.csv; calculation → estimate_from_csv; test → saved last-thirty-six stress; decision effect → paper pilot only, defer adoption.

## Changed-input evidence

Reserve minimum: 10% → 90%; target 6.5%; all other base inputs fixed. The saved prediction anticipated infeasibility, and the run returned no feasible mix. Decision effect: pause, retain the target and ask the committee to reconcile constraints. Prediction was committed as 2cebc22 and pushed through GitHub Desktop before this run. Snapshot hash/time are in evidence/prediction-snapshot.json. The prediction's authorship and the outstanding personal attestation are recorded once in the checkout material.

The zero-cost base result follows unchanged reference weights. Nonzero-turnover scenarios test the actual cost formula. No trading, capital deployment, false attendance, personal recording or Brightspace submission is claimed. Detailed tool use and personal items are in ../../00-Class-Today/AI-CHECKOUT.md.
