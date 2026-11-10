# Saved Project 2 output — November 10

| Portfolio | BIL / IEF / LQD / VT | Gross | Net | Volatility | Verdict |
|---|---|---:|---:|---:|---|
| Equal weight | 25.0% / 25.0% / 25.0% / 25.0% | 3.01% | 2.96% | 7.55% | FAIL: Net modeled return below target |
| Inverse volatility | 87.2% / 5.5% / 4.3% / 2.9% | 3.37% | 3.33% | 1.37% | FAIL: Net modeled return below target |
| Policy benchmark (40% LQD / 60% VT) | 0.0% / 0.0% / 40.0% / 60.0% | 6.26% | 6.20% | 12.33% | FAIL: Net modeled return below target; BIL below reserve floor |
| Constrained portfolio | 60.0% / 0.0% / 0.0% / 40.0% | 6.61% | 6.61% | 6.05% | PASS: modeled checks pass |

| Scenario | BIL / IEF / LQD / VT | Net | Volatility |
|---|---|---:|---:|
| Base | 60% / 0% / 0% / 40% | 6.61% | 6.05% |
| VT estimate minus 1 percentage point | 55% / 0% / 0% / 45% | 6.53% | 6.79% |
| Last 36 returns | 85% / 0% / 0% / 15% | 6.72% | 1.79% |
| Trading cost 100 bps | 60% / 0% / 0% / 40% | 6.61% | 6.05% |
| Last 36 with 100 bps cost | 80% / 0% / 5% / 15% | 6.52% | 2.08% |
| Reserve floor 90% | no feasible mix | — | — |
| ETF concentration cap 50% | 50% / 5% / 0% / 45% | 6.70% | 7.03% |

DGS10 endpoint change: −30 basis points; no rate-rise alert. Paper research pilot only; the twenty-five-point window sensitivity prevents adoption. Gross/net are modeled estimates, not realized backtest performance.
