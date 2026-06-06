import cv2
import pyudev

def find_video_device_by_usb_id():
    vendor_id = '1f3a'
    product_id = '1002'

    context = pyudev.Context()

    for device in context.list_devices(subsystem='video4linux'):
        parent = device.find_parent('usb', 'usb_device')
        if parent is None:
            continue

        vid = parent.attributes.get('idVendor')
        pid = parent.attributes.get('idProduct')

        if vid and pid:
            vid = vid.decode()
            pid = pid.decode()

            if vid.lower() == vendor_id.lower() and pid.lower():
                return device.device_node  # e.g. "/dev/video2"
    return None

def main():
    dev_path = find_video_device_by_usb_id()
    
    if not dev_path:
        print("Camera with given USB ID not found")
        return
    print("Opening camera at:", dev_path)
    cap = cv2.VideoCapture(dev_path)
    if not cap.isOpened():
        print("Failed to open camera")
        return
    print("Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
            break
        cv2.namedWindow("S-Line usb cam", cv2.WINDOW_GUI_NORMAL)
        cv2.imshow("S-Line usb cam", frame)
        cv2.moveWindow('S-Line usb cam',200,100)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    while(True):
        main()
