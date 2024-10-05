import whisper
import time

model = whisper.load_model("turbo").cuda()

start = time.time()
result = model.transcribe("../tests/audio/oppo-zh-cn.wav", initial_prompt=",")
duration = time.time() - start
#print(result)
print(f"Duration: {duration}")
for segment in result["segments"]:
    print(segment["text"])
