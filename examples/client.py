import wave
import asyncio
import websockets
import time
import json

# WebSocket server URL
WEBSOCKET_SERVER_URL = 'ws://localhost:8000/v1/realtime'  # Replace with your WebSocket server URL

async def send_audio_through_websocket():
    # Open the WAV file in read mode
    with wave.open("./audio/oppo-zh-cn.wav", 'rb') as wf:
        # Get properties of the audio file
        n_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        framerate = wf.getframerate()
        chunk_size = 1024  # The size of each audio chunk (in frames)
        
        print(f"Channels: {n_channels}, Sample width: {sample_width}, Framerate: {framerate}")
        
        async with websockets.connect(WEBSOCKET_SERVER_URL, open_timeout=None, close_timeout=None, ping_interval=None) as ws:
            print("Connected to WebSocket server")

            config = {
                "model": "turbo",
                "initial_prompt": ","
            }
            config_json = json.dumps(config)
            await ws.send(config_json)
            
            size = 0
            # Loop through the audio file and read it in chunks
            while True:
                # Read a chunk of audio data
                frames = wf.readframes(chunk_size)
                
                # If no more frames are left, break the loop
                if len(frames) == 0:
                    print(f"All sent.")
                    break

                # Send the audio frames to the WebSocket server
                await ws.send(frames)

                size += len(frames)
                print(f"{size} bytes sent.")

                # Simulate real-time streaming by sleeping for the duration of the chunk
                time.sleep(chunk_size / framerate)

                #msg = await ws.recv()

            print(f"Audio streaming complete. {size} bytes sent.")
        
# Run the WebSocket client
asyncio.run(send_audio_through_websocket())