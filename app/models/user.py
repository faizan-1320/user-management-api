from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    profilepic = Column(String(255), nullable=True)
    name = Column(String(100), nullable=False)
    cellnumber = Column(String(20), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    deletedAt = Column(DateTime, nullable=True)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    modified = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    roleId = Column(Integer, ForeignKey('role.id'), default=2)  # 1=Admin, 2=Normal User

    tokens = relationship("AccessToken", back_populates="user")
