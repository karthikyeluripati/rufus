# src/rufus/agent/ai_agent.py
from typing import Dict, List, Optional
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json
from loguru import logger
from .prompt_templates import (
    STRATEGY_PROMPT,
    RELEVANCE_PROMPT,
    SYNTHESIS_PROMPT
)

class RufusAgent:
    """AI agent for intelligent web scraping."""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.llm = ChatOpenAI(
            model_name=model,
            temperature=0.1,
            api_key=api_key
        )
        
        self.strategy_prompt = ChatPromptTemplate.from_messages([
            ("system", STRATEGY_PROMPT)
        ])
        
        self.relevance_prompt = ChatPromptTemplate.from_messages([
            ("system", RELEVANCE_PROMPT)
        ])
        
        self.synthesis_prompt = ChatPromptTemplate.from_messages([
            ("system", SYNTHESIS_PROMPT)
        ])
    
    async def plan_extraction(
        self,
        url: str,
        instructions: str
    ) -> Dict:
        """Generate extraction strategy based on instructions."""
        try:
            response = await self.llm.agenerate([{
                "url": url,
                "instructions": instructions
            }])
            
            strategy = self._parse_strategy(response.generations[0].text)
            logger.info(f"Generated extraction strategy for {url}")
            return strategy
            
        except Exception as e:
            logger.error(f"Strategy generation failed: {str(e)}")
            return self._get_default_strategy()
    
    async def evaluate_content(
        self,
        content: str,
        context: str
    ) -> Dict:
        """Evaluate content relevance."""
        try:
            response = await self.llm.agenerate([{
                "content": content,
                "context": context
            }])
            
            evaluation = self._parse_evaluation(response.generations[0].text)
            return evaluation
            
        except Exception as e:
            logger.error(f"Content evaluation failed: {str(e)}")
            return {"score": 0.0, "explanation": "Evaluation failed"}
    
    async def synthesize_documents(
        self,
        contents: List[Dict],
        instructions: str
    ) -> Dict:
        """Synthesize extracted content into structured documents."""
        try:
            response = await self.llm.agenerate([{
                "content": json.dumps(contents),
                "instructions": instructions
            }])
            
            synthesis = self._parse_synthesis(response.generations[0].text)
            return synthesis
            
        except Exception as e:
            logger.error(f"Document synthesis failed: {str(e)}")
            return {"error": "Synthesis failed", "raw_content": contents}
    
    def _parse_strategy(self, strategy_text: str) -> Dict:
        """Parse LLM strategy output into structured format."""
        try:
            return json.loads(strategy_text)
        except json.JSONDecodeError:
            logger.error("Failed to parse strategy JSON")
            return self._get_default_strategy()
    
    def _parse_evaluation(self, evaluation_text: str) -> Dict:
        """Parse LLM evaluation output."""
        try:
            return json.loads(evaluation_text)
        except json.JSONDecodeError:
            return {"score": 0.0, "explanation": "Failed to parse evaluation"}
    
    def _parse_synthesis(self, synthesis_text: str) -> Dict:
        """Parse LLM synthesis output."""
        try:
            return json.loads(synthesis_text)
        except json.JSONDecodeError:
            return {"error": "Failed to parse synthesis"}
    
    def _get_default_strategy(self) -> Dict:
        """Return default extraction strategy."""
        return {
            "priority_pages": [],
            "content_patterns": [
                "p", "h1", "h2", "h3", "article",
                ".content", "#main-content"
            ],
            "relevance_criteria": [],
            "ignore_patterns": [
                "nav", "header", "footer",
                ".sidebar", "#menu"
            ],
            "extraction_rules": {
                "text": "getText",
                "links": "getHref",
                "images": "getSrc"
            }
        }