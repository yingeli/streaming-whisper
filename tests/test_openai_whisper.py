import whisper
import time

model = whisper.load_model("turbo").cuda()

start = time.time()
<<<<<<< HEAD
result = model.transcribe("../tests/audio/en-us.wav", temperature=0, initial_prompt="Hi,")
=======
result = model.transcribe("../tests/audio/zh-cn.wav", temperature=0, initial_prompt="Hi,", word_timestamps=True)
>>>>>>> 2fe0533 (dev)
#print(result)
print(f"Language: {result['language']}")
for segment in result["segments"]:
    print(segment["text"])
duration = time.time() - start
print(f"Duration: {duration}")
