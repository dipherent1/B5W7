from fastapi import FastAPI, Query, HTTPException
from loguru import logger
from . import crud
from .schemas import TopProductsResponse, ChannelActivityResponse, SearchResponse

app = FastAPI(title="Kara Medical Insights API", version="1.0.0")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/api/reports/top-products", response_model=TopProductsResponse)
def top_products(limit: int = Query(10, ge=1, le=100)):
    logger.info("Fetching top products, limit={}", limit)
    results = crud.get_top_products(limit=limit)
    return {"results": results}

@app.get("/api/channels/{channel_name}/activity", response_model=ChannelActivityResponse)
def channel_activity(channel_name: str):
    logger.info("Fetching activity for {}", channel_name)
    results = crud.get_channel_activity(channel_name=channel_name)
    if not results:
        raise HTTPException(status_code=404, detail="Channel not found or no data")
    return {"results": results}

@app.get("/api/search/messages", response_model=SearchResponse)
def search_messages(query: str = Query(..., min_length=2)):
    logger.info("Searching messages for {}", query)
    results = crud.search_messages(query=query)
    return {"results": results}
