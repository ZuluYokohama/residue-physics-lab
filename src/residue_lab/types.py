from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping

class Verdict(str, Enum):
    OPEN = "OPEN"
    OPEN_NULL = "OPEN_NULL"
    RESIDUE = "RESIDUE"

class TermTag(str, Enum):
    KNOWN = "known"
    SPECULATIVE = "speculative"

@dataclass(frozen=True)
class Cover:
    name: str
    medium: str
    rotating: bool
    superconducting: bool
    ionization: bool

@dataclass
class Section:
    force_z: float = 0.0
    weight_drop_frac: float = 0.0
    leftover_z: float = 0.0
    notes: Mapping[str, str] = field(default_factory=dict)

@dataclass
class Certificate:
    protocol: str
    verdict: Verdict
    leftover_z: float
    floor_z: float
    l2_on: tuple[str, ...]
    unpaid_restrictions: tuple[str, ...]
    tag: TermTag
    notes: Mapping[str, str] = field(default_factory=dict)
