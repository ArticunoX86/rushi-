from cartesia import Cartesia
from app.core.config import settings

# ==================================================
# CARTESIA CLIENT
# ==================================================
try:
    client = Cartesia(api_key=settings.CARTESIA_API_KEY)
except Exception as e:
    print("Warning: Cartesia API Key not configured correctly.", e)
    client = None

# ==================================================
# TEXT TO SPEECH (Cartesia Sonic)
# Returns: native MP3 audio bytes
# ==================================================
def text_to_speech(text: str):
    if not client:
        print("Cartesia client not initialized. Cannot generate voice.")
        return None
        
    try:
        # Cartesia expects output configuration
        response = client.tts.generate(
            model_id="sonic-latest",
            transcript=text,
            voice={"mode": "id", "id": settings.CARTESIA_VOICE_ID},
            output_format={
                "container": "mp3",
                "encoding": "mp3",
                "sample_rate": 44100
            }
        )
        return response.read()

    except Exception as e:
        print("==============================")
        print("Cartesia TTS Error:", e)
        print("==============================")
        return None
