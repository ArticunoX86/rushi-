from uuid import UUID


from fastapi import (
    HTTPException,
    status,
)


from sqlalchemy.orm import Session


from app.schemas.device import (
    DeviceCreate,
    DeviceUpdate,
)


from app.crud.device import (
    create_device,
    get_device,
    get_device_by_identifier,
    get_devices,
    get_available_device,
    update_device,
    delete_device,
)


from app.models.enums import DeviceStatus



# ==================================================
# REGISTER ANDROID DEVICE
# ==================================================

def register_device(

    db: Session,

    device_data: DeviceCreate,

):


    existing = get_device_by_identifier(

        db,

        device_data.device_identifier,

    )


    if existing:


        # ------------------------------------------
        # UPDATE EXISTING DEVICE
        # ------------------------------------------

        existing.device_name = device_data.device_name

        existing.phone_number = device_data.phone_number

        existing.status = DeviceStatus.ONLINE

        db.commit()

        db.refresh(existing)

        return existing



    # ------------------------------------------
    # CREATE NEW DEVICE
    # ------------------------------------------

    return create_device(

        db,

        device_data,

    )


# ==================================================
# GET ALL DEVICES
# ==================================================

def list_devices(

    db: Session,

):


    return get_devices(

        db

    )



# ==================================================
# GET SINGLE DEVICE
# ==================================================

def get_device_details(

    db: Session,

    device_id: UUID,

):


    device = get_device(

        db,

        device_id,

    )


    if not device:


        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Device not found",

        )


    return device



# ==================================================
# FIND FREE PHONE FOR CALLING
# ==================================================

def find_available_calling_device(
    db: Session,
    active_identifiers: list[str] = None,
):
    from app.models.device import Device
    from app.models.enums import DeviceStatus

    query = db.query(Device).filter(Device.status == DeviceStatus.ONLINE)
    
    if active_identifiers is not None:
        query = query.filter(Device.device_identifier.in_(active_identifiers))

    device = query.first()

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No online calling device available",
        )

    return device



# ==================================================
# UPDATE DEVICE
# ==================================================

def update_device_status(

    db: Session,

    device_id: UUID,

    update_data: DeviceUpdate,

):


    device = get_device_details(

        db,

        device_id,

    )


    return update_device(

        db,

        device,

        update_data,

    )



# ==================================================
# REMOVE DEVICE
# ==================================================

def remove_device(

    db: Session,

    device_id: UUID,

):


    device = get_device_details(

        db,

        device_id,

    )


    return delete_device(

        db,

        device,

    )