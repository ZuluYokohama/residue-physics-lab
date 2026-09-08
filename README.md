# Residue Physics Lab

Compute laboratory: **known physics first**, leftovers graded, claim terms default **off**.

This is not a propulsion device.
This is not a unified-field engine.
Delta-lambda-1 in this repo is an audit-graph gate on leftover shape. It is not a gravitomagnetic field.

## What v0 does

| Protocol | Expected certificate |
|---|---|
| EHD air | OPEN |
| EHD vacuum | OPEN_NULL |
| GEM Harris | OPEN_NULL |
| Li static YBCO | OPEN_NULL |
| Li toggle | RESIDUE + speculative |

Expected harvest: **zero new axioms.**

## Run

```bash
pip install -e ".[dev]"
pytest
python -c "from residue_lab.protocols import run_v0; print([(c.protocol, c.verdict.value) for c in run_v0()])"
```

L0 includes a tiny axisymmetric DEC chart (`residue_lab.dec`) with d1 @ d0 == 0.
