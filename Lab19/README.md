# Lab 19 — Legend Panel

## Run

Double-click Start-Lab19.command, then open http://127.0.0.1:8519. Or from this directory, install requirements.txt and run `python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8519`.

Run `python verify_lab19.py`. Recompute a saved report with `python panel.py NVDA --save`; COST and JPM are also included. Live SEC mode is optional and uses the existing name/contact User-Agent configuration. Offline sources include original SEC JSON and hashes.

## Results

| Company | Buffett | Cathie Wood | Burry |
|---|---|---|---|
| COST | All three checks pass | Growth fails at 7.51%; R&D not known | Both checks pass; latest liabilities/equity 1.49 |
| NVDA | All three checks pass | Both checks pass; growth 68.30%, latest R&D/revenue 8.57% | Cash conversion fails; latest leverage passes at 0.31 |
| JPM | ROE check fails; owner-earnings checks not known | Growth fails; R&D not known | Both checks fail; banking interpretation requires care |

The app shows the common facts, investor/check table, verdicts and three separate memos side by side. The numeric guard runs on every memo; type an unsupported number in any memo to see the warning. The guard cannot prove year/metric associations or qualitative claims.

Cathie Wood's threshold probe changes growth from fifteen to five percent. COST's growth check passes at five, but R&D stays not known. Retain fifteen percent to preserve the intended growth screen; changing the threshold changes the design, not the underlying business.

## Fund company and decision

VT is the equity sleeve in the Project 2 universe. Vanguard's September 30, 2026 holdings page, read November 10, lists NVIDIA first at 4.52%, ahead of Apple at 4.08%. NVIDIA files 10-Ks, so no next-largest-company substitution is needed. See evidence/fund-company.md.

Use the panel only as a conditional research screen. It cannot set ETF weights, value a stock, prove a moat or replace the scholarship mandate. Investigate the cash-conversion disagreement before relying on the favorable growth/business screens. No price data or purchase conclusion is introduced.

## Bull and bear

Bull: NVIDIA passes the profitability/owner-earnings and growth/reinvestment screens on the same annual facts. This supports further research, conditional on checking durability and the meaning of the cash-flow gap.

Bear: operating cash flow falls short of net income in several years, including the latest, so the skeptical screen fails despite low latest leverage. A favorable screen cannot establish cash quality, future growth or an acceptable price.

Our AI-partner discussion uses those same facts; no separate human partner work is claimed. See code-explanation.md for the line-by-line check explanation and checkout material for tool-use details.

## Files

- panel.py: shared facts/checks and replay/live command.
- app.py: panel UI, threshold probe and all-memo guard.
- memos/: distinct investor memos, with facts fingerprints.
- evidence/: COST/JPM/NVDA source snapshots, selected facts/tags, computed reports and validation.
- ../.agents/skills/cathie-growth and burry-cash: discoverable investor skills with bundled wrappers. Existing Buffett skill and Lab18 are preserved.

Sources: current course lab https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md ; SEC EDGAR API; FAskills Cathie Wood and Michael Burry reference pages, read rather than installed.
