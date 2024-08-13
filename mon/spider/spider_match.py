import base64
import json
import time

import requests
import os
import sys
sys.path.append("/java_web/cloudcs2mon/pyspace/")

import confhelper
import dbmapper
from entity import LinkMonResult

work_dir = confhelper.confdata().get("work_dir")

#match_str = "PP(聚丙烯)"
match_str = "松下"
def ocr(png_file):
    start = time.time()
    print("file: "+png_file)
    encoded = base64.b64encode(open(png_file, 'rb').read()).decode("utf-8")
    l = [encoded]
    map = {"images": l}
    #print(json.dumps(map))
    url = "https://mhqym.topwin.net/ppocr/predict/ocr_system"
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    result = requests.post(url,data=json.dumps(map),headers= header)
    #print(result.json())
    str1 = ""
    for i in result.json().get("results")[0]:
        str1 = str1 + i.get("text")
    print(str1)
    print("cost time: "+str(time.time()-start))
    return str1

matchList = []
links = dbmapper.LinkMonResultMapper.list()
if len(links) > 0:
    for r in links:
        #print(r.id,r.pUrl,r.url,r.picPath)
        pic = work_dir+r.picPath.replace("/profile","")
        print(pic)
        if len(pic) > 0 and os.path.exists(pic):
            print(pic)
            ret = ocr(pic)
            linkEntity = LinkMonResult(r.id)
            linkEntity.ocrStr = ret.replace("'"," ")
            linkEntity.status = "1"
            dbmapper.LinkMonResultMapper.update(linkEntity)
            print(linkEntity.id,linkEntity.ocrStr)
            if ret.find(match_str) > -1:
                count = str(ret.count(match_str))
                print("匹配个数："+count)
                matchList.append({"pic":pic,"count":count})

print("检查字符："+match_str+ " 匹配结果：")
print(matchList)