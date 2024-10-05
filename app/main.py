import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, exceptions
from websockets.exceptions import ConnectionClosed
import numpy as np
from audio import AudioBuffer
import json
import time
import asyncio;
from transcribe import transcribe

app = FastAPI()

@app.websocket("/v1/realtime")
async def realtime_transcribe(ws: WebSocket):
    await ws.accept()
    print("Client connected")
    
    config = await ws.receive_json()
    print(config)

    audio_buffer = AudioBuffer()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(receive(ws, audio_buffer))

        async for trans in transcribe(audio_buffer):
            await ws.send_json(trans)

        await ws.send_json({"type": "close"})

        #await ws.close()

async def receive(ws: WebSocket, audio: AudioBuffer) -> None:
    bytes = b""
    while True:
        try:
            received = await ws.receive_bytes()
            bytes = bytes + received
            consumed = audio.append(bytes)
            if len(received) == 0:
                break
            bytes = bytes[consumed:]
        except WebSocketDisconnect:
            print("Client disconnected")
            await asyncio.sleep(10)
            break
        except ConnectionClosed:
            print("Connection closed")
            break
        except Exception as e:
            print(f"Error: {e}")
            #raise
    audio.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)