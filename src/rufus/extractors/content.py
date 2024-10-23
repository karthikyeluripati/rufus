# src/rufus/extractors/content.py
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from .base import BaseExtractor
from loguru import logger

class ContentExtractor(BaseExtractor):
    """Extract text content from HTML."""
    
    async def extract(
        self,
        content: str,
        selectors: Optional[List[str]] = None
    ) -> List[Dict]:
        """Extract content using provided selectors."""
        try:
            soup = BeautifulSoup(content, 'html.parser')
            results = []
            
            if not selectors:
                # Default content extraction
                for tag in ['p', 'h1', 'h2', 'h3', 'article']:
                    elements = soup.find_all(tag)
                    for element in elements:
                        results.append(self._process_element(element))
            else:
                # Selective extraction
                for selector in selectors:
                    elements = soup.select(selector)
                    for element in elements:
                        results.append(self._process_element(element))
            
            return [r for r in results if r["content"].strip()]
            
        except Exception as e:
            logger.error(f"Content extraction failed: {str(e)}")
            return []
    
    def _process_element(self, element: BeautifulSoup) -> Dict:
        """Process a single HTML element."""
        return {
            "type": "text",
            "content": self._clean_text(element.get_text()),
            "metadata": self._extract_metadata(element)
        }
