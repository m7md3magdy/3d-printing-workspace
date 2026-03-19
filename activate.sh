#!/bin/bash
# Activate the 3D printing workspace virtual environment
# Usage: source activate.sh
source "$(dirname "$0")/.venv/bin/activate"
echo "3D printing workspace activated. Python: $(python --version)"
echo "Tools: build123d, trimesh, numpy-stl, matplotlib, Pillow"
echo ""
echo "Workflow:"
echo "  python parts/<name>.py           → generates STL in exports/"
echo "  python scripts/preview.py exports/<name>.stl  → renders preview PNG"
