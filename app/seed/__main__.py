"""CLI entrypoint: python -m app.seed"""

from app.database import SessionLocal
from app.models import *  # noqa: F401,F403 — ensure all models are loaded
from app.seed.seed_data import seed_database

if __name__ == "__main__":
    print("🌱 Seeding Philo Coffee Shop database...")
    db = SessionLocal()
    try:
        seed_database(db)
        print("✅ Seeding complete!")
    except Exception as exc:
        db.rollback()
        print(f"❌ Seeding failed: {exc}")
        raise
    finally:
        db.close()
