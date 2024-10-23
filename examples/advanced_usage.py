# examples/advanced_usage.py
import asyncio
from rufus import RufusClient
from rufus.extractors import StructuredExtractor
import os

async def main():
    # Initialize client with custom configuration
    api_key = os.getenv("RUFUS_API_KEY")
    client = RufusClient(
        api_key=api_key,
        config={
            "max_concurrent_requests": 5,
            "rate_limit": 2,
            "cache_enabled": True
        }
    )
    
    # Custom extraction with structured data
    instructions = """
    Extract the following from the website:
    1. All product pricing tables
    2. FAQ sections
    3. Contact forms
    """
    
    documents = await client.scrape(
        "https://example.com",
        instructions=instructions,
        max_depth=3,
        output_format="json"
    )
    
    # Process structured data
    extractor = StructuredExtractor()
    structured_data = await extractor.extract(
        documents["content"],
        ["table", "form"]
    )
    
    print(json.dumps(structured_data, indent=2))

if __name__ == "__main__":
    asyncio.run(main())