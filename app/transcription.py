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
