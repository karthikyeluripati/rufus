# Rufus API Documentation

## Overview

The Rufus API provides programmatic access to web scraping and content extraction functionality. This document details the available endpoints, request/response formats, and authentication requirements.

## Authentication

All API requests require an API key passed in the header:

```bash
Authorization: Bearer your_api_key
```

## Endpoints

### 1. Scrape Website

Extract content from a specified URL.

**Endpoint:** `POST /api/scrape`

**Request:**
```json
{
    "url": "https://example.com",
    "instructions": "Extract main content",
    "max_depth": 2,
    "output_format": "json"
}
```

**Response:**
```json
{
    "url": "https://example.com",
    "content": {
        "title": "Page Title",
        "headings": ["Heading 1", "Heading 2"],
        "paragraphs": ["Content..."]
    },
    "metadata": {
        "pages_crawled": 1,
        "content_items": 10,
        "processing_time": "2.5 seconds"
    }
}
```

### 2. Check Status

Check the status of a scraping job.

**Endpoint:** `GET /api/status/{job_id}`

**Response:**
```json
{
    "job_id": "123",
    "status": "completed",
    "progress": 100,
    "error": null
}
```

## Rate Limits

- 60 requests per minute per API key
- Maximum 5 concurrent requests

## Error Codes

- `400`: Bad Request
- `401`: Unauthorized
- `429`: Too Many Requests
- `500`: Internal Server Error

## Python Client Usage

```python
from rufus import RufusClient
import asyncio

async def main():
    client = RufusClient(api_key="your_api_key")
    
    results = await client.scrape(
        url="https://example.com",
        instructions="Extract main content",
        max_depth=2
    )
    
    print(results)

asyncio.run(main())
```

## WebSocket API

For real-time updates during scraping:

```javascript
const ws = new WebSocket('wss://api.rufus.com/ws');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Progress:', data.progress);
};
```