import whisper
import time

model = whisper.load_model("turbo").cuda()

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("./audio/en-us.wav")
audio = whisper.pad_or_trim(audio)

start = time.time()
# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

duration = time.time() - start
print(f"Duration: {duration}")