# app/database.py
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

logger = logging.getLogger(__name__)

# --- Verbindungs-URL ---
# Format: postgresql://user:password@host:port/database
DATABASE_URL = "postgresql://nexus:nexus_password@localhost:5432/nexus_db"

# --- Engine erstellen ---
# Die Engine verwaltet den Connection Pool
engine = create_engine(
    DATABASE_URL,
    pool_size=5,          # 5 permanente Verbindungen
    max_overflow=10,      # bis zu 10 zusätzliche bei Spitzenlast
    pool_pre_ping=True,   # prüfe ob Verbindung noch lebt vor Nutzung
    echo=False,           # True = SQL-Abfragen in Terminal ausgeben (für Debugging)
)

# --- Session Factory ---
# Eine Session = eine Transaktion
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,   # wir commiten manuell
    autoflush=False,
)

# --- Base für ORM-Modelle ---
class Base(DeclarativeBase):
    pass


def get_db():
    """
    Dependency für FastAPI.
    Gibt eine Session aus dem Pool und gibt sie danach zurück.
    """
    db = SessionLocal()
    try:
        yield db          # FastAPI benutzt die Session
    finally:
        db.close()        # immer schließen – auch bei Fehler


def check_connection():
    """Prüft ob die Datenbank erreichbar ist."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Datenbankverbindung erfolgreich")
        return True
    except Exception as e:
        logger.error(f"Datenbankverbindung fehlgeschlagen: {e}")
        return False