from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime
import enum

class StatutActe(str, enum.Enum):
    BROUILLON = "BROUILLON"
    FINALISE = "FINALISE"
    SIGNE = "SIGNE"

class Acte(Base):
    __tablename__ = "actes"

    id = Column(Integer, primary_key=True, index=True)
    dossier_id = Column(Integer, ForeignKey("dossiers.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=True)
    titre = Column(String, nullable=False)
    contenu = Column(Text, nullable=True)  # HTML or Text content
    statut = Column(String, default=StatutActe.BROUILLON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    dossier = relationship("Dossier", back_populates="actes")
    template = relationship("Template")
