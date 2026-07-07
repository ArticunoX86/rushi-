from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.enums import (
    PropertyType,
    LeadStatus,
    LeadPriority,
    LeadSource,
)


# ==================================================
# Base Lead Schema
# ==================================================

class LeadBase(BaseModel):

    # Customer Information

    first_name: str

    last_name: Optional[str] = None

    email: Optional[EmailStr] = None

    phone: str



    # Property Requirements

    preferred_city: Optional[str] = None

    preferred_locality: Optional[str] = None


    budget_min: Optional[Decimal] = None

    budget_max: Optional[Decimal] = None


    bedrooms: Optional[int] = None


    property_type: Optional[PropertyType] = None



    # Lead Management

    status: LeadStatus = LeadStatus.NEW

    priority: LeadPriority = LeadPriority.MEDIUM

    source: LeadSource = LeadSource.MANUAL



# ==================================================
# Create Lead
# ==================================================

class LeadCreate(LeadBase):
    pass



# ==================================================
# Update Lead
# ==================================================

class LeadUpdate(BaseModel):

    first_name: Optional[str] = None

    last_name: Optional[str] = None

    email: Optional[EmailStr] = None

    phone: Optional[str] = None


    preferred_city: Optional[str] = None

    preferred_locality: Optional[str] = None


    budget_min: Optional[Decimal] = None

    budget_max: Optional[Decimal] = None


    bedrooms: Optional[int] = None

    property_type: Optional[PropertyType] = None


    status: Optional[LeadStatus] = None

    priority: Optional[LeadPriority] = None


    conversation_summary: Optional[str] = None

    next_followup_time: Optional[datetime] = None



# ==================================================
# Response Schema
# ==================================================

class LeadResponse(LeadBase):

    id: UUID


    call_attempts: int

    last_call_time: Optional[datetime]

    next_followup_time: Optional[datetime]


    conversation_summary: Optional[str]


    assigned_to: Optional[UUID]


    class Config:
        from_attributes = True



# ==================================================
# AI Search Schema
# ==================================================

class LeadSearch(BaseModel):

    status: Optional[LeadStatus] = None

    priority: Optional[LeadPriority] = None


    preferred_city: Optional[str] = None

    property_type: Optional[PropertyType] = None


    min_budget: Optional[Decimal] = None

    max_budget: Optional[Decimal] = None


    bedrooms: Optional[int] = None