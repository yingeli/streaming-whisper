import os
import time
from threading import Lock
from faster_whisper import WhisperModel
from transcription import Transcription, Segment

model_size = "/home/coder/streaming-whisper/models/faster-whisper-large-v3-turbo"

model = WhisperModel(model_size, device="cuda", compute_type="float32")

model_lock = Lock()

def transcribe(
    audio,
    initial_prompt: str,
):
    with model_lock:
        segs, info = model.transcribe(audio, beam_size=1, initial_prompt=initial_prompt, word_timestamps=False, condition_on_previous_text=False, temperature=0, length_penalty=0.0001)
        text = ""
        segments = []
        for s in segs:
            text += s.text
            segment = Segment(text=s.text, start=s.start, end=s.end)
            segments.append(segment)
        trans = Transcription(text=text, segments=segments, language=info.language)
        return trans
        