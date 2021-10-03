import asyncio
import websockets

async def test():
    async with websockets.connect("ws://localhost:8765/register2") as websocket:
        await websocket.send("Hello world!")
        r = await websocket.recv()
        print(f"{r=}")

asyncio.run(test())