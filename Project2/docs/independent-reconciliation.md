# Independent numerical reconciliation — portfolio engine

These two synthetic, hand-calculated checks exercise the portfolio decision calculation independently of the historical price file. They are not the instructor's Week 3 DCF or ABG multi-statement examples, and do not establish that those corporate-finance cases have been reconciled. The test is `python verify_project.py` → `test_manual_two_asset_reconciliation`.

Common inputs, in BIL / IEF / LQD / VT order: expected annual returns 4%, 8%, 3%, 10%; annual volatilities 10%, 20%, 15%, 25%. Correlations are zero except BIL–IEF = 0.25; diagonal = 1. The assumed cost-reference portfolio is 60% BIL / 40% VT. These are deliberately artificial inputs, not market estimates. Costs use the existing one-way-turnover convention.

## Case A: correlated pair, positive verdict

Weights 50% BIL / 50% IEF, target 5.5%, BIL floor 10%, cost 10 bps.

- Gross return: 0.5 × 4% + 0.5 × 8% = **6.00%**.
- Variance: 0.5² × 0.10² + 0.5² × 0.20² + 2 × 0.5 × 0.5 × 0.25 × 0.10 × 0.20 = **0.015**; volatility = √0.015 = **12.2474%**.
- One-way turnover: (|0.5−0.6| + |0.5−0| + |0−0| + |0−0.4|) / 2 = **50%**.
- Drag = 0.50 × 10 / 10,000 = **0.05 percentage points**; net = **5.95%**. Both target and floor pass.

## Case B: two simultaneous failures

Weights 20% BIL / 80% VT, target 8.5%, floor 25%, cost 100 bps; BIL–VT correlation zero.

- Gross return = 0.2 × 4% + 0.8 × 10% = **8.80%**.
- Variance = 0.2² × 0.10² + 0.8² × 0.25² = **0.0404**; volatility = √0.0404 = **20.0998%**.
- One-way turnover = (|0.2−0.6| + |0−0| + |0−0| + |0.8−0.4|) / 2 = **40%**. Drag = 0.4 × 100 / 10,000 = **0.40 percentage points**, giving **8.40% net**.
- Net return fails the 8.5% target and the 20% reserve fails the 25% floor. Both failures must be reported.

The tests compare these independently specified expected results with `engine.evaluate`. Passing the examples checks arithmetic and verdict handling, not forecast accuracy, the historical data vendor, or suitability. The instructor's feedback also asks for a Week 3 twelve-line and a multi-statement ABG reconciliation; those are corporate-finance-model checks and remain unverified here rather than being represented as completed by these portfolio examples.
