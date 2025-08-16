# Convenience runner to execute the whole pipeline once without Dagster UI.
import subprocess, sys

def run(cmd):
    print(">>", cmd)
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        sys.exit(res.returncode)

if __name__ == "__main__":
    run("python scripts/scrape_telegram.py")
    run("python scripts/load_raw_to_postgres.py")
    run("dbt run --profiles-dir /workspace/dbt")
    run("python scripts/run_yolo_enrichment.py")
    print("Pipeline completed.")
