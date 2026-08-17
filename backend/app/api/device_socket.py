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


    from app.database.session import SessionLocal
    from app.models.device import Device
    from app.models.enums import DeviceStatus
    from datetime import datetime, timezone

    await device_manager.connect(
        device_id,
        websocket,
    )

    # Update DB to ONLINE
    db = SessionLocal()
    try:
        device = db.query(Device).filter(Device.device_identifier == device_id).first()
        if device:
            device.status = DeviceStatus.ONLINE
            device.last_seen = datetime.now(timezone.utc)
            db.commit()
    except Exception as e:
        print(f"Failed to update device status to ONLINE: {e}")
    finally:
        db.close()

    try:
        while True:
            data = await websocket.receive_json()
            print("[DEVICE MESSAGE]", device_id, data)
            
            action = data.get("action")

            if action == "CALL_ACCEPTED":
                payload = data.get("payload", {})
                call_id = payload.get("call_id") or payload.get("id")
                from app.models.call import Call
                from app.models.enums import CallStatus
                from app.services.tata_telephony_service import tata_telephony_service
                
                db = SessionLocal()
                try:
                    db_call = db.query(Call).filter(Call.id == call_id).first()
                    if db_call and db_call.status == CallStatus.SCHEDULED:
                        db_call.status = CallStatus.IN_PROGRESS
                        db.commit()
                        
                        # Trigger TATA Telephony
                        tata_response = tata_telephony_service.make_outbound_call(
                            phone_number=db_call.lead.phone,
                            call_id=str(db_call.id)
                        )
                        print(f"TATA call initiated: {tata_response}")
                        
                        # Broadcast CALL_STARTED back to Flutter
                        await device_manager.broadcast_all({
                            "action": "CALL_STARTED",
                            "payload": {
                                "call_id": str(db_call.id),
                                "status": "IN_PROGRESS"
                            }
                        })
                except Exception as e:
                    print(f"Failed to start TATA call: {e}")
                finally:
                    db.close()

            elif action in ["CALL_ENDED", "CALL_COMPLETED", "CALL_REJECTED"]:
                from app.models.call import Call
                from app.models.enums import CallStatus
                
                db = SessionLocal()
                try:
                    device = db.query(Device).filter(Device.device_identifier == device_id).first()
                    current_call_id = device.current_call_id if device else None
                    if device:
                        device.status = DeviceStatus.ONLINE
                        device.current_call_id = None
                        db.commit()

                    if current_call_id or action == "CALL_REJECTED":
                        target_call_id = current_call_id
                        
                        # If rejecting, the call ID might be in the payload, not just current_call_id
                        if action == "CALL_REJECTED" and not target_call_id:
                            target_call_id = data.get("payload", {}).get("call_id") or data.get("payload", {}).get("id")

                        db_call = db.query(Call).filter(Call.id == target_call_id).first() if target_call_id else None
                        if db_call and db_call.status not in [CallStatus.COMPLETED, CallStatus.REJECTED]:
                            db_call.status = CallStatus.COMPLETED if action != "CALL_REJECTED" else CallStatus.REJECTED
                            db_call.end_time = datetime.now(timezone.utc)
                            db.commit()
                            
                            # Trigger Call Analyzer in the background
                            if action != "CALL_REJECTED":
                                from app.services.call_analyzer_service import analyze_call_async
                                asyncio.create_task(analyze_call_async(str(db_call.id)))

                    # Instant Broadcast to all Flutter app listeners
                    await device_manager.broadcast_all({
                        "action": action,
                        "event": action,
                        "payload": {
                            "device_id": device_id,
                            "call_id": str(target_call_id) if target_call_id else "",
                            "status": "COMPLETED" if action != "CALL_REJECTED" else "REJECTED"
                        }
                    })
                except Exception as e:
                    print(f"Failed to update status on CALL_ENDED: {e}")
                finally:
                    db.close()

    except WebSocketDisconnect:
        device_manager.disconnect(device_id)

        # Update DB to OFFLINE
        db = SessionLocal()
        try:
            device = db.query(Device).filter(Device.device_identifier == device_id).first()
            if device:
                device.status = DeviceStatus.OFFLINE
                device.last_seen = datetime.now(timezone.utc)
                db.commit()
        except Exception as e:
            print(f"Failed to update device status to OFFLINE: {e}")
        finally:
            db.close()