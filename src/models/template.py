from sqlalchemy import Column, Integer, String, Text, DateTime
from src.database import Base
from datetime import datetime

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    type_acte = Column(String, nullable=False)  # VENTE, PROCURATION, etc.
    contenu = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
