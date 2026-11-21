# Quick start

Setup, what the three programs actually do, and their limits are in [README.md](README.md). The commands below were run on Python 3.12.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

API at http://localhost:8000/docs :

```bash
RUN_MODE=api python main.py
```

Dashboard at http://localhost:8501 :

```bash
RUN_MODE=dashboard python main.py
```

Agent mode reads `ANTHROPIC_API_KEY` from `.env`. With the key unset, the process raises `TypeError` from the Anthropic SDK on the first message and exits. A completed Claude reply was not part of this check.

```bash
RUN_MODE=agent python main.py
```

Tests, with no API key:

```bash
pytest -q
```
