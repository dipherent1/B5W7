import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

load_dotenv()

def get_db_url() -> str:
    user = os.getenv("POSTGRES_USER", "kara")
    pw = os.getenv("POSTGRES_PASSWORD", "kara_password")
    host = os.getenv("POSTGRES_HOST", "postgres")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "kara")
    return f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}"

ENGINE: Engine = create_engine(get_db_url(), pool_pre_ping=True, future=True)

def run_query(sql: str, params: dict | None = None):
    with ENGINE.begin() as conn:
        result = conn.execute(text(sql), params or {})
        try:
            rows = [dict(r._mapping) for r in result]
        except Exception:
            rows = []
        return rows
