from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)
import uuid
import asyncio
from datetime import datetime

from app.models.enums import (
    CallStatus,
    CallDirection,
    MessageSender,
)
from app.services.call_orchestrator import (
    AICallOrchestrator,
)
from app.database.session import (
    SessionLocal,
)
from app.models.call import (
    Call,
)
from app.models.lead import (
    Lead,
)
from app.services.ai_service import (
    process_customer_message,
)
from app.schemas.ai import (
    AIChatRequest,
)
from app.services.tts_service import (
    generate_ai_voice,
)
from app.services.conversation_service import (
    save_message,
)
from app.schemas.conversation import (
    ConversationCreate,
)

# ==================================================
# GUARDRAIL IMPORTS
# ==================================================
from app.guardrails.call_timeout_manager import (
    register_call,
    increment_turn,
    is_call_expired,
    get_timeout_message,
    unregister_call,
    force_end_call,
)
from app.guardrails.call_state_machine import remove_state_machine
from app.guardrails.sentiment_analyzer import clear_call_sentiment


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
    lead_id: str = None,
):
    await websocket.accept()

    print("\nAI SESSION CREATED:", call_id)

    # ==================================================
    # GUARDRAIL: Register call with timeout manager
    # ==================================================
    register_call(call_id)
    print(f"[GUARDRAIL] Call {call_id} registered with timeout manager")

    loop = asyncio.get_running_loop()
    db = SessionLocal()
    lead_id = None
    dialog_lines = []
    orchestrator = None
    call_uuid = None

    try:
        # ==================================================
        # DATABASE INIT
        # ==================================================
        try:
            call_uuid = uuid.UUID(call_id)
        except ValueError:
            call_uuid = uuid.uuid4()

        db_call = (
            db.query(Call)
            .filter(
                Call.id == call_uuid
            )
            .first()
        )

        lead = None
        if lead_id:
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
        elif db_call and db_call.lead_id:
            lead = db.query(Lead).filter(Lead.id == db_call.lead_id).first()

        if not lead:
            lead = db.query(Lead).first()

        if not lead:
            lead = Lead(
                first_name="John",
                last_name="Doe",
                phone="1234567890",
                preferred_city="Mumbai",
                budget_max=10000000,
            )
            db.add(lead)
            db.commit()
            db.refresh(lead)

        lead_id = lead.id

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

        print("CALL READY:", call_uuid)

        # ==================================================
        # DEEPGRAM TRANSCRIPT CALLBACK
        # ==================================================
        async def on_transcript_callback(
            transcript: str,
            is_final: bool,
        ):
            try:
                print("CUSTOMER:", transcript)

                await websocket.send_json(
                    {
                        "type": "transcript",
                        "text": transcript,
                        "is_final": is_final,
                    }
                )

                if not is_final:
                    return

                # ======================================
                # GUARDRAIL: Check call timeout/turn limit
                # ======================================
                expired, reason = is_call_expired(call_id)
                if expired:
                    print(f"[GUARDRAIL] Call expired: {reason}")
                    timeout_msg = get_timeout_message(call_id)
                    
                    # Send graceful goodbye
                    await websocket.send_json({
                        "type": "ai_reply",
                        "text": timeout_msg,
                    })
                    audio = await loop.run_in_executor(None, generate_ai_voice, timeout_msg)
                    if audio:
                        await websocket.send_bytes(audio)
                    
                    # Log alert
                    try:
                        from app.api.supervisor_alerts import add_alert
                        add_alert(call_id, "timeout", reason, "WARNING")
                    except Exception:
                        pass
                    
                    # Close the connection
                    await asyncio.sleep(3)  # Let the goodbye play
                    await websocket.close()
                    return
                
                # Increment turn counter
                increment_turn(call_id)

                dialog_lines.append(f"Customer: {transcript}")

                # ======================================
                # SAVE CUSTOMER MESSAGE
                # ======================================
                try:
                    save_message(
                        db,
                        ConversationCreate(
                            call_id=call_uuid,
                            sender=MessageSender.CUSTOMER,
                            message=transcript,
                        ),
                    )
                    print("CUSTOMER MESSAGE SAVED")
                except Exception as e:
                    print("CUSTOMER SAVE ERROR:", e)

                # ======================================
                # GEMINI AI
                # ======================================
                try:
                    print("🧠 SENDING TO GEMINI...")
                    ai_response = await loop.run_in_executor(
                        None,
                        process_customer_message,
                        db,
                        AIChatRequest(
                            lead_id=lead_id,
                            call_id=call_uuid,
                            message=transcript,
                        ),
                    )
                    reply_text = ai_response.reply
                    print("🧠 GEMINI RESPONSE RECEIVED")
                except Exception as e:
                    print("GEMINI ERROR:", e)
                    reply_text = "Sorry, can you please repeat that?"

                print("AI RESPONSE:", reply_text)

                dialog_lines.append(f"AI: {reply_text}")

                # ======================================
                # SAVE AI MESSAGE
                # ======================================
                try:
                    save_message(
                        db,
                        ConversationCreate(
                            call_id=call_uuid,
                            sender=MessageSender.AI,
                            message=reply_text,
                        ),
                    )
                    print("AI MESSAGE SAVED")
                except Exception as e:
                    print("AI SAVE ERROR:", e)

                # SEND AI TEXT TO CLIENT
                await websocket.send_json(
                    {
                        "type": "ai_reply",
                        "text": reply_text,
                    }
                )

                # ======================================
                # ELEVENLABS TTS
                # ======================================
                audio = await loop.run_in_executor(
                    None,
                    generate_ai_voice,
                    reply_text,
                )

                if audio:
                    print("VOICE GENERATED:", len(audio))
                    await websocket.send_bytes(audio)

            except Exception as e:
                print("CALLBACK ERROR:", e)

        # ==================================================
        # START ORCHESTRATOR
        # ==================================================
        orchestrator = AICallOrchestrator(
            call_id=str(call_uuid),
            on_transcript=on_transcript_callback,
        )

        await orchestrator.start()

        await websocket.send_json(
            {
                "type": "status",
                "message": "Deepgram connected — speak now!",
            }
        )

        # Wait 1.5 seconds for call line connection to settle, then speak welcome greeting
        await asyncio.sleep(1.5)
        try:
            greeting_name = lead.first_name if (lead and lead.first_name and lead.first_name != "string") else "there"
            city_name = lead.preferred_city if (lead and lead.preferred_city and lead.preferred_city.lower() != "string") else "the area"
            
            # Fetch active voice agent to get the dynamic first_message
            from app.models.voice_agent import VoiceAgent
            active_agent = db.query(VoiceAgent).filter(VoiceAgent.is_active == True).first()
            
            if active_agent and active_agent.first_message:
                intro_text = active_agent.first_message.replace("{lead_name}", greeting_name).replace("{city}", city_name)
            else:
                intro_text = f"Hi {greeting_name}, how's it going? I'm calling because I saw you looking at some properties recently. Are you still searching for a place in {city_name}?"
            
            save_message(
                db,
                ConversationCreate(
                    call_id=call_uuid,
                    sender=MessageSender.AI,
                    message=intro_text,
                ),
            )
            dialog_lines.append(f"AI: {intro_text}")

            await websocket.send_json(
                {
                    "type": "ai_reply",
                    "text": intro_text,
                }
            )

            audio_bytes = await loop.run_in_executor(
                None,
                generate_ai_voice,
                intro_text,
            )
            if audio_bytes:
                print("INTRO VOICE GENERATED:", len(audio_bytes))
                await websocket.send_bytes(audio_bytes)
                
        except Exception as e:
            print("Error generating welcome message:", e)

        # ==================================================
        # AUDIO STREAMING LOOP
        # ==================================================
        while True:
            audio = await websocket.receive_bytes()
            await orchestrator.process_audio_chunk(audio)

    except WebSocketDisconnect:
        print("CLIENT DISCONNECTED")
    except Exception as e:
        print("REALTIME CALL ERROR:", e)
    finally:
        print("CLEANING UP CALL...")

        # ==================================================
        # GUARDRAIL: Clean up all per-call state
        # ==================================================
        unregister_call(call_id)
        remove_state_machine(call_id)
        clear_call_sentiment(call_id)
        print(f"[GUARDRAIL] Cleaned up guardrail state for call {call_id}")

        if orchestrator:
            try:
                await orchestrator.close()
            except Exception as oe:
                print("Error closing orchestrator:", oe)

        if db and call_uuid:
            try:
                db_call = (
                    db.query(Call)
                    .filter(
                        Call.id == call_uuid
                    )
                    .first()
                )

                if db_call:
                    db_call.status = CallStatus.COMPLETED
                    db_call.end_time = datetime.utcnow()
                    db_call.transcript = "\n".join(dialog_lines)

                    if orchestrator.recording_url:
                        db_call.recording_url = orchestrator.recording_url

                    db.commit()
                    print("CALL SAVED")

                from app.services.device_connection_manager import device_manager
                await device_manager.broadcast_all({
                    "action": "CALL_ENDED",
                    "event": "CALL_ENDED",
                    "payload": {
                        "call_id": str(call_uuid),
                        "status": "COMPLETED"
                    }
                })

            except Exception as e:
                print("FINAL SAVE ERROR:", e)
            finally:
                db.close()
                print("DB SESSION CLOSED")

        print("AI SESSION CLOSED:", call_id)