import io
import wave
from app.integrations.deepgram.live import DeepgramLiveClient
from app.integrations.aws.s3_client import upload_audio_file

class AICallOrchestrator:
    def __init__(self, call_id: str, on_transcript=None):
        self.call_id = call_id
        self.deepgram = DeepgramLiveClient(on_transcript=on_transcript)
        self.audio_chunks = []
        self.recording_url = None
        print("AI SESSION CREATED:", call_id)

    async def start(self):
        await self.deepgram.start()

    async def process_audio_chunk(self, audio_chunk: bytes):
        self.audio_chunks.append(audio_chunk)
        await self.deepgram.send_audio(audio_chunk)

    async def close(self):
        print("Closing AI Call...")
        try:
            await self.deepgram.close()
        except Exception as e:
            print("Error closing Deepgram:", e)
        
        print("Total chunks:", len(self.audio_chunks))
        if self.audio_chunks:
            try:
                raw_pcm = b"".join(self.audio_chunks)
                if len(raw_pcm) > 0:
                    print("Compiling call recording:", len(raw_pcm), "pcm bytes")
                    # Convert raw PCM to WAV container
                    wav_io = io.BytesIO()
                    with wave.open(wav_io, 'wb') as wav_file:
                        wav_file.setnchannels(1)
                        wav_file.setsampwidth(2) # 16-bit
                        wav_file.setframerate(16000) # 16kHz
                        wav_file.writeframes(raw_pcm)
                    wav_bytes = wav_io.getvalue()
                    
                    self.recording_url = upload_audio_file(
                        audio_bytes=wav_bytes,
                        call_id=self.call_id,
                        extension="wav",
                        content_type="audio/wav"
                    )
                    print("AWS RECORDING SAVED:", self.recording_url)
            except Exception as e:
                print("AWS UPLOAD FAILED:", e)
        else:
            print("NO AUDIO FOUND")
            
        print("AI SESSION CLOSED:", self.call_id)


async def process_audio_stream(call_id: str, audio_chunk: bytes) -> bytes | None:
    """Stub helper function for voice streaming endpoint in voice.py"""
    print(f"process_audio_stream called: call_id={call_id}, chunk_len={len(audio_chunk)}")
    return None


async def close_call_session(call_id: str):
    """Stub helper function for voice streaming endpoint in voice.py"""
    print(f"close_call_session called: call_id={call_id}")