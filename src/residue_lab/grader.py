from __future__ import annotations
from residue_lab.types import Certificate, TermTag, Verdict

def leftover_weight_frac(sim, l1):
    return sim.weight_drop_frac - l1.weight_drop_frac

def verdict_from_leftover(leftover, floor, l2_on, child_failed=False):
    if child_failed:
        return Verdict.RESIDUE
    if l2_on and abs(leftover) > floor:
        return Verdict.RESIDUE
    if abs(leftover) <= floor:
        return Verdict.OPEN_NULL
    return Verdict.OPEN

def certify(protocol, leftover, floor, l2_on=(), unpaid=(), child_failed=False, notes=None, forced_verdict=None):
    v = forced_verdict or verdict_from_leftover(leftover, floor, l2_on, child_failed=child_failed)
    tag = TermTag.SPECULATIVE if l2_on else TermTag.KNOWN
    return Certificate(protocol, v, leftover, floor, l2_on, unpaid, tag, notes or {})
