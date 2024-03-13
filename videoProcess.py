# 功能：对单帧图像进行人脸检测并进行位置框选

import cv2
import sys


class faceRec:
    def __init__(self, path):
        self.face_cascade = cv2.CascadeClassifier(path  # 加载人脸识别
            )

    def recognize(self, img):
        faces = self.face_cascade.detectMultiScale(img)
        for (x, y, w, h) in faces:  # 绘制矩形框
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        return img


