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
