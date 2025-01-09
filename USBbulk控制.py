import usb.core
import usb.util
import logging
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_usb_device(vid, pid):
    device = usb.core.find(idVendor=vid, idProduct=pid)
    if device is None:
        logging.error(f"无法找到设备: VID={vid:04x}, PID={pid:04x}")
    else:
        logging.info(f"找到设备: VID={vid:04x}, PID={pid:04x}")
    return device

def send_bulk_command(device, endpoint_out, command):
    try:
        device.write(endpoint_out, command)
        logging.info(f"发送命令: {command}")
    except usb.core.USBError as e:
        logging.error(f"发送命令失败: {e}")

def read_bulk_response(device, endpoint_in, size=64):
    try:
        response = device.read(endpoint_in, size)
        response_str = ''.join([chr(x) for x in response])
        logging.info(f"收到响应: {response_str}")
        return response_str
    except usb.core.USBError as e:
        logging.error(f"读取响应失败: {e}")
        return None

class IRCameraControllerGUI(tk.Tk):
    def __init__(self, device, endpoint_out, endpoint_in):
        super().__init__()
        self.device = device
        self.endpoint_out = endpoint_out
        self.endpoint_in = endpoint_in
        self.title("IR Camera Controller")
        self.geometry("800x600")
        self.create_widgets()
        self.cap = cv2.VideoCapture(0)  # 根据实际设备索引修改
        if not self.cap.isOpened():
            logging.error("无法打开相机")
            return
        self.update_video()

    def create_widgets(self):
        # 视频显示标签
        self.video_label = ttk.Label(self)
        self.video_label.grid(row=0, column=0, rowspan=5, padx=10, pady=10)

        # 滑块框架
        sliders_frame = ttk.Frame(self)
        sliders_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        # 定义参数和初始值
        parameters = {
            '亮度': 50,
            '对比度': 50,
            '饱和度': 50,
            '增益': 50,
            '曝光': 50
        }

        # 创建滑块
        self.sliders = {}
        for i, (param, value) in enumerate(parameters.items()):
            label = ttk.Label(sliders_frame, text=param)
            label.grid(row=i, column=0, sticky='w', pady=5)

            slider = ttk.Scale(sliders_frame, from_=0, to=100, orient='horizontal',
                               command=lambda val, p=param: self.update_parameter(p, val))
            slider.set(value)
            slider.grid(row=i, column=1, pady=5, padx=5)
            self.sliders[param] = slider

    def update_parameter(self, parameter, value):
        logging.info(f"调整参数: {parameter}，值: {value}")
        # 根据参数名称发送相应的控制命令
        cmd_map = {
            '亮度': f"SET_BRIGHTNESS:{int(float(value))}",
            '对比度': f"SET_CONTRAST:{int(float(value))}",
            '饱和度': f"SET_SATURATION:{int(float(value))}",
            '增益': f"SET_GAIN:{int(float(value))}",
            '曝光': f"SET_EXPOSURE:{int(float(value))}"
        }
        command = cmd_map.get(parameter)
        if command and self.device:
            send_bulk_command(self.device, self.endpoint_out, command.encode('utf-8'))

            # 读取响应（可选）
            response = read_bulk_response(self.device, self.endpoint_in)
            if response:
                logging.info(f"响应: {response}")

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
    # 替换为您的设备的VID和PID
    VID = 0x20b4
    PID = 0x10f9

    device = find_usb_device(VID, PID)
    if device is None:
        return

    # 设置配置
    try:
        device.set_configuration()
    except usb.core.USBError as e:
        logging.error(f"设置配置失败: {e}")
        return

    # 获取活动配置
    cfg = device.get_active_configuration()
    intf = cfg[(0,0)]

    # 获取端点地址
    endpoint_out = None
    endpoint_in = None
    for ep in intf:
        if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT:
            endpoint_out = ep.bEndpointAddress
        elif usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN:
            endpoint_in = ep.bEndpointAddress

    if endpoint_out is None or endpoint_in is None:
        logging.error("未找到适用的端点。")
        return

    # 启动GUI
    app = IRCameraControllerGUI(device, endpoint_out, endpoint_in)
    app.mainloop()

    # 关闭设备
    usb.util.release_interface(device, intf.bInterfaceNumber)
    usb.util.dispose_resources(device)

if __name__ == "__main__":
    main()
