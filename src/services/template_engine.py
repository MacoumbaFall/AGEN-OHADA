import jinja2
from src.models.dossier import Dossier
from src.models.client import Client

class TemplateEngine:
    """
    Handles merging of data into templates using Jinja2.
    """
    
    def __init__(self):
        self.env = jinja2.Environment(
            loader=jinja2.BaseLoader(),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        
    def render(self, template_content: str, dossier: Dossier) -> str:
        """
        Render a template string with dossier data.
        """
        try:
            template = self.env.from_string(template_content)
            context = self._build_context(dossier)
            return template.render(**context)
        except Exception as e:
            return f"Error rendering template: {str(e)}"
            
    def _build_context(self, dossier: Dossier) -> dict:
        """
        Convert dossier object into a dictionary context for Jinja2.
        """
        context = {
            "dossier": {
                "numero": dossier.numero_dossier,
                "intitule": dossier.intitule,
                "date_ouverture": dossier.date_ouverture.strftime("%d/%m/%Y") if dossier.date_ouverture else "",
                "montant_acte": dossier.montant_acte,
                "description": dossier.description,
            },
            "clients": [],
            "parties": {},
            "date_jour": datetime.now().strftime("%d/%m/%Y")
        }
        
        # Organize parties by role
        # Assuming we can access dossier.parties_associations
        # Note: In synchronous context without active session this might fail if not eager loaded.
        # But usually passed 'dossier' is attached to session or we access attributes triggering load.
        
        for assoc in dossier.parties_associations:
            client = assoc.client
            role = assoc.role_dans_acte.lower().replace(" ", "_") # e.g. "vendeur", "acquereur"
            
            client_data = {
                "nom": client.nom,
                "prenom": client.prenom,
                "nom_complet": f"{client.prenom} {client.nom}" if client.type_client == "PHYSIQUE" else client.nom,
                "adresse": client.adresse,
                "email": client.email,
                "telephone": client.telephone,
                "type": client.type_client
            }
            
            # Add to general list
            context["clients"].append(client_data)
            
            # Add to role specific list/dict
            if role not in context["parties"]:
                context["parties"][role] = []
            context["parties"][role].append(client_data)
            
            # Also allow accessing single party directly if only one (e.g. {{ parties.vendeur.nom }})
            # This overwrites if multiple, but convenient for simple cases
            if role not in context["parties"] or isinstance(context["parties"][role], list):
                 # We keep the list but also might want a direct access helper
                 pass

        # Flatten single-item lists for easier access? 
        # For now, let's keep it simple: parties.vendeur[0].nom or loop
        
        return context

    def get_available_variables(self) -> list:
        """
        Return a list of available variables for documentation/UI.
        """
        return [
            "dossier.numero",
            "dossier.intitule",
            "dossier.date_ouverture",
            "dossier.montant_acte",
            "date_jour",
            "parties.vendeur",
            "parties.acquereur",
            # ... add more
        ]

from datetime import datetime
