# Rufus Web Scraper

Rufus is an AI-powered web scraping tool designed for extracting and structuring web content for RAG (Retrieval-Augmented Generation) systems. It provides intelligent content extraction, structured data output, and an easy-to-use interface.

## 🚀 Features

- **AI-Powered Extraction**: Intelligent content identification and extraction
- **Dynamic Crawling**: Handles JavaScript-rendered content and dynamic pages
- **Smart Content Processing**: Automatically identifies and extracts relevant content
- **Multiple Output Formats**: Supports JSON, CSV, and Markdown outputs
- **User-Friendly Interface**: Streamlit-based UI for easy interaction
- **Robust Error Handling**: Comprehensive error management and recovery
- **Rate Limiting**: Built-in protection against overloading servers

## 📋 Requirements

- Python 3.9 or higher
- Dependencies listed in `requirements.txt`

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rufus
cd rufus
```

2. Create and activate virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -e .
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install chromium
```

5. Create `.env` file:
```env
RUFUS_API_KEY=your_openai_api_key
RUFUS_MAX_DEPTH=3
RUFUS_RATE_LIMIT=2
RUFUS_CACHE_ENABLED=true
```

## 💻 Usage

### Running the Application

1. Start the Streamlit interface:
```bash
streamlit run src/frontend/app.py
```

2. Access the web interface at `http://localhost:8501`

### API Usage

```python
from rufus import RufusClient
import asyncio

async def main():
    # Initialize client
    client = RufusClient(api_key="your_api_key")
    
    # Scrape website
    results = await client.scrape(
        url="https://example.com",
        instructions="Extract main content",
        max_depth=2
    )
    
    print(results)

# Run the scraper
asyncio.run(main())
```

## 📁 Project Structure

```
rufus/
├── src/
│   ├── rufus/
│   │   ├── __init__.py
│   │   ├── agent/
│   │   │   ├── __init__.py
│   │   │   ├── ai_agent.py
│   │   │   └── prompt_templates.py
│   │   ├── crawler/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── async_crawler.py
│   │   │   └── js_crawler.py
│   │   ├── extractors/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── content.py
│   │   │   └── structured.py
│   │   ├── processors/
│   │   │   ├── __init__.py
│   │   │   ├── cleaner.py
│   │   │   └── synthesizer.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── cache.py
│   │       ├── rate_limiter.py
│   │       └── validators.py
│   ├── api/
│   │   └── [API files]
│   └── frontend/
│       └── app.py
├── tests/
├── docs/
└── examples/
```

## 🎯 Features in Detail

### Content Extraction

- **Intelligent Crawling**: Automatically identifies and follows relevant links
- **Content Recognition**: Uses AI to identify important content
- **Structured Data**: Extracts content into organized, structured formats

### Output Formats

1. **JSON**
```json
{
    "url": "https://example.com",
    "content": {
        "title": "Page Title",
        "headings": ["Heading 1", "Heading 2"],
        "paragraphs": ["Content..."]
    },
    "metadata": {
        "pages_crawled": 1,
        "content_items": 10,
        "processing_time": "2.5 seconds"
    }
}
```

2. **CSV Format**
```csv
Type,Content
title,Page Title
heading,Heading 1
paragraph,Content...
```

### User Interface

- Input URL and extraction instructions
- Advanced options for crawl depth and output format
- Real-time progress tracking
- Multiple view modes for results
- Export options

## ⚙️ Configuration

Available environment variables:
- `RUFUS_API_KEY`: OpenAI API key
- `RUFUS_MAX_DEPTH`: Maximum crawl depth
- `RUFUS_RATE_LIMIT`: Requests per second
- `RUFUS_CACHE_ENABLED`: Enable/disable caching

## 🧪 Testing

Run tests using pytest:
```bash
pytest tests/
```

For coverage report:
```bash
pytest tests/ --cov=src/rufus
```

## 🛡️ Error Handling

Rufus includes comprehensive error handling for:
- Invalid URLs
- Connection failures
- Rate limiting
- Content extraction errors
- Processing failures

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Install development dependencies:
```bash
pip install -e ".[dev]"
```
4. Make your changes
5. Run tests
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
```bash
pip install -e .
```

2. **Playwright Issues**
```bash
playwright install chromium
```

3. **API Key Issues**
- Verify `.env` file exists
- Check API key format

### Debug Mode

Enable debug logging:
```bash
export RUFUS_LOG_LEVEL=DEBUG
```

## 📚 Additional Resources

- [API Documentation](docs/api.md)
- [Development Guide](docs/development.md)
- [Deployment Guide](docs/deployment.md)

## ✨ Acknowledgments

- Built with OpenAI's GPT models
- Uses Playwright for JavaScript rendering
- Streamlit for the user interface

---

**Note**: Remember to customize the API key and other sensitive information before deploying.