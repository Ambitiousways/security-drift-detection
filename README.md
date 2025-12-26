!\[Tests](../../actions/workflows/tests.yml/badge.svg)



\# Security Drift Detection



A Python-based security tool that detects when infrastructure deviates from approved security baselines over time. It captures snapshots of observed open ports, evaluates drift against a YAML baseline policy, assigns risk severity, and stores results in an audit-ready history using SQLite.



Repository: https://github.com/Ambitiousways/security-drift-detection



---



\## Why this matters



Security failures often happen because environments \*\*drift\*\*:

\- “Temporary” changes become permanent

\- Legacy services get re-enabled

\- Ports reopen after updates or troubleshooting

\- Baseline controls are unintentionally weakened



This project helps teams answer:



\*\*“What changed, why does it matter, and when did it happen?”\*\*



It is designed for \*\*authorized, non-disruptive\*\* use in enterprise and regulated environments.



---



\## What it does



\- Capture snapshots of observed open ports for a target (authorized scanning)

\- Validate snapshots against a baseline policy (YAML)

\- Flag drift findings with severity and risk scoring

\- Persist results to SQLite for audit/history

\- Provide a clean CLI workflow for repeatable operations



---



\## Key features



\- Baseline-driven evaluation (`baselines/baseline\_policy.yml`)

\- Findings classification:

&nbsp; - Flagged ports (e.g., Telnet/FTP) → HIGH severity

&nbsp; - Unexpected ports (not baseline allowed) → MEDIUM severity

\- Risk scoring + risk level (`LOW | MEDIUM | HIGH`)

\- Persistent run history:

&nbsp; - `history` to list runs

&nbsp; - `show` to retrieve full run result

\- Tests with `pytest`

\- CI via GitHub Actions



---



\## Demo Output



> Save your screenshots under `examples/screenshots/` using these exact filenames:

> - `check\_drift.png`

> - `history.png`

> - `show\_run.png`

> - `cli\_help.png`

> - `tests.png`



\### Drift Check (Baseline Enforcement)

!\[Drift Check](./examples/screenshots/check\_drift.png)



\### History (Audit \& Persistence)

!\[History](./examples/screenshots/history.png)



\### Run Details (Audit Evidence)

!\[Run Details](./examples/screenshots/show\_run.png)



\### CLI Interface

!\[CLI Help](./examples/screenshots/cli\_help.png)



\### Test Suite

!\[Tests Passing](./examples/screenshots/tests.png)



---



\## Project structure



```text

security-drift-detection/

├── baselines/

│   └── baseline\_policy.yml

├── cli/

│   └── main.py

├── db/

│   ├── models.py

│   ├── repo.py

│   └── session.py

├── drift/

│   ├── capture.py

│   └── compare.py

├── examples/

│   └── screenshots/

├── snapshots/

├── tests/

├── requirements.txt

└── README.md



