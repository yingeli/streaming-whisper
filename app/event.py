class Recognition:
    def __init__(self, text, start, end, language):
        self.text = text
        self.start = start
        self.end = end
        self.language = language

    @property
    def duration(self):
        return self.end - self.start

    def to_dict(self):
        return {
            "text": self.text.strip(),
            "start": self.start,
            "end": self.end,
            "language": self.language,            
        }

class RecognizingEvent:
    def __init__(self, recognition: Recognition) -> None:
        self.recognition = recognition

    def to_dict(self):
        return {
            "type": "recognizing",
            "result": self.recognition.to_dict(),
        }
    
class RecognizedEvent:
    def __init__(self, recognition: Recognition) -> None:
        self.recognition = recognition

    def to_dict(self):
        return {
            "type": "recognized",
            "result": self.recognition.to_dict(),
        }
    
class CompletedEvent:
    def to_dict(self):
        return {
            "type": "completed",
        }