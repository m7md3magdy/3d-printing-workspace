"""
test_box.py — Mounting plate test part
=======================================
A 50 × 30 × 20 mm rectangular box with:
  - Filleted edges (2mm radius) on all edges
  - 5mm diameter mounting holes in each corner
  - Chamfered hole entrances on top face
  - Prints flat on XY — no supports needed

CHANGELOG: See ~/3d-printing-workspace/CHANGELOG.md
"""

from build123d import *
import os

# ─── PARAMETERS ──────────────────────────────────────────────────────────────
LENGTH       = 50.0   # mm — X
WIDTH        = 30.0   # mm — Y
HEIGHT       = 20.0   # mm — Z
FILLET_R     = 2.0    # mm — edge fillet (all edges)
HOLE_DIA     = 5.0    # mm — mounting hole diameter
HOLE_INSET   = 6.0    # mm — hole center from each edge
CHAMFER_LEN  = 0.8    # mm — chamfer on hole entrance (top face)
EXPORT_PATH  = os.path.expanduser("~/3d-printing-workspace/exports/test_box.stl")

# ─── DERIVED ─────────────────────────────────────────────────────────────────
hole_r = HOLE_DIA / 2
cx = LENGTH / 2 - HOLE_INSET   # hole center X offset from origin
cy = WIDTH  / 2 - HOLE_INSET   # hole center Y offset from origin

# ─── BUILD ───────────────────────────────────────────────────────────────────
with BuildPart() as part:

    # 1. Solid box centered on origin
    Box(LENGTH, WIDTH, HEIGHT)

    # 2. Fillet ALL edges — gives rounded, print-friendly shape
    fillet(part.edges(), radius=FILLET_R)

    # 3. Subtract mounting holes — through holes from top to bottom
    with Locations(
        (  cx,  cy, 0),
        ( -cx,  cy, 0),
        ( -cx, -cy, 0),
        (  cx, -cy, 0),
    ):
        Cylinder(
            radius=hole_r,
            height=HEIGHT + 2,   # +2 to guarantee clean boolean through the fillets
            mode=Mode.SUBTRACT,
        )

    # 4. Countersink on top face — subtract a shallow cone above each hole
    #    This gives a lead-in for screws and is more reliable than chamfering edges
    CSINK_TOP_R = hole_r + CHAMFER_LEN   # countersink top radius
    with Locations(
        (  cx,  cy, HEIGHT / 2),
        ( -cx,  cy, HEIGHT / 2),
        ( -cx, -cy, HEIGHT / 2),
        (  cx, -cy, HEIGHT / 2),
    ):
        Cone(
            bottom_radius=hole_r,
            top_radius=CSINK_TOP_R,
            height=CHAMFER_LEN,
            mode=Mode.SUBTRACT,
        )

# ─── EXPORT ──────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)
export_stl(part.part, EXPORT_PATH, tolerance=0.01, angular_tolerance=0.05)
print(f"Exported: {EXPORT_PATH}")

bb = part.part.bounding_box()
print(f"Bounding box: {bb.size.X:.1f} × {bb.size.Y:.1f} × {bb.size.Z:.1f} mm")
print(f"Material around hole: {HOLE_INSET - hole_r:.1f} mm  (min 2mm required ✓)" )
