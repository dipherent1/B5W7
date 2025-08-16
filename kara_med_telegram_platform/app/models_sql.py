# Centralized SQL snippets used by the API.
TOP_PRODUCTS_SQL = '''
SELECT product AS product, COUNT(*)::int AS mentions
FROM mart_top_products
GROUP BY product
ORDER BY mentions DESC
LIMIT :limit;
'''

CHANNEL_ACTIVITY_SQL = '''
SELECT channel_name, day::text AS day, messages::int AS messages
FROM mart_channel_activity
WHERE channel_name = :channel_name
ORDER BY day;
'''

SEARCH_MESSAGES_SQL = '''
SELECT message_id, channel_name, message_text, posted_at::text
FROM mart_messages_search
WHERE message_text ILIKE '%' || :query || '%'
ORDER BY posted_at DESC
LIMIT 200;
'''
