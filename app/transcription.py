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
