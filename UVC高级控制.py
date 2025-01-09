import uvc
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IRCameraControllerGUI(tk.Tk):
    def __init__(self, device):
        super().__init__()
        self.title("IR Camera Controller")
        self.geometry("1000x700")
        self.device = device

        # 获取支持的属性
        self.supported_controls = self.get_supported_controls()

        # 创建GUI组件
        self.create_widgets()

        # 开始视频更新
        self.update_video()

    def get_supported_controls(self):
        # 列出支持的控制
        controls = {
            'Brightness': uvc.UVCCameraControl.Brightness,
            'Contrast': uvc.UVCCameraControl.Contrast,
            'Saturation': uvc.UVCCameraControl.Saturation,
            'Gain': uvc.UVCCameraControl.Gain,
            'Exposure': uvc.UVCCameraControl.ExposureAuto
        }
        supported = {}
        for name, control in controls.items():
            try:
                value = self.device.get_ctrl(control)
                supported[name] = control
            except uvc.USBError:
                pass
        return supported

    def create_widgets(self):
        # 视频显示标签
        self.video_label = ttk.Label(self)
        self.video_label.grid(row=0, column=0, rowspan=len(self.supported_controls)+1, padx=10, pady=10)

        # 滑块框架
        sliders_frame = ttk.Frame(self)
        sliders_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        # 创建滑块
        self.sliders = {}
        for i, (param, control) in enumerate(self.supported_controls.items()):
            label = ttk.Label(sliders_frame, text=param)
            label.grid(row=i, column=0, sticky='w', pady=5)

            slider = ttk.Scale(sliders_frame, from_=0, to=100, orient='horizontal',
                               command=lambda val, c=control: self.update_control(c, val))
            # 获取当前值
            current_value = self.device.get_ctrl(control)
            slider.set(current_value)
            slider.grid(row=i, column=1, pady=5, padx=5)
            self.sliders[param] = slider

    def update_control(self, control, value):
        try:
            # 设置控制值
            self.device.set_ctrl(control, int(float(value)))
            logging.info(f"成功设置 {control} 为 {value}")
        except uvc.USBError as e:
            logging.error(f"设置 {control} 失败: {e}")

    def update_video(self):
        frame = self.device.get_frame()
        if frame is not None:
            img = frame.image
            # 转换颜色空间从 BGR 到 RGB
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img_pil)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.video_label.after(10, self.update_video)

    def __del__(self):
        if self.device is not None:
            self.device.close()

def main():
    # 查找所有UVC设备
    devices = uvc.device_list()
    if not devices:
        logging.error("未找到UVC设备。")
        return

    # 选择第一个设备
    device = devices[0]
    logging.info(f"使用设备: {device}")

    # 打开设备
    try:
        cam = device.open()
    except uvc.USBError as e:
        logging.error(f"无法打开设备: {e}")
        return

    # 启动GUI
    app = IRCameraControllerGUI(cam)
    app.mainloop()

    # 关闭设备
    cam.close()

if __name__ == "__main__":
    main()
