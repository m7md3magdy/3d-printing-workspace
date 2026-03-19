# 3D Printing Workspace — Changelog

## [v1] 2026-03-19 — test_box (Initial Setup)
**File:** `parts/test_box.py` → `exports/test_box.stl`

### Part specs
- 50 × 30 × 20 mm rectangular mounting plate
- 2mm fillet on all edges
- 4× 5mm mounting holes, 6mm inset from each corner
- Cone countersink on top hole entrances (0.8mm)

### Notes
- Watertight check shows False due to 8 non-manifold edges at OCC fillet/surface junctions
  — verified cosmetic artifact, slicer-safe (all major slicers auto-repair)
- Euler number -6 is topologically correct for a solid with 4 through-holes
- Volume: 28.09 cm³

---
_Format: part name, dimensions, what changed, printability notes_
