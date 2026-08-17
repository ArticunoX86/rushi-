import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.core.security import hash_password

def seed():
    db = SessionLocal()
    try:
        # Create System Administrator Role if it doesn't exist
        role = db.query(Role).filter(Role.name == "System Administrator").first()
        if not role:
            print("Creating System Administrator role...")
            role = Role(
                name="System Administrator",
                description="Has full access to all features and settings.",
                permissions=["manage_users", "manage_roles", "view_dashboard", "manage_properties", "manage_leads", "manage_calls", "manage_agents", "view_logs"]
            )
            db.add(role)
            db.commit()
            db.refresh(role)
        
        email = "umesh@gmail.com"
        existing = db.query(User).filter(User.email == email).first()
        
        if existing:
            print(f"User {email} already exists. Updating password and permissions...")
            existing.password_hash = hash_password("Umesh123")
            existing.is_superadmin = True
            existing.role_id = role.id
            db.commit()
            print("User updated!")
            return

        print("Creating user...")
        new_user = User(
            first_name="Umesh",
            last_name="",
            email=email,
            phone="+919876543210",
            password_hash=hash_password("Umesh123"),
            role_id=role.id,
            is_active=True,
            is_superadmin=True
        )
        db.add(new_user)
        db.commit()
        print("User umesh@gmail.com created successfully!")
    except Exception as e:
        print(f"Error seeding user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
