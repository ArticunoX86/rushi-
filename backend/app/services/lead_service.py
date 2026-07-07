from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import lead as lead_crud

from app.schemas.lead import (
    LeadCreate,
    LeadUpdate,
    LeadSearch,
)


# ==================================================
# Create Lead
# ==================================================

def create_lead(
    db: Session,
    lead_data: LeadCreate,
):

    return lead_crud.create_lead(
        db,
        lead_data,
    )



# ==================================================
# Get Single Lead
# ==================================================

def get_lead(
    db: Session,
    lead_id: UUID,
):

    lead = lead_crud.get_lead(
        db,
        lead_id,
    )


    if not lead:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )


    return lead



# ==================================================
# Get All Leads
# ==================================================

def get_leads(
    db: Session,
    skip: int = 0,
    limit: int = 50,
):

    return lead_crud.get_leads(
        db,
        skip,
        limit,
    )



# ==================================================
# Update Lead
# ==================================================

def update_lead(
    db: Session,
    lead_id: UUID,
    data: LeadUpdate,
):

    lead = get_lead(
        db,
        lead_id,
    )


    return lead_crud.update_lead(
        db,
        lead,
        data,
    )



# ==================================================
# Delete Lead
# ==================================================

def delete_lead(
    db: Session,
    lead_id: UUID,
):

    lead = get_lead(
        db,
        lead_id,
    )


    return lead_crud.delete_lead(
        db,
        lead,
    )



# ==================================================
# AI Lead Search
# ==================================================

def search_leads(
    db: Session,
    filters: LeadSearch,
):

    return lead_crud.search_leads(
        db,
        filters,
    )