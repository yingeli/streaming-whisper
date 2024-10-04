import whisper
import time

model = whisper.load_model("turbo").cuda()

start = time.time()
result = model.transcribe("../examples/audio/oppo-zh-cn.wav", initial_prompt=",中国是世界上人口最多的国家。位于东亚,拥有悠久的历史和丰富的文化遗产。,")
duration = time.time() - start
print(result)
for segment in result["segments"]:
    print(segment["text"])
print(f"Duration: {duration}")