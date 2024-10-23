# src/rufus/utils/validators.py
from typing import Optional
from urllib.parse import urlparse
import re
from loguru import logger

class Validators:
    """Input validation utilities."""
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format and scheme."""
        try:
            result = urlparse(url)
            return all([
                result.scheme in ['http', 'https'],
                result.netloc,
                len(url) < 2048
            ])
        except Exception as e:
            logger.error(f"URL validation error: {e}")
            return False
    
    @staticmethod
    def validate_selector(selector: str) -> bool:
        """Validate CSS selector syntax."""
        try:
            # Basic CSS selector validation
            pattern = r'^[a-zA-Z0-9_\-\s\.\#\[\]\=\^\$\*\,\>\+\~\:\'\"]+$'
            return bool(re.match(pattern, selector))
        except Exception as e:
            logger.error(f"Selector validation error: {e}")
            return False
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitize extracted text content."""
        # Remove special characters and normalize whitespace
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()