from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    NOTAIRE = "NOTAIRE"
    CLERC = "CLERC"
    COMPTABLE = "COMPTABLE"
    ADMIN = "ADMIN"
    SECRETAIRE = "SECRETAIRE"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # Using String to store Enum value
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    dossiers = relationship("Dossier", back_populates="responsable")
