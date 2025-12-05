from src.database import engine, Base
from src.models.template import Template

# This will create the templates table if it doesn't exist
Base.metadata.create_all(bind=engine)
print("Database schema updated.")
