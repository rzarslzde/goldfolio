# Goldfolio

Track a mixed gold/coin/crypto portfolio value in Toman from a market API.

## Features
- Fetches market prices from BrsApi
- Computes holdings value and total portfolio
- Includes a local readonly Postgres script for holdings query

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python goldfolio.py
```

## Project Structure
- `goldfolio.py` - CLI entrypoint
- `goldfolio/app.py` - core app logic
- `scripts/goldfolio_readonly.py` - local readonly DB query helper
- `sql/holdings_top100.sql` - SQL query for top holdings by market value

## Environment for DB script
Set these if you run `scripts/goldfolio_readonly.py`:
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASS`
- `DB_SSLMODE`
