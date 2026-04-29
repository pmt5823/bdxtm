from flask import Flask, render_template, redirect, url_for
from database import get_all_cars
from car_in import car_in
from car_out import car_out
from plate_recognition import read_plate

app = Flask(__name__)

@app.route("/")
def index():
    cars = get_all_cars()
    return render_template("index.html", cars=cars)

# NÚT XE VÀO -> mở camera
@app.route("/car_in_camera")
def car_in_camera():
    plate = read_plate()   # mở camera đọc biển số
    if plate:
        car_in(plate)
    return redirect(url_for("index"))

# NÚT XE RA -> mở camera + tính tiền
@app.route("/car_out_camera")
def car_out_camera():
    plate = read_plate()
    if plate:
        car_out(plate)
    return redirect(url_for("index"))

app.run(debug=True, threaded=False)