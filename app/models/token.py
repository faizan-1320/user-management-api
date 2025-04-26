# app/models/token.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from app.database import Base

class AccessToken(Base):
    __tablename__ = "accesstoken"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False)
    ttl = Column(Integer, nullable=False)  # in milliseconds
    userId = Column(Integer, ForeignKey('user.id'), nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationship to User
    user = relationship("User", back_populates="tokens")