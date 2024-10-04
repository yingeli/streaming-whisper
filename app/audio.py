import numpy as np
import asyncio
from numpy.typing import NDArray
from collections.abc import AsyncGenerator

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
        self.appended = asyncio.Event()

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
        self.appended.set()
        return len(chunk) * SAMPLE_WIDTH
    
    def close(self) -> None:
        self.closed = True
        self.appended.set()

    #def append(self, data: NDArray[np.float32]) -> None:
    #    self.data = np.append(self.data, data)

    def truncate(self, end: float) -> None:
        len = int(end * SAMPLE_RATE)
        self.data = self.data[len:]
        self.offset += len

    async def chunk(self, min_duration: float):
        while not (self.closed or self.duration >= min_duration):  
            await self.appended.wait()
            self.appended.clear()
        
        return self.data, self.duration, self.closed
