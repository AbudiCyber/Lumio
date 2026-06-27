"""Message model (SQLAlchemy)."""

from sqlalchemy import Column, Integer, String, ForeignKey
from .models import Base

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(String)

    def __repr__(self):
        return f"<Message id={self.id} conversation_id={self.conversation_id} role={self.role!r}>"
