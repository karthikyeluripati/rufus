# src/rufus/utils/rate_limiter.py
import asyncio
from datetime import datetime, timedelta
from typing import Dict
from loguru import logger

class RateLimiter:
    """Token bucket rate limiter."""
    
    def __init__(
        self,
        requests_per_second: int = 2,
        burst_size: int = 5
    ):
        self.rate = requests_per_second
        self.burst_size = burst_size
        self.tokens = burst_size
        self.last_update = datetime.now()
        self.lock = asyncio.Lock()
    
    async def wait(self) -> None:
        """Wait for rate limit clearance."""
        async with self.lock:
            while self.tokens <= 0:
                now = datetime.now()
                time_passed = (now - self.last_update).total_seconds()
                new_tokens = time_passed * self.rate
                
                self.tokens = min(
                    self.burst_size,
                    self.tokens + new_tokens
                )
                self.last_update = now
                
                if self.tokens <= 0:
                    await asyncio.sleep(1.0 / self.rate)
            
            self.tokens -= 1