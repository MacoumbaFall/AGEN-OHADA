from sqlalchemy import Column, Integer, String, Date, Text, DateTime
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    type_client = Column(String, nullable=False) # PHYSIQUE or MORALE
    nom = Column(String, index=True, nullable=False)
    prenom = Column(String, nullable=True)
    date_naissance = Column(Date, nullable=True)
    lieu_naissance = Column(String, nullable=True)
    adresse = Column(Text, nullable=True)
    telephone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    identifiant_unique = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    dossier_associations = relationship("DossierParties", back_populates="client")
