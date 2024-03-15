import tkinter as tk
import cv2
from PIL import Image, ImageTk
import time
import threading
import os



class CameraApp:
    def __init__(self, window, window_title, rec, video_source=0):
        self.window = window
        self.window.title(window_title)
        # 创建一个IntVar变量来存储复选框的值
        self.flip_var = tk.IntVar()

        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)
        # 人脸识别部分
        self.rec = rec

        self.text_to_display = ""
        self.display_text_timer_start = None
        self.display_text_duration = 3  # 文本显示持续时间，单位为秒
        self.show_time = False  # 是否显示时间的标志
        self.flip_value = self.flip_var.get()  # 是否镜像显示

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # 拍照按钮
        self.btn_snapshot = tk.Button(window, text="拍照", width=10, command=self.snapshot)
        self.btn_snapshot.pack(side=tk.LEFT, padx=5, pady=5)  # 添加 padx 和 pady 来控制按钮与其他控件的间距

        # 时间复选框
        self.show_time_checkbox = tk.Checkbutton(self.window, text="时间", command=self.toggle_show_time)
        self.show_time_checkbox.pack(side=tk.LEFT, padx=5, pady=5)  # 添加 padx 和 pady 来控制复选框与其他控件的间距

        # 创建镜像复选框，并将其与flip_var关联起来
        self.flip_checkbox = tk.Checkbutton(self.window, text="水平镜像", variable=self.flip_var,
                                            command=self.toggle_flip)
        self.flip_checkbox.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_exit = tk.Button(window, text="退出", width=10, command=self.exit)
        self.btn_exit.pack(side=tk.RIGHT)

        self.window.protocol("WM_DELETE_WINDOW", self.exit)  # 注册关闭事件处理函数

        self.is_running = True  # 用于控制线程执行
        self.thread = threading.Thread(target=self.update)
        self.thread.start()

        self.window.mainloop()

    def snapshot(self):
        def show_snapshot(frame):
            cv2.imshow("Snapshot", frame)
            cv2.waitKey(500)  # 显示0.5秒后关闭窗口
            cv2.destroyWindow("Snapshot")

        ret, frame = self.vid.read()
        if ret:
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            filename = f"snapshot_{timestamp}.jpg"
            folder_path = timestamp.split("_")[0]
            # 使用os.makedirs()函数创建文件夹，如果文件夹已存在则不会报错
            os.makedirs(folder_path, exist_ok=True)
            cv2.imwrite(folder_path + "/" + filename, frame)
            # 更新要显示的文本信息
            self.text_to_display = f"Photo saved: {filename}"
            # 更新拍照执行时间
            self.display_text_timer_start = time.time()

            # 使用新线程处理图片显示
            threading.Thread(target=show_snapshot, args=(frame,)).start()

    def exit(self):
        self.is_running = False  # 停止线程
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()

    def update(self):
        while self.is_running:
            ret, frame = self.vid.read()
            frame = self.rec.recognize(frame)
            if ret:
                # 根据复选框的状态水平翻转视频帧
                if self.flip_var.get() == 1:
                    # 反转画面 0 垂直、1水平、-1水平和垂直
                    frame = cv2.flip(frame, 1)
                if self.show_time:
                    # 获取当前时间
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # 在帧上绘制当前时间文本
                    cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                # 如果有要显示的文本信息
                if self.text_to_display:
                    # 检查是否需要隐藏文本
                    if time.time() - self.display_text_timer_start > self.display_text_duration:
                        self.text_to_display = ""

                    # 在左下角叠加显示文本信息
                    cv2.putText(frame, self.text_to_display, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 255, 0), 2)
                photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                self.canvas.photo = photo  # 避免被垃圾回收
            time.sleep(0.010)  # 控制刷新频率

    def toggle_show_time(self):
        self.show_time = not self.show_time

    def toggle_flip(self):
        # 空方法，用于处理复选框状态更改时的事件
        pass


if __name__ == "__main__":
    # 创建主窗口并运行应用
    CameraApp(tk.Tk(), "摄像头应用")
