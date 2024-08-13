import time

from whisper_jax import FlaxWhisperPipline
import jax
from functools import cached_property
print(jax.devices()[0])
from moviepy.editor import *
# Windows: C:\Users\你的用户名\.cache\whisper/large-v2.pt
# instantiate pipeline
from jax.experimental.compilation_cache import compilation_cache as cc
#cc.initialize_cache("./cache")
model_path = r"C:\Users\user\.cache\huggingface\hub\models--guillaumekln--faster-whisper-large-v2"
#pipeline = FlaxWhisperPipline(r"openai/whisper-large-v2")
pipeline = FlaxWhisperPipline(model_path)

video = CompositeVideoClip([VideoFileClip("d:\\tmp\\vedio\\test2.mp4").subclip(50,180)])
# 写入剪辑完成的音乐
out = r"d:\\tmp\\vedio\\done.mp4"
video.write_videofile(out)

start = time.time()

# JIT compile the forward call - slow, but we only do once
#result = pipeline("audio.mp3")

# used cached function thereafter - super fast!!
result = pipeline("audio.mp3",return_timestamps=True)

print(result)
print(", ".join([i["text"] for i in result["chunks"] if i is not None]))


print("cost time: {}".format(time.time()-start))




