# src/rufus/extractors/structured.py
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import json
from .base import BaseExtractor
from loguru import logger

class StructuredExtractor(BaseExtractor):
    """Extract structured data from HTML."""
    
    async def extract(
        self,
        content: str,
        selectors: Optional[List[str]] = None
    ) -> List[Dict]:
        """Extract structured data like tables, lists, and forms."""
        try:
            soup = BeautifulSoup(content, 'html.parser')
            results = []
            
            # Extract tables
            results.extend(self._extract_tables(soup))
            
            # Extract lists
            results.extend(self._extract_lists(soup))
            
            # Extract forms
            results.extend(self._extract_forms(soup))
            
            return results
            
        except Exception as e:
            logger.error(f"Structured extraction failed: {str(e)}")
            return []
    
    def _extract_tables(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract table data."""
        results = []
        for table in soup.find_all('table'):
            try:
                headers = []
                for th in table.find_all('th'):
                    headers.append(self._clean_text(th.get_text()))
                
                rows = []
                for tr in table.find_all('tr'):
                    row = []
                    for td in tr.find_all('td'):
                        row.append(self._clean_text(td.get_text()))
                    if row:
                        rows.append(row)
                
                results.append({
                    "type": "table",
                    "headers": headers,
                    "rows": rows,
                    "metadata": self._extract_metadata(table)
                })
                
            except Exception as e:
                logger.error(f"Table extraction failed: {str(e)}")
                continue
        
        return results
    
    def _extract_lists(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract list data."""
        results = []
        for list_tag in soup.find_all(['ul', 'ol']):
            try:
                items = []
                for li in list_tag.find_all('li'):
                    items.append(self._clean_text(li.get_text()))
                
                results.append({
                    "type": "list",
                    "list_type": list_tag.name,
                    "items": items,
                    "metadata": self._extract_metadata(list_tag)
                })
                
            except Exception as e:
                logger.error(f"List extraction failed: {str(e)}")
                continue
        
        return results
    
    def _extract_forms(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract form data."""
        results = []
        for form in soup.find_all('form'):
            try:
                fields = []
                for input_tag in form.find_all(['input', 'select', 'textarea']):
                    fields.append({
                        "type": input_tag.get('type', input_tag.name),
                        "name": input_tag.get('name', ''),
                        "id": input_tag.get('id', ''),
                        "required": input_tag.get('required') is not None
                    })
                
                results.append({
                    "type": "form",
                    "action": form.get('action', ''),
                    "method": form.get('method', 'get'),
                    "fields": fields,
                    "metadata": self._extract_metadata(form)
                })
                
            except Exception as e:
                logger.error(f"Form extraction failed: {str(e)}")
                continue
        
        return results