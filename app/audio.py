import numpy as np
import asyncio
from numpy.typing import NDArray

SAMPLE_RATE = 16000
SAMPLE_WIDTH = 2

class AudioBuffer:
    def __init__(
        self,
        data: NDArray[np.float32] = np.array([], dtype=np.float32),
        offset: int = 0,
    ) -> None:
        self.data = data
        self.offset = offset
        self.closed = False
        self.updated = asyncio.Event()

    @property
    def start(self) -> float:
        return self.offset / SAMPLE_RATE

    @property
    def end(self) -> float:
        return self.start + self.duration
    
    @property
    def duration(self) -> float:
        return len(self.data) / SAMPLE_RATE

    def append(self, buf: bytes) -> int:
        chunk = np.frombuffer(buf, np.int16).flatten().astype(np.float32) / 32768.0
        self.data = np.append(self.data, chunk)
        self.updated.set()
        return len(chunk) * SAMPLE_WIDTH
    
    def close(self) -> None:
        self.closed = True
        self.updated.set()

    def truncate(self, end: float) -> None:
        len = int(end * SAMPLE_RATE)
        self.data = self.data[len:]
        self.offset += len

    async def chunk(self, min_duration: float):
        while not (self.closed or self.duration >= min_duration):  
            await self.updated.wait()
            self.updated.clear()
        
        return AudioChunk(self.data, offset=self.offset, is_final=self.closed)
    
class AudioChunk:
    def __init__(self, data: bytes, offset: int = 0, is_final: bool = False):
        self.data = data
        self.offset = offset
        self.is_final = is_final

    @property
    def start(self) -> float:
        return self.offset / SAMPLE_RATE

    @property
    def end(self) -> float:
        return self.start + self.duration
    
    @property
    def duration(self) -> float:
        return len(self.data) / SAMPLE_RATE
    
