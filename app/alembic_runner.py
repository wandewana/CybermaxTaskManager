import os
from alembic import command
from alembic.config import Config

def run_migrations():
    try:
        print("[Alembic] Starting database migration...")
        alembic_ini_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'alembic.ini')
        alembic_cfg = Config(alembic_ini_path)
        command.upgrade(alembic_cfg, 'head')
        print("[Alembic] Migration completed successfully.")
    except Exception as e:
        print(f"[Alembic] Migration failed: {e}")
        raise
