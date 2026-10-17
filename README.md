# AI Security Platform — Portable Starter (v0.3)


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
