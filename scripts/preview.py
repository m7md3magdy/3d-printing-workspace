#!/usr/bin/env python3
"""
preview.py — Render 3 views of an STL file as a combined PNG.
Usage: python preview.py <path/to/file.stl> [output.png]

Outputs: preview.png in the same directory as the STL (or at the specified path).
"""

from __future__ import annotations
import sys
import os
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")  # headless — no display needed
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image
import io


def load_mesh(stl_path: str) -> trimesh.Trimesh:
    mesh = trimesh.load(stl_path)
    # Handle scenes with multiple geometries
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(list(mesh.geometry.values()))
    return mesh


def render_view(ax, mesh: trimesh.Trimesh, elev: float, azim: float, title: str):
    """Render mesh onto a matplotlib 3D axis from the given viewpoint."""
    verts = mesh.vertices
    faces = mesh.faces

    poly = Poly3DCollection(
        verts[faces],
        alpha=0.85,
        linewidths=0.2,
        edgecolors="#333333",
    )
    # Shade by face normal z-component for basic lighting effect
    normals = mesh.face_normals
    # Map normals to a light direction
    light_dir = np.array([0.5, 0.5, 1.0])
    light_dir /= np.linalg.norm(light_dir)
    intensity = np.clip(normals @ light_dir, 0.15, 1.0)
    face_colors = np.column_stack([
        0.3 + 0.5 * intensity,   # R
        0.55 + 0.3 * intensity,  # G
        0.8 + 0.15 * intensity,  # B
        np.ones_like(intensity) * 0.88  # A
    ])
    poly.set_facecolor(face_colors)
    ax.add_collection3d(poly)

    # Axis limits — equal scale
    bounds = mesh.bounds  # [[xmin,ymin,zmin],[xmax,ymax,zmax]]
    center = bounds.mean(axis=0)
    half_range = (bounds[1] - bounds[0]).max() / 2 * 1.15
    ax.set_xlim(center[0] - half_range, center[0] + half_range)
    ax.set_ylim(center[1] - half_range, center[1] + half_range)
    ax.set_zlim(center[2] - half_range, center[2] + half_range)

    ax.view_init(elev=elev, azim=azim)
    ax.set_title(title, fontsize=9, pad=4)
    ax.set_xlabel("X", fontsize=7, labelpad=2)
    ax.set_ylabel("Y", fontsize=7, labelpad=2)
    ax.set_zlabel("Z", fontsize=7, labelpad=2)
    ax.tick_params(labelsize=6)
    ax.set_box_aspect([1, 1, 1])


def make_preview(stl_path: str, output_path: str | None = None):
    stl_path = os.path.abspath(stl_path)
    if not os.path.isfile(stl_path):
        print(f"ERROR: File not found: {stl_path}")
        sys.exit(1)

    if output_path is None:
        output_path = os.path.join(os.path.dirname(stl_path), "preview.png")

    mesh = load_mesh(stl_path)

    # Bounding box info
    bounds = mesh.bounds
    dims = bounds[1] - bounds[0]
    volume = mesh.volume
    is_watertight = mesh.is_watertight

    print(f"Loaded: {os.path.basename(stl_path)}")
    print(f"  Dimensions (X×Y×Z): {dims[0]:.2f} × {dims[1]:.2f} × {dims[2]:.2f} mm")
    print(f"  Bounding box min:   {bounds[0]}")
    print(f"  Bounding box max:   {bounds[1]}")
    print(f"  Faces: {len(mesh.faces):,}  |  Vertices: {len(mesh.vertices):,}")
    print(f"  Volume: {volume:.2f} mm³  ≈  {volume/1000:.2f} cm³")
    print(f"  Watertight (manifold): {is_watertight}")

    fig = plt.figure(figsize=(14, 5), dpi=150)
    fig.patch.set_facecolor("#1a1a2e")

    views = [
        (15,  -60,  "Isometric"),
        (90,  -90,  "Top (XY)"),
        (0,   -90,  "Front (XZ)"),
    ]

    for i, (elev, azim, title) in enumerate(views):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d")
        ax.set_facecolor("#16213e")
        render_view(ax, mesh, elev, azim, title)

    # Info text overlay
    info = (
        f"File: {os.path.basename(stl_path)}\n"
        f"Size: {dims[0]:.1f} × {dims[1]:.1f} × {dims[2]:.1f} mm\n"
        f"Volume: {volume/1000:.2f} cm³  |  Faces: {len(mesh.faces):,}  |  Watertight: {is_watertight}"
    )
    fig.text(
        0.5, 0.01, info,
        ha="center", va="bottom",
        fontsize=7.5, color="#ccddff",
        bbox=dict(facecolor="#0a0a1a", edgecolor="#334", boxstyle="round,pad=0.4"),
    )

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Preview saved: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python preview.py <file.stl> [output.png]")
        sys.exit(1)
    stl = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    make_preview(stl, out)
