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
            raise HTTPException(
                status_code=400, detail="Name must contain only letters and spaces."
            )
        if len(name) < 2:
            raise HTTPException(
                status_code=400, detail="Name must be at least 2 characters long."
            )
        return name

    @validator("cellnumber")
    def validate_cellnumber(cellnumber: str):
        if not re.match(r"^\d{10}$", cellnumber):
            raise HTTPException(
                status_code=400, detail="Cell number must be exactly 10 digits."
            )
        return cellnumber


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    cellnumber: Optional[str] = None
    profilepic: Optional[str]

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    profilepic: Optional[str] = None
    created: datetime
    modified: datetime

    class Config:
        orm_mode = True
