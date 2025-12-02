from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime

class Dossier(Base):
    __tablename__ = "dossiers"

    id = Column(Integer, primary_key=True, index=True)
    numero_dossier = Column(String, unique=True, index=True, nullable=False)
    intitule = Column(String, nullable=False)
    type_dossier = Column(String, nullable=True)
    statut = Column(String, default="OUVERT")
    date_ouverture = Column(Date, default=datetime.utcnow)
    date_cloture = Column(Date, nullable=True)
    responsable_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    responsable = relationship("User", back_populates="dossiers")
    client_associations = relationship("DossierParties", back_populates="dossier")

class DossierParties(Base):
    __tablename__ = "dossier_parties"

    dossier_id = Column(Integer, ForeignKey("dossiers.id"), primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), primary_key=True)
    role_dans_acte = Column(String, nullable=False)

    dossier = relationship("Dossier", back_populates="client_associations")
    client = relationship("Client", back_populates="dossier_associations")
