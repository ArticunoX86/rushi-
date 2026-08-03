import websocket
import json
import time


DEVICE_ID = "pixel_6a_001"


ws = websocket.WebSocket()


ws.connect(
    f"ws://127.0.0.1:8000/device/connect/{DEVICE_ID}"
)


print("Android device connected 📱")


while True:

    message = ws.recv()

    print(
        "Command received:",
        message
    )


    time.sleep(1)