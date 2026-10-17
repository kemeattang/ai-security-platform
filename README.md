# AI Security Platform — Portable Starter (v0.3)

This is a **reconstructed starter** based on the last verified Day 3 implementation (9 tests), **not a copy of your original laptop's repository**. It does not include unverified Day 4–13 changes.

## Setup (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
python -m uvicorn app.main:app --reload
```

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs . No API key required. Never commit real secrets.
