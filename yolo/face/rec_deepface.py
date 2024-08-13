from deepface import DeepFace
from ultralytics import YOLO
#----Face recognition models
models = [
    "VGG-Face",
    "Facenet",
    "Facenet512",
    "OpenFace",
    "DeepFace",
    "DeepID",
    "ArcFace",
    "Dlib",
    "SFace",
]
backends = [
    'opencv',
    'ssd',
    'dlib',
    'mtcnn',
    'retinaface',
    'mediapipe',
    'yolov8',
    'yunet',
    'fastmtcnn',
]
metrics = ["cosine", "euclidean", "euclidean_l2"]

file1 = r"D:\workspace\spaceai\datasets\test\face\0000.jpg"
file2 = r"D:\workspace\spaceai\datasets\test\face\0006.jpg"
file_path = r"D:\workspace\spaceai\datasets\test\face"

#face verification
result = DeepFace.verify(img1_path = file1, img2_path = file2, model_name = "VGG-Face")
print("result: {}".format(str(result).replace(',',',\n')))

#face recognition
dfs = DeepFace.find(img_path = file1,db_path = file_path, enforce_detection=False,model_name = "VGG-Face")
print(f"recognition: {dfs}")

#embeddings
embedding_objs = DeepFace.represent(img_path =file1, model_name = "VGG-Face")
print(f"embedding_objs: {embedding_objs}")

actions = ['age', 'gender', 'race', 'emotion']
#analyze
#age, gender, facial expression (including angry, fear, neutral, sad, disgust, happy and surprise) and race (including asian, white, middle eastern, indian, latino and black) predictions
objs = DeepFace.analyze(img_path = file1 ,actions=actions)
print(f"analyze:{objs}")

#face detection and alignment
face_objs = DeepFace.extract_faces(img_path = file1, target_size = (224, 224), detector_backend  = backends[4])
print(f"detection and alignment:{face_objs}")

#Real Time Analysis -
#DeepFace.stream(db_path = "C:/User/Sefik/Desktop/database")