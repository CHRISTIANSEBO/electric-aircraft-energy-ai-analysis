from flask import Flask, render_template, request
from pathlib import Path
import sys
import io
import base64
import numpy as np
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from energy_calc import AircraftParams, MissionParams, compute_cruise_power_and_energy

MODEL_PATH = BASE_DIR / "energy_model.pkl"
ml_model = joblib.load(MODEL_PATH)

app = Flask(__name__)

DEFAULTS = {
    "mass": 650.0,
    "wing_area": 12.0,
    "cd0": 0.025,
    "k": 0.045,
    "eta": 0.85,
    "speed": 60.0,
    "distance": 100.0,
    "altitude": 0.0,
    "battery_density": 250.0,
}

def to_float(form, key, default):
    try:
        return float(form.get(key, default))
    except:
        return default

@app.route("/", methods=["GET", "POST"])
def index():
    values = dict(DEFAULTS)
    results = None
    error = None
    plot_url = None
    ml_prediction = None
    ml_error = None

    if request.method == "POST":
        for k in values:
            values[k] = to_float(request.form, k, values[k])

        try:
            aircraft = AircraftParams(
                mass_kg=values["mass"],
                wing_area_m2=values["wing_area"],
                cd0=values["cd0"],
                k=values["k"],
                propulsive_efficiency=values["eta"],
            )

            mission = MissionParams(
                cruise_speed_mps=values["speed"],
                distance_miles=values["distance"],
                altitude_ft=values["altitude"],
                battery_wh_per_kg=values["battery_density"],
            )

            results = compute_cruise_power_and_energy(aircraft, mission)

            X_input = np.array([[values["mass"], values["speed"], values["distance"], values["altitude"]]])
            ml_prediction = ml_model.predict(X_input)[0]
            ml_error = abs(ml_prediction - results["energy_kwh"])

            # Trade Study Plot
            speeds = []
            energies = []

            v = 30
            while v <= 90:
                mission_plot = MissionParams(
                    cruise_speed_mps=v,
                    distance_miles=values["distance"],
                    altitude_ft=values["altitude"],
                    battery_wh_per_kg=values["battery_density"],
                )

                r = compute_cruise_power_and_energy(aircraft, mission_plot)
                speeds.append(v)
                energies.append(r["energy_kwh"])
                v += 2

            plt.figure()
            plt.plot(speeds, energies)
            plt.xlabel("Cruise Speed (m/s)")
            plt.ylabel("Energy Required (kWh)")
            plt.title("Energy vs Speed Trade Study")
            plt.grid(True)

            img = io.BytesIO()
            plt.savefig(img, format="png")
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            plt.close()

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        values=values,
        results=results,
        error=error,
        plot_url=plot_url,
        ml_prediction=ml_prediction,
        ml_error=ml_error,
    )

if __name__ == "__main__":
    app.run(debug=True)
