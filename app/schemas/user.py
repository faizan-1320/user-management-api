import re
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: str
    cellnumber: str
    profilepic: Optional[str]

    @validator("name")
    def validate_name(name: str):
        if not re.match(r"^[A-Za-z\s]+$", name):
            raise HTTPException(status_code=400, detail="Name must contain only letters and spaces.")
        if len(name) < 2:
            raise HTTPException(status_code=400, detail="Name must be at least 2 characters long.")
        return name

    @validator("cellnumber")
    def validate_cellnumber(cellnumber: str):
        if not re.match(r"^\d{10}$", cellnumber):
            raise HTTPException(status_code=400, detail="Cell number must be exactly 10 digits.")
        return cellnumber


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    cellnumber: Optional[str] = None
    profilepic: Optional[str]

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    roleId: Optional[int] = 2

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        return value


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    cellnumber: Optional[str] = None
    profilepic: Optional[str] = None


class User(UserBase):
    id: int
    profilepic: Optional[str] = None
    created: datetime
    modified: datetime

    class Config:
        orm_mode = True
