# ShadowScrub

**Local-first PII sanitization API & dashboard**

ShadowScrub detects and redacts personally identifiable information (PII) from text and documents (`.pdf`, `.docx`) before you send data to AI chatbots, agents, or third-party services.

Built with **Django**, **Microsoft Presidio**, **spaCy**, **Celery**, **Redis**, and **PostgreSQL** — fully containerized with Docker Compose.

---

## Features

### Text sanitization
- Detects names, phones, emails, credit cards, locations, custom employee IDs, ages, and more
- Replaces matches with `[REDACTED]`
- Powered by Microsoft Presidio + spaCy

### Document processing
- Upload **PDF** or **DOCX** files
- Extract text in memory (avoids saving unscrubbed files to disk)
- Background processing with **Celery + Redis**
- Live task status polling
- Download results as `.txt`, matching format (`.pdf` / `.docx`), or copy to clipboard

### REST API
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/sanitize/text/` | POST | Scrub raw text |
| `/api/v1/sanitize/file/` | POST | Upload PDF/DOCX (async) |
| `/api/v1/tasks/<task_id>/` | GET | Poll job status |
| `/api/v1/export/` | POST | Export scrubbed text as PDF/DOCX |

### Web dashboard
- **Dashboard** — request counts, redaction totals, recent logs
- **Playground** — live text testing
- **Documents** — file upload + async results
- **API Keys** — generate and manage keys

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Backend | Django 5, Django REST Framework |
| NLP / PII | Presidio Analyzer & Anonymizer, spaCy |
| Database | PostgreSQL |
| Async jobs | Celery + Redis |
| Documents | pdfplumber, python-docx, reportlab |
| UI | Django templates + Bootstrap 5 |
| Infra | Docker, Docker Compose |

---

## Project structure

```text
ShadowScrub/
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── manage.py
├── .env.example
├── data/
│   └── db/                # PostgreSQL persistent data folder
├── ShadowScrub/           # Project settings + Celery app
├── scrubbing/             # API, engine, tasks, parsers, exporters
├── dashboard/             # Web UI views
└── template/              # Shared HTML templates
```
## Docker setup

```bash
# 1) Create PostgreSQL data folder
mkdir -p data/db

# 2) Copy environment file
cp .env.example .env

# 3) Build and start containers
docker compose up --build

# Or run in background
docker compose up -d --build

# 4) Run migrations
```
## Then open:

```bash
# Dashboard
http://127.0.0.1:8000/dashboard/

# Playground
http://127.0.0.1:8000/dashboard/playground/

# Documents
http://127.0.0.1:8000/dashboard/documents/

# API Keys
http://127.0.0.1:8000/dashboard/keys/

# Admin
http://127.0.0.1:8000/admin/
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# 5) Create superuser
docker compose exec web python manage.py createsuperuser
```
## Useful docker commands

```bash
# Start (foreground)
docker compose up --build

# Start (background)
docker compose up -d --build

# Stop
docker compose down

# Stop and delete DB volume data
docker compose down -v

# Restart services
docker compose restart web
docker compose restart celery_worker

# Migrations / superuser
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser

# Logs
docker compose logs -f
docker compose logs -f web
docker compose logs -f celery_worker

# Container status
docker compose ps
```
