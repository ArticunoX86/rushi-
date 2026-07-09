from app.integrations.elevenlabs.client import (
    text_to_speech,
)

# ==================================================
# GENERATE AI VOICE
# Returns: mp3 audio bytes
# ==================================================
def generate_ai_voice(text: str):
    return text_to_speech(text)