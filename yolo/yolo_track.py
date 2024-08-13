import cv2
from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt",task="detect")  # load a pretrained model (recommended for training)

# yolov8n.pt表示预训练模型
# task代表需要执行的任务：detect, segment, classify, pose
# 使用模型进行指定任务
#results = model(ARGS)

# model = YOLO("yolov8n.pt") task参数也可以不填写，它会根据模型去识别相应任务类别
# 检测视频
file = r"assets/test.mp4"
results = model.track(source=file,show=True)
res = results[0].plot(boxes=True) #boxes=False表示不展示预测框，True表示同时展示预测框
cv2.imshow("YOLOv8", res)
cv2.waitKey(0)