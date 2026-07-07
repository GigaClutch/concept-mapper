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
Static requests are served concurrently (a browser's idle preconnect socket
would deadlock a single-threaded server); the two MUTATING endpoints share
one lock, so file writes still never race.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PIPELINE = ROOT / "pipeline"
SNAPSHOT_FILES = (DATA / "graph.json", DATA / "registry.json")
# applying review decisions touches all five review-governed files
DECISION_FILES = SNAPSHOT_FILES + (DATA / "verification_sample.json",
                                   DATA / "quarantine" / "proposed_edges.json",
                                   DATA / "quarantine" / "proposed_nodes.json")

state = {"spent": 0.0, "cap": 1.50}
MUTEX = threading.Lock()  # serializes the endpoints that write data files


def run_script(name: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(PIPELINE / name), *args],
                          capture_output=True, text=True, cwd=ROOT)


def restore(snapshots: dict) -> None:
    for p, b in snapshots.items():
        tmp = p.with_suffix(".tmp")
        tmp.write_bytes(b)
        tmp.replace(p)


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

    def _read_guarded(self, max_len: int) -> bytes | None:
        """Cross-site and size guard shared by the POST endpoints (they mutate
        data and spend money; a page in the owner's browser can fire simple
        POSTs at localhost without CORS). Returns the body, or None with the
        error response already sent."""
        host = (self.headers.get("Host") or "").split(":")[0].casefold()
        origin = (self.headers.get("Origin") or "").rstrip("/")
        allowed_origins = {f"http://localhost:{self.server.server_port}",
                           f"http://127.0.0.1:{self.server.server_port}"}
        if host not in ("localhost", "127.0.0.1") or \
                (origin and origin not in allowed_origins):
            self._json(403, {"error": "forbidden: this endpoint is local-only"})
            return None
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._json(400, {"error": "bad request body"})
            return None
        if length > max_len:
            self._json(413, {"error": "request body too large"})
            return None
        return self.rfile.read(length)

    def do_POST(self):
        if self.path == "/api/research":
            with MUTEX:
                self._post_research()
        elif self.path == "/api/decisions":
            with MUTEX:
                self._post_decisions()
        else:
            self._json(404, {"error": "unknown endpoint"})

    def _post_research(self):
        body = self._read_guarded(4096)
        if body is None:
            return
        try:
            node_id = json.loads(body or b"{}").get("id", "")
        except json.JSONDecodeError:
            self._json(400, {"error": "bad request body"})
            return
        if state["spent"] >= state["cap"]:
            self._json(200, {"error": f"session budget cap reached "
                                      f"(${state['cap']:.2f}) — restart serve.py "
                                      f"with --max-cost to raise it"})
            return

        snapshots = {p: p.read_bytes() for p in SNAPSHOT_FILES}

        def rollback(msg: str, code: int = 500):
            restore(snapshots)
            rebuild_bundles()
            self._json(code, {"error": msg})

        try:
            import research
            delta = research.research_node(node_id)
        except KeyboardInterrupt:
            raise
        except BaseException as exc:  # noqa: BLE001 — incl. SystemExit, which
            # 'except Exception' misses and which would kill the whole server;
            # count any spend the failed call already made
            state["spent"] += getattr(sys.modules.get("research"), "LAST_COST", 0.0)
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

    def _post_decisions(self):
        """One-click review: save the export, run the whole apply chain
        (apply_review -> metrics -> validate -> evaluate --graph), roll back
        every review-governed file on any failure, rebuild bundles."""
        body = self._read_guarded(512 * 1024)
        if body is None:
            return
        try:
            doc = json.loads(body or b"{}")
            decided = sum(1 for sec in doc.get("decisions", {}).values()
                          for d in sec if d.get("verdict"))
        except (json.JSONDecodeError, AttributeError, TypeError):
            self._json(400, {"error": "bad request body"})
            return
        if not decided:
            self._json(400, {"error": "the export contains no decisions"})
            return

        snapshots = {p: p.read_bytes() for p in DECISION_FILES if p.exists()}
        dec_file = DATA / "review_decisions.json"
        tmp = dec_file.with_suffix(".tmp")
        tmp.write_bytes(body)
        tmp.replace(dec_file)

        summary = ""
        for name, args in (("apply_review.py", ()), ("metrics.py", ()),
                           ("validate.py", ()), ("evaluate.py", ("--graph",))):
            cp = run_script(name, *args)
            if name == "apply_review.py":
                summary = "\n".join(cp.stdout.strip().splitlines()[-3:])
            if cp.returncode != 0:
                restore(snapshots)
                rebuild_bundles()
                tail = "\n".join((cp.stdout + cp.stderr).strip().splitlines()[-4:])
                self._json(500, {"error": f"{name} failed — nothing was applied "
                                          f"(rolled back):\n{tail}"})
                return
        rebuild_bundles()
        print(f"applied {decided} review decision(s)")
        self._json(200, {"ok": True, "applied": decided, "summary": summary})

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
    ThreadingHTTPServer(("127.0.0.1", args.port), handler).serve_forever()


if __name__ == "__main__":
    main()
