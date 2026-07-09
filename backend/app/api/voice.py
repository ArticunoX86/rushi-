import uuid


from fastapi import (
    APIRouter,
)


from fastapi.responses import FileResponse


from pydantic import BaseModel


from app.services.tts_service import (
    generate_ai_voice,
)



router = APIRouter(

    prefix="/voice",

    tags=[
        "Voice"
    ],

)



# ==================================================
# REQUEST MODEL
# ==================================================

class VoiceRequest(BaseModel):

    text: str



# ==================================================
# GENERATE VOICE
# ==================================================

@router.post(
    "/generate"
)
def generate_voice(

    request: VoiceRequest,

):


    audio = generate_ai_voice(

        request.text

    )



    filename = (

        f"ai_voice_{uuid.uuid4()}.mp3"

    )


    filepath = (

        f"temp/{filename}"

    )



    with open(

        filepath,

        "wb"

    ) as file:


        file.write(

            audio

        )



    return FileResponse(

        filepath,

        media_type="audio/mpeg",

        filename=filename,

    )