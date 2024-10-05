import whisper
import time

model = whisper.load_model("turbo").cuda()

start = time.time()
result = model.transcribe("../tests/audio/oppo-en-us.wav", initial_prompt=",")
duration = time.time() - start
print(result)
#for segment in result["segments"]:
#    print(segment["text"])
#print(f"Duration: {duration}")