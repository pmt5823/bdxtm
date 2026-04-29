from flask import Flask, render_template
import csv

app = Flask(__name__)

FILE_NAME = "parking_data.csv"

def load_data():
    cars = []
    try:
        with open(FILE_NAME, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    cars.append({
                        "plate": row[0],
                        "time_in": row[1]
                    })
    except:
        pass
    return cars

@app.route("/")
def index():
    cars = load_data()
    return render_template("index.html", cars=cars)

app.run(debug=True)