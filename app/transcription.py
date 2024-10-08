<<<<<<< HEAD
class Transcription:
    def __init__(self, text, duration, language, segments=[]) -> None:
        self.text = text
        self.duration = duration
        self.language = language
        self.segments = segments

class Segment:
    def __init__(self, text, start, end) -> None:
        self.text = text
        self.start = start
        self.end = end
=======
from typing import List, NamedTuple

class Word(NamedTuple):
    text: str
    start: float
    end: float

class Segment(NamedTuple):
    start: float
    end: float
    words: List[Word]

    @property
    def text(self):
        return "".join([word.text for word in self.words])

class Transcription(NamedTuple):
    duration: float
    language: str
    segments: List[Segment]

    @property
    def text(self):
        return "".join([segment.text for segment in self.segments])
    
    #@property
    #def duration(self):
    #    return self.segments[-1].end
>>>>>>> 2fe0533 (dev)
