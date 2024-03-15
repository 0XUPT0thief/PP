import threading
import tkinter
import gui
import tag
import videoProcess
from remote.remote import create_video_server


def main():
    Rec = videoProcess.faceRec(
        r"D:\Special_Tools\Anaconda\envs\OCR\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml")
    app = create_video_server('remote/users.txt', Rec)
    thread_web = threading.Thread(target=app.run, kwargs={"host": '0.0.0.0'})
    thread_web.start()
    gui.CameraApp(tkinter.Tk(), "摄像头应用", Rec)
    tag.running = 0
    thread_web.join()


if __name__ == "__main__":
    main()
