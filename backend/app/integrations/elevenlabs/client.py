from elevenlabs.client import ElevenLabs
from app.core.config import settings

# ==================================================
# ELEVENLABS CLIENT
# ==================================================
client = ElevenLabs(
    api_key=settings.ELEVENLABS_API_KEY
)

# ==================================================
# TEXT TO SPEECH
# Returns: native MP3 audio bytes from ElevenLabs
# ==================================================
def text_to_speech(text: str):
    try:
        audio_stream = client.text_to_speech.convert(
            voice_id=settings.ELEVENLABS_VOICE_ID,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
            text=text,
        )

        audio_bytes = b""
        for chunk in audio_stream:
            if chunk:
                audio_bytes += chunk

        return audio_bytes

    except Exception as e:
        print("==============================")
        print("ElevenLabs Error:", e)
        print("==============================")
        return None