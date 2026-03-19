"""
viewer/server.py — Auto-refresh preview server for the Claude Code Preview panel.
Serves the viewer HTML + previews directory, and exposes /latest to return
the most recently modified preview PNG.

Usage: python viewer/server.py [port]
"""

import os
import sys
import json
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from pathlib import Path

PORT = int(os.environ.get("PORT", sys.argv[1] if len(sys.argv) > 1 else 3333))
WORKSPACE = Path(__file__).parent.parent          # ~/3d-printing-workspace
PREVIEWS_DIR = WORKSPACE / "previews"
VIEWER_DIR = Path(__file__).parent                # ~/3d-printing-workspace/viewer


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


class ViewerHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # silence request logs

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self._serve_file(VIEWER_DIR / "index.html", "text/html")

        elif self.path == "/latest":
            self._serve_latest()

        elif self.path.startswith("/previews/"):
            fname = self.path[len("/previews/"):]
            fpath = PREVIEWS_DIR / fname
            self._serve_file(fpath, "image/png")

        else:
            self.send_response(404)
            self.end_headers()

    def _serve_file(self, path: Path, content_type: str):
        if not path.exists():
            self.send_response(404)
            self.end_headers()
            return
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)

    def _serve_latest(self):
        import base64
        pngs = sorted(
            PREVIEWS_DIR.glob("*.png"),
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )
        if not pngs:
            payload = json.dumps({"file": None}).encode()
        else:
            latest = pngs[0]
            img_bytes = latest.read_bytes()
            b64 = base64.b64encode(img_bytes).decode("ascii")
            payload = json.dumps({
                "file": latest.name,
                "url":  f"/previews/{latest.name}",
                "mtime": latest.stat().st_mtime,
                "data": f"data:image/png;base64,{b64}",
            }).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    server = ThreadedHTTPServer(("0.0.0.0", PORT), ViewerHandler)
    print(f"Viewer running at http://localhost:{PORT}")
    print(f"Watching: {PREVIEWS_DIR}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
