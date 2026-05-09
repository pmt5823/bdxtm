import sqlite3
from datetime import datetime

DB_NAME = "parking.db"


# ================= KẾT NỐI DB =================
def connect():
    return sqlite3.connect(DB_NAME)


# ================= TẠO DATABASE =================
def init_db():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate TEXT,
        time_in TEXT,
        time_out TEXT,
        fee INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ================= XE VÀO =================
def car_in(plate):
    conn = connect()
    c = conn.cursor()

    # kiểm tra xe đã ở trong bãi chưa
    c.execute("SELECT * FROM cars WHERE plate=? AND time_out IS NULL", (plate,))
    exist = c.fetchone()

    if exist:
        conn.close()
        print("Xe đã ở trong bãi!")
        return

    time_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute(
        "INSERT INTO cars (plate, time_in) VALUES (?, ?)",
        (plate, time_in)
    )

    conn.commit()
    conn.close()
    print("Đã lưu xe vào DB")


# ================= XE RA + TÍNH TIỀN =================
def car_out(plate):
    conn = connect()
    c = conn.cursor()

    c.execute("""
        SELECT id, time_in FROM cars
        WHERE plate=? AND time_out IS NULL
        ORDER BY id DESC LIMIT 1
    """, (plate,))

    row = c.fetchone()

    if row is None:
        conn.close()
        print("Không tìm thấy xe trong bãi")
        return 0

    car_id, time_in = row
    time_in = datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S")
    time_out = datetime.now()

    # ===== TÍNH TIỀN =====
    minutes = int((time_out - time_in).total_seconds() / 60) + 1
    fee = minutes * 5000   # 5k / phút

    c.execute("""
        UPDATE cars
        SET time_out=?, fee=?
        WHERE id=?
    """, (time_out.strftime("%Y-%m-%d %H:%M:%S"), fee, car_id))

    conn.commit()
    conn.close()

    print("Xe ra - phí:", fee)
    return fee


# ================= API CHO WEB =================
def get_all_cars():
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT * FROM cars ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    cars = []
    for row in rows:
        cars.append({
            "id": row[0],
            "plate": row[1],
            "time_in": row[2],
            "time_out": row[3] if row[3] else "Đang gửi",
            "fee": row[4] if row[4] else 0
        })

    return cars


# ================= THỐNG KÊ =================
def get_stats():
    conn = connect()
    c = conn.cursor()

    # xe đang đỗ
    c.execute("SELECT COUNT(*) FROM cars WHERE time_out IS NULL")
    parking = c.fetchone()[0]

    # tổng doanh thu
    c.execute("SELECT SUM(fee) FROM cars WHERE fee IS NOT NULL")
    revenue = c.fetchone()[0]
    if revenue is None:
        revenue = 0

    conn.close()

    return {
        "parking": parking,
        "revenue": revenue
    }