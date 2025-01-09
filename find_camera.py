import cv2

def find_camera():
    for index in range(5):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                cv2.imshow(f'Camera {index}', frame)
                print(f"Camera found at index {index}")
                cap.release()
                cv2.destroyAllWindows()
                return index
        cap.release()
    print("No camera found.")
    return None

if __name__ == "__main__":
    find_camera()
