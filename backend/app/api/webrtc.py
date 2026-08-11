from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.livekit_service import generate_room_token

router = APIRouter(
    prefix="/webrtc",
    tags=["WebRTC AI Streaming"],
)

@router.get("")
def get_webrtc_sessions():
    return []

class TokenRequest(BaseModel):
    call_id: str
    identity: str = "mobile_client"

@router.post("/token")
async def get_webrtc_token(request: TokenRequest):
    """
    Generates a LiveKit WebRTC access token for a given call_id.
    """
    try:
        room_name = f"call_{request.call_id}"
        token = generate_room_token(
            room_name=room_name,
            participant_identity=request.identity,
        )
        return {
            "status": "success",
            "room_name": room_name,
            "token": token,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate WebRTC token: {str(e)}"
        )
