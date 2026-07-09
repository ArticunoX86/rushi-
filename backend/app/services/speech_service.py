from app.integrations.deepgram.client import (
    speech_to_text,
)



# ==================================================
# VOICE PROCESSING SERVICE
# ==================================================

def process_audio(
    audio_url: str,
):


    transcript = speech_to_text(
        audio_url
    )


    return {
        "transcript": transcript
    }