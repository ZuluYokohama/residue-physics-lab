from residue_lab.gem_ampere import ampere_dg_over_g, disk_mesh, solve_ampere
from residue_lab.grader import certify
from residue_lab.types import Verdict
from residue_lab.units import DEFAULT_LAB_DISK, Disk

def test_ampere_residual_and_d2():
    out = ampere_dg_over_g(DEFAULT_LAB_DISK)
    assert out["d2"] == 0.0
    assert out["ampere_rel"] < 1e-8

def test_static_disk_zero_current():
    static = Disk(DEFAULT_LAB_DISK.radius, DEFAULT_LAB_DISK.thickness, DEFAULT_LAB_DISK.density, 0.0)
    mesh = disk_mesh(static)
    b, rel = solve_ampere(mesh, static)
    assert abs(b).max() < 1e-30
    assert rel < 1e-12

def test_ampere_harris_open_null():
    out = ampere_dg_over_g(DEFAULT_LAB_DISK)
    assert out["max_dg_over_g"] < 1e-12
    c = certify("gem_ampere_harris", leftover=out["max_dg_over_g"], floor=1e-12)
    assert c.verdict == Verdict.OPEN_NULL
