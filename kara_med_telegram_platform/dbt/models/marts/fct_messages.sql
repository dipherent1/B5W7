with base as (
  select
    m.raw_id,
    m.channel_name,
    m.message_id,
    m.message_text,
    m.has_image,
    m.image_path,
    m.posted_at::timestamp as posted_at,
    length(coalesce(m.message_text,'')) as message_length
  from {{ ref('stg_telegram_messages') }} m
)

select
  b.raw_id as fact_id,
  c.channel_id,
  b.channel_name,
  b.message_id,
  b.message_text,
  b.has_image,
  b.image_path,
  b.posted_at,
  b.message_length,
  d.day
from base b
left join {{ ref('dim_channels') }} c on c.channel_name = b.channel_name
left join {{ ref('dim_dates') }} d on d.day = date_trunc('day', b.posted_at)::date
