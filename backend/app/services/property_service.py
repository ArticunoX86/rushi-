from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud import property as property_crud

from app.schemas.property import (
    PropertyCreate,
    PropertyUpdate,
    PropertySearch,
)


# ==================================================
# Create Property
# ==================================================

def create_property(
    db: Session,
    property_data: PropertyCreate,
):

    return property_crud.create_property(
        db,
        property_data,
    )



# ==================================================
# Get Single Property
# ==================================================

def get_property(
    db: Session,
    property_id: UUID,
):

    property_obj = property_crud.get_property(
        db,
        property_id,
    )


    if not property_obj:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )


    return property_obj



# ==================================================
# List Properties
# ==================================================

def get_properties(
    db: Session,
    skip: int = 0,
    limit: int = 50,
):

    return property_crud.get_properties(
        db,
        skip,
        limit,
    )



# ==================================================
# Update Property
# ==================================================

def update_property(
    db: Session,
    property_id: UUID,
    data: PropertyUpdate,
):

    property_obj = get_property(
        db,
        property_id,
    )


    return property_crud.update_property(
        db,
        property_obj,
        data,
    )



# ==================================================
# Delete Property
# ==================================================

def delete_property(
    db: Session,
    property_id: UUID,
):

    property_obj = get_property(
        db,
        property_id,
    )


    return property_crud.delete_property(
        db,
        property_obj,
    )



# ==================================================
# AI Property Search
# ==================================================

def search_properties(
    db: Session,
    filters: PropertySearch,
):

    return property_crud.search_properties(
        db,
        filters,
    )