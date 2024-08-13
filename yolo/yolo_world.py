import cv2
from ultralytics import YOLOWorld

# Load a model
model = YOLOWorld('yolov8s-world.pt')  # load a pretrained model (recommended for training)

# yolov8n.pt表示预训练模型
# task代表需要执行的任务：detect, segment, classify, pose
# 使用模型进行指定任务
#results = model(ARGS)

# model = YOLO("yolov8n.pt") task参数也可以不填写，它会根据模型去识别相应任务类别
# 检测图片
file = r".\assets\bus.jpg"
#file = r".\assets\zidane.jpg"

# Define custom classes
model.set_classes(["bus"])

results = model(file)
#print(results)
print(len(results[0].boxes))
print(results[0].boxes.cls)
print(results[0].boxes)
print(results[0].names)
print(results[0].masks)

# Show results
results[0].show()

## Show results
#res = results[0].plot(boxes=True) #boxes=False表示不展示预测框，True表示同时展示预测框
#cv2.imshow("YOLOv8", res)
#cv2.waitKey(0)