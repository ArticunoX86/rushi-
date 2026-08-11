from enum import Enum
import enum


class UserRole(str, Enum):
    SYSTEM_ADMINISTRATOR = "SYSTEM_ADMINISTRATOR"
    CLIENT_HEAD = "CLIENT_HEAD"

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



class CallStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    MISSED = "missed"
    REJECTED = "rejected"


class CallDirection(str, enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class CallOutcome(str, enum.Enum):
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"
    CALLBACK_REQUESTED = "callback_requested"
    NO_RESPONSE = "no_response"
    CONVERTED = "converted"

class MessageSender(str, enum.Enum):

    AI = "ai"

    CUSTOMER = "customer"


class MessageIntent(str, enum.Enum):

    GREETING = "greeting"

    PROPERTY_REQUIREMENT = "property_requirement"

    QUESTION = "question"

    CALLBACK_REQUEST = "callback_request"

    NOT_INTERESTED = "not_interested"

    UNKNOWN = "unknown"


class DeviceStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    BUSY = "BUSY"