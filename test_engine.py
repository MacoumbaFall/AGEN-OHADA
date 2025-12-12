
from src.utils.template_engine import TemplateEngine
from src.models.dossier import Dossier
from datetime import datetime

# Mock Dossier
class MockDossier:
    numero_dossier = "2025-001"
    intitule = "Vente Maison"
    date_ouverture = datetime.now()
    type_dossier = "VENTE"

dossier = MockDossier()
ctx = TemplateEngine.get_dossier_context(dossier)

template_content = "Je soussigné, pour le dossier {{dossier.numero}} intitulé {{dossier.intitule}}, déclare..."
merged = TemplateEngine.merge(template_content, ctx)

print("Original:", template_content)
print("Merged:", merged)

assert "2025-001" in merged
assert "Vente Maison" in merged
print("TEST OK")
