import asyncio
import websockets
import json
import sounddevice as sd
import numpy as np
import uuid
import sys
import pygame
import threading
import io

import requests

# ==========================================
# CONFIG
# ==========================================
BASE_URL = "http://127.0.0.1:8000"
WS_URL = "ws://127.0.0.1:8000/realtime/call"
AUTH_REGISTER = f"{BASE_URL}/auth/register"
AUTH_LOGIN = f"{BASE_URL}/auth/login"
LEADS_ENDPOINT = f"{BASE_URL}/leads"
SAMPLE_RATE = 16000
CHANNELS = 1

# ==========================================
# SETUP
# ==========================================
def setup_call_environment():
    """Registers a dummy user, logs in, creates a lead, and returns the lead."""
    print("🔧 Setting up the test environment...")
    dummy_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    dummy_password = "password123"
    dummy_phone = f"+1{uuid.uuid4().hex[:10].zfill(10)}"
    
    reg_res = requests.post(AUTH_REGISTER, json={
        "first_name": "Test", "last_name": "User",
        "email": dummy_email, "password": dummy_password, "phone": dummy_phone
    })
    if reg_res.status_code != 201:
        print("❌ Failed to register dummy user:", reg_res.text)
        sys.exit(1)
        
    login_res = requests.post(AUTH_LOGIN, data={
        "username": dummy_email, "password": dummy_password
    })
    if login_res.status_code != 200:
        print("❌ Failed to login dummy user:", login_res.text)
        sys.exit(1)
        
    token = login_res.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Fetch existing leads instead of creating a new one
    leads_res = requests.get(LEADS_ENDPOINT, headers=headers)
    if leads_res.status_code == 200:
        leads_list = leads_res.json()
        if len(leads_list) > 0:
            lead = leads_list[0]
            print(f"✅ Picked Existing Salesforce Lead: {lead['first_name']} {lead['last_name']} ({lead['id']})")
            return lead
    
    # Fallback to create dummy lead if none exist
    print("⚠️ No existing leads found. Creating a dummy lead...")
    lead_res = requests.post(LEADS_ENDPOINT, headers=headers, json={
        "first_name": "Alice", "last_name": "Smith",
        "phone": dummy_phone, "preferred_city": "Delhi"
    })
    if lead_res.status_code != 201:
        print("❌ Failed to create lead:", lead_res.text)
        sys.exit(1)
        
    lead = lead_res.json()
    print(f"✅ Dummy Lead Created: {lead['first_name']} {lead['last_name']} ({lead['id']})")
    return lead

# ==========================================
# STATE
# ==========================================
is_playing_audio = False  # To mute mic while AI is speaking

# ==========================================
# AUDIO OUTPUT (PYGAME)
# ==========================================
def init_audio():
    pygame.mixer.init()

def play_audio_bytes(audio_bytes):
    global is_playing_audio
    is_playing_audio = True
    
    # Save MP3 bytes to a temporary file
    temp_file = f"temp_ws_reply_{uuid.uuid4().hex[:6]}.mp3"
    try:
        with open(temp_file, "wb") as f:
            f.write(audio_bytes)
            
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        try:
            pygame.mixer.music.unload()
        except AttributeError:
            pass
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        is_playing_audio = False

# ==========================================
# WEBSOCKET CLIENT
# ==========================================
async def realtime_call(lead_id):
    call_id = str(uuid.uuid4())
    url = f"{WS_URL}/{call_id}?lead_id={lead_id}"
    
    print(f"🔌 Connecting to {url}...")
    
    try:
        async with websockets.connect(url) as ws:
            print("✅ Connected! Start speaking...")
            
            # --- Audio Capture Callback ---
            def audio_callback(indata, frames, time, status):
                if status:
                    print(status, file=sys.stderr)
                
                # Mute microphone while AI is speaking so it doesn't transcribe itself
                if not is_playing_audio:
                    # Convert float32 [-1.0, 1.0] to int16 PCM
                    pcm_data = (indata * 32767).astype(np.int16).tobytes()
                    
                    # Push to websocket loop safely
                    asyncio.run_coroutine_threadsafe(ws.send(pcm_data), loop)

            loop = asyncio.get_running_loop()
            
            # Start streaming microphone in the background
            stream = sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype='float32',
                callback=audio_callback
            )
            
            with stream:
                # --- WebSocket Receive Loop ---
                while True:
                    message = await ws.recv()
                    
                    if isinstance(message, str):
                        # JSON Message (Transcript or AI Text)
                        try:
                            data = json.loads(message)
                            msg_type = data.get("type")
                            
                            if msg_type == "transcript":
                                text = data.get("text", "")
                                is_final = data.get("is_final", False)
                                if is_final and text.strip():
                                    print(f"\n👨 You: {text}")
                                elif text.strip():
                                    print(f"   [listening...] {text}", end='\r')
                                    
                            elif msg_type == "ai_reply":
                                print(f"\n🤖 AI: {data.get('text')}")
                                
                            elif msg_type == "status":
                                print(f"ℹ️ Status: {data.get('message')}")
                                
                        except json.JSONDecodeError:
                            print(f"Received unknown string: {message}")
                            
                    elif isinstance(message, bytes):
                        # Audio Bytes (ElevenLabs MP3)
                        print(f"🔊 Playing AI Voice ({len(message)} bytes)...")
                        # Play in a background thread so it doesn't block the websocket receive loop
                        threading.Thread(target=play_audio_bytes, args=(message,), daemon=True).start()
                        
    except websockets.exceptions.ConnectionClosed:
        print("❌ Server disconnected.")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")

if __name__ == "__main__":
    try:
        requests.get(f"{BASE_URL}/health", timeout=5)
    except Exception as e:
        print(f"❌ Cannot connect to Backend at {BASE_URL}: {e}")
        sys.exit(1)
        
    lead = setup_call_environment()
    init_audio()
    try:
        asyncio.run(realtime_call(lead["id"]))
    except KeyboardInterrupt:
        print("\n🛑 Stopped realtime call.")
