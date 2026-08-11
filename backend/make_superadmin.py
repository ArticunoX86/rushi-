from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user import User

def make_superadmin(email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email.ilike(email)).first()
        if not user:
            print(f"User with email {email} not found.")
            return
        
        user.is_superadmin = True
        db.commit()
        print(f"Successfully upgraded {email} to Super Admin!")
    finally:
        db.close()

if __name__ == "__main__":
    email = input("Enter the email of the user to upgrade to Super Admin: ")
    make_superadmin(email)
