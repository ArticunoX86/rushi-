from fastapi import WebSocket


class DeviceConnectionManager:

    def __init__(self):

        self.active_devices = {}

    # ==================================================
    # CONNECT DEVICE
    # ==================================================

    async def connect(

        self,

        device_id: str,

        websocket: WebSocket,

    ):

        await websocket.accept()

        self.active_devices[device_id] = websocket

        print(f"[DEVICE CONNECTED] {device_id}")

        print(f"[CONNECTED DEVICES] {list(self.active_devices.keys())}")

    # ==================================================
    # DISCONNECT DEVICE
    # ==================================================

    def disconnect(

        self,

        device_id: str,

    ):

        if device_id in self.active_devices:

            del self.active_devices[device_id]

            print(f"[DEVICE DISCONNECTED] {device_id}")

            print(f"[CONNECTED DEVICES] {list(self.active_devices.keys())}")

    # ==================================================
    # SEND COMMAND TO DEVICE
    # ==================================================

    async def send_command(

        self,

        device_id: str,

        command: dict,

    ):

        print("\n" + "=" * 60)
        print("[DEVICE MANAGER]")
        print(f"Connected Devices : {list(self.active_devices.keys())}")
        print(f"Requested Device  : {device_id}")
        print("=" * 60)

        websocket = self.active_devices.get(device_id)

        if websocket:

            print("[DEVICE MANAGER] Device found.")
            print("[DEVICE MANAGER] Sending command...")

            await websocket.send_json(command)

            print("[DEVICE MANAGER] Command sent successfully.\n")

            return True

        print("[DEVICE MANAGER] Device NOT FOUND!\n")

        return False

    # ==================================================
    # BROADCAST TO ALL CONNECTED DEVICES/CLIENTS
    # ==================================================

    async def broadcast_all(self, data: dict):
        for device_id, ws in list(self.active_devices.items()):
            try:
                await ws.send_json(data)
                print(f"[BROADCAST SUCCESS] Sent {data.get('action')} to {device_id}")
            except Exception as e:
                print(f"[BROADCAST ERROR] Failed sending to {device_id}: {e}")


device_manager = DeviceConnectionManager()