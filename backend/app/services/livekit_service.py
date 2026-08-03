import os
from livekit.api import AccessToken, VideoGrants
from app.core.config import settings

def generate_room_token(room_name: str, participant_identity: str) -> str:
    """
    Generates a secure WebRTC LiveKit JWT access token for a room session.
    """
    api_key = getattr(settings, "LIVEKIT_API_KEY", None) or os.environ.get("LIVEKIT_API_KEY", "devkey")
    api_secret = getattr(settings, "LIVEKIT_API_SECRET", None) or os.environ.get("LIVEKIT_API_SECRET", "secret")

    token = (
        AccessToken(api_key, api_secret)
        .with_identity(participant_identity)
        .with_name(participant_identity)
        .with_grants(
            VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
            )
        )
    )

    return token.to_jwt()
