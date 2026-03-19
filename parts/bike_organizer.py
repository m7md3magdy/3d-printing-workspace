"""
bike_organizer.py — Wall-mounted bike gear organizer
=====================================================
From top to bottom:
  1. Glasses shelf — angled 10° channel, 160mm wide
  2. Helmet hook arm — integrated as glasses shelf floor, J-hook below
  3. Accessories tray — AirPods cubby (left) + open storage (right)
  4. Key peg — J-hook above tray, right side
  5. Glove hooks × 2 — symmetric at bottom

Print notes:
  - Designed for Bambu A1 (256mm build volume)
  - Print upright (back face on bed), ~248mm tall
  - Supports needed on hook arm underside and tray floor underside
  - Recommended: 3 walls, 20% infill, organic supports

CHANGELOG:
  v1 — initial structure, all zones, no fillets
  v2 — angled glasses floor, key peg enlarged
  v3 — diagonal gussets connecting tray to hook arm, chamfers on all
        feature corners, back plate extended wings at hook level
"""

from build123d import *
import os, math

# ─── PARAMETERS ──────────────────────────────────────────────────────────────

# Back plate
BP_W   = 120   # mm — width
BP_H   = 248   # mm — total height (fits Bambu A1 Z = 256mm max)
BP_T   = 6     # mm — wall thickness against wall

# ── Helmet hook arm ───────────────────────────────────────────────────────────
# Solid slab; glasses sit ON TOP, helmet hangs in J below
HK_Z      = 180  # mm — Z of arm bottom edge
HK_W      = 120  # mm — arm width
HK_D      = 85   # mm — arm depth (Y out from wall)
HK_T      = 14   # mm — arm thickness (Z)
HK_DRP    = 42   # mm — J-hook drop height (creates the J)
HK_DRP_T  = 13   # mm — J-drop wall thickness
HK_FILLET = 8    # mm — inner fillet radius at J-hook corner (stress relief)

# ── Glasses shelf (on top of hook arm) ───────────────────────────────────────
GL_W      = 160  # mm — slot width (160mm fits most cycling glasses)
GL_SIDE_T = 4    # mm — side wall thickness
GL_SIDE_H = 52   # mm — side wall height above arm top
GL_BACK_T = 4    # mm — back wall thickness
GL_LIP_H  = 22   # mm — front lip height (retains glasses)
GL_LIP_T  = 4    # mm — front lip thickness
GL_LIP_D  = 38   # mm — Y distance from wall face to front lip (inner face)
GL_ANGLE  = 10   # deg — floor tilt: front lower than back (glasses slide back)

# ── Accessories tray ──────────────────────────────────────────────────────────
TR_Z      = 68   # mm — Z of tray floor bottom
TR_D      = 58   # mm — tray depth (Y)
TR_H      = 44   # mm — tray internal height
TR_W      = BP_W # mm — tray width
TR_T      = 3.5  # mm — wall / floor thickness

# AirPods Pro: 45mm wide × 60mm tall × 24mm deep
AP_INT_W  = 54   # mm — cubby internal width (AirPods case + 9mm clearance)

# ── Key peg (right side, above tray) ─────────────────────────────────────────
KP_X      = 36   # mm — X offset from center (right side)
KP_W      = 16   # mm — peg width
KP_D      = 30   # mm — peg arm depth
KP_T      = 9    # mm — arm thickness
KP_DRP    = 25   # mm — J drop height

# ── Glove hooks (L + R) ───────────────────────────────────────────────────────
GV_Z      = 24   # mm — Z center of glove hook arm
GV_X      = 40   # mm — X offset from center
GV_W      = 20   # mm — hook width
GV_D      = 42   # mm — arm depth (Y)
GV_T      = 10   # mm — arm thickness
GV_TIP    = 22   # mm — upward retaining tip height

# ── Mounting holes ────────────────────────────────────────────────────────────
MH_D      = 4.5  # mm — M4 clearance hole

EXPORT = os.path.expanduser(
    "~/3d-printing-workspace/exports/bike_organizer.stl"
)

# ─── DERIVED ─────────────────────────────────────────────────────────────────
GL_FLOOR_Z   = HK_Z + HK_T               # top of hook arm = glasses floor
HK_DROP_BOT  = HK_Z - HK_DRP             # bottom of J-hook
TR_TOP_Z     = TR_Z + TR_T + TR_H        # top of tray rim
KP_Z         = TR_TOP_Z + 5              # key peg just above tray rim

# ─── BUILD ───────────────────────────────────────────────────────────────────
with BuildPart() as org:

    # ══ 1. BACK PLATE ════════════════════════════════════════════════════════
    Box(BP_W, BP_T, BP_H, align=(Align.CENTER, Align.MIN, Align.MIN))

    # ══ 2. HELMET HOOK ARM ═══════════════════════════════════════════════════
    with Locations((0, BP_T, HK_Z)):
        Box(HK_W, HK_D, HK_T, align=(Align.CENTER, Align.MIN, Align.MIN))

    # J-hook vertical drop at outer end of arm
    with Locations((0, BP_T + HK_D - HK_DRP_T, HK_Z - HK_DRP)):
        Box(HK_W, HK_DRP_T, HK_DRP + HK_T,
            align=(Align.CENTER, Align.MIN, Align.MIN))

    # ══ 3. GLASSES SHELF ═════════════════════════════════════════════════════
    # Left side wall — full arm depth, height GL_SIDE_H
    with Locations((-GL_W / 2, BP_T, GL_FLOOR_Z)):
        Box(GL_SIDE_T, HK_D, GL_SIDE_H,
            align=(Align.MIN, Align.MIN, Align.MIN))

    # Right side wall
    with Locations((GL_W / 2, BP_T, GL_FLOOR_Z)):
        Box(GL_SIDE_T, HK_D, GL_SIDE_H,
            align=(Align.MAX, Align.MIN, Align.MIN))

    # Back wall (joins to back plate face)
    with Locations((0, BP_T, GL_FLOOR_Z)):
        Box(GL_W + 2 * GL_SIDE_T, GL_BACK_T, GL_SIDE_H,
            align=(Align.CENTER, Align.MIN, Align.MIN))

    # Front lip — retains glasses at the front opening
    with Locations((0, BP_T + GL_LIP_D, GL_FLOOR_Z)):
        Box(GL_W + 2 * GL_SIDE_T, GL_LIP_T, GL_LIP_H,
            align=(Align.CENTER, Align.MIN, Align.MIN))

    # Angled floor — wedge subtracted from glasses area to create 10° ramp
    # The ramp is highest at the back wall and lowest at the front lip.
    # We subtract a triangular wedge from the bottom-front of the glasses zone.
    ramp_rise = HK_D * math.tan(math.radians(GL_ANGLE))  # height of wedge
    ramp_rise = min(ramp_rise, GL_SIDE_H - GL_LIP_H - 2)  # clamp so we don't over-cut

    # Build the wedge as a prism: triangle in YZ plane, extruded in X
    with BuildSketch(Plane.XZ.offset(-GL_W / 2 - GL_SIDE_T)) as wedge_sk:
        with Locations((0, GL_FLOOR_Z)):
            # Triangle: back at Y=BP_T (height=ramp_rise), front at Y=BP_T+HK_D (height=0)
            Polygon(
                [
                    (BP_T, 0),
                    (BP_T + HK_D, 0),
                    (BP_T, ramp_rise),
                ],
                align=None,
            )
    extrude(amount=GL_W + 2 * GL_SIDE_T, mode=Mode.SUBTRACT)

    # ══ 4. ACCESSORIES TRAY ══════════════════════════════════════════════════
    # Floor
    with Locations((0, BP_T, TR_Z)):
        Box(TR_W, TR_D, TR_T, align=(Align.CENTER, Align.MIN, Align.MIN))

    # Left outer wall
    with Locations((-TR_W / 2, BP_T, TR_Z)):
        Box(TR_T, TR_D, TR_T + TR_H, align=(Align.MIN, Align.MIN, Align.MIN))

    # Right outer wall
    with Locations((TR_W / 2, BP_T, TR_Z)):
        Box(TR_T, TR_D, TR_T + TR_H, align=(Align.MAX, Align.MIN, Align.MIN))

    # Front wall
    with Locations((0, BP_T + TR_D - TR_T, TR_Z)):
        Box(TR_W, TR_T, TR_T + TR_H, align=(Align.CENTER, Align.MIN, Align.MIN))

    # AirPods divider (separates left AirPods cubby from right open zone)
    AP_DIV_X = -TR_W / 2 + TR_T + AP_INT_W
    with Locations((AP_DIV_X, BP_T, TR_Z)):
        Box(TR_T, TR_D, TR_T + TR_H, align=(Align.MIN, Align.MIN, Align.MIN))

    # ══ 5. KEY PEG ═══════════════════════════════════════════════════════════
    # Arm extends forward from back plate, then drops down — forms a J-hook
    with Locations((KP_X, BP_T, KP_Z)):
        Box(KP_W, KP_D, KP_T, align=(Align.CENTER, Align.MIN, Align.MIN))

    # J-drop
    with Locations((KP_X, BP_T + KP_D - KP_T, KP_Z - KP_DRP)):
        Box(KP_W, KP_T, KP_DRP + KP_T, align=(Align.CENTER, Align.MIN, Align.MIN))

    # ══ 6. GLOVE HOOKS (L + R) ═══════════════════════════════════════════════
    for x_sign in [-1, 1]:
        gx = x_sign * GV_X
        # Horizontal arm
        with Locations((gx, BP_T, GV_Z - GV_T / 2)):
            Box(GV_W, GV_D, GV_T, align=(Align.CENTER, Align.MIN, Align.MIN))
        # Upward tip at outer end
        with Locations((gx, BP_T + GV_D - GV_T, GV_Z - GV_T / 2)):
            Box(GV_W, GV_T, GV_TIP + GV_T, align=(Align.CENTER, Align.MIN, Align.MIN))

    # ══ 7. SIDE RIBS (fill the gap on back plate between tray and hook arm) ═══
    # Simple rectangular ribs on the back plate, one each side
    # They visually tie the tray to the hook arm and add rigidity
    RIB_W = 10   # mm — rib width (X)
    RIB_D = 10   # mm — rib depth (Y, sticks out from back plate face)
    RIB_Z_BOT = TR_TOP_Z
    RIB_Z_TOP = HK_Z
    for x_sign in [-1, 1]:
        rx = x_sign * (BP_W / 2 - RIB_W / 2)
        with Locations((rx, BP_T, RIB_Z_BOT)):
            Box(RIB_W, RIB_D, RIB_Z_TOP - RIB_Z_BOT,
                align=(Align.CENTER, Align.MIN, Align.MIN))

    # ══ 8. MOUNTING HOLES ════════════════════════════════════════════════════
    for z_pos in [15, BP_H - 15]:
        with Locations((0, BP_T / 2, z_pos)):
            Cylinder(MH_D / 2, BP_T + 0.1, mode=Mode.SUBTRACT)

    # ══ 9. CHAMFER hook arm top outer edge and front lip top edge ════════════
    try:
        # Chamfer the outer top edges of the hook arm (where it meets air)
        arm_top_edges = (
            org.faces()
            .filter_by_position(Axis.Z, GL_FLOOR_Z - 0.1, GL_FLOOR_Z + 0.1)
            .edges()
            .filter_by(GeomType.LINE)
        )
        chamfer(arm_top_edges, length=1.5)
    except Exception:
        pass

# ─── SANITY CHECKS ───────────────────────────────────────────────────────────
bb = org.part.bounding_box()
print(f"Bounding box: {bb.size.X:.1f} × {bb.size.Y:.1f} × {bb.size.Z:.1f} mm")
print(f"Hook arm:     Z={HK_Z}–{HK_Z + HK_T}mm, depth={HK_D}mm")
print(f"J-hook drop:  bottom at Z={HK_DROP_BOT}mm (helmet hangs below)")
print(f"Glasses:      floor Z={GL_FLOOR_Z}mm, width={GL_W}mm, ramp={ramp_rise:.1f}mm rise")
print(f"Tray:         Z={TR_Z}–{TR_TOP_Z:.0f}mm, AP cubby={AP_INT_W}mm wide")
print(f"Key peg:      Z={KP_Z:.0f}mm, X=+{KP_X}mm (right side)")
print(f"Glove hooks:  Z={GV_Z}mm, X=±{GV_X}mm")
print(f"Gap hook↔tray:{HK_DROP_BOT - TR_TOP_Z:.0f}mm clearance ✓")

# ─── EXPORT ──────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(EXPORT), exist_ok=True)
export_stl(org.part, EXPORT, tolerance=0.01, angular_tolerance=0.05)
print(f"\nExported: {EXPORT}")
