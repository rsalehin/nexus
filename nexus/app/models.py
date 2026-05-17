# app/models.py  (erweitert)
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: Optional[int] = None

    @field_validator("username")
    @classmethod
    def username_must_be_valid(cls, value: str) -> str:
        """Benutzername: 3-20 Zeichen, nur Buchstaben/Zahlen/Unterstrich."""
        value = value.strip()
        if len(value) < 3:
            raise ValueError("Benutzername muss mindestens 3 Zeichen haben")
        if len(value) > 20:
            raise ValueError("Benutzername darf maximal 20 Zeichen haben")
        if not value.replace("_", "").isalnum():
            raise ValueError("Benutzername darf nur Buchstaben, Zahlen und _ enthalten")
        return value.lower()   # immer klein speichern

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Passwort muss mindestens 8 Zeichen haben")
        return value

    @field_validator("age")
    @classmethod
    def age_must_be_realistic(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and (value < 0 or value > 150):
            raise ValueError("Alter muss zwischen 0 und 150 liegen")
        return value


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime


class DocumentCreate(BaseModel):
    title: str
    content: str
    is_public: bool = False

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Titel darf nicht leer sein")
        if len(value) > 200:
            raise ValueError("Titel darf maximal 200 Zeichen haben")
        return value


class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    is_public: bool
    owner_id: int
    created_at: datetime
    word_count: int