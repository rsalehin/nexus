# app/db_models.py
from datetime import datetime
from sqlalchemy import String, Text, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class UserDB(Base):
    __tablename__ = "users"

    id:         Mapped[int]      = mapped_column(Integer, primary_key=True)
    username:   Mapped[str]      = mapped_column(String(20), nullable=False, unique=True)
    email:      Mapped[str]      = mapped_column(String(255), nullable=False, unique=True)
    password:   Mapped[str]      = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relation: Ein User hat viele Dokumente
    documents: Mapped[list["DocumentDB"]] = relationship(back_populates="owner")

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"


class DocumentDB(Base):
    __tablename__ = "documents"

    id:         Mapped[int]      = mapped_column(Integer, primary_key=True)
    title:      Mapped[str]      = mapped_column(String(200), nullable=False)
    content:    Mapped[str]      = mapped_column(Text, nullable=False)
    is_public:  Mapped[bool]     = mapped_column(Boolean, default=False)
    owner_id:   Mapped[int]      = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relation: Ein Dokument gehört einem User
    owner: Mapped["UserDB"] = relationship(back_populates="documents")

    def __repr__(self):
        return f"<Document id={self.id} title={self.title}>"