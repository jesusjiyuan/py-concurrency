import json
import os
import time

import whisper
from moviepy.editor import *
import sys
#sys.path.append("/java_web/cloudcs2mon/pyspace/")
os.chdir(os.path.dirname(__file__))


v_file = r"d:\tmp\vedio\dian-AVC.mp4"
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


def whisper_rec(id,vfile):
    video = VideoFileClip(vfile)
    video_len = video.duration
    print("video_len: ",video_len)
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


import websockets
import asyncio
from datetime import datetime
import json

# 连接WebSocket服务器并进行消息处理的异步函数
async def websocket_handler(uri):
    async with websockets.connect(uri) as websocket:
        # 订阅消息
        sub_message = {
            "type": "subscribe",
            "data": {
                "type": "whisper"
            }
        }
        await websocket.send(json.dumps(sub_message))
        print("Subscribed to whispers")

        # 接收并处理消息
        while True:
            message = await websocket.recv()
            message_data = json.loads(message)
            if message_data.get('type') == 'whisper':
                print(f"Received whisper at {datetime.now()}: {message_data['data']['message']}")
                # 将语音转文字逻辑放在这里

# 运行WebSocket客户端
start_uri = "ws://localhost:8888/myws"
asyncio.get_event_loop().run_until_complete(websocket_handler(start_uri))

# v_file = file_path
# whisper_rec("",v_file)