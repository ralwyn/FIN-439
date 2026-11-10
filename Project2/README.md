# Campus Opportunity Scholarship Fund — Project 2

Education, not investment advice.

Python web app for a fictional scholarship-fund committee: two transparent baselines, policy benchmark, constrained portfolio, mandate verdicts, archived-vintage rate monitor and stress results. Start with the saved evidence; no live data key is required.

## Run from this Project2 folder

Python 3.12 recommended. In a fresh folder/environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python verify_project.py
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8510 --browser.gatherUsageStats false
```

On this Mac, double-click Start-Project2.command. It uses the existing FIN439/.venv. Open http://127.0.0.1:8510. The app works offline from included saved sources. Do not launch a second server on the same port.

To recompute the saved audit: `python engine.py`. Visible results: [evidence/visible-output.md](evidence/visible-output.md) and [executed-results.json](evidence/executed-results.json). The default constrained mix is 60% BIL / 40% VT, but the window stress moves 25 points: paper research pilot only, not adoption.

## Review

- [Mandate](docs/mandate.md)
- [Decision memo](docs/decision-memo.md)
- [Validation](docs/validation-and-ai-use.md)
- [Data card](docs/data-card.md)
- [Cold run](docs/cold-run.md)
- [Frozen must-fix list](docs/must-fix.md)
- [Recording outlines](docs/recording-outlines.md)
- [Submission manifest](submission-manifest.csv)

Historical arithmetic estimates are not rolling-five-year compound forecasts. Signal is a governance monitor, not evidence of predictive advantage. PASS refers to implemented numerical checks, not full client suitability. No paid API, credential or public hosting is required. The sibling Lab19 folder contains the full investor-panel app; this app includes its computed NVIDIA table.
