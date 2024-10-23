# src/rufus/agent/prompt_templates.py
"""Prompt templates for the AI agent."""

STRATEGY_PROMPT = """You are an expert web crawler tasked with extracting specific information.

URL: {url}
Instructions: {instructions}

Create a detailed extraction strategy that includes:
1. Key pages to prioritize
2. Content patterns to match
3. Relevance criteria
4. Navigation paths

Strategy should be provided in JSON format with the following structure:
{
    "priority_pages": ["list of important pages"],
    "content_patterns": ["CSS selectors for relevant content"],
    "relevance_criteria": ["keywords and patterns"],
    "ignore_patterns": ["patterns to skip"],
    "extraction_rules": {"element_type": "extraction_rule"}
}"""

RELEVANCE_PROMPT = """Evaluate the relevance of the following content:

Content: {content}
Context: {context}

Rate the relevance on a scale of 0-1 and explain why:
{
    "score": 0.0-1.0,
    "explanation": "reason for score",
    "key_matches": ["matched criteria"]
}"""

SYNTHESIS_PROMPT = """Synthesize the following extracted content into a structured document:

Content: {content}
Instructions: {instructions}

Organize the content into a clean, structured format suitable for RAG systems.
Focus on maintaining context and relationships between pieces of information."""