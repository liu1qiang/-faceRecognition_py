#对收集到的人脸图片进行训练，生成yml文件
import numpy as np
from PIL import Image
import os
from cv2 import cv2 as cv2 
# 人脸数据路径
path = './Facedata'

detector = cv2.CascadeClassifier(r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]  # join函数的作用？
    faceSamples = []
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')   # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x: x + w])
            ids.append(id)
    return faceSamples, ids


print('Training faces. It will take a few seconds. Wait ...')
faces, ids = getImagesAndLabels(path)
print (ids,len(ids))
if len(ids) == 0:
    print ("训练图像数据不能小于1张")
else:
    recognizer.train(faces, np.array(ids))
    recognizer.write(r'face_trainer\trainer.yml')
    print("{0} faces trained. Exiting Program".format(len(np.unique(ids))))