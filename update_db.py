from src.database import engine, Base
from src.models import User, Client, Dossier, Template, Acte

# This will create the templates table if it doesn't exist
Base.metadata.create_all(bind=engine)
print("Database schema updated.")
