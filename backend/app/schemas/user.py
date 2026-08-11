from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from typing import Optional
from app.schemas.role import RoleResponse

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    is_active: bool = True
    is_superadmin: bool = False
    role_id: UUID

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[UUID] = None

class UserResponse(UserBase):
    id: UUID
    role: RoleResponse

    model_config = ConfigDict(from_attributes=True)
