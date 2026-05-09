import cv2
from datetime import datetime
from plate_utils import read_plate
from database import car_in as db_car_in


def car_in():
    print("\n===== XE VÀO =====")
    print("Nhấn SPACE để chụp - ESC để thoát")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print(" Không mở được camera")
        return

    plate = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print(" Không đọc được frame")
            break

        cv2.imshow("Camera - Xe vao", frame)
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

        # ESC để thoát
        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    if plate is None:
        print(" Hủy thao tác xe vào")
        return

    # Lưu DB
    db_car_in(plate)
    print(" Xe vào thành công:", plate)