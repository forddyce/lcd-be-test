from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    """
    model for the 'users' table.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Unique identifier for the user.")
    email = Column(String(255), unique=True, index=True, nullable=False, comment="User's unique email address.")
    hashed_password = Column(String(255), nullable=False, comment="Hashed password for security.")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Timestamp when the user account was created.")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="Timestamp of the last update to the user account.")

    def __repr__(self):
        """
        string of the user object, for debug purposes
        """
        return f"<User(id={self.id}, email='{self.email}')>"
    
"""
posts will be stored in memory so I skip that
"""