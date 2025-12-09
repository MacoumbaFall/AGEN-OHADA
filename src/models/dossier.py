from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Numeric, Text
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
    
    # Financial fields
    montant_acte = Column(Numeric(15, 2), nullable=True)
    emoluments = Column(Numeric(15, 2), nullable=True)
    debours = Column(Numeric(15, 2), nullable=True)
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    responsable = relationship("User", back_populates="dossiers")
    parties_associations = relationship("DossierParties", back_populates="dossier")
    historique = relationship("DossierHistorique", back_populates="dossier", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="dossier", cascade="all, delete-orphan")
    actes = relationship("Acte", back_populates="dossier", cascade="all, delete-orphan")


class DossierParties(Base):
    __tablename__ = "dossier_parties"

    dossier_id = Column(Integer, ForeignKey("dossiers.id"), primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), primary_key=True)
    role_dans_acte = Column(String, nullable=False)

    dossier = relationship("Dossier", back_populates="parties_associations")
    client = relationship("Client", back_populates="dossier_associations")


class DossierHistorique(Base):
    __tablename__ = "dossier_historique"

    id = Column(Integer, primary_key=True, index=True)
    dossier_id = Column(Integer, ForeignKey("dossiers.id"), nullable=False)
    ancien_statut = Column(String, nullable=True)
    nouveau_statut = Column(String, nullable=False)
    date_changement = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    commentaire = Column(Text, nullable=True)

    dossier = relationship("Dossier", back_populates="historique")
    user = relationship("User")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    dossier_id = Column(Integer, ForeignKey("dossiers.id"), nullable=False)
    titre = Column(String, nullable=False)
    type_document = Column(String, nullable=False)
    chemin_fichier = Column(String, nullable=False)
    date_upload = Column(DateTime, default=datetime.utcnow)
    taille_fichier = Column(Integer, nullable=True)

    dossier = relationship("Dossier", back_populates="documents")
