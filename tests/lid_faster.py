import time
from faster_whisper import WhisperModel

model = WhisperModel("large-v3-turbo", device="cuda")

#model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")


start = time.time()

language_info = model.detect_language_multi_segment("./audio/en-us.wav")
print(f"Detected language: {language_info}")

duration = time.time() - start
print(f"Duration: {duration}")