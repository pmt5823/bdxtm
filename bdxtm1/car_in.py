from database import insert_car
from plate_recognition import get_plate_from_camera

def car_in():
    print("🚗 XE VÀO")

    plate = get_plate_from_camera()

    if plate is None:
        print("❌ Không đọc được biển")
        return

    print("Biển số:", plate)
    insert_car(plate)