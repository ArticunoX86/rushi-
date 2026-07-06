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

from app.schemas.property import (
    PropertyCreate,
    PropertyUpdate,
    PropertyResponse,
    PropertySearch,
)

from app.services import property_service


router = APIRouter(
    prefix="/properties",
    tags=["Properties"],
)


# ==================================================
# Create Property
# ==================================================

@router.post(
    "",
    response_model=PropertyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return property_service.create_property(
        db,
        property_data,
    )



# ==================================================
# Get All Properties
# ==================================================

@router.get(
    "",
    response_model=List[PropertyResponse],
)
def get_properties(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return property_service.get_properties(
        db,
        skip,
        limit,
    )



# ==================================================
# Get Property By ID
# ==================================================

@router.get(
    "/{property_id}",
    response_model=PropertyResponse,
)
def get_property(
    property_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return property_service.get_property(
        db,
        property_id,
    )



# ==================================================
# Update Property
# ==================================================

@router.put(
    "/{property_id}",
    response_model=PropertyResponse,
)
def update_property(
    property_id: UUID,
    data: PropertyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return property_service.update_property(
        db,
        property_id,
        data,
    )



# ==================================================
# Delete Property
# ==================================================

@router.delete(
    "/{property_id}",
)
def delete_property(
    property_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    property_service.delete_property(
        db,
        property_id,
    )


    return {
        "message": "Property deleted successfully"
    }



# ==================================================
# AI Search Endpoint
# ==================================================

@router.post(
    "/search",
    response_model=List[PropertyResponse],
)
def search_properties(
    filters: PropertySearch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return property_service.search_properties(
        db,
        filters,
    )