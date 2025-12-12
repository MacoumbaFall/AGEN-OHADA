from src.database import SessionLocal
from sqlalchemy import inspect

db = SessionLocal()
try:
    inspector = inspect(db.bind)
    cols = inspector.get_columns('actes')
    print('Columns in actes table:')
    for c in cols:
        print(f"  {c['name']}: {c['type']}")
finally:
    db.close()
