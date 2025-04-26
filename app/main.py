from fastapi import FastAPI
from app.routes import users, auth
from app.database import engine, Base
from app.models.role import Role
from app.database import SessionLocal

app = FastAPI()

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize default roles
db = SessionLocal()
try:
    if not db.query(Role).filter(Role.id == 1).first():
        admin_role = Role(id=1, name="Admin", description="Administrator role")
        db.add(admin_role)
        db.commit()

    if not db.query(Role).filter(Role.id == 2).first():
        user_role = Role(id=2, name="User", description="Normal user role")
        db.add(user_role)
        db.commit()
finally:
    db.close()

# Include routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(users.router, prefix="/api", tags=["users"])

