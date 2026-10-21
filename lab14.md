# FIN 439 — Lab 14: Portfolio Baselines

Prepared with AI assistance. Inputs are course-authored training values, not market estimates. CPI of 2.5% is a labelled estimate. Technical results below were executed and checked; partner participation and an independent oral explanation are not claimed.

## Define

What does each simple portfolio earn and risk — and does any of them meet the Meridian mandate?

## Represent

| Sleeve | Expected return | Volatility | Reserve eligible? |
|---|---:|---:|---|
| Treasury bills | 3.5% | 0.5% | Yes |
| Treasury 10-year note | 4.3% | 7.0% | Yes |
| Investment-grade bond fund | 5.0% | 6.0% | No |
| Global equity index fund | 8.0% | 16.0% | No |

| Correlation | Bills | 10-year | IG bonds | Equity |
|---|---:|---:|---:|---:|
| Bills | 1.00 | 0.10 | 0.05 | 0.00 |
| 10-year | 0.10 | 1.00 | 0.80 | -0.10 |
| IG bonds | 0.05 | 0.80 | 1.00 | 0.25 |
| Equity | 0.00 | -0.10 | 0.25 | 1.00 |

The objective is CPI + 4 percentage points = 6.5%. The reserve minimum is 3%, consistent with the existing Lab 13 checker and Session 15. Passing the return objective alone does not establish mandate compliance.

## Implement and run

`portfolio.py` uses only the Python standard library. It builds covariance from correlation and volatility, computes the three baselines, and exposes reusable functions. Inputs are editable at the top. All calculations use decimal returns and weights; formatting converts them to percentages.

Run in this folder:

```sh
python3 portfolio.py
python3 mandate.py --verify
python3 verify_lab14.py
```

## Validate

Weight order: bills / 10-year / IG bonds / equity.

| Portfolio | Weights (%) | Return | Volatility | Reserve eligible | Meets 6.5%? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

Rounded inverse-volatility weights sum to 99.9%; the unrounded computed weights sum to 100%.

All published values match. A temporary copy of the correlation table with IG–equity set to 0.50 in both cells produces 11.00% benchmark volatility. Setting both cells to 1.3 is rejected; changing only one cell to 0.50 is rejected as asymmetric. Original inputs remain at 0.25. These are automated checks, not a claim that a partner ran the file. See `validation.txt` for executed evidence.

The existing Lab 13 `mandate.py` already contains candidate E: 40% IG bonds and 60% equity. It was copied into this package and rerun. E has 0.0% eligible reserves and fails the 3% reserve requirement. It passes the other checkable rules, but calendar-year loss still requires CIO clarification and turnover is not evaluated without holdings/trades and approvals. See `mandate-results.txt`.

**Conclusion:** none of the three baselines meets both the return objective and reserve requirement. The benchmark meets the return objective but fails reserves. Equal weight and inverse volatility have sufficient reserves but miss the return objective.

## Diversification and the hand calculation

Diversification combines exposures whose returns do not move perfectly together. Risk depends on covariance as well as standalone volatility. For positive weights, a correlation below +1 reduces variance relative to otherwise identical perfectly correlated assets. It does not guarantee a portfolio less volatile than every constituent: this benchmark is less volatile than equity but more volatile than IG bonds. Diversification cannot eliminate systematic risk.

For the benchmark:

- Expected return = 0.40 × 0.050 + 0.60 × 0.080 = 0.068 = **6.80%**.
- Bond–equity covariance = 0.25 × 0.06 × 0.16 = **0.0024**.
- Variance = (0.40² × 0.06²) + (0.60² × 0.16²) + (2 × 0.40 × 0.60 × 0.0024).
- Variance = 0.000576 + 0.009216 + 0.001152 = **0.010944**.
- Volatility = √0.010944 = **10.46%**.

At correlation +1 the same weighted portfolio has volatility 0.40 × 6% + 0.60 × 16% = 12%. The actual correlation lowers this to 10.46%. Omitting covariance entirely gives 9.90%, which implicitly assumes zero correlation and understates this benchmark's risk.

## Explain the risk code

`covariance_matrix` computes each cell as correlation[i][j] × volatility[i] × volatility[j]. In `portfolio_variance`, the outer index selects one asset and the inner index selects every asset paired with it. Each term multiplies their weights by their covariance. Diagonal terms are each asset's weighted variance; off-diagonal terms include both bond–equity and equity–bond, producing the factor of two in the hand calculation. `portfolio_volatility` takes the square root to return to return units. Multiplying by 100 when displaying gives percent volatility.

Practice question to answer before requesting an explanation: Why does the double sum need no explicit factor of two, and what assumption would deleting all off-diagonal terms impose?

## Reflection — draft for review

Inverse volatility puts about 84.3% into bills because bills have the smallest volatility. Their reciprocal volatility is 200, versus about 14.29 for the note, 16.67 for IG bonds, and 6.25 for equity. Normalizing these values heavily favors bills. This allocation rule uses standalone volatility, so it does not directly optimize expected return or account for correlations when choosing weights.

I would show the CIO the benchmark first because it is the client's reference allocation and exposes the key conflict: its 6.80% expected return clears the objective, yet its 0% reserve weight violates the mandate. I would then use the other baselines to show the cost of reducing risk: they hold more reserves but earn less than 6.5%. None should be presented as an acceptable final allocation without further work and clarification of unresolved mandate terms.

## Personal checkout still required

- Review the code and written explanation, then complete the oral explanation and partner swap/break activity. Record actual participation only.
- Answer the practice question and complete the requested AI quiz interaction.
- Upload `lab14.md`, `portfolio.py`, and `mandate.py` to your course GitHub repository; include the verification files if desired. Submit the actual GitHub links in Brightspace → Quizzes → Lab 14. No upload or submission is claimed here.

## Separate preparation before Lab 15

The Thursday preparation is not represented as completed by this Tuesday package. It requires your own Project 2 mandate, a corresponding selection of three to six funds, five years of monthly adjusted-close prices in `prices.csv`, and sources/download dates. Your personal mandate was not supplied with these materials, so a personal universe or market history has not been invented. Streamlit setup and the Lab 15 app are separate next steps.
