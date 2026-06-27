"""Conversation model (SQLAlchemy)."""

from sqlalchemy import Column, Integer, String
from .models import Base

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(String)
    updated_at = Column(String)

    def __repr__(self):
        return f"<Conversation id={self.id} title={self.title!r} user_id={self.user_id}>"
