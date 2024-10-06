import whisper
import time

model = whisper.load_model("turbo").cuda()

start = time.time()
result = model.transcribe("../tests/audio/oppo-th-th.wav", initial_prompt="Hi,", language="th")
duration = time.time() - start
#print(result)
print(f"Duration: {duration}")
print(f"Language: {result['language']}")
for segment in result["segments"]:
    print(segment["text"])
