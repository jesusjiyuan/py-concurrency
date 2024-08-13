import json
import os
import time

import whisper
from moviepy.editor import *
import sys
#sys.path.append("/java_web/cloudcs2mon/pyspace/")
os.chdir(os.path.dirname(__file__))


#v_file = r"d:\tmp\vedio\dian-AVC.mp4"
v_file = r"d:\tmp\vedio\ff2a2c53bcfbbe8bfcdf22c0b077a59a.webm"
# 写入剪辑完成的音乐
out_file = r"d:\tmp\vedio\done1.mp4"

ai_model_dir=r"D:\aimodel\whisper"
#ai_model_dir=r"/java_web/jucunmgr/pyspace"
# tiny base small medium large-v2 large-v3
ai_model_nm="medium"

videos = []
keyws = []
print("sys.argv: {}".format(sys.argv))
file_path = sys.argv[1]
initial_prompt = "以下是普通话的句子，这是一段会议记录。"
# Windows: C:\Users\你的用户名\.cache\whisper/large-v2.pt
whisper_model = whisper.load_model(download_root=ai_model_dir,name=ai_model_nm)
#whisper_model = whisper.load_model(name=ai_model_nm)


def convert_webm_to_mp3(input_webm, output_mp3):
    video_clip = VideoFileClip(input_webm)
    audio = video_clip.audio
    audio.write_audiofile(output_mp3)
    video_clip.close()
    global vfile
    vfile = output_mp3

def cmd_convert_webm_to_mp3():
    cmd = "ffmpeg -i {} -c:a libmp3lame -q:a 4 {} >> /dev/null".format(v_file,v_file.replace("webm","mp3"))
    os.system(cmd)

def whisper_rec(id,vfile):
    #video = VideoFileClip(vfile)
    #video_len = video.duration
    #print("video_len: ",video_len)
    matched_kwords=[]

    start = time.time()
    result = whisper_model.transcribe(vfile, language='zh',initial_prompt=initial_prompt)
    result_json = json.dumps(result,ensure_ascii=False)
    print(result_json)
    print("whisper cost time: {}".format(time.time()-start))
    #print(", ".join([i["text"] for i in result["segments"] if i is not None]))
    #print(["[%.2fs -> %.2fs] %s " % (i["start"], i["end"], i["text"]) for i in result["segments"] if i is not None])
    #keyws = dbmapper.MonKeywordMapper.list()
    print("keyword size ",len(keyws))
    for i in result["segments"]:
        result = []
        if i is not None:
            result.append(i["text"])
            print(''.join(result))
            #print("[%.2fs -> %.2fs] %s " % (i["start"], i["end"], i["text"]))

#cmd_convert_webm_to_mp3()
#v_file = file_path
whisper_rec("",v_file)