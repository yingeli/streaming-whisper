from faster_whisper import WhisperModel
import time

model_size = "deepdml/faster-whisper-large-v3-turbo-ct2"
# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

start = time.time()
segments, info = model.transcribe("./audio/en-us.wav", temperature=0, initial_prompt="Hi,")

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    #for word in segment.words:
    #    print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))

duration = time.time() - start
print(f"Duration: {duration}")