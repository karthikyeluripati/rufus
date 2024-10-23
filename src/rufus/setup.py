from setuptools import setup, find_packages

setup(
    name="rufus",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "aiohttp>=3.9.1",
        "beautifulsoup4>=4.12.2",
        "fastapi>=0.109.1",
        "langchain>=0.1.0",
        "loguru>=0.7.2",
        "openai>=1.3.7",
        "playwright>=1.41.1",
        "pydantic>=2.5.2",
        "python-dotenv>=1.0.0",
        "redis>=5.0.1",
        "streamlit>=1.29.0",
        "uvicorn>=0.27.0",
    ],
    python_requires=">=3.9",
)