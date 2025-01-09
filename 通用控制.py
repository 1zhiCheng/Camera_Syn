import cv2
import serial
import threading
import time
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def open_serial_port(port, baudrate=9600, timeout=1):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        logging.info(f"打开串行端口: {port}，波特率: {baudrate}")
        return ser
    except serial.SerialException as e:
        logging.error(f"无法打开串行端口: {e}")
        return None

def send_serial_command(ser, command):
    try:
        ser.write(command.encode())  # 根据协议可能需要发送字节
        logging.info(f"发送命令: {command}")
        time.sleep(0.5)  # 等待响应
        response = ser.read_all().decode()
        logging.info(f"收到响应: {response}")
        return response
    except Exception as e:
        logging.error(f"发送命令失败: {e}")
        return None

def control_camera_serial(ser, command_interval=10):
    while True:
        command = 'TRIGGER'  # 替换为实际命令
        response = send_serial_command(ser, command)
        logging.info(f"命令响应: {response}")
        time.sleep(command_interval)

def capture_video(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        logging.error(f"无法打开相机，设备索引: {camera_index}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.warning("无法获取视频帧，退出循环。")
            break

        cv2.imshow('IR Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logging.info("用户请求退出程序。")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 替换为您的串行端口，如COM3
    ser = open_serial_port('COM3', baudrate=115200)
    if ser:
        # 启动控制线程
        control_thread = threading.Thread(target=control_camera_serial, args=(ser, 10), daemon=True)
        control_thread.start()

        # 启动视频捕获
        capture_video(camera_index=0)
