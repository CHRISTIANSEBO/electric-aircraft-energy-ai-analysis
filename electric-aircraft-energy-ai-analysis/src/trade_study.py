import argparse
import os
from math import isfinite

import matplotlib.pyplot as plt

from energy_calc import AircraftParams, MissionParams, compute_cruise_power_and_energy


def parse_args():
    p = argparse.ArgumentParser(description="Trade Study: Energy and Power vs Cruise Speed")
    p.add_argument("--vmin", type=float, default=30.0, help="Min cruise speed (m/s)")
    p.add_argument("--vmax", type=float, default=90.0, help="Max cruise speed (m/s)")
    p.add_argument("--step", type=float, default=2.0, help="Speed step (m/s)")
    p.add_argument("--distance", type=float, default=100.0, help="Distance (miles)")
    p.add_argument("--altitude", type=float, default=0.0, help="Altitude (ft)")
    p.add_argument("--out", type=str, default="outputs/energy_vs_speed.png", help="Output plot path")
    return p.parse_args()


def frange(start, stop, step):
    x = start
    while x <= stop + 1e-9:
        yield x
        x += step


def main():
    args = parse_args()

    aircraft = AircraftParams()
    speeds = []
    powers_kw = []
    energies_kwh = []

    for v in frange(args.vmin, args.vmax, args.step):
        mission = MissionParams(
            cruise_speed_mps=v,
            distance_miles=args.distance,
            altitude_ft=args.altitude,
            battery_wh_per_kg=250.0,
        )
        r = compute_cruise_power_and_energy(aircraft, mission)

        power_kw = r["power_w"] / 1000.0
        energy_kwh = r["energy_kwh"]

        if all(isfinite(x) for x in [power_kw, energy_kwh]):
            speeds.append(v)
            powers_kw.append(power_kw)
            energies_kwh.append(energy_kwh)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    # Plot Energy vs Speed
    plt.figure()
    plt.xlabel("Cruise Speed (m/s)")
    plt.ylabel("Energy for Mission (kWh)")
    plt.title(f"Energy vs Speed (Distance={args.distance} mi, Altitude={args.altitude} ft)")
    plt.plot(speeds, energies_kwh)
    plt.grid(True)
    plt.savefig(args.out, dpi=200, bbox_inches="tight")

    print(f"Saved plot -> {args.out}")
    print(f"Speed range: {args.vmin}-{args.vmax} m/s | step {args.step} m/s")
    print(f"Example: min energy = {min(energies_kwh):.2f} kWh at {speeds[energies_kwh.index(min(energies_kwh))]:.1f} m/s")


if __name__ == "__main__":
    main()
