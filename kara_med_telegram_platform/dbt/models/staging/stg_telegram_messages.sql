with src as (
  select
    id as raw_id,
    channel_name,
    message_id,
    message_text,
    has_image,
    image_path,
    posted_at
  from raw.telegram_messages
)

select
  raw_id,
  channel_name,
  message_id,
  message_text,
  has_image,
  image_path,
  posted_at::timestamp as posted_at
from src
