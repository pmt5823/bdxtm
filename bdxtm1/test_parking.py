from parking_system import car_enter, car_exit

plate = input("Nhập biển số: ")
mode = input("1 = xe vào | 2 = xe ra : ")

if mode == "1":
    car_enter(plate)
else:
    car_exit(plate)