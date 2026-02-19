from dataclasses import dataclass
from math import exp

G = 9.80665


@dataclass(frozen=True)
class AircraftParams:
    mass_kg: float = 650.0
    wing_area_m2: float = 12.0
    cd0: float = 0.025
    k: float = 0.045
    propulsive_efficiency: float = 0.85


@dataclass(frozen=True)
class MissionParams:
    cruise_speed_mps: float = 60.0
    distance_miles: float = 100.0
    altitude_ft: float = 0.0
    battery_wh_per_kg: float = 250.0


def air_density_kg_per_m3(altitude_ft: float) -> float:
    h = altitude_ft * 0.3048
    rho0 = 1.225
    H = 8500.0
    return rho0 * exp(-h / H)


def miles_to_meters(mi: float) -> float:
    return mi * 1609.344


def compute_cruise_power_and_energy(aircraft: AircraftParams, mission: MissionParams):
    rho = air_density_kg_per_m3(mission.altitude_ft)
    v = mission.cruise_speed_mps
    s = aircraft.wing_area_m2
    eta = aircraft.propulsive_efficiency

    weight_n = aircraft.mass_kg * G
    q = 0.5 * rho * v * v
    cl = weight_n / (q * s)
    cd = aircraft.cd0 + aircraft.k * (cl ** 2)

    drag = 0.5 * rho * v * v * s * cd
    power_w = (drag * v) / eta

    distance_m = miles_to_meters(mission.distance_miles)
    time_s = distance_m / v
    energy_j = power_w * time_s

    energy_wh = energy_j / 3600
    energy_kwh = energy_wh / 1000
    battery_mass_kg = energy_wh / mission.battery_wh_per_kg

    return {
        "rho_kg_m3": rho,
        "cl": cl,
        "cd": cd,
        "drag_n": drag,
        "power_w": power_w,
        "time_s": time_s,
        "energy_wh": energy_wh,
        "energy_kwh": energy_kwh,
        "battery_mass_kg": battery_mass_kg,
    }
