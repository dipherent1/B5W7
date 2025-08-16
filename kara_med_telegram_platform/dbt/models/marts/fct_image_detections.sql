-- This table is populated by the YOLO script into raw.image_detections, then modeled here to join to messages.
with det as (
  select
    message_id,
    channel_name,
    image_path,
    detected_object_class,
    confidence_score
  from raw.image_detections
), msgs as (
  select message_id, channel_name, fact_id
  from {{ ref('fct_messages') }}
)

select
  m.fact_id,
  d.message_id,
  d.channel_name,
  d.image_path,
  d.detected_object_class,
  d.confidence_score
from det d
left join msgs m using (message_id, channel_name)
