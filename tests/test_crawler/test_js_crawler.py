import pytest
from rufus.crawler import JSCrawler

@pytest.mark.asyncio
async def test_js_crawler_basic():
    """Test basic crawling functionality."""
    crawler = JSCrawler()
    url = "https://example.com"
    
    results = await crawler.crawl(url, max_depth=1)
    assert isinstance(results, list)
    assert len(results) > 0

@pytest.mark.asyncio
async def test_js_crawler_depth_limit():
    """Test crawling depth limit."""
    crawler = JSCrawler()
    url = "https://example.com"
    
    results = await crawler.crawl(url, max_depth=0)
    assert len(results) <= 1

@pytest.mark.asyncio
async def test_js_crawler_error_handling():
    """Test crawler error handling."""
    crawler = JSCrawler()
    url = "https://nonexistent.example.com"
    
    results = await crawler.crawl(url)
    assert len(results) == 0
