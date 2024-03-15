import tkinter
import cv2
import gui
import videoProcess



def main():
    Rec = videoProcess.faceRec(
        r"D:\Special_Tools\Anaconda\envs\OCR\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml")

    gui.CameraApp(tkinter.Tk(), "摄像头应用", Rec)


if __name__ == "__main__":
    main()
