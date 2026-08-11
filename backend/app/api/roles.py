from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database.session import get_db
from app.core.dependencies import get_current_user, RequirePermissions
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse
from app.crud.role import get_roles, get_role_by_id, create_role, update_role, delete_role

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    dependencies=[Depends(RequirePermissions(["manage_roles"]))]
)

@router.get("", response_model=List[RoleResponse])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = get_roles(db, skip=skip, limit=limit)
    return roles

@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_new_role(role_in: RoleCreate, db: Session = Depends(get_db)):
    role = Role(
        name=role_in.name,
        description=role_in.description,
        permissions=role_in.permissions,
    )
    return create_role(db, role)

@router.put("/{role_id}", response_model=RoleResponse)
def update_existing_role(role_id: UUID, role_in: RoleUpdate, db: Session = Depends(get_db)):
    role = get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    if role_in.name is not None:
        role.name = role_in.name
    if role_in.description is not None:
        role.description = role_in.description
    if role_in.permissions is not None:
        role.permissions = role_in.permissions
        
    return update_role(db, role)

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_role(role_id: UUID, db: Session = Depends(get_db)):
    role = get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    if role.users:
        raise HTTPException(status_code=400, detail="Cannot delete role with assigned users")
        
    delete_role(db, role)
    return None
