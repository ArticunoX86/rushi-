import asyncio
import os
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, VoicePipelineAgent
from livekit.plugins import deepgram, elevenlabs, google
from app.core.config import settings

async def entrypoint(ctx: JobContext):
    """
    LiveKit WebRTC AI Voice Agent worker entrypoint.
    Auto-connects to newly assigned rooms and runs real-time STT -> LLM -> TTS pipeline.
    """
    print(f"🤖 WebRTC AI Agent joining room: {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Initialize Voice Pipeline Agent (Deepgram STT -> Gemini LLM -> ElevenLabs TTS)
    stt_provider = deepgram.STT(
        api_key=settings.DEEPGRAM_API_KEY,
        model="nova-2-general",
        language="en-US"
    )
    
    llm_provider = google.LLM(
        api_key=settings.GEMINI_API_KEY,
        model="gemini-2.5-flash"
    )
    
    tts_provider = elevenlabs.TTS(
        api_key=settings.ELEVENLABS_API_KEY,
        voice_id=settings.ELEVENLABS_VOICE_ID
    )

    agent = VoicePipelineAgent(
        stt=stt_provider,
        llm=llm_provider,
        tts=tts_provider,
    )

    agent.start(ctx.room)
    await agent.say(
        "Hello! I am your Real Estate AI Assistant. How can I help you find your dream property today?",
        allow_interruptions=True
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
