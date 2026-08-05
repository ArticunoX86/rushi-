import requests
import uuid
import sys
import time
import os
import wave
import numpy as np

# Make sure these libraries are installed:
# pip install requests sounddevice numpy pygame
try:
    import sounddevice as sd
    import pygame
except ImportError:
    print("Missing required libraries. Please run:")
    print("pip install requests sounddevice numpy pygame")
    sys.exit(1)

# Configuration
BASE_URL = "http://127.0.0.1:8000"
AUTH_REGISTER = f"{BASE_URL}/auth/register"
AUTH_LOGIN = f"{BASE_URL}/auth/login"
LEADS_ENDPOINT = f"{BASE_URL}/leads"
CHAT_ENDPOINT = f"{BASE_URL}/ai/chat"
VOICE_GENERATE = f"{BASE_URL}/voice/generate"
SPEECH_TRANSCRIBE = f"{BASE_URL}/speech/transcribe-file"

SAMPLE_RATE = 16000
CHANNELS = 1

def init_audio_player():
    pygame.mixer.init()

def play_mp3(filepath):
    """Plays an MP3 file using pygame."""
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    try:
        pygame.mixer.music.unload()
    except AttributeError:
        pass # Older pygame versions don't have unload

def record_audio_to_wav(filename="temp_mic.wav", duration=5):
    """Records audio from the microphone for a fixed duration."""
    print(f"\n🎙️ Recording for {duration} seconds... Speak now!")
    recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
    sd.wait()
    print("🛑 Recording finished.")
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(recording.tobytes())
    return filename

def setup_call_environment():
    """Registers a dummy user, logs in, creates a lead, and returns the lead & token."""
    print("🔧 Setting up the test environment...")
    
    # 1. Register User
    dummy_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    dummy_password = "password123"
    dummy_phone = f"+1{uuid.uuid4().hex[:10].zfill(10)}"
    
    reg_res = requests.post(AUTH_REGISTER, json={
        "first_name": "Test",
        "last_name": "User",
        "email": dummy_email,
        "password": dummy_password,
        "phone": dummy_phone
    })
    
    if reg_res.status_code != 201:
        print("❌ Failed to register dummy user:", reg_res.text)
        sys.exit(1)
    
    # 2. Login User
    login_res = requests.post(AUTH_LOGIN, data={
        "username": dummy_email,
        "password": dummy_password
    })
    
    if login_res.status_code != 200:
        print("❌ Failed to login dummy user:", login_res.text)
        sys.exit(1)
        
    token = login_res.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create Lead
    lead_res = requests.post(LEADS_ENDPOINT, headers=headers, json={
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+15550100",
        "preferred_city": "Mumbai"
    })
    
    if lead_res.status_code != 201:
        print("❌ Failed to create lead:", lead_res.text)
        sys.exit(1)
        
    lead = lead_res.json()
    print(f"✅ Lead Created: {lead['first_name']} {lead['last_name']} ({lead['id']})")
    
    return lead['id'], lead['first_name']


def simulate_voice_call():
    init_audio_player()
    
    # Step 1: Setup
    lead_id, first_name = setup_call_environment()
    call_id = str(uuid.uuid4())
    
    print("\n======================================================")
    print("📞 REALTIME VOICE AI CALL SIMULATION")
    print("======================================================")
    
    # AI Starts the Conversation
    intro_text = f"Hello! Am I speaking with {first_name}?"
    print(f"🤖 AI Agent: {intro_text}")
    
    # Generate Voice for Intro
    intro_audio_file = f"temp_ai_reply_{uuid.uuid4().hex[:6]}.mp3"
    voice_res = requests.post(VOICE_GENERATE, json={"text": intro_text})
    if voice_res.status_code == 200:
        with open(intro_audio_file, "wb") as f:
            f.write(voice_res.content)
        play_mp3(intro_audio_file)
    
    # Conversation Loop
    while True:
        try:
            # 1. Record customer audio
            wav_file = record_audio_to_wav(duration=6)
            
            # 2. STT: Transcribe Audio
            print("⏳ Transcribing audio (STT)...")
            with open(wav_file, "rb") as f:
                stt_res = requests.post(SPEECH_TRANSCRIBE, files={"file": f})
                
            if stt_res.status_code != 200:
                print("❌ STT Error:", stt_res.text)
                continue
                
            transcript = stt_res.json().get("transcript", "")
            if not transcript.strip():
                print("⚠️ Silence detected. Try again.")
                continue
                
            print(f"👨 Customer: {transcript}")
            
            # 3. AI Brain: Get Response
            print("⏳ Generating AI response (LLM)...")
            ai_res = requests.post(CHAT_ENDPOINT, json={
                "lead_id": lead_id,
                "call_id": call_id,
                "message": transcript
            })
            
            if ai_res.status_code != 200:
                print("❌ AI Error:", ai_res.text)
                continue
                
            ai_data = ai_res.json()
            ai_reply = ai_data.get("reply", "")
            print(f"🤖 AI Agent: {ai_reply}")
            
            # 4. TTS: Generate Audio
            print("⏳ Synthesizing speech (TTS)...")
            reply_audio_file = f"temp_ai_reply_{uuid.uuid4().hex[:6]}.mp3"
            tts_res = requests.post(VOICE_GENERATE, json={"text": ai_reply})
            if tts_res.status_code == 200:
                with open(reply_audio_file, "wb") as f:
                    f.write(tts_res.content)
                play_mp3(reply_audio_file)
                
        except KeyboardInterrupt:
            print("\nEnding simulated call.")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            break

if __name__ == "__main__":
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print("✅ Backend is connected and healthy.")
    except Exception as e:
        print(f"❌ Cannot connect to Backend at {BASE_URL}: {e}")
        sys.exit(1)
        
    simulate_voice_call()
