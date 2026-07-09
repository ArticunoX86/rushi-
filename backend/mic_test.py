import websocket
import sounddevice as sd
import threading
import pygame
import time
import json
import sys



# ==================================================
# CONFIG
# ==================================================

SAMPLE_RATE = 16000

CHANNELS = 1

BLOCK_SIZE = 3200


BACKEND_WS_URL = "ws://127.0.0.1:8000/realtime/call/live123"


# ==================================================
# DETECT BEST INPUT DEVICE  (mono-capable)
# ==================================================

def find_input_device():
    """Pick the best available input device."""
    devices    = sd.query_devices()
    default_in = sd.default.device[0]

    if devices[default_in]["max_input_channels"] >= 1:
        print(f"[MIC] Input: [{default_in}] {devices[default_in]['name']}")
        return default_in, 1

    for i, dev in enumerate(devices):
        if dev["max_input_channels"] >= 1:
            print(f"[MIC] Input: [{i}] {dev['name']}")
            return i, 1

    print("[MIC] ❌ No input device found!")
    sys.exit(1)


INPUT_DEVICE, CHANNELS = find_input_device()



# ==================================================
# CONNECT WEBSOCKET TO BACKEND
# ==================================================

ws = websocket.WebSocket()

ws.connect(BACKEND_WS_URL)

print("🎙️  Connected to AI Agent backend")
print("=" * 50)



# ==================================================
# AI AUDIO PLAYER
# ==================================================

pygame.mixer.init()



# ==================================================
# RECEIVE MESSAGES FROM BACKEND
# ==================================================

def receive_loop():

    while True:
        try:
            response = ws.recv()


            # ──────────────────────────────────────
            # AI VOICE AUDIO  (bytes)
            # ──────────────────────────────────────
            if isinstance(response, bytes):

                sys.stdout.write("\r\033[K")   # clear current line
                print(f"\n🔊  AI audio received ({len(response)} bytes)")

                # Unload previous music from pygame mixer to avoid Permission Denied locking
                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                except Exception:
                    pass

                # Safely write the file with retry fallback
                success = False
                for _ in range(3):
                    try:
                        with open("ai_response.mp3", "wb") as f:
                            f.write(response)
                        success = True
                        break
                    except IOError:
                        time.sleep(0.1)

                if success:
                    try:
                        pygame.mixer.music.load("ai_response.mp3")
                        pygame.mixer.music.play()
                        print("🔊  AI speaking...\n")
                    except Exception as play_err:
                        print(f"Error playing audio: {play_err}")
                else:
                    print("⚠️ Could not write AI audio file (locked by system)")


                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)


            # ──────────────────────────────────────
            # JSON MESSAGE  (transcript / ai_reply / status)
            # ──────────────────────────────────────
            else:
                try:
                    data = json.loads(response)
                    msg_type = data.get("type", "")


                    # ── Live transcription ──────────────────
                    if msg_type == "transcript":

                        text     = data.get("text", "").strip()
                        is_final = data.get("is_final", False)

                        if text:
                            if is_final:
                                # Final: clear interim line, print permanently
                                sys.stdout.write("\r\033[K")
                                print(f"✅  You said: {text}")
                                sys.stdout.flush()
                            else:
                                # Interim: overwrite same line
                                preview = text[:80]
                                sys.stdout.write(f"\r🎙️  {preview}   ")
                                sys.stdout.flush()


                    # ── AI text reply ────────────────────────
                    elif msg_type == "ai_reply":

                        text = data.get("text", "").strip()
                        sys.stdout.write("\r\033[K")
                        print(f"\n🤖  AI: {text}\n")
                        sys.stdout.flush()


                    # ── Backend status messages ──────────────
                    elif msg_type == "status":

                        msg = data.get("message", "")
                        print(f"\n[BACKEND] {msg}")


                except Exception:
                    pass

        except Exception as e:
            sys.stdout.write("\r\033[K")
            print(f"\n[Receiver] closed: {e}")
            break



receiver_thread = threading.Thread(
    target=receive_loop,
    daemon=True,
)
receiver_thread.start()



# ==================================================
# MICROPHONE CALLBACK
# ==================================================

chunk_count = [0]

def mic_callback(
    indata,
    frames,
    time_info,
    status,
):
    if status:
        print(f"[MIC STATUS] {status}")

    chunk_count[0] += 1

    # Log every 5 seconds to confirm audio is flowing
    if chunk_count[0] % 25 == 1:
        print(f"\n[MIC] Streaming... chunk #{chunk_count[0]}  ({len(indata.tobytes())} bytes)")

    try:
        ws.send_binary(indata.tobytes())
    except Exception as e:
        print(f"[MIC SEND ERROR] {e}")



# ==================================================
# START MICROPHONE STREAM
# ==================================================

print("\nSpeak now 🎙️  — Press Ctrl+C to stop\n")

try:
    with sd.InputStream(
        device     = INPUT_DEVICE,
        samplerate = SAMPLE_RATE,
        channels   = CHANNELS,
        dtype      = "int16",
        blocksize  = BLOCK_SIZE,
        callback   = mic_callback,
    ):
        while True:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\nStopping call...")



# ==================================================
# CLOSE
# ==================================================

time.sleep(0.5)
ws.close()
print("Stopped ✅")