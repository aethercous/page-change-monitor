# Directions — page-change-monitor

## What this is
Change-detection sentinel agent. Snapshots page text, compares against a prior snapshot, and uses an LLM to judge if the delta is material.

## Setup
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `cp .env.example .env` → set `OPENAI_API_KEY`

## Run
```bash
# First run creates baseline
python -m src.main watch https://example.com --store data/example.json

# Later run diffs against baseline
python -m src.main watch https://example.com --store data/example.json
```

## API keys
| Variable | Required | Source |
|----------|----------|--------|
| OPENAI_API_KEY | Yes | https://platform.openai.com/api-keys |
| SENTINEL_THRESHOLD | No | materiality score 0–1 (default 0.55) |
