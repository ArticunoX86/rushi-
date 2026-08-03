import asyncio
import websockets


async def test():

    uri = (
        "ws://127.0.0.1:8000"
        "/voice/stream/test-call-001"
    )


    async with websockets.connect(uri) as websocket:


        print(
            "Connected to AI voice stream"
        )


        with open(
            "test.wav",
            "rb"
        ) as f:


            audio = f.read()


        await websocket.send(
            audio
        )


        response = await websocket.recv()


        with open(
            "ai_reply.mp3",
            "wb"
        ) as f:


            f.write(
                response
            )


        print(
            "AI response saved: ai_reply.mp3"
        )



asyncio.run(
    test()
)