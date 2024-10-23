# src/api/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import (
    ScrapeRequest,
    ScrapeResponse,
    ErrorResponse
)
from rufus import RufusClient
from loguru import logger
import os

app = FastAPI(
    title="Rufus API",
    description="AI-powered web scraping API for RAG systems",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for Rufus client
async def get_rufus_client():
    api_key = os.getenv("RUFUS_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="API key not configured"
        )
    return RufusClient(api_key=api_key)

@app.post(
    "/scrape",
    response_model=ScrapeResponse,
    responses={400: {"model": ErrorResponse}}
)
async def scrape_website(
    request: ScrapeRequest,
    client: RufusClient = Depends(get_rufus_client)
):
    """Scrape website content based on provided instructions."""
    try:
        documents = await client.scrape(
            url=request.url,
            instructions=request.instructions,
            max_depth=request.max_depth,
            output_format=request.output_format
        )
        
        return ScrapeResponse(
            status="success",
            data=documents
        )
        
    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )