import tkinter

import cv2
from PIL import Image, ImageTk


class gui:
    """程序窗口"""

    def __init__(self, window_name):
        self.mainWindow = tkinter.Tk(window_name)
        self.videoSize = (300, 400)
        # 视频显示画布
        self.canvas = tkinter.Canvas(self.mainWindow, bg='white', width=self.videoSize[0], height=self.videoSize[1])

    def ImageConvert(self, img):  # 图像转换，以在画布中显示
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image).resize(self.videoSize)
        image = ImageTk.PhotoImage(image=image)
        return image

    def videoShow(self, img):
        while True:
            pic = self.ImageConvert(img)
            self.canvas.create_image(0, 0, anchor='nw', image=pic)
            self.mainWindow.update_idletasks()
            self.mainWindow.update()

    def show(self):
        self.mainWindow.mainloop()
