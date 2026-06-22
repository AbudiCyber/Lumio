"""Data models (SQLAlchemy).

Keep models simple and declarative here.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User id={self.id} username={self.username!r}>"
