from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)
import uuid
import asyncio
import json
from datetime import datetime
from app.models.enums import CallStatus, CallDirection

from app.services.call_orchestrator import (
    AICallOrchestrator,
)
from app.database.session import SessionLocal
from app.models.call import Call
from app.models.lead import Lead
from app.services.ai_service import process_customer_message
from app.schemas.ai import AIChatRequest
from app.services.tts_service import generate_ai_voice


router = APIRouter(

    prefix="/realtime",

    tags=[
        "Realtime AI Call"
    ],

)



# ==================================================
# REALTIME CALL SOCKET
# ==================================================

@router.websocket(
    "/call/{call_id}"
)
async def realtime_call(

    websocket: WebSocket,

    call_id: str,

):

    await websocket.accept()

    print(f"\n{'='*50}")
    print(f"[REALTIME] WebSocket connected: {call_id}")
    print(f"{'='*50}\n")

    loop = asyncio.get_running_loop()

    # ── Optional DB setup (don't crash if DB is down) ──
    db          = None
    lead_id     = None
    call_uuid   = None
    dialog_lines = []

    try:
        db = SessionLocal()

        lead = db.query(Lead).first()
        if not lead:
            lead = Lead(
                first_name="John",
                last_name="Doe",
                phone="1234567890",
                preferred_city="Mumbai",
                budget_max=10000000
            )
            db.add(lead)
            db.commit()
            db.refresh(lead)

        lead_id = lead.id
        print(f"[REALTIME] Lead: {lead.first_name} {lead.last_name} (id={lead.id})")

        # Parse / create call UUID
        try:
            call_uuid = uuid.UUID(call_id)
        except ValueError:
            call_uuid = uuid.uuid4()

        db_call = db.query(Call).filter(Call.id == call_uuid).first()
        if not db_call:
            db_call = Call(
                id=call_uuid,
                lead_id=lead.id,
                direction=CallDirection.OUTBOUND,
                status=CallStatus.IN_PROGRESS,
            )
            db.add(db_call)
            db.commit()
            db.refresh(db_call)

        print(f"[REALTIME] Call record ready: {call_uuid}")

    except Exception as db_err:
        print(f"[REALTIME] ⚠️  DB unavailable ({db_err}) — running without DB")
        call_uuid = uuid.uuid4()


    # ==================================================
    # TRANSCRIPT CALLBACK
    # ==================================================

    async def on_transcript_callback(transcript: str, is_final: bool):
        try:
            label = "FINAL" if is_final else "interim"
            print(f"[TRANSCRIPT] {label}: {transcript}")

            # ── Always send transcript to client ──
            await websocket.send_json({
                "type":     "transcript",
                "text":     transcript,
                "is_final": is_final,
            })

            # ── AI pipeline only on final ──
            if is_final:
                dialog_lines.append(f"Customer: {transcript}")

                if db and lead_id:
                    ai_response = await loop.run_in_executor(
                        None,
                        process_customer_message,
                        db,
                        AIChatRequest(
                            lead_id=lead_id,
                            call_id=call_uuid,
                            message=transcript
                        )
                    )
                    reply_text = ai_response.reply
                else:
                    reply_text = "I've received your message. Thank you."

                print(f"[AI REPLY]: {reply_text}")
                dialog_lines.append(f"AI: {reply_text}")

                await websocket.send_json({
                    "type": "ai_reply",
                    "text": reply_text,
                })

                audio = await loop.run_in_executor(
                    None,
                    generate_ai_voice,
                    reply_text
                )

                if audio:
                    print(f"[TTS] Sending {len(audio)} bytes of MP3 audio to client")
                    await websocket.send_bytes(audio)

        except Exception as ex:
            print(f"[REALTIME] Callback error: {ex}")


    # ==================================================
    # START DEEPGRAM + LISTEN
    # ==================================================

    orchestrator = AICallOrchestrator(
        call_id=str(call_uuid),
        on_transcript=on_transcript_callback
    )

    await orchestrator.start()

    # Tell the client Deepgram is live
    await websocket.send_json({
        "type":    "status",
        "message": "Deepgram connected — speak now!",
    })

    print("[REALTIME] Deepgram live — waiting for audio...")

    try:
        while True:
            audio_chunk = await websocket.receive_bytes()
            await orchestrator.process_audio_chunk(audio_chunk)

    except WebSocketDisconnect:
        print(f"\n[REALTIME] Client disconnected: {call_id}")
    except Exception as e:
        print(f"\n[REALTIME] Error: {e}")
    finally:
        await orchestrator.close()

        # ── Save call to DB if available ──
        if db and call_uuid:
            try:
                db_call = db.query(Call).filter(Call.id == call_uuid).first()
                if db_call:
                    if orchestrator.recording_url:
                        db_call.recording_url = orchestrator.recording_url
                    if dialog_lines:
                        db_call.transcript = "\n".join(dialog_lines)
                    db_call.status = CallStatus.COMPLETED
                    db_call.end_time = datetime.utcnow()
                    total_bytes = sum(len(c) for c in orchestrator.audio_chunks)
                    db_call.duration_seconds = int(total_bytes / 32000)
                    db.commit()
                    print(f"[REALTIME] Saved to DB | Duration: {db_call.duration_seconds}s | S3: {orchestrator.recording_url}")
            except Exception as dbe:
                print(f"[REALTIME] DB save error: {dbe}")
            finally:
                db.close()

        print(f"[REALTIME] Session closed: {call_id}")