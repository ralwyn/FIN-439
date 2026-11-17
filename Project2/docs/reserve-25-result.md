# Locked changed-input record: BIL reserve 10% → 25%

[Student's prediction, committed and pushed before the test](https://github.com/ralwyn/FIN-439/blob/da80deb9f4ee76665ccbec69db9d9b468e91ee5e/Project2/docs/prediction-reserve-25.md). Commit: `da80deb9f4ee76665ccbec69db9d9b468e91ee5e`. The student submitted the prediction in chat; independent AI-off authorship must be confirmed by the student. The assistant had explained the mandate and possible categories of inputs beforehand.

The test changed only the minimum BIL weight from 10% to 25%, holding the 6.5% net target, all 59 monthly returns, 10 basis points per one-way turnover, the 100% single-ETF cap, and the remaining assumptions fixed. The engine minimizes modeled volatility over a long-only, fully invested five-percentage-point grid subject to the implemented rules. Run after publication: `engine.compare(reserve=.10)` and `engine.compare(reserve=.25)`. Full machine-readable results and UTC execution time: [reserve-25-result.json](../evidence/reserve-25-result.json).

| Measure | 10% floor | 25% floor |
|---|---:|---:|
| BIL / IEF / LQD / VT | 60% / 0% / 0% / 40% | 60% / 0% / 0% / 40% |
| Net modeled annual return | 6.6145% | 6.6145% |
| Annualized modeled volatility | 6.0518% | 6.0518% |
| Mandate verdict | PASS | PASS |

**Expected versus actual:** The student expected the floor to bind at 25%, with greater VT exposure and volatility, or potentially infeasibility. Neither occurred. The selected 60% BIL weight already exceeds both floors; raising the minimum to 25% removes no selected solution. IEF is zero, as predicted, but it was already zero in the base case. The 6.5% modeled target is exceeded by only about 0.115 percentage points, not comfortably; modeled passing is not a guarantee of future results.

**Diagnosis and decision effect:** The floor is a minimum, not a target. The optimizer seeks minimum modeled volatility, not maximum return or minimum BIL. The sample estimates are approximately 3.66% BIL and 11.05% VT; IEF's estimated annual return is approximately −1.73%, so the premise that BIL is the lowest-returning asset does not hold for these saved estimates. Since the unchanged 60/40 mix was already the minimum-volatility feasible selection, it remains selected when the floor increases to 25%. This run alone does not support switching the recommendation or show that 25% makes the portfolio riskier. The prior paper-pilot recommendation and other documented concerns remain, including sensitivity to the estimation window. The committee must decide whether a 25% minimum fits its actual spending needs; this is a modeled stress, not investment advice.
