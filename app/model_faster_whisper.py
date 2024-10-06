import os
import time
from threading import Lock
from faster_whisper import WhisperModel
from transcription import Transcription, Segment

model_size = "deepdml/faster-whisper-large-v3-turbo-ct2"
model = WhisperModel(model_size, device="cuda")

model_lock = Lock()

def transcribe(
    audio,
    initial_prompt: str,
):
    with model_lock:
        #segs, info = model.transcribe(audio, beam_size=1, initial_prompt=initial_prompt, word_timestamps=False, condition_on_previous_text=False, temperature=0, length_penalty=0.0001)
        segs, info = model.transcribe(audio, initial_prompt=initial_prompt, temperature=0, word_timestamps=True)
        text = ""
        segments = []
        duration = 0
        for s in segs:
            text += s.text
            segment = Segment(text=s.text, start=s.start, end=s.end)
            segments.append(segment)
            duration = s.end
        trans = Transcription(text=text, duration=duration, segments=segments, language=info.language)
        return trans