
**cmd:**
yolo TASK MODE ARGS
举例：yolo detect predict model=yolov8n.pt source='1.jpg'
表示对图片1.jpg进行目标检测

TASK (optional) 表示模型任务类型，可以从列表 [detect, segment, classify, pose]选一个. 分别代表检测、分割、分类、姿态检测任务 
MODE (required) 表示模型需要执行的操作，可以从列表 [train, val, predict, export, track, benchmark]选一个，分别代表训练、验证、预测、模型转换、追踪、基准模型评估 
ARGS (optional) 表示其他的一些参数设置，后面详细说明

pip install onnx>=1.12.0 onnxruntime -i https://mirror.baidu.com/pypi/simple


**yolo export**
Predict:         yolo predict task=detect model=runs\detect\train2\weights\best.onnx imgsz=640
Validate:        yolo val task=detect model=runs\detect\train2\weights\best.onnx imgsz=640 data=coco128.yaml
Visualize:       https://netron.app
