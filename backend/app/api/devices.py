from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session


from app.database.session import (
    get_db,
)


from app.schemas.device import (
    DeviceCreate,
    DeviceUpdate,
    DeviceResponse,
)


from app.services.device_service import (
    register_device,
    list_devices,
    get_device_details,
    find_available_calling_device,
    update_device_status,
    remove_device,
)



router = APIRouter(

    prefix="/devices",

    tags=[
        "Android Calling Devices"
    ],

)



# ==================================================
# REGISTER DEVICE
# ==================================================

@router.post(
    "/register",
    response_model=DeviceResponse,
)
def register_android_device(

    device: DeviceCreate,

    db: Session = Depends(get_db),

):

    return register_device(

        db,

        device,

    )



# ==================================================
# GET ALL DEVICES
# ==================================================

@router.get(
    "",
    response_model=list[DeviceResponse],
)
def get_all_android_devices(

    db: Session = Depends(get_db),

):

    return list_devices(

        db

    )



# ==================================================
# GET AVAILABLE DEVICE
# ==================================================

@router.get(
    "/available",
    response_model=DeviceResponse,
)
def get_available_android_device(

    db: Session = Depends(get_db),

):

    return find_available_calling_device(

        db

    )



# ==================================================
# GET DEVICE BY ID
# ==================================================

@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
)
def get_android_device(

    device_id: UUID,

    db: Session = Depends(get_db),

):

    return get_device_details(

        db,

        device_id,

    )



# ==================================================
# UPDATE DEVICE
# ==================================================

@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
)
def update_android_device(

    device_id: UUID,

    update_data: DeviceUpdate,

    db: Session = Depends(get_db),

):

    return update_device_status(

        db,

        device_id,

        update_data,

    )



# ==================================================
# DELETE DEVICE
# ==================================================

@router.delete(
    "/{device_id}",
)
def delete_android_device(

    device_id: UUID,

    db: Session = Depends(get_db),

):

    remove_device(

        db,

        device_id,

    )


    return {

        "message": "Device deleted successfully"

    }