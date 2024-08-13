# import json
#
#     import face_recognition as face
#     import matplotlib.pyplot as plt
#
#     file = r"D:\workspace\spaceai\datasets\test\face\刘亦菲_0.jpg"
#     file1 = r"D:\workspace\spaceai\datasets\test\face\刘亦菲_4.jpg"
#
#
#     def showim(face_locations):
#         # 打印每张脸的位置信息
#         for face_location in face_locations:
#             top, right, bottom, left = face_location
#             print(f"发现一张脸位于 Top: {top}, Left: {left}, Bottom: {bottom}, Right: {right}")
#
#             # 绘制人脸框
#             plt.imshow(image[top:bottom, left:right])
#             plt.show()
#     # 加载图片
#     image = face.load_image_file(file)
#     image1 = face.load_image_file(file1)
#     face_locations1 = face.face_locations(image1, model="cnn")
#
#     # 检测图片中的所有人脸 hog cnn
#     face_locations = face.face_locations(image, model="cnn")
#     face_landmarks = face.face_landmarks(image,face_locations)
#     print(f"face_landmarks:")
#     [print(str(land).replace("],","]'\n")) for land in face_landmarks]
#     #print(json.dumps(face_landmarks[0],indent=1))
#
#     showim(face_locations)
#     showim(face_locations1)
#
#
#     known = face.face_encodings(image,face_locations)[0]
#     unknown = face.face_encodings(image1,face_locations1)[0]
#     distance = face.face_distance([known],unknown)
#     print(f"distance :{distance}")
#     rec_result = face.compare_faces([known],unknown,tolerance=0.3)
#     print(f"rec_result: {rec_result}")
#
#
