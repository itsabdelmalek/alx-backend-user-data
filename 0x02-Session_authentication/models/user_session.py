#!/usr/bin/env python3
"""
Module for UserSession model
"""
from models.base import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class UserSession(BaseModel, Base):
    """
    UserSession class
    """
    __tablename__ = 'user_sessions'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    session_id = Column(String(60), nullable=False)

    user = relationship("User", back_populates="sessions")
