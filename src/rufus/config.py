# src/rufus/config.py
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

DEFAULT_CONFIG: Dict[str, Any] = {
    "max_depth": 3,
    "rate_limit": 2,
    "timeout": 30,
    "max_retries": 3,
    "cache_enabled": True,
    "user_agent": "Rufus/1.0 Web Scraper",
}

def get_config() -> Dict[str, Any]:
    """Get configuration with environment variables."""
    config = DEFAULT_CONFIG.copy()
    
    # Override with environment variables if they exist
    env_vars = {
        "RUFUS_MAX_DEPTH": ("max_depth", int),
        "RUFUS_RATE_LIMIT": ("rate_limit", int),
        "RUFUS_TIMEOUT": ("timeout", int),
        "RUFUS_MAX_RETRIES": ("max_retries", int),
        "RUFUS_CACHE_ENABLED": ("cache_enabled", lambda x: x.lower() == "true"),
    }
    
    for env_var, (config_key, type_func) in env_vars.items():
        if value := os.getenv(env_var):
            try:
                config[config_key] = type_func(value)
            except ValueError:
                pass
    
    return config