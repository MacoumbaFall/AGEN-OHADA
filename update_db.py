from src.database import engine, Base
from src.models.dossier import Dossier, DossierParties, DossierHistorique
from src.models.client import Client
from src.models.user import User

print("Updating database schema...")
Base.metadata.create_all(bind=engine)
print("Database schema updated successfully.")
