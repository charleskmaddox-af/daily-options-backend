# Option Checklist – FastAPI

## Local dev
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DBNAME
uvicorn app.main:app --reload

## DigitalOcean App Platform
- Create a Managed PostgreSQL DB (copy connection string).
- Create an App → GitHub repo → Autodetect Python.
- Build Command: pip install -r requirements.txt
- Run Command: uvicorn app.main:app --host 0.0.0.0 --port 8080
- Environment variables:
  - DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DBNAME
  - ALLOWED_ORIGINS=https://your-frontend-domain.com, http://localhost:3000
  - SECRET_KEY=your-secret
