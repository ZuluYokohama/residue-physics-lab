"""Cochain Ampere + Whitney face B + static/rotating restriction."""
from __future__ import annotations
import numpy as np
from residue_lab.dec import build_mesh
from residue_lab.units import DEFAULT_LAB_DISK, Disk, G_EARTH, MU_G

def disk_mesh(disk=None, nr=8, nz=6):
    disk = disk or DEFAULT_LAB_DISK
    return build_mesh(nr=nr, nz=nz, r_max=disk.radius, z_max=disk.thickness)

def face_areas(mesh):
    return np.outer(np.diff(mesh.z), np.diff(mesh.r)).ravel()

def face_radii(mesh):
    r_c = 0.5 * (mesh.r[:-1] + mesh.r[1:])
    z_c = 0.5 * (mesh.z[:-1] + mesh.z[1:])
    rr, _ = np.meshgrid(r_c, z_c, indexing="xy")
    return rr.ravel()

def mass_current_2form(mesh, disk):
    return disk.density * disk.omega * face_radii(mesh) * face_areas(mesh)

def solve_ampere(mesh, disk):
    rhs = MU_G * mass_current_2form(mesh, disk)
    b, *_ = np.linalg.lstsq(mesh.d1, rhs, rcond=None)
    scale = max(float(np.linalg.norm(rhs)), 1e-40)
    return b, float(np.linalg.norm(mesh.d1 @ b - rhs) / scale)

def _edge_ids(mesh, i, j):
    n_r_edges = (mesh.nr - 1) * mesh.nz
    bottom = j * (mesh.nr - 1) + i
    top = (j + 1) * (mesh.nr - 1) + i
    left = n_r_edges + j * mesh.nr + i
    right = n_r_edges + j * mesh.nr + (i + 1)
    return bottom, top, left, right

def physical_b_on_faces(mesh, b_form):
    dr = np.diff(mesh.r)
    dz = np.diff(mesh.z)
    mag = np.zeros(mesh.n_faces)
    for j in range(mesh.nz - 1):
        for i in range(mesh.nr - 1):
            f = j * (mesh.nr - 1) + i
            bottom, top, left, right = _edge_ids(mesh, i, j)
            br = 0.5 * (b_form[bottom] / dr[i] + b_form[top] / dr[i])
            bz = 0.5 * (b_form[left] / dz[j] + b_form[right] / dz[j])
            mag[f] = float(np.hypot(br, bz))
    return mag

def ampere_dg_over_g(disk=None, nr=8, nz=6):
    disk = disk or DEFAULT_LAB_DISK
    mesh = disk_mesh(disk, nr=nr, nz=nz)
    b, rel = solve_ampere(mesh, disk)
    frac = np.abs(disk.omega * face_radii(mesh) * physical_b_on_faces(mesh, b)) / G_EARTH
    return {
        "max_dg_over_g": float(frac.max()) if frac.size else 0.0,
        "ampere_rel": rel,
        "d2": float(np.linalg.norm(mesh.d1 @ mesh.d0)),
        "n_faces": float(mesh.n_faces),
        "omega": float(disk.omega),
    }

def restriction_static_rotating(disk=None):
    disk = disk or DEFAULT_LAB_DISK
    static = Disk(disk.radius, disk.thickness, disk.density, 0.0)
    rot = ampere_dg_over_g(disk)
    st = ampere_dg_over_g(static)
    return {
        "static_dg_over_g": st["max_dg_over_g"],
        "rotating_dg_over_g": rot["max_dg_over_g"],
        "static_ampere_rel": st["ampere_rel"],
        "rotating_ampere_rel": rot["ampere_rel"],
        "glues": float(st["max_dg_over_g"] < 1e-18 and rot["max_dg_over_g"] < 1e-12),
    }
