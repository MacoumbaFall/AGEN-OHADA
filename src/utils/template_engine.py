import re
from typing import Dict, Any, List

class TemplateEngine:
    """
    Simple template engine to handle variable replacement in acts.
    Supports {{variable}} syntax.
    """
    
    @staticmethod
    def extract_variables(content: str) -> List[str]:
        """
        Extract all variable names from content formatted as {{variable}}.
        Returns a list of unique variable names.
        """
        if not content:
            return []
        # Find all matches for {{ variable }} with optional whitespace
        pattern = r"\{\{\s*([\w\.]+)\s*\}\}"
        matches = re.findall(pattern, content)
        return sorted(list(set(matches)))

    @staticmethod
    def merge(content: str, data: Dict[str, Any]) -> str:
        """
        Replace variables in content with values from data dictionary.
        If a variable is missing in data, it is left as is or replaced by placeholder?
        For now, we replace with "[MISSING: variable]" to highlight it, or just keep it.
        Let's try to replace found ones and leave others or replace with empty string.
        """
        if not content:
            return ""
            
        def replace_match(match):
            key = match.group(1).strip()
            # Handle nested keys if we support them later, e.g. client.name
            # For now simple dictionary lookup
            val = data.get(key)
            if val is None:
                # Check for dotted access manually if needed, or flat dict
                # Let's try to resolve dotted access logic briefly
                parts = key.split('.')
                current = data
                try:
                    for part in parts:
                        current = current[part]
                    val = current
                except (KeyError, TypeError, AttributeError):
                    pass
            
            return str(val) if val is not None else f"{{{{{key}}}}}"

        pattern = r"\{\{\s*([\w\.]+)\s*\}\}"
        return re.sub(pattern, replace_match, content)

    @staticmethod
    def get_dossier_context(dossier, parties: List = None) -> Dict[str, Any]:
        """
        Helper to convert a Dossier object and its related data into a context dictionary.
        """
        ctx = {
            "dossier": {
                "numero": dossier.numero_dossier,
                "intitule": dossier.intitule,
                "date_ouverture": str(dossier.date_ouverture),
                "type": dossier.type_dossier
            },
            "date_jour": datetime.now().strftime("%d/%m/%Y"),
            "ville_signature": "Dakar" # Default
        }
        
        # Add parties
        # This requires traversing parties and role
        # We'll rely on the caller to provide a structured dict or enhance this later
        return ctx

from datetime import datetime
