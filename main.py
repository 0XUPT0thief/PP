import cv2

import gui
import videoProcess


def main():
    Gui = gui.gui("智能监控系统")
    faceRec = videoProcess.faceRec(
        r"D:\Special_Tools\Anaconda\envs\OCR\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml")
    camera = cv2.VideoCapture(0)
    while True:
        success, img = camera.read()
        img = faceRec.recognize(img)
        Gui.videoShow(img)
        if cv2.waitKey(17) == 27:
            break

    Gui.show()


if __name__ == "__main__":
    main()
