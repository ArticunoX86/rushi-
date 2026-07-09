import io
import wave
import numpy as np

from app.integrations.deepgram.live import DeepgramLiveClient
from app.integrations.aws.s3_client import upload_audio_file

CUSTOMER_RATE = 16000
VOLUME_MULTIPLIER = 3.5  # Gain multiplier to boost microphone volume

class AICallOrchestrator:
    def __init__(self, call_id: str, on_transcript=None):
        self.call_id = call_id
        self.deepgram = DeepgramLiveClient(on_transcript=on_transcript)
        self.audio_chunks = []           # Customer chunks (16kHz, 16-bit mono)
        self.recording_url = None
        print(f"[ORCHESTRATOR] Session created: {call_id}")

    async def start(self):
        await self.deepgram.start()

    async def process_audio_chunk(self, audio_chunk: bytes):
        self.audio_chunks.append(audio_chunk)
        await self.deepgram.send_audio(audio_chunk)

    def add_ai_audio(self, pcm_data: bytes):
        pass

    async def close(self):
        print("[ORCHESTRATOR] Closing session...")
        await self.deepgram.close()

        if not self.audio_chunks:
            print("[ORCHESTRATOR] No audio captured — skipping recording.")
            return

        try:
            # Reconstruct the customer audio
            raw_bytes = b"".join(self.audio_chunks)
            
            # Boost the volume safely using numpy
            audio_data = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32)
            audio_data = audio_data * VOLUME_MULTIPLIER
            
            # Clip values to prevent overflow distortion and convert back to 16-bit
            audio_data = np.clip(audio_data, -32768, 32767).astype(np.int16)
            boosted_bytes = audio_data.tobytes()

            # Save to WAV format
            wav_io = io.BytesIO()
            with wave.open(wav_io, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2) # 16-bit
                wav_file.setframerate(CUSTOMER_RATE)
                wav_file.writeframes(boosted_bytes)

            wav_data = wav_io.getvalue()
            
            # Upload WAV to S3
            self.recording_url = upload_audio_file(
                audio_bytes=wav_data,
                call_id=self.call_id,
                extension="wav",
                content_type="audio/wav"
            )
            print(f"[ORCHESTRATOR] AWS recording saved with boosted volume (WAV): {self.recording_url}")
        except Exception as e:
            print(f"[ORCHESTRATOR] Recording upload failed: {e}")