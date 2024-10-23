# src/rufus/processors/cleaner.py
import re
from typing import Dict, List
from bs4 import BeautifulSoup
from loguru import logger

class ContentCleaner:
    """Clean and normalize extracted content."""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
    
    def clean(self, content: List[Dict]) -> List[Dict]:
        """Clean and normalize content."""
        try:
            cleaned = []
            for item in content:
                cleaned_item = self._clean_item(item)
                if cleaned_item:
                    cleaned.append(cleaned_item)
            return cleaned
        except Exception as e:
            logger.error(f"Content cleaning failed: {str(e)}")
            return content
    
    def _clean_item(self, item: Dict) -> Dict:
        """Clean individual content item."""
        try:
            if "content" in item:
                item["content"] = self._clean_text(item["content"])
            
            if "type" in item and item["type"] == "table":
                item["headers"] = [
                    self._clean_text(h) for h in item.get("headers", [])
                ]
                item["rows"] = [
                    [self._clean_text(cell) for cell in row]
                    for row in item.get("rows", [])
                ]
            
            return item if self._is_valid_content(item) else None
            
        except Exception as e:
            logger.error(f"Item cleaning failed: {str(e)}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        try:
            # Remove HTML tags
            text = BeautifulSoup(text, "html.parser").get_text()
            
            # Normalize whitespace
            text = re.sub(r'\s+', ' ', text)
            
            # Remove special characters
            text = re.sub(r'[^\w\s\-.,?!]', '', text)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Text cleaning failed: {str(e)}")
            return text
    
    def _is_valid_content(self, item: Dict) -> bool:
        """Check if cleaned content is valid."""
        if not item:
            return False
            
        content = item.get("content", "")
        if isinstance(content, str):
            # Check minimum content length and maximum ratio of special characters
            return (
                len(content) >= 3 and
                len(re.findall(r'[^\w\s]', content)) / len(content) < 0.3
            )
        return True