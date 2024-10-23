# src/rufus/client.py
from typing import Dict, Optional, Any, List
import os
import logging
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime

try:
    from loguru import logger
except ImportError:
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

class RufusClient:
    """Main client interface for Rufus."""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict] = None):
        self.api_key = api_key or os.getenv('RUFUS_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required")
        
        self.config = config or {}
        self.visited_urls = set()
        self.session = None
    
    async def _init_session(self):
        """Initialize aiohttp session."""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
    
    async def scrape(
        self,
        url: str,
        instructions: str,
        max_depth: int = 2,
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """Scrape website content based on instructions."""
        try:
            start_time = datetime.now()
            logger.info(f"Starting scrape for URL: {url}")
            
            await self._init_session()
            content = await self._scrape_url(url, max_depth)
            
            # Process and format results
            processed_content = self._process_content(content, instructions)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "url": url,
                "instructions": instructions,
                "content": processed_content,
                "metadata": {
                    "pages_crawled": len(self.visited_urls),
                    "content_items": len(content),
                    "processing_time": f"{processing_time:.1f} seconds",
                    "extracted_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Scraping failed: {str(e)}")
            raise
        
        finally:
            if self.session:
                await self.session.close()
                self.session = None
    
    async def _scrape_url(self, url: str, max_depth: int) -> List[Dict]:
        """Scrape content from a URL."""
        if url in self.visited_urls:
            return []
        
        self.visited_urls.add(url)
        content = []
        
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.warning(f"Failed to fetch {url}: {response.status}")
                    return []
                
                html = await response.text()
                page_content = self._extract_content(html)
                content.extend(page_content)
                
                # Extract and follow links if needed
                if len(self.visited_urls) < max_depth:
                    links = self._extract_links(html, url)
                    for link in links[:3]:  # Limit to 3 links for testing
                        if link not in self.visited_urls:
                            child_content = await self._scrape_url(link, max_depth)
                            content.extend(child_content)
                
                return content
                
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return []
    
    def _extract_content(self, html: str) -> List[Dict]:
        """Extract content from HTML."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            content = []
            
            # Extract title
            if soup.title:
                content.append({
                    "type": "title",
                    "content": soup.title.string.strip()
                })
            
            # Extract main content
            main_content = soup.find(['main', 'article']) or soup.find('div', {'class': ['content', 'main']})
            if not main_content:
                main_content = soup.body
            
            # Extract text content
            for element in main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                text = element.get_text(strip=True)
                if text:
                    content.append({
                        "type": element.name,
                        "content": text
                    })
            
            return content
            
        except Exception as e:
            logger.error(f"Content extraction error: {str(e)}")
            return []
    
    def _extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract links from HTML."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            links = []
            
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('http'):
                    links.append(href)
                elif href.startswith('/'):
                    links.append(f"{base_url.rstrip('/')}{href}")
            
            return links
            
        except Exception as e:
            logger.error(f"Link extraction error: {str(e)}")
            return []
    
    def _process_content(self, content: List[Dict], instructions: str) -> Dict:
        """Process extracted content."""
        grouped_content = {
            "title": "",
            "headings": [],
            "paragraphs": [],
        }
        
        for item in content:
            if item["type"] == "title":
                grouped_content["title"] = item["content"]
            elif item["type"].startswith('h'):
                grouped_content["headings"].append(item["content"])
            elif item["type"] == 'p':
                grouped_content["paragraphs"].append(item["content"])
        
        return grouped_content