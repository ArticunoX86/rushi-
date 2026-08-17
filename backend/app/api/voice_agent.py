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
from app.crud.voice_agent import voice_agent as crud_voice_agent
from app.schemas.voice_agent import VoiceAgentResponse, VoiceAgentCreate, VoiceAgentUpdate
from typing import List



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



@router.get("", response_model=List[VoiceAgentResponse])
def get_voice_agents(db: Session = Depends(get_db)):
    return crud_voice_agent.get_all(db)

@router.post("", response_model=VoiceAgentResponse)
def create_voice_agent(agent_in: VoiceAgentCreate, db: Session = Depends(get_db)):
    return crud_voice_agent.create(db, obj_in=agent_in)

@router.put("/{agent_id}", response_model=VoiceAgentResponse)
def update_voice_agent(agent_id: UUID, agent_in: VoiceAgentUpdate, db: Session = Depends(get_db)):
    agent = crud_voice_agent.get(db, agent_id=agent_id)
    if not agent:
        return {"error": "Voice agent not found"}
    return crud_voice_agent.update(db, db_obj=agent, obj_in=agent_in)

@router.delete("/{agent_id}")
def delete_voice_agent(agent_id: UUID, db: Session = Depends(get_db)):
    agent = crud_voice_agent.get(db, agent_id=agent_id)
    if not agent:
        return {"error": "Voice agent not found"}
    crud_voice_agent.delete(db, agent_id=agent_id)
    return {"status": "deleted"}

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