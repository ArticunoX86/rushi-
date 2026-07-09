from sqlalchemy.orm import Session


from app.schemas.ai import (
    AIChatRequest,
)


from app.services.speech_service import (
    process_audio,
)


from app.services.ai_service import (
    process_customer_message,
)


from app.services.tts_service import (
    generate_ai_voice,
)



# ==================================================
# COMPLETE AI VOICE AGENT PIPELINE
# ==================================================

def process_voice_conversation(

    db: Session,

    audio_url: str,

    lead_id,

    call_id,

):


    # ==================================================
    # STEP 1
    # AUDIO -> TEXT (DEEPGRAM)
    # ==================================================

    transcript_response = process_audio(

        audio_url

    )


    if not transcript_response:


        return {

            "error":

            "Unable to understand audio"

        }



    transcript = transcript_response[

        "transcript"

    ]



    print(

        "CUSTOMER:",

        transcript

    )



    # ==================================================
    # STEP 2
    # TEXT -> AI BRAIN
    # ==================================================

    ai_response = process_customer_message(

        db,

        AIChatRequest(

            lead_id=lead_id,

            call_id=call_id,

            message=transcript,

        ),

    )



    print(

        "AI RESPONSE:",

        ai_response.reply

    )



    # ==================================================
    # STEP 3
    # TEXT -> VOICE
    # ==================================================

    audio = generate_ai_voice(

        ai_response.reply

    )



    # ==================================================
    # FINAL RESPONSE
    # ==================================================

    return {


        "customer_text":

            transcript,


        "ai_reply":

            ai_response.reply,


        "audio":

            audio,

    }