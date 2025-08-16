import os
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
from telethon.errors.rpcerrorlist import FloodWaitError
import json
import asyncio

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID", "0"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "")
SESSION = os.getenv("TELEGRAM_SESSION_NAME", "kara_session")
CHANNELS = [c.strip() for c in os.getenv("TELEGRAM_CHANNELS", "").split(",") if c.strip()]
DATA_DIR = "data/raw"
IMG_DIR = os.path.join(DATA_DIR, "images")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

async def scrape():
    if not API_ID or not API_HASH:
        logger.error("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH")
        return

    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.start()
    logger.info("Connected to Telegram as {}", SESSION)

    for channel in CHANNELS:
        logger.info("Scraping channel: {}", channel)
        try:
            entity = await client.get_entity(channel)
        except Exception as e:
            logger.error("Failed to get entity for {}: {}", channel, e)
            continue

        offset_id = 0
        limit = 200
        total = 0
        messages_out = []
        while True:
            try:
                history = await client(GetHistoryRequest(
                    peer=entity,
                    offset_id=offset_id,
                    offset_date=None,
                    add_offset=0,
                    limit=limit,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
            except FloodWaitError as e:
                logger.warning("Flood wait: {} seconds", e.seconds)
                await asyncio.sleep(e.seconds + 1)
                continue

            if not history.messages:
                break

            for msg in history.messages:
                has_image = bool(msg.media)
                image_path = None
                if has_image:
                    try:
                        fname = f"{entity.id}_{msg.id}.jpg"
                        fpath = os.path.join(IMG_DIR, fname)
                        await client.download_media(msg, file=fpath)
                        image_path = fpath
                    except Exception as e:
                        logger.warning("Failed to download media for {} #{}: {}", channel, msg.id, e)

                messages_out.append({
                    "channel_name": getattr(entity, "title", str(channel)),
                    "message_id": msg.id,
                    "message_text": getattr(msg, "message", "") or "",
                    "has_image": bool(msg.media),
                    "image_path": image_path,
                    "posted_at": msg.date.isoformat() if msg.date else None,
                    "raw_json": msg.to_dict() if hasattr(msg, "to_dict") else None
                })
                total += 1

            offset_id = history.messages[-1].id

        # Write JSON batch
        stamp = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
        out_path = os.path.join(DATA_DIR, f"telegram_messages_{entity.id}_{stamp}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(messages_out, f, ensure_ascii=False, indent=2)
        logger.info("Saved {} messages to {}", len(messages_out), out_path)

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(scrape())
