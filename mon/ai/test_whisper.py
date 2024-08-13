import json
import os
import time

import whisper
from moviepy.editor import *
import sys
sys.path.append("/java_web/cloudcs2mon/pyspace/")
os.chdir(os.path.dirname(__file__))

import confhelper
import dbmapper
from entity import MonVideoResult, MonVideoResultExt, MonTask

v_file = "d:\\tmp\\vedio\\done.mp4"
# 写入剪辑完成的音乐
out_file = r"d:\\tmp\\vedio\\done1.mp4"
#out_path = confhelper.confdata().get("out_path")
out_prefix = confhelper.confdata().get("out_prefix")
work_dir = confhelper.confdata().get("work_dir")
ai_model_dir = confhelper.confdata().get("ai_model_dir")
ai_model_nm = confhelper.confdata().get("ai_model_nm")
videos = []
keyws = []
print("sys.argv: {}".format(sys.argv))
batchNo = sys.argv[1]
# Windows: C:\Users\你的用户名\.cache\whisper/large-v2.pt
whisper_model = whisper.load_model(download_root=ai_model_dir,name=ai_model_nm)

def whisper_rec(id,vfile):
    video = VideoFileClip(vfile)
    video_len = video.duration
    print("video_len: ",video_len)
    matched_kwords=[]

    start = time.time()
    result = whisper_model.transcribe(vfile)
    result_json = json.dumps(result,ensure_ascii=False)
    print(result_json)
    print("whisper cost time: {}".format(time.time()-start))
    #print(", ".join([i["text"] for i in result["segments"] if i is not None]))
    #print(["[%.2fs -> %.2fs] %s " % (i["start"], i["end"], i["text"]) for i in result["segments"] if i is not None])
    #keyws = dbmapper.MonKeywordMapper.list()
    print("keyword size ",len(keyws))
    match_count=0
    videoResultExts = []
    for i in result["segments"]:
        if i is not None:
            print("[%.2fs -> %.2fs] %s " % (i["start"], i["end"], i["text"]))
            if len(keyws) >0:
                for k in keyws:
                    print("keyword: ",k.name)
                    if i["text"].find(k.name) > -1:
                        match_count = match_count + 1
                        monVideoResultExt = save_clip(id,vfile,i["start"],i["end"])
                        monVideoResultExt.kwords = k.name
                        print("monVideoResultExt: ",monVideoResultExt)
                        videoResultExts.append(monVideoResultExt)
    _update = MonVideoResult(id=id,raw=result_json,status="1",vedioDuration=video_len,endTime=time.localtime())
    if len(videoResultExts) > 0:
        _update.status="2"
        dbmapper.MonVideoResultMapper.update(_update)
        for vext in videoResultExts:
            count = dbmapper.MonVideoResultExtMapper.count(MonVideoResultExt(vId=vext.vId,start=vext.starts,end=vext.ends))
            if int(count) > 0:
                dbmapper.MonVideoResultExtMapper.update(vext)
            else:
                dbmapper.MonVideoResultExtMapper.insert(vext)
    else:
        _update.status="1"
        dbmapper.MonVideoResultMapper.update(_update)
    dbmapper.MonTaskMapper.update(MonTask(batchNo=batchNo,status="1",endTime=time.localtime()))


def save_clip(id,vfile,s_start,s_end) -> MonVideoResultExt:
    s_start = str('{:.2f}'.format(s_start).replace("s",""))
    s_end = str('{:.2f}'.format(s_end).replace("s",""))
    f_outpath = work_dir+"/monvedio/"+id
    db_outpath = out_prefix+id
    outfilename = "clip_"+s_start+"_"+s_end+".mp4"
    if not os.path.exists(f_outpath):
        os.mkdir(f_outpath)
    CompositeVideoClip([VideoFileClip(vfile).subclip(s_start,s_end)]).write_videofile(f_outpath+"/"+outfilename)
    #dbmapper.MonVideoResultExtMapper.insert(MonVideoResultExt(vId=id,start=s_start,end=s_end,vSlicePath=db_outpath+"/"+outfilename))
    return MonVideoResultExt(vId=id,start=s_start,end=s_end,vSlicePath=db_outpath+"/"+outfilename)
    #if video_len > 50:
    #    f_outpath = work_dir+"/monvedio/"+id
    #    db_outpath = out_prefix+id
    #    outfilename = "clip_40.mp4"
    #    s_start=40
    #    s_end=42
    #    if not os.path.exists(f_outpath):
    #        os.mkdir(f_outpath)
#
    #    CompositeVideoClip([VideoFileClip(vfile).subclip(40,42)]).write_videofile(f_outpath+"/"+outfilename)
    #    dbmapper.MonVideoResultExtMapper.insert(MonVideoResultExt(vId=id,start=s_start,end=s_end,vSlicePath=db_outpath+"/"+outfilename))

if "dev" == confhelper.curenv():
    videos.append(MonVideoResult(id="1",vedioUrl=v_file))
if "prod" == confhelper.curenv():
    monTask = dbmapper.MonTaskMapper.get_by_batchno(batchNo=batchNo)
    if monTask is not None and len(monTask.targetIds) > 0 :
        videos = dbmapper.MonVideoResultMapper.list_by_ids(monTask.targetIds.split(","))
    if monTask is not None and len(monTask.kwIds) > 0 :
        keyws = dbmapper.MonKeywordMapper.list_by_ids(monTask.kwIds.split(","))
if len(videos) > 0 :
    for v in videos:
        print(v.id,v.vedioUrl)
        vfile = v.vedioUrl
        if vfile.find("profile") != -1:
            vfile = work_dir+vfile.replace("profile","")
        whisper_rec(v.id,vfile)


#CompositeVideoClip([VideoFileClip(v_file).subclip(51,52)]).write_videofile("d:\\tmp\\vedio\\clip1.mp4")
#CompositeVideoClip([VideoFileClip(v_file).subclip(60,61)]).write_videofile("d:\\tmp\\vedio\\clip2.mp4")
