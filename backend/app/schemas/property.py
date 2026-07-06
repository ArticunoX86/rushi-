from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import (
    PropertyType,
    ListingType,
    PropertyStatus,
    FurnishingType,
)


# ==================================================
# Base Schema
# ==================================================

class PropertyBase(BaseModel):

    title: str
    description: Optional[str] = None

    property_type: PropertyType
    listing_type: ListingType
    status: PropertyStatus = PropertyStatus.AVAILABLE


    # Location

    city: str
    locality: str
    address: str
    pincode: Optional[str] = None


    # Pricing

    price: Decimal
    maintenance_cost: Optional[Decimal] = None


    # Details

    bedrooms: int
    bathrooms: int
    area_sqft: int

    furnishing: FurnishingType


    # Amenities

    parking: bool = False
    lift: bool = False
    security: bool = False


    # Owner

    owner_name: str
    owner_phone: str



# ==================================================
# Create Property
# ==================================================

class PropertyCreate(PropertyBase):
    pass



# ==================================================
# Update Property
# ==================================================

class PropertyUpdate(BaseModel):

    title: Optional[str] = None
    description: Optional[str] = None

    status: Optional[PropertyStatus] = None

    price: Optional[Decimal] = None
    maintenance_cost: Optional[Decimal] = None

    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None

    furnishing: Optional[FurnishingType] = None

    parking: Optional[bool] = None
    lift: Optional[bool] = None
    security: Optional[bool] = None



# ==================================================
# Response Schema
# ==================================================

class PropertyResponse(PropertyBase):

    id: UUID

    assigned_to: Optional[UUID]

    class Config:
        from_attributes = True



# ==================================================
# Search Filters
# ==================================================

class PropertySearch(BaseModel):

    city: Optional[str] = None
    locality: Optional[str] = None

    property_type: Optional[PropertyType] = None
    listing_type: Optional[ListingType] = None

    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None

    bedrooms: Optional[int] = None

    parking: Optional[bool] = None