from dagster import job, op
import subprocess

@op
def scrape_telegram_data():
    subprocess.check_call("python scripts/scrape_telegram.py", shell=True)

@op
def load_raw_to_postgres():
    subprocess.check_call("python scripts/load_raw_to_postgres.py", shell=True)

@op
def run_dbt_transformations():
    subprocess.check_call("dbt run --profiles-dir /workspace/dbt", shell=True)
    subprocess.check_call("dbt test --profiles-dir /workspace/dbt", shell=True)

@op
def run_yolo_enrichment():
    subprocess.check_call("python scripts/run_yolo_enrichment.py", shell=True)

@job
def pipeline_job():
    y = scrape_telegram_data()
    l = load_raw_to_postgres()
    t = run_dbt_transformations()
    e = run_yolo_enrichment()
    # simple linear ordering
    y >> l >> t >> e
