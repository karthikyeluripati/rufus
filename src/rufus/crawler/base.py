# src/rufus/crawler/base.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from loguru import logger
from ..utils import Validators, RateLimiter

class BaseCrawler(ABC):
    """Base crawler class defining the interface for all crawlers."""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.visited_urls: Set[str] = set()
        self.rate_limiter = RateLimiter(
            requests_per_second=self.config.get('rate_limit', 2)
        )
        self.validators = Validators()
    
    @abstractmethod
    async def crawl(
        self,
        url: str,
        max_depth: int = 3,
        selectors: Optional[List[str]] = None
    ) -> List[Dict]:
        """Crawl the website and extract content."""
        pass
    
    def is_valid_url(self, url: str, base_url: str) -> bool:
        """Check if URL is valid and belongs to the same domain."""
        if not self.validators.validate_url(url):
            return False
            
        try:
            parsed = urlparse(url)
            base_parsed = urlparse(base_url)
            return parsed.netloc == base_parsed.netloc
        except Exception as e:
            logger.error(f"URL validation error: {e}")
            return False
    
    async def extract_links(
        self,
        html: str,
        base_url: str
    ) -> List[str]:
        """Extract valid links from HTML content."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            links = set()
            
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']
                absolute_url = urljoin(base_url, href)
                
                if self.is_valid_url(absolute_url, base_url):
                    links.add(absolute_url)
            
            return list(links)
        except Exception as e:
            logger.error(f"Link extraction error: {e}")
            return []