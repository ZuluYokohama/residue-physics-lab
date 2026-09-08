"""Tiny axisymmetric DEC chart. Not a production Maxwell solver.

Invariant required of every mesh: d1 @ d0 == 0.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class AxisymMesh:
    nr: int
    nz: int
    r_max: float
    z_max: float
    r: np.ndarray
    z: np.ndarray
    d0: np.ndarray
    d1: np.ndarray
    n_nodes: int
    n_edges: int
    n_faces: int

def _node(i, j, nr):
    return j * nr + i

def build_mesh(nr=6, nz=6, r_max=0.10, z_max=0.02):
    if nr < 2 or nz < 2:
        raise ValueError("need at least 2 nodes on each axis")
    r = np.linspace(0.0, r_max, nr)
    z = np.linspace(0.0, z_max, nz)
    n_nodes = nr * nz
    n_r_edges = (nr - 1) * nz
    n_z_edges = nr * (nz - 1)
    n_edges = n_r_edges + n_z_edges
    n_faces = (nr - 1) * (nz - 1)
    d0 = np.zeros((n_edges, n_nodes))
    d1 = np.zeros((n_faces, n_edges))
    def r_edge(i, j):
        return j * (nr - 1) + i
    def z_edge(i, j):
        return n_r_edges + j * nr + i
    for j in range(nz):
        for i in range(nr - 1):
            e = r_edge(i, j)
            d0[e, _node(i, j, nr)] = -1.0
            d0[e, _node(i + 1, j, nr)] = 1.0
    for j in range(nz - 1):
        for i in range(nr):
            e = z_edge(i, j)
            d0[e, _node(i, j, nr)] = -1.0
            d0[e, _node(i, j + 1, nr)] = 1.0
    for j in range(nz - 1):
        for i in range(nr - 1):
            f = j * (nr - 1) + i
            d1[f, r_edge(i, j)] = 1.0
            d1[f, z_edge(i + 1, j)] = 1.0
            d1[f, r_edge(i, j + 1)] = -1.0
            d1[f, z_edge(i, j)] = -1.0
    return AxisymMesh(nr, nz, r_max, z_max, r, z, d0, d1, n_nodes, n_edges, n_faces)

def d2_residual(mesh):
    return float(np.linalg.norm(mesh.d1 @ mesh.d0))
