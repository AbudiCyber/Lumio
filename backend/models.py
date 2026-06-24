"""Data models (SQLAlchemy).

Keep models simple and declarative here.
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(String)
    email = Column(String, unique=True)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    last_login = Column(String)

    def __repr__(self):
        return f"<User id={self.id} username={self.username!r}>"
