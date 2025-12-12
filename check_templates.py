from src.database import get_db
from src.models.template import Template

db = next(get_db())
templates = db.query(Template).all()

if templates:
    print(f"[OK] Found {len(templates)} templates:")
    for t in templates:
        print(f"   - ID: {t.id}, Name: {t.nom}")
else:
    print("[ERROR] No templates found in database")
