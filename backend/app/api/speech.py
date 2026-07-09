from fastapi import (
    APIRouter,
)


from pydantic import BaseModel


from app.services.speech_service import (
    process_audio,
)



router = APIRouter(
    prefix="/speech",
    tags=["Speech"],
)



# ==================================================
# REQUEST SCHEMA
# ==================================================

class SpeechRequest(BaseModel):

    audio_url: str



# ==================================================
# RESPONSE SCHEMA
# ==================================================

class SpeechResponse(BaseModel):

    transcript: str | None



# ==================================================
# TRANSCRIBE AUDIO
# ==================================================

@router.post(
    "/transcribe",
    response_model=SpeechResponse,
)
def transcribe_audio(
    request: SpeechRequest,
):


    result = process_audio(
        request.audio_url
    )


    return result