from flask import Flask, render_template, jsonify
from car_in import car_in
from car_out import car_out
import sqlite3

app = Flask(__name__)

# ================= DB =================
def get_db():
    conn = sqlite3.connect("parking.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")

# ================= XE ĐANG GỬI =================
@app.route("/api/cars")
def api_cars():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM cars
        WHERE time_out IS NULL
        ORDER BY id DESC
    """)

    data = cur.fetchall()
    conn.close()

    cars = []
    for c in data:
        cars.append({
            "id": c["id"],
            "plate": c["plate"],
            "time_in": c["time_in"]
        })

    return jsonify(cars)

# ================= LỊCH SỬ =================
@app.route("/api/history")
def api_history():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM cars
        WHERE time_out IS NOT NULL
        ORDER BY id DESC
    """)

    data = cur.fetchall()
    conn.close()

    history = []
    for c in data:
        history.append({
            "id": c["id"],
            "plate": c["plate"],
            "time_in": c["time_in"],
            "time_out": c["time_out"],
            "fee": c["fee"]
        })

    return jsonify(history)

# ================= CAMERA XE VÀO =================
@app.route("/car_in_camera")
def car_in_cam():
    car_in()
    return "Xe vào OK"

# ================= CAMERA XE RA =================
@app.route("/car_out_camera")
def car_out_cam():
    car_out()
    return "Xe ra OK"

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)