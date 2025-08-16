from sqlalchemy import text
from app.database import ENGINE

DDL = '''
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS mart;

-- RAW tables
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    id BIGSERIAL PRIMARY KEY,
    channel_name TEXT,
    message_id BIGINT,
    message_text TEXT,
    has_image BOOLEAN,
    image_path TEXT,
    posted_at TIMESTAMPTZ,
    raw_json JSONB
);

-- STAGING & MART views will be created by dbt runs.

-- Helper materialized marts for API (created if not exists)
CREATE TABLE IF NOT EXISTS mart_top_products (
    product TEXT,
    mentions INTEGER
);

CREATE TABLE IF NOT EXISTS mart_channel_activity (
    channel_name TEXT,
    day DATE,
    messages INTEGER
);

CREATE TABLE IF NOT EXISTS mart_messages_search (
    message_id BIGINT,
    channel_name TEXT,
    message_text TEXT,
    posted_at TIMESTAMPTZ
);
'''

with ENGINE.begin() as conn:
    conn.execute(text(DDL))

print("Database initialized.")
