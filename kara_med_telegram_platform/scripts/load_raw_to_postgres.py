import os, json, glob
from loguru import logger
from sqlalchemy import text
from app.database import ENGINE

DATA_DIR = "data/raw"

def load_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def upsert_messages(rows):
    SQL = text('''
        INSERT INTO raw.telegram_messages
        (channel_name, message_id, message_text, has_image, image_path, posted_at, raw_json)
        VALUES (:channel_name, :message_id, :message_text, :has_image, :image_path, :posted_at, CAST(:raw_json AS JSONB))
        ON CONFLICT (id) DO NOTHING;
    ''')
    with ENGINE.begin() as conn:
        for r in rows:
            conn.execute(SQL, {
                "channel_name": r.get("channel_name"),
                "message_id": r.get("message_id"),
                "message_text": r.get("message_text"),
                "has_image": r.get("has_image"),
                "image_path": r.get("image_path"),
                "posted_at": r.get("posted_at"),
                "raw_json": json.dumps(r.get("raw_json") or {})
            })

def main():
    files = sorted(glob.glob(os.path.join(DATA_DIR, "telegram_messages_*.json")))
    if not files:
        logger.warning("No raw JSON files found in {}", DATA_DIR)
        return
    for fp in files:
        try:
            rows = load_file(fp)
            logger.info("Loading {} rows from {}", len(rows), fp)
            upsert_messages(rows)
        except Exception as e:
            logger.error("Failed to load {}: {}", fp, e)
    logger.info("Done.")

if __name__ == "__main__":
    main()
