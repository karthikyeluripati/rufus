# src/rufus/crawler/async_crawler.py
import aiohttp
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from .base import BaseCrawler
from loguru import logger
import asyncio

class AsyncCrawler(BaseCrawler):
    """Asynchronous crawler for static content."""
    
    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.session = None
    
    async def _init_session(self):
        """Initialize aiohttp session."""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={
                    'User-Agent': 'Rufus/1.0 Web Scraper (https://github.com/yourusername/rufus)'
                }
            )
    
    async def crawl(
        self,
        url: str,
        max_depth: int = 3,
        selectors: Optional[List[str]] = None
    ) -> List[Dict]:
        """Crawl website asynchronously."""
        await self._init_session()
        
        try:
            return await self._crawl_recursive(
                url,
                max_depth,
                selectors,
                depth=0
            )
        finally:
            await self.session.close()
            self.session = None
    
    async def _crawl_recursive(
        self,
        url: str,
        max_depth: int,
        selectors: Optional[List[str]],
        depth: int
    ) -> List[Dict]:
        if depth >= max_depth or url in self.visited_urls:
            return []
        
        await self.rate_limiter.wait()
        self.visited_urls.add(url)
        
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.warning(f"Failed to fetch {url}: {response.status}")
                    return []
                
                html = await response.text()
                content = self._extract_content(html, selectors)
                
                if depth < max_depth:
                    links = await self.extract_links(html, url)
                    tasks = []
                    
                    for link in links:
                        if link not in self.visited_urls:
                            task = self._crawl_recursive(
                                link,
                                max_depth,
                                selectors,
                                depth + 1
                            )
                            tasks.append(task)
                    
                    if tasks:
                        results = await asyncio.gather(*tasks)
                        for result in results:
                            content.extend(result)
                
                return content
                
        except Exception as e:
            logger.error(f"Error crawling {url}: {str(e)}")
            return []
    
    def _extract_content(
        self,
        html: str,
        selectors: Optional[List[str]]
    ) -> List[Dict]:
        """Extract content based on selectors."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            content = []
            
            if not selectors:
                # Default content extraction
                for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    elements = soup.find_all(tag)
                    for element in elements:
                        text = self.validators.sanitize_text(element.get_text())
                        if text:
                            content.append({
                                'type': tag,
                                'content': text,
                                'metadata': self._extract_metadata(element)
                            })
            else:
                # Selective content extraction
                for selector in selectors:
                    if self.validators.validate_selector(selector):
                        elements = soup.select(selector)
                        for element in elements:
                            text = self.validators.sanitize_text(element.get_text())
                            if text:
                                content.append({
                                    'type': 'selected',
                                    'content': text,
                                    'metadata': self._extract_metadata(element)
                                })
            
            return content
            
        except Exception as e:
            logger.error(f"Content extraction error: {str(e)}")
            return []
    
    def _extract_metadata(self, element) -> Dict:
        """Extract metadata from HTML element."""
        return {
            'tag': element.name,
            'classes': element.get('class', []),
            'id': element.get('id'),
            'attributes': {
                k: v for k, v in element.attrs.items()
                if k not in ['class', 'id']
            },
            'parent_tag': element.parent.name if element.parent else None
        }