# tests/test_agent/test_ai_agent.py
import pytest
from rufus.agent import RufusAgent

@pytest.mark.asyncio
async def test_agent_strategy_generation():
    """Test strategy generation."""
    agent = RufusAgent("test-key")
    
    strategy = await agent.plan_extraction(
        "https://example.com",
        "Extract product information"
    )
    
    assert isinstance(strategy, dict)
    assert "priority_pages" in strategy
    assert "content_patterns" in strategy

@pytest.mark.asyncio
async def test_agent_content_evaluation():
    """Test content relevance evaluation."""
    agent = RufusAgent("test-key")
    
    evaluation = await agent.evaluate_content(
        "Sample product description",
        "Extract product information"
    )
    
    assert isinstance(evaluation, dict)
    assert "score" in evaluation
    assert 0 <= evaluation["score"] <= 1