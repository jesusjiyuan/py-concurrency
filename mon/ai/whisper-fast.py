from faster_whisper import WhisperModel
import logging

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

#model_size = "large-v2"
model_size = "large"
model_path = r"C:\Users\user\.cache\huggingface\hub\models--guillaumekln--faster-whisper-large-v2"
audio_file =  r"d:\tmp\vedio\done.mp4"
# Run on GPU with FP16
#model = WhisperModel(local_files_only=True,download_root=r".cache\whisper",model_size_or_path="large-v2", device="cpu", compute_type="int8")
model = WhisperModel(local_files_only=False,download_root=r"D:\aimodel\whisper",model_size_or_path="medium", device="cpu", compute_type="int8")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe(audio_file, beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))