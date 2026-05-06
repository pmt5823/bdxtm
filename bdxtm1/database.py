import sqlite3
from datetime import datetime

DB_NAME = "parking.db"


# ================= TẠO DATABASE =================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
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
def insert_car(plate):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    time_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        INSERT INTO cars (plate, time_in, time_out, fee)
        VALUES (?, ?, ?, ?)
    """, (plate, time_in, "", 0))

    conn.commit()
    conn.close()


# ================= XE RA =================
def car_exit(plate):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # tìm xe chưa ra
    cur.execute("""
        SELECT id, time_in FROM cars
        WHERE plate=? AND time_out=''
        ORDER BY id DESC LIMIT 1
    """, (plate,))

    row = cur.fetchone()

    if row is None:
        conn.close()
        return False

    car_id = row[0]
    time_in = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
    time_out = datetime.now()

    # tính tiền (3000đ mỗi phút demo)
    minutes = int((time_out - time_in).total_seconds() / 60) + 1
    fee = minutes * 3000

    cur.execute("""
        UPDATE cars
        SET time_out=?, fee=?
        WHERE id=?
    """, (time_out.strftime("%Y-%m-%d %H:%M:%S"), fee, car_id))

    conn.commit()
    conn.close()

    return True