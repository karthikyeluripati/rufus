# examples/basic_usage.py
import asyncio
from rufus import RufusClient
import os

async def main():
    # Initialize client
    api_key = os.getenv("RUFUS_API_KEY")
    client = RufusClient(api_key=api_key)
    
    # Example: Extract HR information
    instructions = "We're making a chatbot for HR in San Francisco."
    documents = await client.scrape(
        "https://www.sfgov.com",
        instructions=instructions,
        max_depth=2
    )
    
    print(json.dumps(documents, indent=2))

if __name__ == "__main__":
    asyncio.run(main())