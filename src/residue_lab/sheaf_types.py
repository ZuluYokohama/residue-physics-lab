from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping

class CoverKind(str, Enum):
    PHYSICS = "physics"
    INSTITUTION = "institution"
    GEOPOLITICS = "geopolitics"
    NARRATIVE = "narrative"

class CellKind(str, Enum):
    ACTOR = "actor"
    PAPER = "paper"
    GRANT = "grant"
    UTTERANCE = "utterance"
    EVENT = "event"

class Intent(str, Enum):
    SEEK = "seek"
    ATTACH = "attach"
    OBSCURE = "obscure"
    INHERIT = "inherit"
    BOUND = "bound"
    CRITIQUE = "critique"

class SheafStatus(str, Enum):
    OPEN = "OPEN"
    OPEN_NULL = "OPEN_NULL"
    RESIDUE = "RESIDUE"
    UNKNOWN = "UNKNOWN"
    CONTESTED = "CONTESTED"

@dataclass(frozen=True)
class Cell:
    id: str
    kind: CellKind
    label: str
    year: int | None
    covers: tuple[CoverKind, ...]
    intent: Intent
    status: SheafStatus
    source: str
    notes: str = ""

@dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    kind: str
    covers: tuple[CoverKind, ...]
    notes: str = ""

@dataclass(frozen=True)
class Face:
    id: str
    vertices: tuple[str, str, str]
    covers: tuple[CoverKind, CoverKind]
    glues: bool
    status: SheafStatus
    unpaid: str
    notes: str = ""

@dataclass
class SheafCertificate:
    protocol: str
    status: SheafStatus
    glues: bool
    covers: tuple[str, ...]
    unpaid: tuple[str, ...]
    notes: Mapping[str, str] = field(default_factory=dict)
