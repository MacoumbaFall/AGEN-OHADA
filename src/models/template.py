from sqlalchemy import Column, Integer, String, Text, DateTime
from src.database import Base
from datetime import datetime

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)  # Matches SQL 'nom'
    type_acte = Column(String, nullable=False)  # VENTE, PROCURATION, etc.
    contenu = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    # variables column does not exist in DB currently
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
