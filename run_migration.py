"""
Migration script to add Phase 2 database changes
Runs the SQL migration for financial columns, status history, and documents
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "agen_ohada_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Dcadmin01")

def run_migration():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("🔄 Running Phase 2 migration...")
        
        # Read the migration SQL file
        with open('migrations/phase2_migration.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Execute the migration
        cursor.execute(sql_script)
        
        print("✅ Phase 2 migration completed successfully!")
        print("   - Added financial columns to dossiers table")
        print("   - Created dossier_historique table")
        print("   - Created documents table")
        print("   - Created indexes")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    run_migration()
