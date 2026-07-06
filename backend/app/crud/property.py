from uuid import UUID

from sqlalchemy.orm import Session

from app.models.property import Property
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
    property_obj = Property(
        **property_data.model_dump()
    )

    db.add(property_obj)
    db.commit()
    db.refresh(property_obj)

    return property_obj



# ==================================================
# Get Property By ID
# ==================================================

def get_property(
    db: Session,
    property_id: UUID,
):

    return (
        db.query(Property)
        .filter(Property.id == property_id)
        .first()
    )



# ==================================================
# Get All Properties
# ==================================================

def get_properties(
    db: Session,
    skip: int = 0,
    limit: int = 50,
):

    return (
        db.query(Property)
        .offset(skip)
        .limit(limit)
        .all()
    )



# ==================================================
# Update Property
# ==================================================

def update_property(
    db: Session,
    property_obj: Property,
    update_data: PropertyUpdate,
):

    update_dict = update_data.model_dump(
        exclude_unset=True
    )


    for field, value in update_dict.items():

        setattr(
            property_obj,
            field,
            value,
        )


    db.commit()
    db.refresh(property_obj)


    return property_obj



# ==================================================
# Delete Property
# ==================================================

def delete_property(
    db: Session,
    property_obj: Property,
):

    db.delete(property_obj)

    db.commit()

    return True



# ==================================================
# Search Properties (AI Ready)
# ==================================================

def search_properties(
    db: Session,
    filters: PropertySearch,
):

    query = db.query(Property)


    if filters.city:

        query = query.filter(
            Property.city.ilike(
                f"%{filters.city}%"
            )
        )


    if filters.locality:

        query = query.filter(
            Property.locality.ilike(
                f"%{filters.locality}%"
            )
        )


    if filters.property_type:

        query = query.filter(
            Property.property_type
            ==
            filters.property_type
        )


    if filters.listing_type:

        query = query.filter(
            Property.listing_type
            ==
            filters.listing_type
        )


    if filters.min_price:

        query = query.filter(
            Property.price
            >=
            filters.min_price
        )


    if filters.max_price:

        query = query.filter(
            Property.price
            <=
            filters.max_price
        )


    if filters.bedrooms:

        query = query.filter(
            Property.bedrooms
            ==
            filters.bedrooms
        )


    if filters.parking is not None:

        query = query.filter(
            Property.parking
            ==
            filters.parking
        )


    return query.all()