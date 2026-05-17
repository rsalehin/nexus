# app/main.py
import time
import logging
from datetime import datetime
from fastapi import FastAPI, Request, Response, HTTPException
from app.models import UserCreate, UserResponse, DocumentCreate, DocumentResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Nexus", version="0.1.0")


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    logger.info(f"→ {request.method} {request.url.path}")
    response: Response = await call_next(request)
    elapsed = (time.perf_counter() - start) * 1000
    logger.info(f"← {response.status_code} | {elapsed:.2f}ms")
    return response


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    """
    FastAPI liest den Request-Body und gibt ihn an Pydantic.
    Pydantic validiert. Wenn ok → user ist ein sauberes Python-Objekt.
    """
    logger.info(f"Neuer User: {user.username} ({user.email})")

    # Simulierte Antwort (ohne DB noch)
    # Wichtig: Passwort kommt NICHT in UserResponse zurück
    return UserResponse(
        id=1,
        username=user.username,
        email=user.email,
        created_at=datetime.now(),
    )


@app.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document(doc: DocumentCreate):
    word_count = len(doc.content.split())
    logger.info(f"Neues Dokument: '{doc.title}' ({word_count} Wörter)")

    return DocumentResponse(
        id=1,
        title=doc.title,
        content=doc.content,
        is_public=doc.is_public,
        owner_id=1,
        created_at=datetime.now(),
        word_count=word_count,
    )