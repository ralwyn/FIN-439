# FIN 439 coursework — Rohan Alwyn

## Current work

| Lab | Entry point | Verified work | Student follow-through |
|---|---|---|---|
| [16 — Provenance Gate](Lab16/README.md) | `Lab16/asof.py` | Row funnel, signals, later-date probe, sanity-check study solution | Review/explain; Brightspace checkout |
| [17 — Point-in-Time Audit](Lab17/README.md) | `Lab17/asof_app.py` | Live app; four known answers; PAYEMS; DGS10 data card and evidence | Manual page check; own the admission decision; checkout |
| [18 — Buffett as Skill](Lab18/README.md) | `Lab18/buffett_app.py` | Skill, SEC script, COST/JPM, memos and numeric flag | Personalize request; fresh no-skill comparison; trust decision; checkout |
| [15 — Portfolio Stability](Lab15/lab15.md) | `Lab15/app.py` | Prior work preserved | See prior submission receipt |
| [14 — Portfolio Baselines](lab14.md) | `portfolio.py` | Prior work preserved | See prior work |

Start with [CATCH-UP.md](CATCH-UP.md) for the learning sequence and remaining checklist. [STUDY-GUIDE.md](STUDY-GUIDE.md) explains the core ideas and gives short self-check questions. [SUBMISSION-LINKS.md](SUBMISSION-LINKS.md) lists the GitHub URLs for checkout. [app-validation.txt](app-validation.txt) records interactive widget checks. [PUBLICATION.md](PUBLICATION.md) records the verified GitHub delivery.

The student reports that the professor waived in-person attendance and partner activities because of career fairs (November 3, 2026). No partner work is outstanding or claimed. AI-written memos, practice answers and decision drafts are identified; Brightspace submissions and personal judgments are not fabricated.

## Environment

Python 3.12; install each lab's direct requirements in a virtual environment. No paid data service or API key is required. Launchers use the existing course environment when available, or a repository-local `.venv`. Apps run only on `127.0.0.1`; no public hosting has been created. Required third-party libraries are Streamlit, pandas and requests. The arithmetic/source-selection scripts for labs 16 and 18 use the standard library.

Repository structure keeps each lab's code, notes and evidence together. Lab 18's skill is at `.agents/skills/buffett-business` so Codex can discover it from this repository. Original source snapshots, download timestamps and hashes support reproducibility. Scratch work, local caches, environments and credentials are excluded.

These are AI-assisted learning demonstrations, not investment advice. Current-file facts and model judgments should not be repurposed as a historical trading signal without an explicit point-in-time filing filter.
