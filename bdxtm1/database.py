import sqlite3
from datetime import datetime

DB_NAME = "parking.db"

# Tạo database và bảng
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT,
            time_in TEXT
        )
    """)

    conn.commit()
    conn.close()

# Thêm xe vào bãi
def add_car(plate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    time_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO cars (plate, time_in) VALUES (?,?)",
                   (plate, time_in))

    conn.commit()
    conn.close()

# Lấy danh sách xe đang gửi (WEB dùng hàm này)
def get_all_cars():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()

    conn.close()
    return cars

# Tìm xe theo biển số
def find_car(plate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cars WHERE plate=?", (plate,))
    car = cursor.fetchone()

    conn.close()
    return car

# Xoá xe khi ra bãi
def remove_car(plate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cars WHERE plate=?", (plate,))

    conn.commit()
    conn.close()