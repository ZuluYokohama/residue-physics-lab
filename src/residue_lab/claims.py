from dataclasses import dataclass
from residue_lab.types import Section, TermTag
from residue_lab.units import DEFAULT_LAB_DISK, G_EARTH

@dataclass(frozen=True)
class ClaimTerm:
    name: str
    tag: TermTag
    unpaid_restriction: str
    source: str

TERMS = {
    "li_torr_lab_bg": ClaimTerm(
        "li_torr_lab_bg", TermTag.SPECULATIVE,
        "controlled rotating type-II SC + independent gravimeter; Harris magnitude unpaid",
        "Li & Torr 1991-93; Harris 1999",
    ),
}

def apply_l2(name, cover, l1, disk=None, enabled=False):
    if not enabled:
        return l1
    if name == "li_torr_lab_bg":
        advertised = 1.0e-3
        d = disk or DEFAULT_LAB_DISK
        return Section(force_z=l1.force_z, weight_drop_frac=advertised,
                       leftover_z=advertised * d.density * 3.141592653589793 * d.radius**2 * d.thickness * G_EARTH,
                       notes={"l2": name, "tag": "speculative"})
    return l1
