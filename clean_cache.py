import shutil
import os
import pathlib

def clean_rio_cache():
    # Chemin vers le cache Rio
    # C:\Users\macou\AppData\Local\Cache\rio
    user_home = pathlib.Path.home()
    cache_dir = user_home / "AppData" / "Local" / "Cache" / "rio"
    
    print(f"🔍 Recherche du cache Rio dans : {cache_dir}")
    
    if cache_dir.exists():
        try:
            print("🧹 Suppression du cache en cours...")
            shutil.rmtree(cache_dir)
            print("✅ Cache supprimé avec succès !")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression du cache : {e}")
            # Tentative de renommage si la suppression échoue (souvent dû aux verrous fichiers)
            try:
                backup_name = cache_dir.with_name(f"rio_backup_{os.getpid()}")
                os.rename(cache_dir, backup_name)
                print(f"⚠️  Impossible de supprimer, dossier renommé en : {backup_name}")
            except Exception as rename_error:
                print(f"❌ Impossible de renommer le dossier : {rename_error}")
    else:
        print("ℹ️  Aucun dossier de cache Rio trouvé.")

if __name__ == "__main__":
    clean_rio_cache()
