# tests/conftest.py
import pytest
import asyncio
from rufus import RufusClient
import os

@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def rufus_client():
    """Create Rufus client for testing."""
    api_key = os.getenv("RUFUS_API_KEY", "test-key")
    client = RufusClient(api_key=api_key)
    yield client

@pytest.fixture
def sample_html():
    """Sample HTML content for testing."""
    return """
    <html>
        <body>
            <h1>Test Page</h1>
            <p>Sample content</p>
            <table>
                <tr><th>Header</th></tr>
                <tr><td>Data</td></tr>
            </table>
        </body>
    </html>
    """
