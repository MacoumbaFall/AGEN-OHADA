from src.database import SessionLocal
from src.models.user import User
from src.auth import get_password_hash
import sys

# Set encoding to utf-8 for console output if possible, though writing to file is safer if we want to avoid issues.
# But here we will just avoid fancy characters.

def reset_admin():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "admin").first()
        if user:
            print("User admin found. Resetting password...")
            user.password_hash = get_password_hash("admin123")
            db.commit()
            print("Password reset to 'admin123'.")
        else:
            print("User admin NOT found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin()
