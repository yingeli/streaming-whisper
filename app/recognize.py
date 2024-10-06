import time
from audio import AudioBuffer
from collections.abc import AsyncGenerator
from os.path import commonprefix
from transcription import Transcription
from model_openai_whisper import transcribe
from event import RecognizingEvent, RecognizedEvent, Recognition

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
                start = chunk.start
                end = chunk.start + trans.duration
                recog = Recognition(text=trans.text, start=start, end=end, language=trans.language)
                yield RecognizedEvent(recog)
            return
        
        text, recognized_duration = recognizer.recognize(trans)
                
        if text == None:
            continue
        
        if recognized_duration > 0:
            audio.truncate(recognized_duration)
            chunk_duration -= recognized_duration        
            
            initial_prompt = text

            start = chunk.start
            end = chunk.start + recognized_duration
            recog = Recognition(text=text, start=start, end=end, language=trans.language)
            yield RecognizedEvent(recog)
        else:        
            start = chunk.start
            end = chunk.end
            recog = Recognition(text=text, start=start, end=end, language=trans.language)
            yield RecognizingEvent(recog)

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