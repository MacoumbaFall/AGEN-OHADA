"""
Check if the migration was applied correctly
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

def check_columns():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        print("Checking dossiers table columns...")
        
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'dossiers'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\nColumns in 'dossiers' table:")
        for col_name, col_type in columns:
            print(f"  - {col_name}: {col_type}")
        
        # Check for specific columns
        column_names = [col[0] for col in columns]
        required_columns = ['montant_acte', 'emoluments', 'debours', 'description']
        
        print("\nRequired financial columns:")
        for col in required_columns:
            status = "YES" if col in column_names else "NO"
            print(f"  {status} {col}")
        
        # Check for other tables
        print("\nChecking for Phase 2 tables...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('dossier_historique', 'documents');
        """)
        
        tables = cursor.fetchall()
        print("Phase 2 tables found:")
        for table in tables:
            print(f"  + {table[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_columns()
