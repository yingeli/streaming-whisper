class Transcription:
    def __init__(self, text="", segments=[], language=None) -> None:
        self.text = text
        self.segments = segments
        self.language = language

class Segment:
    def __init__(self, text="", start=0, end=0) -> None:
        self.text = text
        self.start = start
        self.end = end


