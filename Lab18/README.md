# Lab 18 — Legend Investor as Skill

Head start built November 3, 2026 with AI assistance. This follows the November 1 investor-skills lab, which supersedes the older trading-strategy material referenced in the Lab 17 slides.

## What is built

- A repository-discoverable skill at `../.agents/skills/buffett-business/SKILL.md` with a bundled standard-library script.
- Keyless SEC ticker lookup and companyfacts download, with an identifying User-Agent and local cache.
- Five annual 10-K periods, permitted tag fallbacks, latest-filing selection, USD units and full provenance.
- Code-computed ROE, owner earnings and the three checks; missing values never estimated.
- A Streamlit app with chart, table, checks, memo and an unsupported-number flag.
- COST and JPM memos written by the AI after reading the computed reports; fingerprints bind each memo to its facts.

## Run from the repository root

```sh
python -m pip install -r Lab18/requirements.txt
python .agents/skills/buffett-business/scripts/edgar_facts.py COST --out Lab18/evidence
python -m streamlit run Lab18/buffett_app.py
python Lab18/verify_lab18.py
```

For live SEC requests, set `SEC_USER_AGENT` to your name and contact email, or use your configured Git identity. No key is required. The email is not hard-coded into the published source. Open Codex in this repository and invoke `$buffett-business` for COST or another ticker. The script computes facts; the model then writes a memo. The Streamlit app does not secretly call a paid model API. For an arbitrary ticker with no saved memo, it asks you to invoke the skill or paste a generated memo.

For a reproducible offline run:

```sh
python .agents/skills/buffett-business/scripts/edgar_facts.py COST --facts-file Lab18/evidence/COST-companyfacts.json.gz --source-meta Lab18/evidence/COST-source.json --out Lab18/evidence
```

Repeat with JPM. The app also has an explicitly labeled **Saved verified download** mode. The original SEC responses are compressed, and their source metadata records URLs, download timestamps and SHA-256 hashes of the uncompressed bytes. The recorded-download mode recomputes the selection and arithmetic; it does not load a pasted answer table.

## Reading synthesis and scope

[FAskills' Buffett reference](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md) emphasizes business understanding, moat durability, management, owner earnings and margin of safety. Those ideas motivate judgment; the lab's numerical checks do not prove them. Its full framework asks for maintenance-capex estimates, forecasts and valuation, but this assignment deliberately uses operating cash flow minus total capital spending and excludes price analysis. FAskills was read, not installed; none of its paid sources were used.

[Official skills documentation](https://learn.chatgpt.com/docs/build-skills) describes a folder with `SKILL.md`, name/description metadata and optional bundled resources. Codex can discover repository skills under `.agents/skills`; open the repository as your working folder. Names and descriptions are available first, and detailed instructions load when the skill is selected. The skill fixes the workflow and arithmetic source; the model's wording and judgment can still vary.

[SEC API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) describes keyless companyfacts and submissions APIs. Companyfacts contains facts from multiple forms and periods, so the code filters rather than treating every record as an annual fact.

## Financial selection rules worth understanding

Fiscal periods are labeled by their real end dates. The `fy` field can identify the later filing that repeats a comparative value; grouping by it can assign an old value to the wrong year. Annual net-income periods anchor the five year ends. Flows must match that year's start and end and have an annual duration; 52/53-week years are accepted. Equity must be an instant at the same end. For a selected tag and period the latest filing wins. Tag priority follows the handout; no substitution outside its permitted tags. Conflicting equally recent values stop the run.

ROE is net income divided by year-end equity, not average equity. Owner earnings is the course cash-flow proxy, not a proven amount distributable without harming the business. Derived values name their source tags/formulas. Missing source facts print `not found`; unavailable checks and ROE with nonpositive equity print `not known`.

## Validation achieved

All five COST rows match the supplied table, including the one-decimal ROEs. See `evidence/COST-printed.md` and `evidence/COST-facts.json` for every value and its provenance. All three checks pass. The 2023 fiscal year has 53 weeks; it is not dropped by an exact-365-day test.

JPM's permitted capital-spending tags are absent, so owner earnings remain `not found` in all five rows and both owner-earnings checks remain `not known`. Its ROE consistency check fails. See `evidence/JPM-printed.md` and its memo.

The memo guard accepts supported amounts and equivalent decimal formatting but flags a fabricated 40.0% ROE. It also distinguishes a percentage from an equal cash number. The guard checks numeric presence, not semantic correctness: swapping supported values between years can still escape it. Manual verification of company/year/metric associations remains necessary. Memo fingerprints warn if facts change after a memo was written.

## My build request — study draft to personalize

Build a Buffett business-quality skill and a Streamlit viewer using only keyless SEC data. Keep five actual fiscal-year-end periods from annual 10-K facts, use the course's tags and fallback rules, retain each tag/period/filing/accession, and compute all financial numbers and checks in code. Do not estimate absent facts or introduce valuation. Let the AI write an explicitly simulated business memo only after the script prints its evidence, then validate its numbers and display it with the chart, table, checks and required source disclosure. Verify COST, preserve JPM's gaps, and show that an inserted unsupported ROE is flagged.

This is an AI-authored draft, provided so the student can understand and write their own request as the lab asks.

## Code explanation practice

Open `make_row`: it calls `select_fact` for each required field, keeping the selected tag and filing evidence. It reads each numeric value, computes ROE only when equity is positive and both inputs exist, and computes owner earnings only when both cash-flow inputs exist. `None` represents missingness internally; the report renders the exact required wording. A missing field is not set to zero. Explain next how `select_fact` tries the fallback only when no valid primary-tag fact exists for the same period.

Practice question: why not select the largest `fy` for every number? Because a later filing may repeat earlier comparative periods; the period start/end identify the measurement year.

## Trust decision — proposed answer for student review

Trust the computed COST table and explicit checks within their documented definitions, but treat the simulated **watch it** verdict as a limited business screen until qualitative evidence supports business durability and management. Passing the checks does not establish a sensible purchase price. This is a proposed answer, not the student's recorded personal decision.

## In-class work still required

- Read the skills/FAskills prework and personalize the build request.
- Explain one computable item (ROE) versus one judgment item (durability of a moat).
- Personally demonstrate COST, switch to JPM, and insert 40.0% into the editable memo to see the warning.
- Run the required fresh browser chat with no skill and compare its sources/numbers with the script. No such fresh-chat comparison is claimed in this package.
- Review the one-year selection code and be ready to explain missing-value handling. Partner work is waived per the professor's career-fair accommodation, as reported by the student on November 3.
- Make and record your own trust decision, complete reflection and Brightspace checkout.

## Lab 19 preparation

Keep this build working. Read Graham and Burry, and identify the largest company in the VT holding sleeve from a current holdings source. Add current assets, current liabilities and liabilities later to the shared fact engine. Graham adds a latest current ratio threshold and net-income tests; Burry adds cash-flow coverage and leverage tests. All use the same facts. The panel and open challenge have not been represented as completed Lab 18 requirements.
