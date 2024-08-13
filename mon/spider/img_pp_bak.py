from paddleocr import PaddleOCR, draw_ocr
import os

from paddleocr.tools.infer.utility import draw_ocr_box_txt, draw_boxes

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

ocr = PaddleOCR(use_angle_cls=True, lang="ch",ocr_version="PP-OCRv4"
                ,rec_image_shape="3, 96, 960"
                ,use_onnx=False
                ,det_limit_side_len=10000
                ,det_limit_type="max"
                )
img_path = 'pic/1-27-0E·LANDKIDS童装秋装新品男女童时尚拼色立领半拉链上衣.png'
result = ocr.ocr(img_path, cls=True)
print(result)
for line in result:
    print(len(line))
    print(line)
print('图片中的第一个检测结果')
print(result[0][0])
#print('图片中的第二个检测结果')
#print(result[0][1])
print('图片中的第一个检测结果的框坐标')
print(result[0][0][0])
print('图片中的第一个检测结果的文字')
print(result[0][0][1][0])

from  PIL import  Image

image = Image.open(img_path).convert('RGB')

width, height = image.size

boxes = [result[0][i][0] for i in range(len(result[0]))]
print(boxes)
txts = [result[0][i][1][0] for i in range(len(result[0]))]
print(txts)
scores = [result[0][i][1][1] for i in range(len(result[0]))]
print(scores)
im_show = draw_boxes(image, boxes)
im_show = Image.fromarray(im_show)
im_show.save('./pic/1-27-0E·LANDKIDS童装秋装新品男女童时尚拼色立领半拉链上衣-check.png')