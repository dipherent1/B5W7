from .database import run_query
from .models_sql import TOP_PRODUCTS_SQL, CHANNEL_ACTIVITY_SQL, SEARCH_MESSAGES_SQL

def get_top_products(limit: int = 10):
    return run_query(TOP_PRODUCTS_SQL, {"limit": limit})

def get_channel_activity(channel_name: str):
    return run_query(CHANNEL_ACTIVITY_SQL, {"channel_name": channel_name})

def search_messages(query: str):
    return run_query(SEARCH_MESSAGES_SQL, {"query": query})
