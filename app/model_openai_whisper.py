import os
from threading import Lock
import torch
import whisper
from transcription import Transcription, Segment, Word

model_name = os.getenv("ASR_MODEL", "turbo")
model_path = os.getenv("ASR_MODEL_PATH", os.path.join(os.path.expanduser("~"), ".cache", "whisper"))

if torch.cuda.is_available():
    model = whisper.load_model(model_name, download_root=model_path).cuda()
else:
    model = whisper.load_model(model_name, download_root=model_path)
model_lock = Lock()

IGNORE_TAIL_DURATION = 0.3

def transcribe(
    audio,
    initial_prompt: str,
):
    with model_lock:
<<<<<<< HEAD
        result = model.transcribe(audio, initial_prompt=initial_prompt, temperature=0)
        #result = model.transcribe(audio, initial_prompt=initial_prompt, word_timestamps=False, logprob_threshold=-0.3)
        segments = []
        duration = 0
        for s in result["segments"]:
            segment = Segment(text=s["text"], start=s["start"], end=s["end"])
            segments.append(segment)
            duration = s["end"]
        trans = Transcription(text=result["text"], duration=duration, language=result["language"], segments=segments)
        return trans
=======
        result = model.transcribe(audio, initial_prompt=initial_prompt, temperature=0, word_timestamps=True)

    segments = []
    text = ""
    end_detected = False
    for s in result["segments"]:
        words = []
        segment_text = ""
        for w in s["words"]:
            if w["start"] >= s["end"]:
                end_detected = True
                break
            word = Word(text=w["word"], start=w["start"], end=w["end"])
            words.append(word)
            segment_text += word.text
        
        if len(words) == 0:
            break
        
        segment = Segment(start=s["start"], end=words[-1].end, words=words)
        segments.append(segment)
        text += segment.text
                
        if end_detected:
            break
    
    trans = Transcription(duration=segments[-1].end, language=result["language"], segments=segments)
    trim(trans)    
    return trans

def trim(trans, trim_threshold=0.1) -> None:
    while len(trans.segments) > 0:
        segment = trans.segments[-1]
        while len(segment.words) > 0:
            word = segment.words[-1]
            if word.start + trim_threshold < segment.end:
                break
            print(f"Trimming word: {word.text} from {segment.text}")
            segment.words.pop()
        if len(segment.words) > 0:
            break
        trans.segments.pop()
>>>>>>> 2fe0533 (dev)
