select distinct
  channel_name,
  md5(channel_name)::uuid as channel_id
from {{ ref('stg_telegram_messages') }}
