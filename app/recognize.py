import time
from audio import AudioBuffer
from collections.abc import AsyncGenerator
from os.path import commonprefix
from transcription import Transcription
from model_faster_whisper import transcribe
from event import RecognizingEvent, RecognizedEvent, Recognition

async def recognize(
    audio: AudioBuffer,
    initial_prompt: str = "Hi,",
    init_step: float = 1.2,
    step: float = 0.8,
) -> AsyncGenerator[dict, None]:
    chunk_duration = 0
    recognizer = Recognizer()
    while True:
        chunk = await audio.chunk(max(init_step, chunk_duration + step))
        chunk_duration = chunk.duration

        trans = transcribe(chunk.data, initial_prompt=initial_prompt)
        if trans.duration == 0:
            continue

        if chunk.is_final:
            if len(chunk.data) > 0:
                start = chunk.start
                end = chunk.start + trans.duration
                recog = Recognition(text=trans.text, start=start, end=end, language=trans.language)
                yield RecognizedEvent(recog)
            return
        
        text, duration, recognized = recognizer.recognize(trans)
        if duration == 0:
            continue
        
        recog = Recognition(text=text, start=chunk.start, end=chunk.start + duration, language=trans.language)
        if recognized:
            audio.truncate(duration)
            chunk_duration -= duration

            initial_prompt = text
            
            yield RecognizedEvent(recog)     
        else:
            yield RecognizingEvent(recog)     

class Recognizer:
    def __init__(self) -> None:
        self.prev_text = ""
        self.prev_segments = []

    def recognize(self, trans: Transcription):
        if len(trans.segments) == 0:
            return "", 0, False
        
        words = trans.segments[0].words
        for i in range(len(words)-1, -1, -1):
            word = words[i]
            if word.text[-1] in [".", "。", "?", "？", "!", "！"]:
                text = "".join([w.text for w in words[:i+1]])
                if self.prev_text.startswith(text):
                    self.prev_segments = []
                    self.prev_text = "".join([w.text for w in words[i+1:]]).join([s.text for s in trans.segments[1:]])
                    return text, word.end, True

        if len(trans.segments) > 1 and len(self.prev_segments) > 1:
            segment = trans.segments[0]
            if segment.text == self.prev_segments[0].text:
                self.prev_segments = trans.segments[1:]
                self.prev_text = "".join([segment.text for segment in self.prev_segments])
                return segment.text, segment.words[-1].end, True
        
        if trans.text == self.prev_text:
            return "", 0, False

        self.prev_text = trans.text
        self.prev_segments = trans.segments
        return trans.text, trans.duration, False
