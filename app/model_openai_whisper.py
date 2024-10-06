import os
from threading import Lock
import torch
import whisper
from transcription import Transcription, Segment

model_name = os.getenv("ASR_MODEL", "turbo")
model_path = os.getenv("ASR_MODEL_PATH", os.path.join(os.path.expanduser("~"), ".cache", "whisper"))

if torch.cuda.is_available():
    model = whisper.load_model(model_name, download_root=model_path).cuda()
else:
    model = whisper.load_model(model_name, download_root=model_path)
model_lock = Lock()

def transcribe(
    audio,
    initial_prompt: str,
):
    with model_lock:
        result = model.transcribe(audio, initial_prompt=initial_prompt, temperature=0)
        #result = model.transcribe(audio, initial_prompt=initial_prompt, word_timestamps=False, logprob_threshold=-0.3)
        segments = []
        for s in result["segments"]:
            segment = Segment(text=s["text"], start=s["start"], end=s["end"])
            segments.append(segment)
        trans = Transcription(text=result["text"], segments=segments, language=result["language"])
        return trans