# src/rufus/extractors/base.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from loguru import logger

class BaseExtractor(ABC):
    """Base class for content extractors."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
    
    @abstractmethod
    async def extract(
        self,
        content: str,
        selectors: Optional[List[str]] = None
    ) -> List[Dict]:
        """Extract content based on selectors."""
        pass
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        return " ".join(text.split())
    
    def _extract_metadata(self, element: BeautifulSoup) -> Dict:
        """Extract metadata from element."""
        return {
            "tag": element.name,
            "classes": element.get("class", []),
            "id": element.get("id"),
            "attributes": dict(element.attrs)
        }
