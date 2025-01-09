import cv2

def adjust_camera_properties_interactively(camera_index):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"Cannot open camera at index {camera_index}")
        return

    # 回调函数（空，因为我们会在主循环中读取滑块值）
    def nothing(x):
        pass

    # 创建窗口和滑块
    cv2.namedWindow('Adjust IR Camera')
    cv2.createTrackbar('Brightness', 'Adjust IR Camera', 50, 100, nothing)
    cv2.createTrackbar('Contrast', 'Adjust IR Camera', 50, 100, nothing)
    cv2.createTrackbar('Saturation', 'Adjust IR Camera', 50, 100, nothing)
    cv2.createTrackbar('Gain', 'Adjust IR Camera', 50, 100, nothing)
    cv2.createTrackbar('Exposure', 'Adjust IR Camera', 0, 100, nothing)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # 获取滑块值并转换为浮点数
        brightness = cv2.getTrackbarPos('Brightness', 'Adjust IR Camera') / 100.0
        contrast = cv2.getTrackbarPos('Contrast', 'Adjust IR Camera') / 100.0
        saturation = cv2.getTrackbarPos('Saturation', 'Adjust IR Camera') / 100.0
        gain = cv2.getTrackbarPos('Gain', 'Adjust IR Camera') / 100.0
        exposure = (cv2.getTrackbarPos('Exposure', 'Adjust IR Camera') - 50) / 10.0  # 假设曝光范围

        # 设置相机参数
        cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        cap.set(cv2.CAP_PROP_CONTRAST, contrast)
        cap.set(cv2.CAP_PROP_SATURATION, saturation)
        cap.set(cv2.CAP_PROP_GAIN, gain)
        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)

        cv2.imshow('Adjust IR Camera', frame)

        if cv2.waitKey(1) == ord('q'):
            print("Exiting video capture.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_index = 1  # 替换为您的 IR 相机的设备索引
    adjust_camera_properties_interactively(camera_index)
