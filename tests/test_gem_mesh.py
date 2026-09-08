from residue_lab.gem_mesh import gem_mesh_dg_over_g
from residue_lab.grader import certify
from residue_lab.types import Verdict
from residue_lab.units import DEFAULT_LAB_DISK, gem_lab_floor_dg_over_g

def test_mesh_d2_still_zero_on_disk():
    out = gem_mesh_dg_over_g(DEFAULT_LAB_DISK)
    assert out["d2"] == 0.0
    assert out["n_faces"] > 0

def test_mesh_gem_under_harris_floor():
    out = gem_mesh_dg_over_g(DEFAULT_LAB_DISK)
    floor = max(1e-12, gem_lab_floor_dg_over_g(DEFAULT_LAB_DISK) * 100)
    assert out["max_dg_over_g"] < 1e-12
    c = certify("gem_harris_mesh", leftover=out["max_dg_over_g"], floor=floor)
    assert c.verdict == Verdict.OPEN_NULL
