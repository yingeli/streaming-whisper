from faster_whisper import WhisperModel, BatchedInferencePipeline
import time

model_size = "turbo"
# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")

#model = WhisperModel(model_size, device="cpu", compute_type="int8")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

batched_model = BatchedInferencePipeline(model=model)

start = time.time()
#segments, info = batched_model.transcribe("./audio/en-10mins.wav", temperature=0, batch_size=16)
segments, info = model.transcribe("./audio/en-10mins.wav", temperature=0)
#    beam_size=1,
#    temperature=0,  
#    initial_prompt="Hi,", 
    #word_timestamps=True,
    #condition_on_previous_text=False, 
    #vad_filter=True,
#    )

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    #for word in segment.words:
    #    print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))

duration = time.time() - start
print(f"Duration: {duration}")