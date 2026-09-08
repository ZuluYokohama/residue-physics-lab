from residue_lab.types import Cover, Section
from residue_lab.units import DEFAULT_LAB_DISK

def lab_covers():
    return {
        "ehd_air": Cover("ehd_air", "air", False, False, True),
        "ehd_vacuum": Cover("ehd_vacuum", "vacuum", False, False, False),
        "gem_rotating": Cover("gem_rotating", "solid", True, False, False),
        "li_static_sc": Cover("li_static_sc", "solid", False, True, False),
        "li_toggle": Cover("li_toggle", "solid", True, True, False),
    }

def default_disk():
    return DEFAULT_LAB_DISK

def empty_section():
    return Section()
