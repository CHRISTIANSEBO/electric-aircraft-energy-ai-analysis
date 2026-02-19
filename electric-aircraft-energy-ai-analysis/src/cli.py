import argparse
from energy_calc import AircraftParams, MissionParams, compute_cruise_power_and_energy


def parse_args():
    p = argparse.ArgumentParser(description="Electric Aircraft Energy Calculator (Cruise Only)")
    p.add_argument("--mass", type=float, default=650.0, help="Aircraft mass in kg")
    p.add_argument("--wing-area", type=float, default=12.0, help="Wing area in m^2")
    p.add_argument("--cd0", type=float, default=0.025, help="Zero-lift drag coefficient")
    p.add_argument("--k", type=float, default=0.045, help="Induced drag factor")
    p.add_argument("--eta", type=float, default=0.85, help="Propulsive efficiency (0-1]")

    p.add_argument("--speed", type=float, default=60.0, help="Cruise speed in m/s")
    p.add_argument("--distance", type=float, default=100.0, help="Distance in miles")
    p.add_argument("--altitude", type=float, default=0.0, help="Cruise altitude in feet")
    p.add_argument("--battery-density", type=float, default=250.0, help="Battery energy density in Wh/kg")
    return p.parse_args()


def main():
    args = parse_args()

    aircraft = AircraftParams(
        mass_kg=args.mass,
        wing_area_m2=args.wing_area,
        cd0=args.cd0,
        k=args.k,
        propulsive_efficiency=args.eta,
    )
    mission = MissionParams(
        cruise_speed_mps=args.speed,
        distance_miles=args.distance,
        altitude_ft=args.altitude,
        battery_wh_per_kg=args.battery_density,
    )

    results = compute_cruise_power_and_energy(aircraft, mission)

    print("\nElectric Aircraft Energy Calculator (Cruise Only) - Scenario")
    print("-----------------------------------------------------------")
    print(f"Mass: {aircraft.mass_kg:.1f} kg | Wing area: {aircraft.wing_area_m2:.2f} m^2")
    print(f"Cruise speed: {mission.cruise_speed_mps:.1f} m/s | Distance: {mission.distance_miles:.1f} miles")
    print(f"Altitude: {mission.altitude_ft:.0f} ft | Battery density: {mission.battery_wh_per_kg:.0f} Wh/kg")
    print()
    print(f"Air density: {results['rho_kg_m3']:.3f} kg/m^3")
    print(f"CL required: {results['cl']:.3f}")
    print(f"CD estimated: {results['cd']:.4f}")
    print(f"Drag: {results['drag_n']:.1f} N")
    print(f"Power required: {results['power_w'] / 1000.0:.2f} kW")
    print(f"Flight time: {results['time_s'] / 60.0:.1f} minutes")
    print(f"Energy required: {results['energy_kwh']:.2f} kWh")
    print(f"Estimated battery mass: {results['battery_mass_kg']:.1f} kg")
    print()


if __name__ == "__main__":
    main()
