from app.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.utils.security import get_password_hash


def create_admin():
    db = SessionLocal()
    try:
        admin_role = db.query(Role).filter(Role.id == 1).first()
        if not admin_role:
            admin_role = Role(id=1, name="Admin", description="Administrator role")
            db.add(admin_role)
            db.commit()
        admin_user = db.query(User).filter(User.roleId == 1).first()
        if admin_user:
            print("Admin user already exists!")
            return

        admin_user = User(
            name="Admin",
            email="admin@example.com",
            cellnumber="1234567890",
            password=get_password_hash("admin123"),
            roleId=1,
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error creating admin user: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
