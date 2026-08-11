from fastapi import (
    APIRouter,
    Depends,
)


from fastapi.responses import FileResponse


from pydantic import BaseModel


from uuid import UUID


from sqlalchemy.orm import Session


import uuid

import os



from app.database.session import (
    get_db,
)


from app.services.voice_agent_service import (
    process_voice_conversation,
)



router = APIRouter(

    prefix="/voice-agent",

    tags=[
        "AI Voice Agent"
    ]

)



# ==================================================
# REQUEST MODEL
# ==================================================

class VoiceAgentRequest(BaseModel):

    audio_url: str

    lead_id: UUID

    call_id: UUID



# ==================================================
# GET ALL AGENTS (MOCK)
# ==================================================

@router.get("")
def get_voice_agents():
    # Return empty list or mock data to satisfy frontend
    return []

# ==================================================
# PROCESS COMPLETE AI CALL
# ==================================================

@router.post(
    "/process"
)
def process_call(

    request: VoiceAgentRequest,

    db: Session = Depends(get_db),

):


    result = process_voice_conversation(

        db,

        request.audio_url,

        request.lead_id,

        request.call_id,

    )



    if "error" in result:


        return result



    os.makedirs(

        "temp",

        exist_ok=True

    )



    filename = (

        f"ai_response_{uuid.uuid4()}.mp3"

    )


    filepath = (

        f"temp/{filename}"

    )



    with open(

        filepath,

        "wb"

    ) as file:


        file.write(

            result["audio"]

        )



    return FileResponse(

        filepath,

        media_type="audio/mpeg",

        filename=filename,

        headers={

            "X-Customer-Text":

                result["customer_text"],


            "X-AI-Reply":

                result["ai_reply"],

        },

    )