from sqlalchemy.orm import Session
from app.models.user import User
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.utils.validators import validate_password


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id, User.deletedAt.is_(None)).first()


def get_user_by_cellnumber(db: Session, cellnumber: str):
    return (
        db.query(User)
        .filter(User.cellnumber == cellnumber, User.deletedAt.is_(None))
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(User)
        .filter(User.roleId != 1, User.deletedAt.is_(None))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user(
    db: Session,
    name: str,
    email: str,
    cellnumber: str,
    password: str,
    roleId: int,
    profilepic: str = None,
):
    validate_password(password)

    from app.utils.security import get_password_hash

    hashed_password = get_password_hash(password)
    new_user = User(
        name=name,
        email=email,
        cellnumber=cellnumber,
        password=hashed_password,
        roleId=roleId,
        profilepic=profilepic,
        created=datetime.now(timezone.utc),
        modified=datetime.now(timezone.utc),
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        if "user.email" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered.",
            )
        elif "user.cellnumber" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cellnumber is already registered.",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate entry or database integrity error.",
            )


def update_user(db: Session, user_id: int, user_data: dict):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail="User not found or already deleted."
        )

    new_cell = user_data.get("cellnumber")
    if new_cell and new_cell != db_user.cellnumber:
        existing_user = (
            db.query(User)
            .filter(User.cellnumber == new_cell, User.deletedAt.is_(None))
            .first()
        )
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=400,
                detail="Cellnumber is already registered by another user.",
            )

    new_email = user_data.get("email")
    if new_email and new_email != db_user.email:
        existing_user = (
            db.query(User)
            .filter(User.email == new_email, User.deletedAt.is_(None))
            .first()
        )
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=400,
                detail="Email is already registered by another user.",
            )

    for key, value in user_data.items():
        setattr(db_user, key, value)

    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Update failed: cellnumber or email already exists."
        )

    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail="User not found or already deleted."
        )

    db_user.deletedAt = datetime.now(timezone.utc)
    db.commit()
    return db_user
