# Goldfolio

Track a mixed gold/coin/crypto portfolio value in Toman from a market API.

## Features
- Fetches market prices from BrsApi
- Computes holdings value and total portfolio
- Includes a local readonly Postgres script for holdings query

## Local Quick Start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python goldfolio.py
```

## Docker Deployment (Exact Steps)

### 1) Prerequisites
- Docker Engine 24+
- Docker Compose plugin (optional)

### 2) Build image from project root
```bash
docker build -t goldfolio:latest .
```

### 3) Run portfolio CLI in container
```bash
docker run --rm --name goldfolio-cli goldfolio:latest
```

### 4) Run readonly PostgreSQL script in container
Replace placeholders with your real DB values:
```bash
docker run --rm --name goldfolio-db \
  -e DB_HOST=<db-host> \
  -e DB_PORT=5432 \
  -e DB_NAME=goldfolio \
  -e DB_USER=<db-user> \
  -e DB_PASS=<db-password> \
  -e DB_SSLMODE=require \
  goldfolio:latest \
  python scripts/goldfolio_readonly.py
```

### 5) Deploy with Docker Compose (same repo)
Use normal mode for CLI:
```bash
docker compose up --build goldfolio
```

Use DB profile for readonly DB query:
```bash
docker compose --profile db up --build readonly-db-query
```

### 6) Stop and clean up
```bash
docker compose down
```

## Project Structure
- `goldfolio.py` - CLI entrypoint
- `goldfolio/app.py` - core app logic
- `Dockerfile` - container image build definition
- `docker-compose.yml` - compose services for CLI + DB query mode
- `scripts/goldfolio_readonly.py` - local readonly DB query helper
- `sql/holdings_top100.sql` - SQL query for top holdings by market value
- `requirements.txt` - Python dependencies
- `pyproject.toml` - project metadata

## Environment for DB script
Set these if you run `scripts/goldfolio_readonly.py`:
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASS`
- `DB_SSLMODE`
