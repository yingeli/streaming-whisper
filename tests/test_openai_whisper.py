import whisper
import time

model = whisper.load_model("turbo").cuda()

start = time.time()

result = model.transcribe("../tests/audio/zh-cn.wav", temperature=0, initial_prompt="Hi,", word_timestamps=True)
#print(result)
print(f"Language: {result['language']}")
for segment in result["segments"]:
    print(segment["text"])
duration = time.time() - start
print(f"Duration: {duration}")
