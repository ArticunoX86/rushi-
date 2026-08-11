from uuid import UUID
from sqlalchemy.orm import Session
from app.models.role import Role

def get_role_by_id(db: Session, role_id: UUID) -> Role | None:
    return db.get(Role, role_id)

def get_role_by_name(db: Session, name: str) -> Role | None:
    return db.query(Role).filter(Role.name == name).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100) -> list[Role]:
    return db.query(Role).offset(skip).limit(limit).all()

def create_role(db: Session, role: Role) -> Role:
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def update_role(db: Session, role: Role) -> Role:
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def delete_role(db: Session, role: Role) -> None:
    db.delete(role)
    db.commit()
