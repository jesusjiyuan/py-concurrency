import time
from io import BytesIO

import requests
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
import sys
sys.path.append("/java_web/cloudcs2mon/pyspace/")
import os
os.chdir(os.path.dirname(__file__))

import logs

from paddleocr.tools.infer.utility import draw_ocr_box_txt, draw_boxes

import confhelper
import dbmapper
from entity import LinkMonResult, MonKeyword, MonLinkBatch, MonTask

logger = logs.get_logger("simple")
logger.info("hello")

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

ocr = PaddleOCR(use_angle_cls=True, lang="ch",ocr_version="PP-OCRv4"
                ,rec_image_shape="3, 96, 960"
                ,use_onnx=False
                ,det_limit_side_len=10000
                ,det_limit_type="max"
                )
# img_path = confhelper.confdata().get("img_path")
# out_img_path = confhelper.confdata().get("out_img_path")
# db_out_img_path = confhelper.confdata().get("db_out_img_path")
# out_prefix = confhelper.confdata().get("out_prefix")
work_dir = confhelper.confdata().get("work_dir")
print("sys.argv: {}".format(sys.argv))
batchNo = sys.argv[1]

def invoke_ocr(id,imgfile,picPath):
    result = ocr.ocr(imgfile, cls=True)
    print(result)
    for line in result:
        print(len(line))
        print(line)
    print('图片中的第一个检测结果')
    print(result[0][0])
    print('图片中的第一个检测结果的框坐标')
    print(result[0][0][0])
    print('图片中的第一个检测结果的文字')
    print(result[0][0][1][0])

    from  PIL import  Image

    image = Image.open(imgfile).convert('RGB')
    width, height = image.size
    boxes = [result[0][i][0] for i in range(len(result[0]))]
    print(boxes)
    txts = [result[0][i][1][0] for i in range(len(result[0]))]
    print(txts)
    scores = [result[0][i][1][1] for i in range(len(result[0]))]
    print(scores)
    ocrStr = "".join(txts).replace("'","")
    boxes1 = []
    matched_kwords=[]
    #dbmapper.MonKeywordMapper.list()
    monTask = dbmapper.MonTaskMapper.get_by_batchno(batchNo=batchNo)
    if monTask is not None and len(monTask.kwIds) > 0:
        keyws = dbmapper.MonKeywordMapper.list_by_ids(monTask.kwIds.split(","))
        for i in range(len(result[0])):
            box = result[0][i][0]
            txt = result[0][i][1][0]
            if len(keyws) > 0:
                for k in keyws:
                    print("keyword :",k.name)
                    if str(txt).find(k.name) > -1:
                        matched_kwords.append(k.name)
                        boxes1.append(box)
        if len(boxes1) > 0:
            im_show = draw_boxes(image, boxes1)
            im_show = Image.fromarray(im_show)
            ofile = picPath.replace(".png","-check.png")
            ofile = work_dir + "/monlink"+ofile
            im_show.save(ofile)
            db_ofile = "/profile"+ofile.replace(work_dir,"")
            print("ocr: ",ofile)
            dbmapper.LinkMonResultMapper.updateMatch(LinkMonResult(id=id,ocrStr=ocrStr,matchPicPath=db_ofile,status="2",kwords=",".join(matched_kwords)))
        else:
            dbmapper.LinkMonResultMapper.updateMatch(LinkMonResult(id=id,ocrStr=ocrStr,matchPicPath="",status="1",kwords=""))

os.chdir(os.path.dirname(__file__))
links = dbmapper.LinkMonResultMapper.list(LinkMonResult(batchNo=batchNo))
if len(links) > 0:
    for l in links:
        print(l.id,l.picPath,l.linkId)
        #picPath = work_dir + l.picPath.replace("/profile","")
        #if os.path.exists(picPath):
        #    invoke_ocr(l.id,picPath)
        #    dbmapper.MonLinkBatchMapper.updateSatus(MonLinkBatch(batchNo=batchNo,linkId=l.linkId,status="1",endTime=time.localtime()))
        try:
            picPath = "http://112.64.36.81:8088/"+ l.picPath
            resp = requests.get(picPath)
            img_data = resp.content
            # 创建Image对象并保存为文件
            image = Image.open(BytesIO(img_data))
            output_filepath = "d:/tmp/image.png"
            image.save(output_filepath)
            invoke_ocr(l.id,output_filepath,picPath)
            dbmapper.MonLinkBatchMapper.updateSatus(MonLinkBatch(batchNo=batchNo,linkId=l.linkId,status="1",endTime=time.localtime()))
        except Exception as e:
            print(e)
    dbmapper.MonTaskMapper.updateStatus(MonTask(batchNo=batchNo,status="1",endTime=time.localtime()))