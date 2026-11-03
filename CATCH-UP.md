# Catch-up plan and completion tracker

Prepared November 3, 2026. The student's next class is Lab 18. Labs 16–17 were untouched at the start of this session. The professor's career-fair accommodation waives in-person attendance and partner activities, as reported by the student; those are not blockers.

## Work completed in this package

- [x] Recover the existing FIN-439 repo and keep earlier work intact.
- [x] Retain the BIL / IEF / LQD / VT scholarship-fund universe.
- [x] Lab 16: build and run the filter, reproduce all known answers, and run the April 15 probe.
- [x] Lab 16: provide worked sanity calculations, code explanation and reflection draft.
- [x] Lab 17: build the live FRED/ALFRED app and reproduce all four historical values plus PAYEMS.
- [x] Lab 17: add DGS10 evidence, month-end comparison, data card and conditional admission draft.
- [x] Lab 18: create the discoverable Buffett skill and SEC script; reproduce every COST row/check.
- [x] Lab 18: preserve JPM's gaps, write evidence-bound memos, and test the unsupported-number flag.
- [x] Test the apps' widget behavior, recorded replay and error paths.

## Your learning pass — about 45–60 minutes

1. **Lab 16, 10 minutes:** run `asof.py`. Explain measured date versus publication date, why AAA uses 103 rather than 104 or 109, and why a timing gate does not catch an economically strange price. Reproduce one yield by hand.
2. **Lab 17, 10–15 minutes:** launch the app. Set October 5, 2026; inspect the four values. Add PAYEMS and set January 15, 2025. See the gap between 159,536 then and 158,316 in the recorded current file. Independently read the three DGS10 values on the source page. Review the proposed admission rule and choose your own call.
3. **Lab 18, 15–20 minutes:** read the skills/FAskills prework, personalize the build request, open COST, switch to JPM, then append an unsupported 40.0% ROE to COST's memo and see the warning. Explain the code that chooses one year and where missing values originate. Remove the probe text afterward; editing the app's text area does not alter the saved memo.
4. **Lab 18, 5–10 minutes:** run the requested fresh browser chat without a skill: “Is Costco a Buffett business? Give its ROE for the last five years.” Compare sources and fiscal definitions with the script. Save the real comparison and make your trust decision. Do not claim this experiment has already happened.

## Submission checklist

- [ ] Student reviews and approves the Lab 16 reflection and understands its code.
- [ ] Student completes Lab 17's manual source check and owns the admit/quarantine/reject call.
- [ ] Student personalizes the Lab 18 request and records the actual no-skill comparison.
- [ ] Student records their own Lab 18 trust decision and reflection.
- [ ] Student pastes the appropriate GitHub links into Brightspace checkouts.
- [ ] Student verifies any late-credit rules for labs 16–17; no policy has been inferred from the handouts.

## Lab 19 — later, not part of the backlog being claimed complete

Extend the same facts engine with liabilities/current assets/current liabilities. Graham: latest current ratio at least 2, positive net income each year, net income grew first-to-last. Burry: operating cash flow at least net income each year, latest liabilities no more than twice equity. Test the threshold change, run on the largest company in a Project 2 fund (VT is the equity sleeve), then make the panel decision. Verify the current holding rather than assuming a ticker. Open-ended challenges come after the required labs.

## Material cautions

The lab's ROE uses year-end equity, and its owner-earnings formula uses total capex. These differ from other defensible financial definitions; do not compare outputs without checking formulas. Lab 18's latest-filing rule can use restated past facts and is not a historical as-of backtest. The memo's numeric flag checks presence, not whether a number was assigned to the correct metric or year. These limits belong in your explanation.
