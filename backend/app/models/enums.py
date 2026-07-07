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

class LeadStatus(str, Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    INTERESTED = "INTERESTED"
    NOT_INTERESTED = "NOT_INTERESTED"
    FOLLOW_UP = "FOLLOW_UP"
    CONVERTED = "CONVERTED"


class LeadPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class LeadSource(str, Enum):
    WEBSITE = "WEBSITE"
    MANUAL = "MANUAL"
    CSV_IMPORT = "CSV_IMPORT"
    API = "API"