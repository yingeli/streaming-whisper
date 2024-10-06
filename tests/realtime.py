import wave
import asyncio
import websockets
import time
import json
from websockets.exceptions import ConnectionClosed

# WebSocket server URL
WEBSOCKET_SERVER_URL = 'ws://localhost:8000/v1/realtime'  # Replace with your WebSocket server URL

async def transcribe():
    # Open the WAV file in read mode
    start = time.time()
    with wave.open("./audio/oppo-en-us.wav", 'rb') as wf:       
        #async with websockets.connect(WEBSOCKET_SERVER_URL, open_timeout=None, close_timeout=None, ping_interval=None) as ws:
        async with websockets.connect(WEBSOCKET_SERVER_URL) as ws:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(send(ws, wf))

                while True:
                    try:
                        msg = await ws.recv()
                        event = json.loads(msg)
                        if event["type"] == "close":
                            break
                        time_elapsed = time.time() - start
                        type = event["type"]
                        text = event["result"]
                        print(f"{time_elapsed}: {type}: {text}")
                        if type == "recognized":
                            #print(f"{time_elapsed}: recognized: {text}")
                            print("")                   
                    except ConnectionClosed:
                        print("Connection closed.")
                        break

                await ws.close()

async def send(ws: websockets.WebSocketClientProtocol, wf) -> None:
    config = {
        "model": "turbo",
        "initial_prompt": ","
    }

    await ws.send(json.dumps(config))
    
    # Get properties of the audio file
    # n_channels = wf.getnchannels()
    # sample_width = wf.getsampwidth()
    framerate = wf.getframerate()
    chunk_size = 1024  # The size of each audio chunk (in frames)

    while True:
        # Read a chunk of audio data
        frames = wf.readframes(chunk_size)

        # Send the audio frames to the WebSocket server
        await ws.send(frames)

        # If no more frames are left, break the loop
        if len(frames) == 0:
            break

        # Simulate real-time streaming by sleeping for the duration of the chunk
        await asyncio.sleep(chunk_size / framerate)
        
# Run the WebSocket client
asyncio.run(transcribe())