from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app import crud
from app.crud import user as crud_user
from app.utils.security import get_current_admin, get_current_user
from app.database import get_db
from app.schemas.user import User, UserOut
from app.utils.validators import validate_name, validate_cellnumber,validate_image_upload
from pydantic import EmailStr
from datetime import datetime
import os
from pathlib import Path
from fastapi.responses import JSONResponse

router = APIRouter()

UPLOAD_DIR = Path("static/profilepics")


@router.post("/users", response_model=User)
def create_user(
    name: str = Form(...),
    email: EmailStr = Form(...),
    cellnumber: str = Form(...),
    password: str = Form(...),
    roleId: int = Form(2),
    profilepic: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    db_user = crud_user.get_user_by_cellnumber(db, cellnumber=cellnumber)
    if db_user:
        raise HTTPException(status_code=400, detail="Cellnumber already registered")

    profilepic_url = None
    if profilepic:
        validate_image_upload(profilepic)

        folder = "static/profile_pics"
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, profilepic.filename)
        with open(filepath, "wb") as buffer:
            buffer.write(profilepic.file.read())
        profilepic_url = filepath

    new_user = crud.user.create_user(
        db=db,
        name=name,
        email=email,
        cellnumber=cellnumber,
        password=password,
        roleId=roleId,
        profilepic=profilepic_url,
    )
    return User.from_orm(new_user)


@router.get("/users/{user_id}", response_model=UserOut)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.roleId != 1 and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this user.",
        )

    return db_user


@router.patch("/users/{user_id}", response_model=User)
def update_user(
    user_id: int,
    name: Optional[str] = Form(None),
    email: Optional[EmailStr] = Form(None),
    cellnumber: Optional[str] = Form(None),
    profilepic: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    db_user = crud.user.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {}

    if name:
        validate_name(name)
        update_data["name"] = name
    if email:
        update_data["email"] = email
    if cellnumber:
        validate_cellnumber(cellnumber)
        update_data["cellnumber"] = cellnumber

    if profilepic:
        validate_image_upload(profilepic)
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        filename = f"{datetime.utcnow().timestamp()}_{profilepic.filename}"
        file_path = UPLOAD_DIR / filename

        with open(file_path, "wb") as f:
            f.write(profilepic.file.read())

        update_data["profilepic"] = f"static/profilepics/{filename}"

    return crud.user.update_user(db=db, user_id=user_id, user_data=update_data)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    crud.user.delete_user(db=db, user_id=user_id)

    return JSONResponse(
        status_code=200, content={"message": "User deleted successfully."}
    )


@router.get("/users", response_model=List[UserOut])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users
