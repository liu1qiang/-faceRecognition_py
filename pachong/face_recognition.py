#encoding=utf8
#对训练好的yml文件进行人脸检测判断是谁，目前只有30%的识别率
from cv2 import cv2 as cv2 
import redis
import json
pool = redis.ConnectionPool(host="127.0.0.1", port=6379,max_connections=1024,decode_responses=True)
conn = redis.Redis(connection_pool=pool)
names = conn.lrange("names",0,-1)
print ("库中取得姓名列表：")
print (names)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

idnum = 0
cam = cv2.VideoCapture(0)
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH))
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        idnum, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        print (idnum)
        if confidence < 100:
            print ('当前识别人名为：'+names[idnum])
            idnum = names[idnum]
            confidence = "{0}%".format(round(100 - confidence))
        else:
            print ("未识别到人")
            idnum = "unknown"
            confidence = "{0}%".format(round(100 - confidence))

        cv2.putText(img, str(idnum), (x+5, y-5), font, 1, (0, 0, 255), 1)
        cv2.putText(img, str(confidence), (x+5, y+h-5), font, 1, (0, 0, 0), 1)

    cv2.imshow('camera', img)
    k = cv2.waitKey(10)
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()