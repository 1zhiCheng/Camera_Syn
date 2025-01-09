import usb.core
import usb.util
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
        for cfg in device:
            for intf in cfg:
                print(f"  接口: {intf.bInterfaceClass}, 子类: {intf.bInterfaceSubClass}, 协议: {intf.bInterfaceProtocol}")
                for ep in intf:
                    print(f"    端点: {ep.bEndpointAddress}, 属性: {ep.bmAttributes}")

if __name__ == "__main__":
    list_usb_devices()
