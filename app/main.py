import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import numpy as np
from audio import AudioBuffer
from model import transcribe
import json
import time
import asyncio;

app = FastAPI()

@app.websocket("/v1/realtime")
async def realtime_transcribe(ws: WebSocket):
    await ws.accept()
    print("Client connected")
    
    config = await ws.receive_json()
    print(config)

    start = time.time()

    audio_buffer = AudioBuffer()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(receive(ws, audio_buffer))

        prev_transcribe_duration = 0
        initial_prompt = ","
        while True:
            min_duration = max(1.5, prev_transcribe_duration + 0.5)
            chunk, duration, closed = await audio_buffer.chunk(min_duration)

            result = transcribe(chunk, initial_prompt=initial_prompt, word_timestamps=False)
            time_stamp = time.time() - start
            prev_transcribe_duration = duration
            #print(f"{duration}: {result}")

            if closed:
                text = result["text"]
                print(f"{duration}: recognized: {text}")
                break
            
            if len(result["segments"]) > 1:
                segment = result["segments"][0]
                end = segment["end"]
                audio_buffer.truncate(end)
                prev_transcribe_duration = 0
                text = segment["text"]
                initial_prompt = text
                print(f"{time_stamp}: recognized: {text}")
            else:
                text = result["text"]
                print(f"{time_stamp}: recognizing: {text}")
                
            prev_transcribe_duration = audio_buffer.duration

        #await ws.send_text(f"Received {audio_buffer.duration} secs, {size} bytes")
    
    #print(f"Received {audio_buffer.duration} secs, {size} bytes")

async def receive(ws: WebSocket, audio: AudioBuffer) -> None:
    bytes = b""
    while True:
        try:
            bytes = bytes + await ws.receive_bytes()
            consumed = audio.append(bytes)
            bytes = bytes[consumed:]
        except WebSocketDisconnect:
            print("Client disconnected")
            break
        except Exception as e:
            print(f"Error: {e}")
            raise
    audio.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)