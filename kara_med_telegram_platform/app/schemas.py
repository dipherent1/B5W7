from pydantic import BaseModel
from typing import List, Optional

class ProductCount(BaseModel):
    product: str
    mentions: int

class ChannelActivity(BaseModel):
    channel_name: str
    day: str
    messages: int

class SearchResult(BaseModel):
    message_id: int
    channel_name: str
    message_text: str
    posted_at: str

class TopProductsResponse(BaseModel):
    results: List[ProductCount]

class ChannelActivityResponse(BaseModel):
    results: List[ChannelActivity]

class SearchResponse(BaseModel):
    results: List[SearchResult]
