"""
Script pour réinitialiser complètement la base de données
"""
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Paramètres de connexion
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "Dcadmin01"
DB_NAME = "agen_ohada_db"

def reset_database():
    """Supprime et recrée toutes les tables"""
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        print("🗑️  Suppression des tables existantes...")
        
        # Supprimer toutes les tables dans le bon ordre (contraintes FK)
        drop_tables = """
        DROP TABLE IF EXISTS compta_mouvements CASCADE;
        DROP TABLE IF EXISTS compta_ecritures CASCADE;
        DROP TABLE IF EXISTS compta_comptes CASCADE;
        DROP TABLE IF EXISTS formalites CASCADE;
        DROP TABLE IF EXISTS actes CASCADE;
        DROP TABLE IF EXISTS dossier_parties CASCADE;
        DROP TABLE IF EXISTS dossiers CASCADE;
        DROP TABLE IF EXISTS clients CASCADE;
        DROP TABLE IF EXISTS users CASCADE;
        """
        
        cursor.execute(drop_tables)
        conn.commit()
        print("✅ Tables supprimées avec succès!")
        
        # Lire et exécuter le fichier schema.sql
        print("📝 Création des nouvelles tables...")
        with open('schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        cursor.execute(schema_sql)
        conn.commit()
        
        print("✅ Schéma de base de données créé avec succès!")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Erreur lors de la réinitialisation:")
        print(f"   {e}")
        return False
    except FileNotFoundError:
        print("❌ Fichier schema.sql introuvable!")
        return False

if __name__ == "__main__":
    print("🚀 Réinitialisation de la base de données AGEN-OHADA\n")
    print("⚠️  ATTENTION: Cette opération va SUPPRIMER toutes les données!\n")
    
    if reset_database():
        print("\n✅ Réinitialisation terminée avec succès!")
    else:
        print("\n❌ Échec de la réinitialisation.")
