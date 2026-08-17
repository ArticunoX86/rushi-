from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.tenant import Tenant
from app.models.call import Call
from app.models.device import Device
from app.models.enums import DeviceStatus
from pydantic import BaseModel
import datetime

# Pydantic schemas for the admin routes
class TenantCreate(BaseModel):
    name: str
    is_active: bool = True

class TenantResponse(BaseModel):
    id: UUID
    name: str
    is_active: bool
    created_at: datetime.datetime
    
    class Config:
        orm_mode = True

class UserAdminUpdate(BaseModel):
    is_superadmin: bool
    tenant_id: UUID | None = None

class UserAdminResponse(BaseModel):
    id: UUID
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_superadmin: bool
    tenant_id: UUID | None = None
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class DeviceAdminResponse(BaseModel):
    id: UUID
    device_name: str
    device_identifier: str
    status: DeviceStatus
    tenant_id: UUID | None = None
    last_seen: datetime.datetime | None = None

    class Config:
        orm_mode = True

router = APIRouter(
    prefix="/admin",
    tags=["Super Admin"],
)

def get_superadmin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super Admin privileges required."
        )
    return current_user

# ==================================================
# Manage Tenants
# ==================================================
@router.post("/tenants", response_model=TenantResponse)
def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin_user),
):
    tenant = Tenant(name=tenant_data.name, is_active=tenant_data.is_active)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

@router.get("/tenants", response_model=List[TenantResponse])
def get_tenants(
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin_user),
):
    return db.query(Tenant).all()

@router.put("/tenants/{tenant_id}", response_model=TenantResponse)
def update_tenant(
    tenant_id: UUID,
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin_user),
):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
        
    tenant.name = tenant_data.name
    tenant.is_active = tenant_data.is_active
    db.commit()
    db.refresh(tenant)
    return tenant

@router.delete("/tenants/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tenant(
    tenant_id: UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin_user),
):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
        
    db.delete(tenant)
    db.commit()
    return None

# ==================================================
# Manage Users
# ==================================================
@router.get("/users", response_model=List[UserAdminResponse])
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin_user),
):
    return db.query(User).all()

@router.put("/users/{user_id}", response_model=UserAdminResponse)
def update_user_admin(
    user_id: UUID,
    user_data: UserAdminUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.is_superadmin = user_data.is_superadmin
    user.tenant_id = user_data.tenant_id
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_admin(
    user_id: UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    db.delete(user)
    db.commit()
    return None

# ==================================================
# Manage Devices
# ==================================================
@router.get("/devices", response_model=List[DeviceAdminResponse])
def get_all_devices(
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin_user),
):
    return db.query(Device).all()

@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device_admin(
    device_id: UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin_user),
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
        
    db.delete(device)
    db.commit()
    return None

# ==================================================
# Global Stats
# ==================================================
@router.get("/stats")
def get_global_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(get_superadmin_user),
):
    total_tenants = db.query(Tenant).count()
    total_calls = db.query(Call).count()
    total_users = db.query(User).count()
    
    return {
        "total_tenants": total_tenants,
        "total_calls": total_calls,
        "total_users": total_users,
        "active_ai_minutes": total_calls * 2.5 # Mock metric
    }
