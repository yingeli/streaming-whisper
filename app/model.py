import os
from io import StringIO
from threading import Lock
from typing import BinaryIO, Union

import torch
import whisper
from whisper.utils import ResultWriter, WriteJSON, WriteSRT, WriteTSV, WriteTXT, WriteVTT

model_name = os.getenv("ASR_MODEL", "turbo")
model_path = os.getenv("ASR_MODEL_PATH", os.path.join(os.path.expanduser("~"), ".cache", "whisper"))

if torch.cuda.is_available():
    model = whisper.load_model(model_name, download_root=model_path).cuda()
    print("cuda!")
else:
    model = whisper.load_model(model_name, download_root=model_path)
model_lock = Lock()

def transcribe(
    audio,
    initial_prompt: str,
    word_timestamps: bool,
):
    with model_lock:
        result = model.transcribe(audio, initial_prompt=initial_prompt)

    return result