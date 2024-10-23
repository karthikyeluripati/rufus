# src/rufus/crawler/js_crawler.py
from typing import Dict, List, Optional
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from loguru import logger
from .base import BaseCrawler

class JSCrawler(BaseCrawler):
    """Crawler capable of handling JavaScript-rendered content."""
    
    async def crawl(
        self,
        url: str,
        max_depth: int = 3,
        selectors: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Crawl JavaScript-rendered website content.
        
        Args:
            url: Website URL to crawl
            max_depth: Maximum crawl depth
            selectors: Optional CSS selectors for content extraction
            
        Returns:
            List of extracted content items
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            
            try:
                return await self._crawl_recursive(
                    context,
                    url,
                    max_depth,
                    selectors,
                    depth=0
                )
            finally:
                await browser.close()
    
    async def _crawl_recursive(
        self,
        context,
        url: str,
        max_depth: int,
        selectors: Optional[List[str]],
        depth: int
    ) -> List[Dict]:
        """
        Recursively crawl pages and extract content.
        
        Args:
            context: Playwright browser context
            url: Current URL to crawl
            max_depth: Maximum crawl depth
            selectors: CSS selectors for content extraction
            depth: Current crawl depth
            
        Returns:
            List of extracted content items
        """
        if depth >= max_depth or url in self.visited_urls:
            return []
        
        await self.rate_limiter.wait()
        self.visited_urls.add(url)
        
        try:
            page = await context.new_page()
            await page.goto(url, wait_until='networkidle')
            
            # Extract content
            content = await self._extract_content(page, selectors)
            
            # Find and crawl links if needed
            if depth < max_depth:
                links = await self._extract_js_links(page)
                for link in links:
                    if link not in self.visited_urls:
                        child_content = await self._crawl_recursive(
                            context,
                            link,
                            max_depth,
                            selectors,
                            depth + 1
                        )
                        content.extend(child_content)
            
            return content
            
        except Exception as e:
            logger.error(f"Error crawling {url}: {str(e)}")
            return []
        
        finally:
            if 'page' in locals():
                await page.close()
    
    async def _extract_content(
        self,
        page,
        selectors: Optional[List[str]]
    ) -> List[Dict]:
        """
        Extract content from page using selectors.
        
        Args:
            page: Playwright page object
            selectors: CSS selectors for content extraction
            
        Returns:
            List of extracted content items
        """
        try:
            # Get page content after JavaScript execution
            html_content = await page.content()
            soup = BeautifulSoup(html_content, 'html.parser')
            content = []
            
            if not selectors:
                # Default content extraction
                for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article']:
                    elements = soup.find_all(tag)
                    for element in elements:
                        text = self.validators.sanitize_text(element.get_text())
                        if text:
                            content.append({
                                'type': tag,
                                'content': text,
                                'metadata': self._extract_metadata(element),
                                'url': page.url
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
                                    'metadata': self._extract_metadata(element),
                                    'url': page.url
                                })
            
            return content
            
        except Exception as e:
            logger.error(f"Content extraction error: {str(e)}")
            return []
    
    async def _extract_js_links(self, page) -> List[str]:
        """
        Extract links from JavaScript-rendered page.
        
        Args:
            page: Playwright page object
            
        Returns:
            List of extracted URLs
        """
        try:
            # Get all links after JavaScript execution
            links = await page.evaluate("""
                () => Array.from(document.querySelectorAll('a[href]'))
                    .map(a => a.href)
                    .filter(href => href.startsWith('http'))
            """)
            
            # Filter valid links
            valid_links = []
            for link in links:
                if self.is_valid_url(link, page.url):
                    valid_links.append(link)
            
            return valid_links
            
        except Exception as e:
            logger.error(f"Link extraction error: {str(e)}")
            return []
    
    def _extract_metadata(self, element) -> Dict:
        """
        Extract metadata from HTML element.
        
        Args:
            element: BeautifulSoup element
            
        Returns:
            Dictionary of element metadata
        """
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