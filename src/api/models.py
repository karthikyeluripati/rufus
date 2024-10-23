# src/api/models.py
from pydantic import BaseModel, HttpUrl
from typing import Dict, Optional, Literal

class ScrapeRequest(BaseModel):
    """Request model for website scraping."""
    url: HttpUrl
    instructions: str
    max_depth: Optional[int] = 3
    output_format: Optional[Literal["json", "csv", "markdown"]] = "json"
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "instructions": "Extract FAQ content",
                "max_depth": 2,
                "output_format": "json"
            }
        }

class ScrapeResponse(BaseModel):
    """Response model for scraping results."""
    status: str
    data: Dict

class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str