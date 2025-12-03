from src.database import get_db, engine
from src.models.dossier import Dossier, DossierHistorique, DossierParties
from src.models.client import Client
from src.models.user import User
from sqlalchemy.orm import configure_mappers
from datetime import datetime
import sys

configure_mappers()

def verify_history():
    db = next(get_db())
    
    # 1. Create a test dossier
    print("Creating test dossier...")
    dossier = Dossier(
        numero_dossier=f"TEST-{datetime.now().timestamp()}",
        intitule="Test History Dossier",
        statut="OUVERT"
    )
    db.add(dossier)
    db.commit()
    db.refresh(dossier)
    print(f"Dossier created with ID: {dossier.id}, Status: {dossier.statut}")
    
    # 2. Simulate status change (logic from dossier_edit.py)
    print("Simulating status change to INSTRUCTION...")
    new_status = "INSTRUCTION"
    
    if dossier.statut != new_status:
        historique = DossierHistorique(
            dossier_id=dossier.id,
            ancien_statut=dossier.statut,
            nouveau_statut=new_status,
            date_changement=datetime.utcnow(),
            commentaire="Test status change"
        )
        db.add(historique)
        dossier.statut = new_status
        db.commit()
        
    print(f"Dossier status updated to: {dossier.statut}")
    
    # 3. Verify history record
    print("Verifying history record...")
    history = db.query(DossierHistorique).filter(
        DossierHistorique.dossier_id == dossier.id
    ).first()
    
    if history:
        print(f"✅ History record found!")
        print(f"   Old: {history.ancien_statut}")
        print(f"   New: {history.nouveau_statut}")
        print(f"   Date: {history.date_changement}")
        print(f"   Comment: {history.commentaire}")
        
        if history.ancien_statut == "OUVERT" and history.nouveau_statut == "INSTRUCTION":
            print("✅ Status transition correct.")
        else:
            print("❌ Status transition incorrect.")
            sys.exit(1)
    else:
        print("❌ No history record found.")
        sys.exit(1)
        
    # Cleanup
    print("Cleaning up...")
    db.delete(history)
    db.delete(dossier)
    db.commit()
    print("Cleanup done.")

if __name__ == "__main__":
    verify_history()
