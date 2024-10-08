import os
import time
from threading import Lock
from faster_whisper import WhisperModel
from transcription import Transcription, Segment, Word
from typing import Optional

model_size = "deepdml/faster-whisper-large-v3-turbo-ct2"
model = WhisperModel(model_size, device="cuda")

model_lock = Lock()

def transcribe(
    audio,
    initial_prompt: str,
):
    with model_lock:
        #segs, info = model.transcribe(audio, beam_size=1, initial_prompt=initial_prompt, word_timestamps=False, condition_on_previous_text=False, temperature=0, length_penalty=0.0001)
<<<<<<< HEAD
        segs, info = model.transcribe(audio, initial_prompt=initial_prompt, temperature=0, word_timestamps=True)
        text = ""
        segments = []
        duration = 0
=======
        segs, info = model.transcribe(audio, 
                                      initial_prompt=initial_prompt, 
                                      temperature=0, 
                                      word_timestamps=True,
                                      condition_on_previous_text=False,
                                      )

        segments = []
        #text = ""
        end_detected = False
>>>>>>> 2fe0533 (dev)
        for s in segs:
            words = []
            for w in s.words:
                #if w.start >= s.end:
                #    end_detected = True
                #    break
                word = Word(text=w.word, start=w.start, end=w.end)
                words.append(word)
        
            #if len(words) == 0:
            #    break
        
            segment = Segment(start=s.start, end=s.end, words=words)
            segments.append(segment)
<<<<<<< HEAD
            duration = s.end
        trans = Transcription(text=text, duration=duration, segments=segments, language=info.language)
        return trans
=======
            #text += segment.text
                
            if end_detected:
                break
    
        trans = Transcription(duration=info.duration, language=info.language, segments=segments)
        trim(trans)
        return trans
    
def trim(trans, trim_threshold=0.1) -> None:
    while len(trans.segments) > 0:
        segment = trans.segments[-1]
        while len(segment.words) > 0:
            word = segment.words[-1]
            if word.start + trim_threshold < segment.end:
                break
            segment.words.pop()
        if len(segment.words) > 0:
            break
        trans.segments.pop()

>>>>>>> 2fe0533 (dev)
