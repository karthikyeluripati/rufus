# src/rufus/utils/cache.py
import redis
from typing import Optional, Any
import json
import os
from loguru import logger

class Cache:
    """Redis-based caching system for Rufus."""
    
    def __init__(self):
        self.enabled = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
        if self.enabled:
            try:
                self.redis = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379'))
                self.redis.ping()
            except Exception as e:
                logger.warning(f"Cache initialization failed: {e}")
                self.enabled = False
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.enabled:
            return None
            
        try:
            value = self.redis.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        expires_in: int = 3600
    ) -> bool:
        """Set value in cache with expiration."""
        if not self.enabled:
            return False
            
        try:
            self.redis.setex(
                key,
                expires_in,
                json.dumps(value)
            )
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False