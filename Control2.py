import usb.core
import usb.util
import logging

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
        # 发送命令到设备的OUT端点
        device.write(endpoint_out, command)
        logging.info(f"发送命令: {command}")
    except usb.core.USBError as e:
        logging.error(f"发送命令失败: {e}")

def read_bulk_response(device, endpoint_in, size=64):
    try:
        # 从设备的IN端点读取响应
        response = device.read(endpoint_in, size)
        response_str = ''.join([chr(x) for x in response])
        logging.info(f"收到响应: {response_str}")
        return response_str
    except usb.core.USBError as e:
        logging.error(f"读取响应失败: {e}")
        return None

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

    # 发送命令
    command = b'SET_BRIGHTNESS:70'  # 根据设备协议调整
    send_bulk_command(device, endpoint_out, command)

    # 读取响应
    response = read_bulk_response(device, endpoint_in)

if __name__ == "__main__":
    main()
