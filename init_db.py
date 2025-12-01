"""
Script d'initialisation de la base de données PostgreSQL
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

def create_database():
    """Crée la base de données si elle n'existe pas"""
    try:
        # Connexion au serveur PostgreSQL (base postgres par défaut)
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Vérifier si la base existe
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_NAME,)
        )
        exists = cursor.fetchone()
        
        if not exists:
            # Créer la base de données
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(DB_NAME)
                )
            )
            print(f"✅ Base de données '{DB_NAME}' créée avec succès!")
        else:
            print(f"ℹ️  La base de données '{DB_NAME}' existe déjà.")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Erreur lors de la création de la base de données:")
        print(f"   {e}")
        return False

def execute_schema():
    """Exécute le fichier schema.sql"""
    try:
        # Connexion à la base de données créée
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Lire et exécuter le fichier schema.sql
        with open('schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        cursor.execute(schema_sql)
        conn.commit()
        
        print("✅ Schéma de base de données créé avec succès!")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Erreur lors de l'exécution du schéma:")
        print(f"   {e}")
        return False
    except FileNotFoundError:
        print("❌ Fichier schema.sql introuvable!")
        return False

if __name__ == "__main__":
    print("🚀 Initialisation de la base de données AGEN-OHADA\n")
    
    # Étape 1: Créer la base de données
    if create_database():
        # Étape 2: Exécuter le schéma
        if execute_schema():
            print("\n✅ Initialisation terminée avec succès!")
        else:
            print("\n⚠️  La base existe mais le schéma n'a pas pu être créé.")
    else:
        print("\n❌ Échec de l'initialisation.")
