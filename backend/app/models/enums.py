from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    SALES_MANAGER = "SALES_MANAGER"
    SALES_EXECUTIVE = "SALES_EXECUTIVE"

class PropertyType(str, Enum):
    APARTMENT = "APARTMENT"
    VILLA = "VILLA"
    HOUSE = "HOUSE"
    PLOT = "PLOT"
    COMMERCIAL = "COMMERCIAL"


class ListingType(str, Enum):
    SALE = "SALE"
    RENT = "RENT"


class PropertyStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    SOLD = "SOLD"
    RENTED = "RENTED"
    INACTIVE = "INACTIVE"


class FurnishingType(str, Enum):
    FURNISHED = "FURNISHED"
    SEMI_FURNISHED = "SEMI_FURNISHED"
    UNFURNISHED = "UNFURNISHED"