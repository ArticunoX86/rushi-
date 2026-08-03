import uuid

from datetime import datetime

from pydantic import BaseModel

from app.models.enums import (
    DeviceStatus,
)


# ==================================================
# BASE DEVICE SCHEMA
# ==================================================

class DeviceBase(
    BaseModel,
):

    device_name: str

    device_identifier: str

    phone_number: str | None = None


# ==================================================
# CREATE DEVICE
# ==================================================

class DeviceCreate(
    DeviceBase,
):

    pass


# ==================================================
# UPDATE DEVICE
# ==================================================

class DeviceUpdate(
    BaseModel,
):

    status: DeviceStatus | None = None

    current_call_id: str | None = None


# ==================================================
# DEVICE RESPONSE
# ==================================================

class DeviceResponse(
    DeviceBase,
):

    id: uuid.UUID

    status: DeviceStatus

    current_call_id: str | None = None

    last_seen: datetime | None = None

    created_at: datetime

    class Config:

        from_attributes = True