"""
Test script for Phase 3 - Act Creation
This script tests the act creation functionality by directly calling the backend logic
"""
from src.database import SessionLocal
from src.models.acte import Acte
from src.models.dossier import Dossier
from src.models.template import Template
from src.utils.template_engine import TemplateEngine

def test_acte_creation():
    """Test creating an act with a template"""
    session = SessionLocal()
    try:
        # Step 1: Get a dossier
        dossier = session.query(Dossier).first()
        if not dossier:
            print("[ERROR] No dossier found in database")
            return False
        
        print(f"[OK] Using dossier: {dossier.numero_dossier} - {dossier.intitule}")
        
        # Step 2: Get a template
        template = session.query(Template).filter(Template.nom == "Procuration Générale").first()
        if not template:
            print("[ERROR] Template 'Procuration Générale' not found")
            return False
        
        print(f"[OK] Using template: {template.nom}")
        
        # Step 3: Generate content from template
        ctx = TemplateEngine.get_dossier_context(dossier)
        contenu = TemplateEngine.merge(template.contenu, ctx)
        
        print(f"[OK] Generated content ({len(contenu)} characters)")
        print(f"     Preview: {contenu[:100]}...")
        
        # Step 4: Create the acte
        acte = Acte(
            dossier_id=dossier.id,
            template_id=template.id,
            titre=f"Ma Procuration Test - {dossier.numero_dossier}",
            contenu=contenu,
            statut="FINALISE"
        )
        session.add(acte)
        session.commit()
        
        print(f"[OK] Acte created successfully!")
        print(f"     ID: {acte.id}")
        print(f"     Titre: {acte.titre}")
        print(f"     Statut: {acte.statut}")
        print(f"     Created at: {acte.created_at}")
        
        # Step 5: Verify the acte was saved
        saved_acte = session.query(Acte).filter(Acte.id == acte.id).first()
        if saved_acte:
            print(f"[OK] Acte verified in database")
            print(f"     Dossier: {saved_acte.dossier.numero_dossier}")
            print(f"     Template: {saved_acte.template.nom}")
            return True
        else:
            print("[ERROR] Acte not found after save")
            return False
            
    except Exception as e:
        print(f"[ERROR] Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        session.rollback()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    print("="*60)
    print("Phase 3 - Act Creation Test")
    print("="*60)
    
    success = test_acte_creation()
    
    print("="*60)
    if success:
        print("[SUCCESS] Phase 3 test completed successfully!")
    else:
        print("[FAILED] Phase 3 test failed")
    print("="*60)
