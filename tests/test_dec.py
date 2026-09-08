import numpy as np
from residue_lab.dec import build_mesh, d2_residual

def test_d2_is_zero():
    mesh = build_mesh(5, 4, 0.1, 0.02)
    assert d2_residual(mesh) == 0.0

def test_mesh_counts():
    nr, nz = 5, 4
    mesh = build_mesh(nr, nz)
    assert mesh.n_nodes == nr * nz
    assert mesh.n_edges == (nr - 1) * nz + nr * (nz - 1)
    assert mesh.n_faces == (nr - 1) * (nz - 1)

def test_gradient_of_constant_is_zero():
    mesh = build_mesh(4, 4)
    phi = np.ones(mesh.n_nodes)
    assert np.allclose(mesh.d0 @ phi, 0.0)
