import cv2
from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n-pose.pt",task="pose")  # load a pretrained model (recommended for training)

# yolov8n.pt表示预训练模型
# task代表需要执行的任务：detect, segment, classify, pose
# 使用模型进行指定任务
#results = model(ARGS)

# model = YOLO("yolov8n.pt") task参数也可以不填写，它会根据模型去识别相应任务类别
# 检测视频
file = r"assets/test.mp4"
cap = cv2.VideoCapture(file)
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    if success:
        results = model(frame)
        # Visualize the results on the frame
        annotated_frame = results[0].plot(boxes=False)
        # Display the annotated frame
        cv2.imshow("YOLOv8", annotated_frame)
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

