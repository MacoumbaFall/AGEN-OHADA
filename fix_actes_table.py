from src.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()
try:
    # Drop the old actes table
    print("Dropping old actes table...")
    db.execute(text("DROP TABLE IF EXISTS actes CASCADE"))
    db.commit()
    print("OK - Old actes table dropped")
    
    # Recreate with correct structure
    print("Creating new actes table...")
    db.execute(text("""
        CREATE TABLE actes (
            id SERIAL PRIMARY KEY,
            dossier_id INTEGER NOT NULL REFERENCES dossiers(id) ON DELETE CASCADE,
            template_id INTEGER REFERENCES templates(id),
            titre VARCHAR(255) NOT NULL,
            contenu TEXT,
            statut VARCHAR(50) DEFAULT 'BROUILLON',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
    """))
    db.commit()
    print("OK - New actes table created successfully")
    
except Exception as e:
    print(f"ERROR: {e}")
    db.rollback()
finally:
    db.close()

