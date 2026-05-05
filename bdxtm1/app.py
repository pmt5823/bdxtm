from flask import Flask, render_template, redirect, url_for
import sqlite3

from car_in import car_in
from car_out import car_out

app = Flask(__name__)

# ================= DATABASE =================
def get_all_cars():
    conn = sqlite3.connect("parking.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM cars ORDER BY id DESC")
    cars = cur.fetchall()

    conn.close()
    return cars


# ================= TRANG CHÍNH =================
@app.route("/")
def index():
    cars = get_all_cars()
    return render_template("index.html", cars=cars)


# ================= XE VÀO =================
@app.route("/car_in_camera")
def car_in_camera():
    car_in()
    return redirect(url_for("index"))


# ================= XE RA =================
@app.route("/car_out_camera")
def car_out_camera():
    car_out()
    return redirect(url_for("index"))


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)