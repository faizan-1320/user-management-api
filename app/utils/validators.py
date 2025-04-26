import re
from fastapi import HTTPException, UploadFile
import imghdr


def validate_name(name: str):
    if not re.match(r"^[A-Za-z\s]+$", name):
        raise HTTPException(
            status_code=400, detail="Name must contain only letters and spaces."
        )
    if len(name.strip()) < 2:
        raise HTTPException(
            status_code=400, detail="Name must be at least 2 characters long."
        )
    return name


def validate_cellnumber(cellnumber: str):
    if not re.match(r"^\d{10}$", cellnumber):
        raise HTTPException(
            status_code=400, detail="Cell number must be exactly 10 digits."
        )
    return cellnumber


def validate_image_upload(file: UploadFile):
    valid_types = ["jpeg", "png", "jpg"]

    content = file.file.read()
    file.file.seek(0)

    file_type = imghdr.what(None, h=content)
    if file_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image format. Allowed formats: {', '.join(valid_types)}",
        )
