from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_id(
    db: Session,
    user_id: UUID,
) -> User | None:
    """
    Get a user by ID.
    """
    return db.get(User, user_id)


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    """
    Get a user by email.
    """
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_phone(
    db: Session,
    phone: str,
) -> User | None:
    """
    Get a user by phone number.
    """
    return (
        db.query(User)
        .filter(User.phone == phone)
        .first()
    )


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    """
    Get a list of users.
    """
    return db.query(User).offset(skip).limit(limit).all()


def create_user(
    db: Session,
    user: User,
) -> User:
    """
    Create a new user.
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_last_login(
    db: Session,
    user: User,
) -> User:
    """
    Update the user's last login timestamp.
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(
    db: Session,
    user: User,
) -> User:
    """
    Update an existing user.
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(
    db: Session,
    user: User,
) -> None:
    """
    Delete a user.
    """
    db.delete(user)
    db.commit()