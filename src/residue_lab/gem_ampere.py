"""Cochain Ampere for L1 GEM. B_g is a 1-form. (d1 @ B)_f = mu_g I_f."""
from __future__ import annotations
import numpy as np
from residue_lab.dec import AxisymMesh, build_mesh
from residue_lab.units import DEFAULT_LAB_DISK, Disk, G_EARTH, MU_G

def disk_mesh(disk=None, nr=8, nz=6):
    disk = disk or DEFAULT_LAB_DISK
    return build_mesh(nr=nr, nz=nz, r_max=disk.radius, z_max=disk.thickness)

def face_areas(mesh):
    dr = np.diff(mesh.r)
    dz = np.diff(mesh.z)
    return np.outer(dz, dr).ravel()

def face_radii(mesh):
    r_c = 0.5 * (mesh.r[:-1] + mesh.r[1:])
    z_c = 0.5 * (mesh.z[:-1] + mesh.z[1:])
    rr, _ = np.meshgrid(r_c, z_c, indexing="xy")
    return rr.ravel()

def edge_lengths(mesh):
    nr, nz = mesh.nr, mesh.nz
    lengths = np.empty(mesh.n_edges)
    dr = np.diff(mesh.r)
    dz = np.diff(mesh.z)
    k = 0
    for _j in range(nz):
        for i in range(nr - 1):
            lengths[k] = dr[i]
            k += 1
    for j in range(nz - 1):
        for _i in range(nr):
            lengths[k] = dz[j]
            k += 1
    return lengths

def mass_current_2form(mesh, disk):
    return disk.density * disk.omega * face_radii(mesh) * face_areas(mesh)

def solve_ampere(mesh, disk):
    i_f = mass_current_2form(mesh, disk)
    rhs = MU_G * i_f
    b, *_ = np.linalg.lstsq(mesh.d1, rhs, rcond=None)
    residual = mesh.d1 @ b - rhs
    scale = max(float(np.linalg.norm(rhs)), 1e-40)
    return b, float(np.linalg.norm(residual) / scale)

def physical_b_on_faces(mesh, b_form):
    lengths = edge_lengths(mesh)
    b_phys_edge = b_form / np.maximum(lengths, 1e-16)
    mag = np.zeros(mesh.n_faces)
    for f in range(mesh.n_faces):
        edges = np.flatnonzero(mesh.d1[f])
        mag[f] = float(np.mean(np.abs(b_phys_edge[edges])))
    return mag

def ampere_dg_over_g(disk=None, nr=8, nz=6):
    disk = disk or DEFAULT_LAB_DISK
    mesh = disk_mesh(disk, nr=nr, nz=nz)
    b, rel = solve_ampere(mesh, disk)
    mag = physical_b_on_faces(mesh, b)
    frac = np.abs(disk.omega * face_radii(mesh) * mag) / G_EARTH
    return {
        "max_dg_over_g": float(frac.max()) if frac.size else 0.0,
        "ampere_rel": rel,
        "d2": float(np.linalg.norm(mesh.d1 @ mesh.d0)),
        "n_faces": float(mesh.n_faces),
    }
