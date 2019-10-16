#人脸图片数据收集
from cv2 import cv2 as cv2 
import os
import numpy as np

# 人脸识别分类器
face_detector = cv2.CascadeClassifier(r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')

# 识别眼睛的分类器
# eyeCascade = cv2.CascadeClassifier(r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\Lib\site-packages\cv2\data\haarcascade_eye.xml')

# 开启摄像头
cap = cv2.VideoCapture(0)
face_id = input('\n enter user id:')
ok = True

while True:

    # 从摄像头读取图片

    sucess, img = cap.read()

    # 转为灰度图片

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 检测人脸

    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    count = 0
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))
        count += 1

        # 保存图像
        cv2.imwrite("Facedata/User." + str(face_id) + '.' + str(count) + '.jpg', gray[y: y + h, x: x + w])

        cv2.imshow('image', img)

    # 保持画面的持续。

    k = cv2.waitKey(1)

    if k == 27:   # 通过esc键退出摄像
        break

    elif count >= 1000:  # 得到1000个样本后退出摄像
        break

# 关闭摄像头
cap.release()
cv2.destroyAllWindows()