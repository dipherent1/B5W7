with dates as (
  select date_trunc('day', posted_at)::date as day
  from {{ ref('stg_telegram_messages') }}
)
select distinct
  day,
  extract(isodow from day)::int as iso_dow,
  extract(week from day)::int as iso_week,
  extract(month from day)::int as month,
  extract(year from day)::int as year
from dates
