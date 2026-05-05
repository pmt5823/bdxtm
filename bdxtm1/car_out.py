from database import car_exit
from plate_recognition import get_plate_from_camera

def car_out():
    print("🚗 XE RA")

    plate = get_plate_from_camera()

    if plate is None:
        print("❌ Không đọc được biển")
        return

    print("Biển số:", plate)
    car_exit(plate)