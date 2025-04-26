import re
from fastapi import HTTPException

def validate_name(name: str):
    if not re.match(r"^[A-Za-z\s]+$", name):
        raise HTTPException(
            status_code=400,
            detail="Name must contain only letters and spaces."
        )
    if len(name.strip()) < 2:
        raise HTTPException(
            status_code=400,
            detail="Name must be at least 2 characters long."
        )
    return name

def validate_cellnumber(cellnumber: str):
    if not re.match(r"^\d{10}$", cellnumber):
        raise HTTPException(
            status_code=400,
            detail="Cell number must be exactly 10 digits."
        )
    return cellnumber
