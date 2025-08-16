.PHONY: up down logs init dbt-run dbt-test scrape load yolo api

up:
	docker compose up --build -d

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

init:
	docker compose exec app python scripts/init_db.py

scrape:
	docker compose exec app python scripts/scrape_telegram.py

load:
	docker compose exec app python scripts/load_raw_to_postgres.py

dbt-run:
	docker compose exec app dbt run

dbt-test:
	docker compose exec app dbt test

yolo:
	docker compose exec app python scripts/run_yolo_enrichment.py

api:
	open http://localhost:8000/docs || true
