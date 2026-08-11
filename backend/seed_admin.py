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
        
        # Check if admin already exists
        admin_email = "admin@example.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        
        if existing_admin:
            print(f"Admin user {admin_email} already exists.")
            return

        print("Creating admin user...")
        admin_user = User(
            first_name="System",
            last_name="Admin",
            email=admin_email,
            phone="+1234567890",
            password_hash=hash_password("admin123"),
            role_id=role.id,
            is_active=True,
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully!")
    except Exception as e:
        print(f"Error seeding admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
