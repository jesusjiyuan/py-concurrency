import time

import whisper
#from transformers import WhisperProcessor, WhisperForConditionalGeneration
from moviepy.editor import *
# Windows: C:\Users\你的用户名\.cache\whisper/large-v2.pt
whisper_model = whisper.load_model(download_root=r"C:\Users\user\.cache\whisper",name="large-v2")

video = CompositeVideoClip([VideoFileClip("d:\\tmp\\vedio\\test2.mp4").subclip(50,180)])
# 写入剪辑完成的音乐
out = r"d:\\tmp\\vedio\\done.mp4"
video.write_videofile(out)

start = time.time()
result = whisper_model.transcribe(out)
print(result)
#print(", ".join([i["text"] for i in result["segments"] if i is not None]))
#print(["[%.2fs -> %.2fs] %s " % (i["start"], i["end"], i["text"]) for i in result["segments"] if i is not None])
for i in result["segments"]:
    if i is not None:
        print("[%.2fs -> %.2fs] %s " % (i["start"], i["end"], i["text"]))
print("cost time: {}".format(time.time()-start))

CompositeVideoClip([VideoFileClip("d:\\tmp\\vedio\\test2.mp4").subclip(51,52)]).write_videofile("d:\\tmp\\vedio\\clip1.mp4")
CompositeVideoClip([VideoFileClip("d:\\tmp\\vedio\\test2.mp4").subclip(60,61)]).write_videofile("d:\\tmp\\vedio\\clip2.mp4")
