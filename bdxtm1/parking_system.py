import csv
from datetime import datetime

FILE_NAME = "parking_data.csv"
PRICE_PER_HOUR = 5000  # 5k / giờ (bạn đổi tùy ý)

# ===============================
# đọc danh sách xe đang gửi
# ===============================
def load_data():
    data = {}
    try:
        with open(FILE_NAME, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    data[row[0]] = row[1]
    except:
        pass
    return data

# ===============================
# lưu lại danh sách xe
# ===============================
def save_data(data):
    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        for plate, time_in in data.items():
            writer.writerow([plate, time_in])

# ===============================
# xe vào bãi
# ===============================
def car_enter(plate):
    data = load_data()

    if plate in data:
        print("Xe đã có trong bãi!")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data[plate] = now
    save_data(data)

    print("Xe vào:", plate)
    print("Thời gian vào:", now)

# ===============================
# xe ra bãi + tính tiền
# ===============================
def car_exit(plate):
    data = load_data()

    if plate not in data:
        print("Không tìm thấy xe trong bãi!")
        return

    time_in = datetime.strptime(data[plate], "%Y-%m-%d %H:%M:%S")
    time_out = datetime.now()

    hours = (time_out - time_in).total_seconds() / 3600
    cost = int(hours * PRICE_PER_HOUR) + 5000  # tối thiểu 5k

    print("Xe ra:", plate)
    print("Thời gian vào:", time_in)
    print("Thời gian ra:", time_out)
    print("Tiền gửi:", cost, "VND")

    del data[plate]
    save_data(data)