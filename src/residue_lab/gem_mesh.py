"""L1 GEM on the axisymmetric DEC chart.

Azimuthal mass current on faces. B_g ~ mu_g K_m, K_m = rho omega r.
a ~ v B_g. Order-of-magnitude cochain estimate, not a GR solve.
"""
from __future__ import annotations
import numpy as np
from residue_lab.dec import AxisymMesh, build_mesh
from residue_lab.units import DEFAULT_LAB_DISK, Disk, G_EARTH, MU_G

def disk_mesh(disk=None, nr=8, nz=6):
    disk = disk or DEFAULT_LAB_DISK
    return build_mesh(nr=nr, nz=nz, r_max=disk.radius, z_max=disk.thickness)

def face_centers(mesh):
    r_c = 0.5 * (mesh.r[:-1] + mesh.r[1:])
    z_c = 0.5 * (mesh.z[:-1] + mesh.z[1:])
    rr, zz = np.meshgrid(r_c, z_c, indexing="xy")
    return rr.ravel(), zz.ravel()

def mass_current_on_faces(mesh, disk):
    rr, _ = face_centers(mesh)
    return disk.density * disk.omega * rr

def gem_accel_on_faces(mesh, disk):
    k_m = mass_current_on_faces(mesh, disk)
    b_g = MU_G * k_m
    rr, _ = face_centers(mesh)
    return np.abs(disk.omega * rr * b_g)

def gem_mesh_dg_over_g(disk=None, nr=8, nz=6):
    disk = disk or DEFAULT_LAB_DISK
    mesh = disk_mesh(disk, nr=nr, nz=nz)
    a = gem_accel_on_faces(mesh, disk)
    frac = a / G_EARTH
    return {
        "max_dg_over_g": float(frac.max()) if frac.size else 0.0,
        "mean_dg_over_g": float(frac.mean()) if frac.size else 0.0,
        "n_faces": float(mesh.n_faces),
        "d2": float(np.linalg.norm(mesh.d1 @ mesh.d0)),
    }
