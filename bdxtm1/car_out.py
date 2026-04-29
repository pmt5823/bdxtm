from database import find_car, remove_car
from datetime import datetime

PRICE_PER_HOUR = 5000  # 5k / giờ

def car_out(plate):
    car = find_car(plate)

    if car is None:
        print("Không tìm thấy xe!")
        return

    time_in = datetime.strptime(car[2], "%Y-%m-%d %H:%M:%S")
    time_out = datetime.now()

    hours = (time_out - time_in).total_seconds() / 3600
    money = int(hours * PRICE_PER_HOUR)

    remove_car(plate)

    print("Xe ra:", plate)
    print("Số tiền:", money, "VND")