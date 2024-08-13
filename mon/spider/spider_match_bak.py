import base64
import json
import time

import requests
import os

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
def traverse_dir(path):
    for root, dirs, files in os.walk(path):
        print("当前目录：", root)
        print("子目录列表：", dirs)
        #print("文件列表：", files)
        for pic in files:
            ret = ocr(root+"\\"+pic)
            if ret.find(match_str) > -1:
                count = str(ret.count(match_str))
                print("匹配个数："+count)
                #matchList.append(pic)
                matchList.append({"pic":pic,"count":count})

#dir_path = "D:\DOC\docker-k8s\docker\python\pic\jiadian"
dir_path = "D:\\tmp\pic\jiadian"
print('待遍历的目录为：', dir_path)
print('遍历结果为：')
traverse_dir(dir_path)
# for pic in picList:
#     ret = ocr(pic)
#     if ret.find(match_str) > -1:
#         matchList.append(pic)

print("检查字符："+match_str+ " 匹配结果：")
print(matchList)