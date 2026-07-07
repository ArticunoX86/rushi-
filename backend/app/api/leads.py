from typing import List
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.orm import Session


from app.database.session import get_db
from app.core.dependencies import get_current_user


from app.models.user import User


from app.schemas.lead import (
    LeadCreate,
    LeadUpdate,
    LeadResponse,
    LeadSearch,
)


from app.services import lead_service
from app.services import recommendation_service



router = APIRouter(
    prefix="/leads",
    tags=["Leads"],
)



# ==================================================
# Create Lead
# ==================================================

@router.post(
    "",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lead(
    lead_data: LeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return lead_service.create_lead(
        db,
        lead_data,
    )




# ==================================================
# Get All Leads
# ==================================================

@router.get(
    "",
    response_model=List[LeadResponse],
)
def get_leads(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return lead_service.get_leads(
        db,
        skip,
        limit,
    )




# ==================================================
# Get Lead By ID
# ==================================================

@router.get(
    "/{lead_id}",
    response_model=LeadResponse,
)
def get_lead(
    lead_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return lead_service.get_lead(
        db,
        lead_id,
    )




# ==================================================
# Update Lead
# ==================================================

@router.put(
    "/{lead_id}",
    response_model=LeadResponse,
)
def update_lead(
    lead_id: UUID,
    data: LeadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return lead_service.update_lead(
        db,
        lead_id,
        data,
    )




# ==================================================
# Delete Lead
# ==================================================

@router.delete(
    "/{lead_id}",
)
def delete_lead(
    lead_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    lead_service.delete_lead(
        db,
        lead_id,
    )


    return {
        "message": "Lead deleted successfully"
    }




# ==================================================
# AI Lead Search
# ==================================================

@router.post(
    "/search",
    response_model=List[LeadResponse],
)
def search_leads(
    filters: LeadSearch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return lead_service.search_leads(
        db,
        filters,
    )

# ==================================================
# Property Recommendations
# ==================================================

@router.get(
    "/{lead_id}/recommendations"
)
def recommend_properties(
    lead_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return recommendation_service.get_property_recommendations(
        db,
        lead_id,
    )