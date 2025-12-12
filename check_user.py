from src.database import get_db
from src.models.user import User
from src.auth import verify_password

db = next(get_db())
user = db.query(User).filter(User.username == "admin").first()

if user:
    print(f"[OK] User 'admin' exists")
    print(f"   ID: {user.id}")
    print(f"   Username: {user.username}")
    print(f"   Email: {user.email}")
    
    # Test password verification
    if verify_password("admin123", user.password_hash):
        print("[OK] Password 'admin123' is correct")
    else:
        print("[ERROR] Password 'admin123' is incorrect")
else:
    print("[ERROR] User 'admin' does not exist")
