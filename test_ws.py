import asyncio
import websockets

async def test():
    try:
        async with websockets.connect('ws://127.0.0.1:8000/api/v1/stream/cognitive') as ws:
            print("Connected!")
            message = await ws.recv()
            print("Received:", message[:100])
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test())
