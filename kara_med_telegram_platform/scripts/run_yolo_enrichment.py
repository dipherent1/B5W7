import os
from loguru import logger
from dotenv import load_dotenv
from ultralytics import YOLO
import json
from sqlalchemy import text
from app.database import ENGINE

load_dotenv()

YOLO_MODEL = os.getenv("YOLO_MODEL", "yolov8n.pt")

def ensure_table():
    with ENGINE.begin() as conn:
        conn.execute(text('''
        CREATE TABLE IF NOT EXISTS raw.image_detections (
            id BIGSERIAL PRIMARY KEY,
            message_id BIGINT,
            channel_name TEXT,
            image_path TEXT,
            detected_object_class TEXT,
            confidence_score DOUBLE PRECISION
        );
        '''))

def insert_detection(d):
    with ENGINE.begin() as conn:
        conn.execute(text('''
        INSERT INTO raw.image_detections
        (message_id, channel_name, image_path, detected_object_class, confidence_score)
        VALUES (:message_id, :channel_name, :image_path, :cls, :conf)
        '''), d)

def main():
    ensure_table()
    model = YOLO(YOLO_MODEL)  # downloads weights on first run if needed

    # fetch images from raw.telegram_messages
    rows = []
    with ENGINE.begin() as conn:
        res = conn.execute(text("SELECT message_id, channel_name, image_path FROM raw.telegram_messages WHERE has_image = TRUE AND image_path IS NOT NULL"))
        rows = [dict(r._mapping) for r in res]

    if not rows:
        logger.warning("No images found to process.")
        return

    for r in rows:
        img = r["image_path"]
        if not img or not os.path.exists(img):
            continue
        results = model(img)
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                cls_name = result.names.get(cls_id, str(cls_id))
                insert_detection({
                    "message_id": r["message_id"],
                    "channel_name": r["channel_name"],
                    "image_path": img,
                    "cls": cls_name,
                    "conf": conf
                })
    logger.info("YOLO enrichment completed.")

if __name__ == "__main__":
    main()
