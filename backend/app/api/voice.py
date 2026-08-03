import uuid

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from fastapi.responses import FileResponse

from pydantic import BaseModel

from app.services.tts_service import (
    generate_ai_voice,
)

from app.services.call_orchestrator import (
    process_audio_stream,
    close_call_session,
)


router = APIRouter(
    prefix="/voice",
    tags=[
        "Voice",
    ],
)


# ==================================================
# REQUEST MODEL
# ==================================================

class VoiceRequest(BaseModel):

    text: str


# ==================================================
# TEXT → VOICE TEST ENDPOINT
# ==================================================

@router.post(
    "/generate",
)
def generate_voice(

    request: VoiceRequest,

):

    audio = generate_ai_voice(

        request.text,

    )

    filename = (

        f"ai_voice_{uuid.uuid4()}.mp3"

    )

    filepath = (

        f"temp/{filename}"

    )

    with open(

        filepath,

        "wb",

    ) as file:

        file.write(

            audio,

        )

    return FileResponse(

        filepath,

        media_type="audio/mpeg",

        filename=filename,

    )


# ==================================================
# REAL-TIME CALL AUDIO STREAM
# ==================================================

@router.websocket(
    "/stream/{call_id}",
)
async def voice_stream(

    websocket: WebSocket,

    call_id: str,

):

    await websocket.accept()

    print(

        f"[VOICE] Stream started: {call_id}"

    )

    try:

        while True:

            # Receive PCM audio from Flutter/Android

            audio_chunk = await websocket.receive_bytes()

            # STT → AI → TTS

            ai_voice = await process_audio_stream(

                call_id,

                audio_chunk,

            )

            # Send AI voice back to device

            if ai_voice:

                await websocket.send_bytes(

                    ai_voice,

                )

    except WebSocketDisconnect:

        await close_call_session(

            call_id,

        )

        print(

            f"[VOICE] Stream ended: {call_id}"

        )

    except Exception as e:

        await close_call_session(

            call_id,

        )

        print(

            f"[VOICE ERROR] {e}"

        )

        await websocket.close()