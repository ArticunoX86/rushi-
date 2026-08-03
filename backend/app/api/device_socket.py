from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)


from app.services.device_connection_manager import (
    device_manager,
)



router = APIRouter(

    prefix="/device",

    tags=[
        "Android Device Socket"
    ],

)



# ==================================================
# ANDROID DEVICE LIVE CONNECTION
# ==================================================

@router.websocket(
    "/connect/{device_id}"
)
async def connect_device(

    websocket: WebSocket,

    device_id: str,

):


    await device_manager.connect(

        device_id,

        websocket,

    )


    try:


        while True:


            data = await websocket.receive_json()

            print(
                "[DEVICE MESSAGE]",
                device_id,
                data,
            )
            
            action = data.get("action")
            if action in ["CALL_ENDED", "CALL_COMPLETED", "CALL_REJECTED"]:
                from app.database.session import SessionLocal
                from app.models.device import Device
                from app.models.call import Call
                from app.models.enums import DeviceStatus, CallStatus
                from datetime import datetime, timezone
                
                db = SessionLocal()
                try:
                    device = db.query(Device).filter(Device.device_identifier == device_id).first()
                    current_call_id = device.current_call_id if device else None
                    if device:
                        device.status = DeviceStatus.ONLINE
                        device.current_call_id = None
                        db.commit()

                    if current_call_id:
                        db_call = db.query(Call).filter(Call.id == current_call_id).first()
                        if db_call and db_call.status != CallStatus.COMPLETED:
                            db_call.status = CallStatus.COMPLETED
                            db_call.end_time = datetime.now(timezone.utc)
                            db.commit()

                    # Instant Broadcast to all Flutter app listeners
                    await device_manager.broadcast_all({
                        "action": "CALL_ENDED",
                        "event": "CALL_ENDED",
                        "payload": {
                            "device_id": device_id,
                            "call_id": str(current_call_id) if current_call_id else "",
                            "status": "COMPLETED"
                        }
                    })
                except Exception as e:
                    print(f"Failed to update status on CALL_ENDED: {e}")
                finally:
                    db.close()




    except WebSocketDisconnect:


        device_manager.disconnect(

            device_id,

        )