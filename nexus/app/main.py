# app/main.py
import time
import logging
from datetime import datetime
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db, check_connection
from app.db_models import UserDB, DocumentDB
from app.models import UserCreate, UserResponse, DocumentCreate, DocumentResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Nexus", version="0.1.0")


@app.on_event("startup")
def startup():
    """Wird einmal beim Start ausgeführt."""
    check_connection()


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    logger.info(f"→ {request.method} {request.url.path}")
    response: Response = await call_next(request)
    elapsed = (time.perf_counter() - start) * 1000
    logger.info(f"← {response.status_code} | {elapsed:.2f}ms")
    return response


@app.get("/health")
def health(db: Session = Depends(get_db)):
    """Health Check prüft auch die Datenbankverbindung."""
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        raise HTTPException(status_code=503, detail="Datenbank nicht erreichbar")


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Prüfen ob Username oder Email schon existieren
    existing = db.query(UserDB).filter(
        (UserDB.username == user.username) | (UserDB.email == user.email)
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Username oder Email bereits vergeben")

    # Neuen User in DB speichern
    # Hinweis: Passwort wird hier noch als Klartext gespeichert
    # Hashing kommt in Phase 4 (Auth)
    db_user = UserDB(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)   # id und created_at von DB laden

    logger.info(f"Neuer User erstellt: {db_user.username} (id={db_user.id})")
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        created_at=db_user.created_at,
    )


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User nicht gefunden")

    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        created_at=db_user.created_at,
    )


@app.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    # Erstmal hardcoded owner_id=1 – Auth kommt in Phase 4
    db_doc = DocumentDB(
        title=doc.title,
        content=doc.content,
        is_public=doc.is_public,
        owner_id=1,
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    logger.info(f"Neues Dokument: '{db_doc.title}' (id={db_doc.id})")
    return DocumentResponse(
        id=db_doc.id,
        title=db_doc.title,
        content=db_doc.content,
        is_public=db_doc.is_public,
        owner_id=db_doc.owner_id,
        created_at=db_doc.created_at,
        word_count=len(db_doc.content.split()),
    )