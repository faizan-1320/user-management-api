from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.token import AccessToken


def create_token(db: Session, user_id: int, token: str, ttl: int):
    """
    Store a new access token in the database
    Args:
        db: Database session
        user_id: ID of the user the token belongs to
        token: The JWT token string
        ttl: Time-to-live in milliseconds
    Returns:
        The created AccessToken record
    """
    db_token = AccessToken(
        token=token, ttl=ttl, userId=user_id, created=datetime.utcnow()
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token
