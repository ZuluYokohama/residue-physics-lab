from residue_lab.types import Section
from residue_lab.units import DEFAULT_LAB_DISK, G_EARTH, gem_lab_delta_g

EHD_K = 2.5e-12
EHD_DEFAULT_V = 2.0e4

def l1_ehd(cover, voltage=EHD_DEFAULT_V):
    if cover.medium == "air" and cover.ionization:
        return Section(force_z=EHD_K * voltage * voltage, notes={"module": "ehd"})
    return Section(force_z=0.0, notes={"module": "ehd"})

def l1_gem_weight_drop(cover, disk=None):
    disk = disk or DEFAULT_LAB_DISK
    if not cover.rotating:
        return Section(weight_drop_frac=0.0, notes={"module": "gem"})
    return Section(weight_drop_frac=gem_lab_delta_g(disk) / G_EARTH, notes={"module": "gem"})

def l1_london_static_weight_drop(cover):
    return Section(weight_drop_frac=0.0, notes={"module": "london"})
