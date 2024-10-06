import time
from audio import AudioBuffer
from collections.abc import AsyncGenerator
from os.path import commonprefix
from transcription import Transcription
from model_openai_whisper import transcribe

async def recognize(
    audio: AudioBuffer,
    initial_prompt: str = "Hi,",
    init_step: float = 1.5,
    step: float = 0.5,
) -> AsyncGenerator[dict, None]:
    chunk_duration = 0
    recognizer = Recognizer()
    while True:
        chunk = await audio.chunk(max(init_step, chunk_duration + step))
        chunk_duration = chunk.duration

        trans = transcribe(chunk.data, initial_prompt=initial_prompt)

        if chunk.is_final:
            if len(chunk.data) > 0:
                text = trans.text
                yield recognized(text)
            return
        
        text, recognized_duration = recognizer.recognize(trans)
                
        if text == None:
            continue
        
        if recognized_duration > 0:
            audio.truncate(recognized_duration)
            chunk_duration -= recognized_duration        
            
            initial_prompt = text
            
            yield recognized(text)
        else:        
            yield recognizing(text)

class Recognizer:
    def __init__(self) -> None:
        self.prev_text = ""
        self.prev_recognizing_len = 0

    def recognize(self, trans: Transcription):
        text = trans.text
        confirmed = commonprefix([self.prev_text, text])

        if len(trans.segments) > 1:
            segment = trans.segments[0]
            if len(confirmed) >= len(segment.text):
                # recongnized
                self.prev_text = "".join([s.text for s in trans.segments[1:]])
                self.prev_recognizing_len = 0

                return segment.text, segment.end
 
        self.prev_text = text

        if len(confirmed.strip()) > 0 and len(confirmed) > self.prev_recognizing_len:
            self.prev_recognizing_len = len(confirmed)
            return confirmed, 0
        else:
            return None, 0

def recognized(text):
    return {
        "type": "recognized",
        "result": text,
    }

def recognizing(text):
    return {
        "type": "recognizing",
        "result": text,
    }