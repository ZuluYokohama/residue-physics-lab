from __future__ import annotations
import math
from dataclasses import dataclass

G = 6.67430e-11
C = 2.99792458e8
G_EARTH = 9.80665
PI = math.pi
MU_G = 16.0 * PI * G / (C * C)

@dataclass(frozen=True)
class Disk:
    radius: float
    thickness: float
    density: float
    omega: float

def gem_lab_delta_g(disk):
    i_m = disk.density * disk.omega * disk.thickness * disk.radius**2
    b_g = MU_G * i_m / max(disk.radius, 1e-12)
    return abs(disk.omega * disk.radius * b_g)

def gem_lab_floor_dg_over_g(disk):
    return gem_lab_delta_g(disk) / G_EARTH

DEFAULT_LAB_DISK = Disk(0.10, 0.01, 6000.0, 100.0)
