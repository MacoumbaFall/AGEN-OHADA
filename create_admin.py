from src.database import SessionLocal
from src.models.user import User, UserRole
from src.auth import get_password_hash

def create_admin_user():
    db = SessionLocal()
    try:
        # Vérifier si l'utilisateur admin existe déjà
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("ℹ️  L'utilisateur 'admin' existe déjà.")
            return

        # Créer l'utilisateur admin
        admin_user = User(
            username="admin",
            email="admin@agen-ohada.local",
            password_hash=get_password_hash("admin123"), # Mot de passe par défaut
            role=UserRole.ADMIN
        )
        db.add(admin_user)
        db.commit()
        print("✅ Utilisateur 'admin' créé avec succès (Mot de passe: admin123)")
    
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
