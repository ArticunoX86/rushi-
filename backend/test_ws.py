import websocket
import sounddevice as sd
import time



# ==================================================
# CONFIG
# ==================================================

SAMPLE_RATE = 16000

CHANNELS = 1

BLOCK_SIZE = 3200





# ==================================================
# CONNECT WEBSOCKET
# ==================================================

ws = websocket.WebSocket()


ws.connect(

    "ws://127.0.0.1:8001/realtime/call/live123"

)



print(

    "Connected To AI Call Server"

)



print(

    "Speak now..."

)






# ==================================================
# MICROPHONE CALLBACK
# ==================================================

def callback(

    indata,

    frames,

    time_info,

    status,

):


    if status:


        print(

            status

        )



    audio_bytes = indata.tobytes()



    ws.send_binary(

        audio_bytes

    )








# ==================================================
# START LIVE AUDIO STREAM
# ==================================================

with sd.InputStream(

    samplerate=SAMPLE_RATE,

    channels=CHANNELS,

    dtype="int16",

    blocksize=BLOCK_SIZE,

    callback=callback,

):


    time.sleep(10)








# ==================================================
# CLOSE CALL
# ==================================================

ws.close()



print(

    "Call Ended"

)