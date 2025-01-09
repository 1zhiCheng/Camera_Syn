import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IRCameraControllerGUI(tk.Tk):
    def __init__(self, camera_index=0):
        super().__init__()
        self.title("IR Camera Controller")
        self.geometry("1000x700")
        self.camera_index = camera_index

        # 初始化相机
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            logging.error("无法打开相机")
            self.destroy()
            return

        # 获取相机支持的属性
        self.supported_properties = self.get_supported_properties()

        # 创建GUI组件
        self.create_widgets()

        # 开始视频更新
        self.update_video()

    def get_supported_properties(self):
        # 列出常用的相机属性
        properties = {
            '亮度': cv2.CAP_PROP_BRIGHTNESS,
            '对比度': cv2.CAP_PROP_CONTRAST,
            '饱和度': cv2.CAP_PROP_SATURATION,
            '增益': cv2.CAP_PROP_GAIN,
            '曝光': cv2.CAP_PROP_EXPOSURE
        }
        supported = {}
        for name, prop in properties.items():
            value = self.cap.get(prop)
            if value != -1:
                supported[name] = prop
        return supported

    def create_widgets(self):
        # 视频显示标签
        self.video_label = ttk.Label(self)
        self.video_label.grid(row=0, column=0, rowspan=len(self.supported_properties)+1, padx=10, pady=10)

        # 滑块框架
        sliders_frame = ttk.Frame(self)
        sliders_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        # 创建滑块
        self.sliders = {}
        for i, (param, prop) in enumerate(self.supported_properties.items()):
            label = ttk.Label(sliders_frame, text=param)
            label.grid(row=i, column=0, sticky='w', pady=5)

            slider = ttk.Scale(sliders_frame, from_=0, to=100, orient='horizontal',
                               command=lambda val, p=prop: self.update_parameter(p, val))
            # 获取当前值并映射到滑块范围
            current_value = self.cap.get(prop)
            if param == '曝光':
                # 曝光值可能为负数，调整滑块范围
                slider.configure(from_=-100, to=100)
            slider.set(current_value)
            slider.grid(row=i, column=1, pady=5, padx=5)
            self.sliders[param] = slider

    def update_parameter(self, prop, value):
        try:
            # 设置相机属性
            if prop == cv2.CAP_PROP_EXPOSURE:
                # 曝光值需要转换为适当的范围
                exposure_value = float(value)
                success = self.cap.set(prop, exposure_value)
            else:
                success = self.cap.set(prop, float(value))
            if success:
                logging.info(f"成功设置属性 {prop} 为 {value}")
            else:
                logging.warning(f"无法设置属性 {prop} 为 {value}")
        except Exception as e:
            logging.error(f"设置属性失败: {e}")

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            # 转换颜色空间从 BGR 到 RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.video_label.after(10, self.update_video)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

def main():
    # 尝试多个设备索引以找到正确的相机
    #for index in range(5):
    if True:
        index = 1
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            logging.info(f"找到打开的相机设备: {index}")
            cap.release()
            app = IRCameraControllerGUI(camera_index=index)
            app.mainloop()
            return
    logging.error("未找到可用的相机设备。")

if __name__ == "__main__":
    main()
