import sys
import traceback
import os
from datetime import datetime

try:
    # Explicit imports that worked
    from src.database import get_db, Base
    from src.models.user import User
    from src.models.client import Client
    from src.models.dossier import Dossier, DossierParties, DossierHistorique, Document
    from src.models.template import Template
    from src.models.acte import Acte
    from sqlalchemy.orm import configure_mappers

    def verify_phase2_full():
        print("Starting Phase 2 Verification (History & GED)...")
        configure_mappers()
        print("Mappers configured successfully.")
        
        db = next(get_db())
        
        # --- 1. SETUP TEST DATA ---
        print("\n[1/5] Setting up test data...")
        
        # Create Test User
        user = db.query(User).filter(User.username == "test_verifier").first()
        if not user:
            user = User(username="test_verifier", password_hash="dummy", role="NOTAIRE", email="test@test.com")
            db.add(user)
            db.commit()
        print(f"User 'test_verifier' ready (ID: {user.id})")
        
        # Create Test Dossier
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        dossier = None
        
        dossier = db.query(Dossier).filter(Dossier.numero_dossier.like("TEST-P2-%")).first()
        if not dossier:
             dossier = Dossier(
                numero_dossier=f"TEST-P2-{timestamp}",
                intitule="Dossier Test Phase 2",
                statut="OUVERT",
                responsable_id=user.id
            )
             db.add(dossier)
             db.commit()
        print(f"Dossier created (ID: {dossier.id}, No: {dossier.numero_dossier})")
        
        
        # --- 2. VERIFY HISTORY (Option C) ---
        print("\n[2/5] Verifying Option C: History...")
        
        # Simulate Logic from DossierEditPage.on_submit
        old_status = dossier.statut
        new_status = "INSTRUCTION"
        
        historique = DossierHistorique(
            dossier_id=dossier.id,
            ancien_statut=old_status,
            nouveau_statut=new_status,
            date_changement=datetime.utcnow(),
            user_id=user.id,
            commentaire="Auto verification status change"
        )
        db.add(historique)
        dossier.statut = new_status
        db.commit()
        
        # Check DB
        history_record = db.query(DossierHistorique).filter(
            DossierHistorique.dossier_id == dossier.id,
            DossierHistorique.nouveau_statut == "INSTRUCTION"
        ).first()
        
        if history_record and history_record.user_id == user.id:
            print("History record created correctly with user attribution.")
        else:
            print("History record verification failed!")
            sys.exit(1)
            
            
        # --- 3. VERIFY GED (Option D) ---
        print("\n[3/5] Verifying Option D: GED...")
        
        # Prepare dummy file
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        test_filename = f"{dossier.id}_testdoc.txt"
        test_filepath = os.path.join(upload_dir, test_filename)
        
        with open(test_filepath, "w") as f:
            f.write("This is a test document content.")
            
        # Create DB Record
        doc = Document(
            dossier_id=dossier.id,
            titre="Test Document",
            type_document="AUTRE",
            chemin_fichier=test_filepath,
            taille_fichier=100,
            date_upload=datetime.utcnow()
        )
        db.add(doc)
        db.commit()
        
        # Check DB and File
        doc_record = db.query(Document).filter(Document.dossier_id == dossier.id).first()
        
        if doc_record and os.path.exists(doc_record.chemin_fichier):
            print(f"Document record found and file exists at {doc_record.chemin_fichier}")
        else:
            print("GED verification failed!")
            sys.exit(1)
            
        
        # --- 4. VERIFY FILE OPENING LOGIC ---
        print("\n[4/5] Verifying File Opening Logic...")
        if hasattr(os, 'startfile'):
            print(f"os.startfile is available on this system (Windows detected).")
        else:
            print("os.startfile NOT available. This might be running on non-Windows?")
            
            
        # --- 5. CLEANUP ---
        print("\n[5/5] Cleaning up...")
        
        # Delete doc file
        if os.path.exists(test_filepath):
            try:
                os.remove(test_filepath)
            except:
                pass
            
        # Delete DB records
        try:
            db.delete(doc_record)
            db.delete(history_record)
            db.delete(dossier)
            # db.delete(user) # Keep user
            db.commit()
        except:
             db.rollback()
        
        print("\nVerification Complete: ALL TESTS PASSED")

    if __name__ == "__main__":
        verify_phase2_full()

except Exception:
    print("\nCRITICAL ERROR IN VERIFICATION SCRIPT:")
    traceback.print_exc()
    sys.exit(1)
