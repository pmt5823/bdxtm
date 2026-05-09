import cv2
from datetime import datetime
from plate_utils import read_plate
from database import car_out as db_car_out


def car_out():
    print("\n===== XE RA =====")
    print("Nhấn SPACE để chụp - ESC để thoát")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print(" Không mở được camera")
        return None

    plate = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print(" Không đọc được frame")
            break

        cv2.imshow("Camera - Xe ra", frame)
        key = cv2.waitKey(1)

        # Nhấn SPACE để chụp
        if key == 32:
            print(" Đã chụp ảnh")

            plate = read_plate(frame)

            if plate is None:
                print(" Không nhận diện được biển số")
                continue

            print(" Biển số:", plate)
            break

        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    if plate is None:
        print(" Hủy thao tác xe ra")
        return None

    # Tính tiền từ database
    fee = db_car_out(plate)

    if fee is None:
        print(" Không tìm thấy xe trong bãi")
        return None

    print(" Phí gửi xe:", fee, "VND")
    print(" Xe ra thành công:", plate)

    return fee