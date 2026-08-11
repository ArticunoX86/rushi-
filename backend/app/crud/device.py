from uuid import UUID

from datetime import datetime


from sqlalchemy.orm import Session


from app.models.device import Device


from app.models.enums import DeviceStatus


from app.schemas.device import (
    DeviceCreate,
    DeviceUpdate,
)



# ==================================================
# REGISTER DEVICE
# ==================================================

def create_device(

    db: Session,

    device_data: DeviceCreate,

):


    device = Device(

        **device_data.model_dump(),

        status=DeviceStatus.ONLINE,

        last_seen=datetime.utcnow(),

    )


    db.add(
        device
    )


    db.commit()


    db.refresh(
        device
    )


    return device



# ==================================================
# GET DEVICE BY ID
# ==================================================

def get_device(

    db: Session,

    device_id: UUID,

):


    return (

        db.query(Device)

        .filter(
            Device.id == device_id
        )

        .first()

    )



# ==================================================
# GET DEVICE BY IDENTIFIER
# ==================================================

def get_device_by_identifier(

    db: Session,

    device_identifier: str,

):


    return (

        db.query(Device)

        .filter(
            Device.device_identifier
            ==
            device_identifier
        )

        .first()

    )



# ==================================================
# GET ALL DEVICES
# ==================================================

def get_devices(
    db: Session,
):
    devices = db.query(Device).all()
    now = datetime.utcnow()
    updated = False
    for d in devices:
        if d.status == DeviceStatus.ONLINE and d.last_seen:
            # If not seen in 60 seconds, mark as offline
            if (now - d.last_seen.replace(tzinfo=None)).total_seconds() > 60:
                d.status = DeviceStatus.OFFLINE
                updated = True
    
    if updated:
        db.commit()

    return devices



# ==================================================
# GET FREE CALLING DEVICE
# ==================================================

def get_available_device(
    db: Session,
):
    # First update stale devices
    get_devices(db)
    
    return (
        db.query(Device)
        .filter(
            Device.status
            ==
            DeviceStatus.ONLINE
        )
        .first()
    )



# ==================================================
# UPDATE DEVICE STATUS
# ==================================================

def update_device(

    db: Session,

    device: Device,

    update_data: DeviceUpdate,

):


    data = update_data.model_dump(

        exclude_unset=True

    )


    for key, value in data.items():


        setattr(

            device,

            key,

            value,

        )


    device.last_seen = datetime.utcnow()


    db.commit()


    db.refresh(

        device

    )


    return device



# ==================================================
# DELETE DEVICE
# ==================================================

def delete_device(

    db: Session,

    device: Device,

):


    db.delete(

        device

    )


    db.commit()


    return True