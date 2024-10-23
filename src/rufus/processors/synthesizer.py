# src/rufus/processors/synthesizer.py
from typing import Dict, List, Optional
import json
from loguru import logger

class ContentSynthesizer:
    """Synthesize extracted content into structured documents."""
    
    async def synthesize(
        self,
        content: List[Dict],
        format: str = "json"
    ) -> Dict:
        """Synthesize content into specified format."""
        try:
            # Group content by type
            grouped = self._group_content(content)
            
            # Process each group
            processed = self._process_groups(grouped)
            
            # Format output
            if format == "json":
                return self._format_json(processed)
            elif format == "csv":
                return self._format_csv(processed)
            elif format == "markdown":
                return self._format_markdown(processed)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            logger.error(f"Content synthesis failed: {str(e)}")
            return {"error": str(e), "raw_content": content}
    
    def _group_content(self, content: List[Dict]) -> Dict:
        """Group content by type and structure."""
        groups = {
            "text": [],
            "tables": [],
            "lists": [],
            "forms": [],
            "other": []
        }
        
        for item in content:
            content_type = item.get("type", "other")
            if content_type in groups:
                groups[content_type].append(item)
            else:
                groups["other"].append(item)
        
        return groups
    
    def _process_groups(self, grouped: Dict) -> Dict:
        """Process and structure each content group."""
        processed = {}
        
        # Process text content
        if grouped["text"]:
            processed["text_content"] = self._process_text(grouped["text"])
        
        # Process tables
        if grouped["tables"]:
            processed["tables"] = self._process_tables(grouped["tables"])
        
        # Process lists
        if grouped["lists"]:
            processed["lists"] = self._process_lists(grouped["lists"])
        
        # Process forms
        if grouped["forms"]:
            processed["forms"] = self._process_forms(grouped["forms"])
        
        # Add metadata
        processed["metadata"] = {
            "total_items": sum(len(g) for g in grouped.values()),
            "content_types": {k: len(v) for k, v in grouped.items() if v}
        }
        
        return processed
    
    def _process_text(self, text_content: List[Dict]) -> List[Dict]:
        """Process and organize text content."""
        # Sort by relevance if available
        text_content.sort(
            key=lambda x: x.get("metadata", {}).get("relevance", 0),
            reverse=True
        )
        
        # Group by hierarchy (h1, h2, etc.)
        hierarchy = {}
        for item in text_content:
            tag = item.get("metadata", {}).get("tag", "p")
            if tag not in hierarchy:
                hierarchy[tag] = []
            hierarchy[tag].append(item["content"])
        
        return {
            "hierarchy": hierarchy,
            "full_text": "\n\n".join(item["content"] for item in text_content)
        }
    
    def _format_json(self, processed: Dict) -> Dict:
        """Format content as JSON."""
        return {
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "content": processed
        }
    
    def _format_csv(self, processed: Dict) -> Dict:
        """Format content as CSV-compatible structure."""
        csv_data = []
        
        # Convert text content
        if "text_content" in processed:
            for text in processed["text_content"].get("hierarchy", {}).values():
                csv_data.extend([{"type": "text", "content": t} for t in text])
        
        # Convert tables
        if "tables" in processed:
            for table in processed["tables"]:
                csv_data.extend([{
                    "type": "table_row",
                    "content": json.dumps(row)
                } for row in table["rows"]])
        
        return {
            "format": "csv",
            "data": csv_data
        }
    
    def _format_markdown(self, processed: Dict) -> Dict:
        """Format content as Markdown."""
        md_content = []
        
        # Convert text content
        if "text_content" in processed:
            hierarchy = processed["text_content"]["hierarchy"]
            for tag, texts in hierarchy.items():
                level = int(tag[1]) if tag.startswith('h') else 0
                for text in texts:
                    if level > 0:
                        md_content.append(f"{'#' * level} {text}\n")
                    else:
                        md_content.append(f"{text}\n\n")
        
        # Convert tables
        if "tables" in processed:
            for table in processed["tables"]:
                md_content.append(self._table_to_markdown(table))
        
        return {
            "format": "markdown",
            "content": "\n".join(md_content)
        }