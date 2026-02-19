import random
import csv
from energy_calc import AircraftParams, MissionParams, compute_cruise_power_and_energy

def generate_data(n=1000):
    with open("dataset.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["mass", "speed", "distance", "altitude", "energy_kwh"])

        for _ in range(n):
            mass = random.uniform(500, 800)
            speed = random.uniform(35, 85)
            distance = random.uniform(50, 150)
            altitude = random.uniform(0, 10000)

            aircraft = AircraftParams(mass_kg=mass)
            mission = MissionParams(
                cruise_speed_mps=speed,
                distance_miles=distance,
                altitude_ft=altitude,
                battery_wh_per_kg=250
            )

            result = compute_cruise_power_and_energy(aircraft, mission)

            writer.writerow([mass, speed, distance, altitude, result["energy_kwh"]])

    print("Dataset generated.")

if __name__ == "__main__":
    generate_data()
