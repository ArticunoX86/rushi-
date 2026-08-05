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

# ==================================================
# TRANSCRIBE UPLOADED AUDIO FILE
# ==================================================

from fastapi import UploadFile, File, HTTPException
from deepgram import DeepgramClient, PrerecordedOptions
from app.core.config import settings

@router.post("/transcribe-file")
async def transcribe_uploaded_file(
    file: UploadFile = File(...)
):
    try:
        deepgram = DeepgramClient(settings.DEEPGRAM_API_KEY)
        audio_data = await file.read()
        
        payload = {
            "buffer": audio_data,
        }
        
        options = PrerecordedOptions(
            model="nova-2",
            language="hi",
            smart_format=True,
        )
        
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        
        transcript = response.results.channels[0].alternatives[0].transcript
        
        return {"transcript": transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))