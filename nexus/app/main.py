# app/main.py
from fastapi import FastAPI

app = FastAPI(title="Nexus", version="0.1.0")


@app.get("/")
def root():
    return {"message": "Willkommen bei Nexus", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}