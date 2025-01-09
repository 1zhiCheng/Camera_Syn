import usb.core
import usb.util
import serial.tools.list_ports
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def list_usb_devices():
    devices = usb.core.find(find_all=True)
    for device in devices:
        vid = f"{device.idVendor:04x}"
        pid = f"{device.idProduct:04x}"
        try:
            manufacturer = usb.util.get_string(device, device.iManufacturer)
        except:
            manufacturer = "Unknown"
        try:
            product = usb.util.get_string(device, device.iProduct)
        except:
            product = "Unknown"
        print(f"设备: VID={vid}, PID={pid}, 制造商={manufacturer}, 产品={product}")

def find_faker_usb_device(vid=None, pid=None):
    devices = serial.tools.list_ports.comports()
    for port in devices:
        description = port.description
        # 假设描述中包含制造商或产品名称
        if "FAKER-USB" in description:
            print(f"找到FAKER-USB设备: {port.device}, 描述: {description}, VID: {port.vid}, PID: {port.pid}")
            return port.device
    print("未找到FAKER-USB设备。")
    return None

if __name__ == "__main__":
    print("列出所有USB设备:")
    list_usb_devices()
    
    print("\n查找FAKER-USB设备的COM端口:")
    com_port = find_faker_usb_device()
    if com_port:
        print(f"选择的COM端口: {com_port}")
    else:
        print("请检查FAKER-USB转接器连接和驱动程序。")
