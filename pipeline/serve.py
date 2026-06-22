"""Local app server (D7): serves the viewer and the on-demand research API.

  python pipeline/serve.py [--port 8742] [--max-cost 1.50]

GET  /...                static files from viewer/ (the no-server build still
                         works by opening index.html directly; research is the
                         only feature that needs this process)
GET  /api/status         {"spent": .., "cap": ..}
POST /api/research       {"id": "<node_id>"} -> research delta (research.py)

Safety: a per-session budget cap; graph.json/registry.json are snapshotted
before every research call, validate.py runs after it, and any failure (or
red validation) restores the snapshot byte-for-byte. Viewer data bundles are
rebuilt after every successful change so the static build never goes stale.
Single-threaded on purpose — requests serialize, so file writes never race.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PIPELINE = ROOT / "pipeline"
SNAPSHOT_FILES = (DATA / "graph.json", DATA / "registry.json")

state = {"spent": 0.0, "cap": 1.50}


def run_script(name: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(PIPELINE / name)],
                          capture_output=True, text=True, cwd=ROOT)


def rebuild_bundles() -> None:
    for script in ("build_viewer_data.py", "build_review_data.py"):
        cp = run_script(script)
        if cp.returncode != 0:
            print(cp.stdout, cp.stderr)


class Handler(SimpleHTTPRequestHandler):
    def _json(self, code: int, doc: dict) -> None:
        body = json.dumps(doc, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/status":
            self._json(200, {"spent": round(state["spent"], 4), "cap": state["cap"]})
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/research":
            self._json(404, {"error": "unknown endpoint"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            node_id = json.loads(self.rfile.read(length) or b"{}").get("id", "")
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"error": "bad request body"})
            return
        if state["spent"] >= state["cap"]:
            self._json(200, {"error": f"session budget cap reached "
                                      f"(${state['cap']:.2f}) — restart serve.py "
                                      f"with --max-cost to raise it"})
            return

        snapshots = {p: p.read_bytes() for p in SNAPSHOT_FILES}

        def rollback(msg: str, code: int = 500):
            for p, b in snapshots.items():
                p.write_bytes(b)
            rebuild_bundles()
            self._json(code, {"error": msg})

        try:
            import research
            delta = research.research_node(node_id)
        except Exception as exc:  # noqa: BLE001 — surface anything to the UI
            rollback(f"research failed: {exc}")
            return
        state["spent"] += delta.get("cost", 0.0) or 0.0
        if delta.get("error"):
            self._json(200, {**delta, "spent": round(state["spent"], 4)})
            return
        cp = run_script("validate.py")
        if cp.returncode != 0:
            tail = "\n".join(cp.stdout.strip().splitlines()[-4:])
            rollback(f"validation rejected the update (rolled back):\n{tail}")
            return
        rebuild_bundles()
        self._json(200, {**delta, "spent": round(state["spent"], 4)})

    def log_message(self, fmt, *args):
        if "/api/" in (args[0] if args else ""):
            super().log_message(fmt, *args)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", type=int, default=8742)
    ap.add_argument("--max-cost", type=float, default=1.50,
                    help="session budget cap for research calls, USD")
    args = ap.parse_args()
    state["cap"] = args.max_cost
    handler = partial(Handler, directory=str(ROOT / "viewer"))
    print(f"Concept Mapper at http://localhost:{args.port}/ "
          f"(research budget cap ${args.max_cost:.2f})")
    HTTPServer(("127.0.0.1", args.port), handler).serve_forever()


if __name__ == "__main__":
    main()
