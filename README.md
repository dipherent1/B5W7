# Kara Solutions — Telegram Medical Insights Platform

An end-to-end ELT data product: scrape Telegram channels, load to a data lake and Postgres, 
transform with dbt into a star schema, enrich images with YOLOv8, and expose analytics via FastAPI. 
Orchestrated with Dagster. Containerized with Docker.

> **Note:** This repository is submission-ready. You only need to set secrets in a `.env` file and run a few commands.

## Quick Start

1. **Clone & configure**  
   ```bash
   cp .env.example .env
   # edit .env with your credentials (Telegram API, DB password)
   ```

2. **Build & run**  
   ```bash
   docker compose up --build -d
   ```

3. **Initialize database schemas**  
   ```bash
   docker compose exec app python scripts/init_db.py
   ```

4. **Run the orchestrated pipeline (from Dagster UI)**  
   Visit: http://localhost:3000  (dagster-webserver)  
   Or run once via CLI:
   ```bash
   docker compose exec app python scripts/pipeline_cli.py
   ```

5. **API**  
   FastAPI docs are at: http://localhost:8000/docs

## Services

- **PostgreSQL** on `localhost:5433` with database `kara`.
- **App** (Python/uvicorn) on `http://localhost:8000`.
- **Dagster UI** on `http://localhost:3000`.

## Project Structure

```
.
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── app/
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   ├── models_sql.py
│   └── crud.py
├── scripts/
│   ├── scrape_telegram.py
│   ├── load_raw_to_postgres.py
│   ├── run_yolo_enrichment.py
│   ├── init_db.py
│   └── pipeline_cli.py
├── orchestration/
│   ├── repo.py
│   └── jobs.py
├── dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml.example
│   └── models/
│       ├── staging/
│       │   ├── stg_telegram_messages.sql
│       │   └── schema.yml
│       └── marts/
│           ├── dim_channels.sql
│           ├── dim_dates.sql
│           ├── fct_messages.sql
│           ├── fct_image_detections.sql
│           └── schema.yml
├── data/
│   └── raw/  # JSON and images land here from scraping
└── Makefile
```

## dbt Setup

Inside the running container:
```bash
dbt deps
dbt debug --profiles-dir /workspace/dbt
dbt run   --profiles-dir /workspace/dbt
dbt test  --profiles-dir /workspace/dbt
dbt docs generate --profiles-dir /workspace/dbt
```

`profiles.yml` is provided as `dbt/profiles.yml.example`. Copy it to `~/.dbt/profiles.yml` or set `DBT_PROFILES_DIR=/workspace/dbt` and rename to `profiles.yml` in that directory.

## Channels Used

- Chemed Telegram Channel
- https://t.me/lobelia4cosmetics
- https://t.me/tikvahpharma
- More from: https://et.tgstat.com/medicine

## Notes

- This template includes sensible defaults, tests, and logging. 
- For YOLO, ultralytics will download a pretrained model on first run inside the container.
- All secrets are managed via `.env` / environment variables.
