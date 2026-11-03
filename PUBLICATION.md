# Publication record — November 3, 2026

Published to https://github.com/ralwyn/FIN-439 on branch `main` through the student's existing GitHub Desktop sign-in. The app confirmed **push complete**. No new credentials or permissions were created. Earlier Lab 14/15 files were preserved.

## Organized coursework commits

- `cf235af` — Lab 16 provenance filter, results and validation.
- `a8e3d22` — Lab 17 live audit app, data card and original-source evidence.
- `1dc1427` — Lab 18 Buffett skill, SEC script, app, COST/JPM memos and validation.
- `3347fe8` — Catch-up guide, study guide, submission links and shared widget checks.

A final follow-up records publication and tidies evidence formatting. GitHub checkout links are in `SUBMISSION-LINKS.md`; publication does not claim Brightspace submission or awarded credit.

## Local organization

The published working checkout is the FIN-439 folder beside this record. New labs and study guides were also copied into the student's existing `Desktop/FIN439` course folder. Existing Lab14, Lab15, the shared virtual environment and the original START-HERE.md were not replaced. Lab 18's skill was added under `.agents/skills/buffett-business`.

Each lab contains its own README, scripts and executed validation. Source evidence contains URLs, UTC timestamps and hashes. Environments, local download caches and credentials are excluded from Git.

## Verification

Lab 16: five checks pass, including the later-date equality and publication boundary.

Lab 17: six recorded-source checks pass; all four historical values match, and PAYEMS preserves the original 159,536 and records 381 revised dates. The live rates app rendered in the browser.

Lab 18: eleven checks pass, including all COST values, JPM gaps, annual-period selection, fallback priority, missing inputs, nonpositive equity and numeric formats. The actual live SEC downloader reproduced the recorded COST facts. The skill validator passes. Both app widget suites pass. In the browser, an inserted 40.0% was visibly flagged and then removed; its screenshot is in `Lab18/evidence/unsupported-number-probe.png`.

Partner work is waived per the student's report of the professor's career-fair accommodation. Student review/personal decisions, the actual fresh no-skill comparison and Brightspace checkout remain distinct steps, listed in `CATCH-UP.md`.
