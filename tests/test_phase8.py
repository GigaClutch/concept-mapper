"""Phase 8 tests: apply_review round-trip, D4 auto-flip, /api/decisions.

Fixture-based, no network, no .env — temp data dirs with patched module
constants, same conventions as test_phase7.py.
"""

import http.client
import json
import sys
import threading
import types
import unittest
from functools import partial
from http.server import HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import apply_review  # noqa: E402
import ground  # noqa: E402
import serve  # noqa: E402
from test_phase7 import PatchedDirsMixin, write  # noqa: E402


def graph_fixture():
    return {
        "meta": {"built": "2026-01-01"},
        "nodes": [{"id": i, "label": i.title(), "type": t, "metrics": {}}
                  for i, t in (("virtue", "concept"), ("vice", "concept"),
                               ("plato", "person"), ("stray", "concept"))],
        "edges": [
            {"source": "virtue", "type": "DEVELOPED_BY", "target": "plato",
             "weight": 0.75, "origin": "backbone", "status": "grounded",
             "evidence": [{"article_id": "art1", "quote": "q1"}]},
            {"source": "vice", "type": "CONTRASTS_WITH", "target": "virtue",
             "weight": 0.5, "origin": "backbone", "status": "unverified",
             "evidence": []},
            # rejecting this one orphans 'stray'
            {"source": "stray", "type": "IS_A", "target": "virtue",
             "weight": 0.5, "origin": "backbone", "status": "unverified",
             "evidence": []},
        ],
        "articles": [],
    }


class TestApplyReviewRoundTrip(PatchedDirsMixin, unittest.TestCase):
    PATCH = ((apply_review, "DATA", "data"),
             (apply_review, "DECISIONS", "data/review_decisions.json"),
             (apply_review, "QUAR_EDGES", "data/quarantine/proposed_edges.json"),
             (apply_review, "QUAR_NODES", "data/quarantine/proposed_nodes.json"),
             (apply_review, "SAMPLE", "data/verification_sample.json"))

    def setUp(self):
        super().setUp()
        d = self.tmp / "data"
        write(d / "graph.json", graph_fixture())
        write(d / "registry.json", {"meta": {"count": 4}, "nodes": [
            {"id": "virtue", "label": "Virtue", "type": "concept"},
            {"id": "vice", "label": "Vice", "type": "concept"},
            {"id": "plato", "label": "Plato", "type": "person"},
            {"id": "stray", "label": "Stray", "type": "concept"}]})
        write(d / "verification_sample.json", {"sample": [
            {"source": "virtue", "type": "DEVELOPED_BY", "target": "plato",
             "verdict": "", "notes": ""},
            {"source": "stray", "type": "IS_A", "target": "virtue",
             "verdict": "", "notes": ""}]})
        write(d / "quarantine" / "proposed_edges.json", {"meta": {}, "proposals": [
            {"source": "vice", "type": "DEVELOPED_BY", "target": "plato",
             "quote": "pq", "article_id": "art1", "status": "quarantined"}]})
        write(d / "quarantine" / "proposed_nodes.json", {"meta": {}, "proposed_nodes": [
            {"label": "Temperance", "type": "concept"}]})
        write(d / "review_decisions.json", {"exported": "2026-07-07", "decisions": {
            "sample": [
                {"source": "virtue", "type": "DEVELOPED_BY", "target": "plato",
                 "verdict": "accept", "note": ""},
                {"source": "stray", "type": "IS_A", "target": "virtue",
                 "verdict": "reject", "note": "made up"}],
            "proposed_edges": [
                {"source": "vice", "type": "DEVELOPED_BY", "target": "plato",
                 "article_id": "art1", "verdict": "accept", "note": ""}],
            "proposed_nodes": [
                {"label": "Temperance", "verdict": "accept", "note": ""}],
            "researched_edges": [], "researched_nodes": []}})

    def test_round_trip(self):
        apply_review.main()
        d = self.tmp / "data"
        graph = json.loads((d / "graph.json").read_text(encoding="utf-8"))
        edges = {(e["source"], e["type"], e["target"]): e for e in graph["edges"]}
        # accept -> confirmed
        self.assertEqual(edges[("virtue", "DEVELOPED_BY", "plato")]["status"], "confirmed")
        # reject -> edge gone AND the node it orphaned gone
        self.assertNotIn(("stray", "IS_A", "virtue"), edges)
        self.assertNotIn("stray", {n["id"] for n in graph["nodes"]})
        # accepted proposal merged with evidence, origin grounding, weight n=1
        merged = edges[("vice", "DEVELOPED_BY", "plato")]
        self.assertEqual(merged["origin"], "grounding")
        self.assertEqual(merged["evidence"][0]["quote"], "pq")
        self.assertEqual(merged["weight"], 0.5)
        # audit trail in quarantine + sample verdicts written back
        quar = json.loads((d / "quarantine" / "proposed_edges.json").read_text(encoding="utf-8"))
        self.assertEqual(quar["proposals"][0]["status"], "accepted")
        qn = json.loads((d / "quarantine" / "proposed_nodes.json").read_text(encoding="utf-8"))
        self.assertIn("approved", qn["proposed_nodes"][0]["status"])
        sample = json.loads((d / "verification_sample.json").read_text(encoding="utf-8"))
        verdicts = {s["source"]: s["verdict"] for s in sample["sample"]}
        self.assertEqual(verdicts, {"virtue": "accept", "stray": "reject"})


class TestGroundApplyAutoFlip(PatchedDirsMixin, unittest.TestCase):
    PATCH = ((ground, "DATA", "data"),
             (ground, "RESPONSE_DIR", "data/ground/responses"),
             (ground, "PROPOSED_EDGES", "data/quarantine/proposed_edges.json"),
             (ground, "ARTICLE_CACHE", "cache/sep/articles"))

    def setUp(self):
        super().setUp()
        d = self.tmp / "data"
        write(d / "graph.json", {
            "meta": {}, "nodes": [], "articles": [],
            "edges": [{"source": "virtue", "type": "DEVELOPED_BY", "target": "plato",
                       "weight": 0.5, "origin": "backbone", "status": "unverified",
                       "evidence": []}]})
        write(d / "registry.json", {"nodes": [
            {"id": "virtue", "label": "Virtue", "type": "concept"},
            {"id": "vice", "label": "Vice", "type": "concept"},
            {"id": "plato", "label": "Plato", "type": "person"}]})
        write(d / "corpus.json", {"meta": {}, "articles": [
            {"id": "art1", "title": "T", "url": "u", "priority": 1,
             "retrieved": "2026-01-01", "grounded_edges": 0, "proposed_edges": 0}]})
        write(d / "ground" / "responses" / "art1.json", {
            "meta": {"article_id": "art1", "date": "2026-01-01"},
            "groundings": [],
            "proposed_edges": [
                # person DEVELOPED_BY concept: backwards, flips to a NEW edge
                {"source": "plato", "type": "DEVELOPED_BY", "target": "vice",
                 "quote": "flip me"},
                # backwards duplicate of the existing graph edge: dropped
                {"source": "plato", "type": "DEVELOPED_BY", "target": "virtue",
                 "quote": "dup"},
                # valid as stated: untouched
                {"source": "vice", "type": "IS_A", "target": "virtue",
                 "quote": "fine"}]})
        (self.tmp / "cache" / "sep" / "articles").mkdir(parents=True)

    def test_flip_drop_and_passthrough(self):
        ground.cmd_apply(None)
        quar = json.loads((self.tmp / "data" / "quarantine" / "proposed_edges.json")
                          .read_text(encoding="utf-8"))
        by_key = {(p["source"], p["type"], p["target"]): p for p in quar["proposals"]}
        self.assertEqual(len(quar["proposals"]), 2)
        flipped = by_key[("vice", "DEVELOPED_BY", "plato")]
        self.assertTrue(flipped.get("flipped"))
        self.assertNotIn(("plato", "DEVELOPED_BY", "virtue"), by_key)
        self.assertFalse(by_key[("vice", "IS_A", "virtue")].get("flipped"))


class TestDecisionsEndpoint(PatchedDirsMixin, unittest.TestCase):
    """POST /api/decisions runs the chain in order; a failing step restores
    every review-governed file byte-for-byte."""

    PATCH = ()

    def setUp(self):
        super().setUp()
        self.files = {}
        names = ("graph.json", "registry.json", "verification_sample.json",
                 "proposed_edges.json", "proposed_nodes.json")
        for n in names:
            p = self.tmp / n
            p.write_text(f'{{"pristine": "{n}"}}', encoding="utf-8")
            self.files[n] = p
        self._saved = [(serve, a, getattr(serve, a)) for a in
                       ("SNAPSHOT_FILES", "DECISION_FILES", "DATA", "run_script")]
        serve.DATA = self.tmp
        serve.DECISION_FILES = tuple(self.files.values())
        self.calls = []
        self.fail_at = None
        tmp, calls = self.tmp, self.calls

        def fake_run_script(name, *args):
            calls.append((name, args))
            if name == "apply_review.py":
                # the real apply mutates the data files (not the decisions file)
                for p in tmp.glob("*.json"):
                    if p.name != "review_decisions.json":
                        p.write_text('{"mutated": true}', encoding="utf-8")
            rc = 1 if name == self.fail_at else 0
            return types.SimpleNamespace(returncode=rc, stdout=f"{name} out",
                                         stderr="")

        serve.run_script = fake_run_script
        self.server = HTTPServer(("127.0.0.1", 0),
                                 partial(serve.Handler, directory=str(self.tmp)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        for mod, attr, val in self._saved:
            setattr(mod, attr, val)
        super().tearDown()

    def post(self, doc):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port,
                                          timeout=10)
        conn.request("POST", "/api/decisions", json.dumps(doc),
                     {"Content-Type": "application/json"})
        resp = conn.getresponse()
        out = (resp.status, json.loads(resp.read().decode("utf-8")))
        conn.close()
        return out

    DECISIONS = {"exported": "2026-07-07", "decisions": {
        "sample": [{"source": "a", "type": "IS_A", "target": "b",
                    "verdict": "accept", "note": ""}]}}

    def test_success_runs_chain_in_order(self):
        status, doc = self.post(self.DECISIONS)
        self.assertEqual(status, 200)
        self.assertTrue(doc["ok"])
        self.assertEqual(doc["applied"], 1)
        self.assertEqual(doc["summary"], "apply_review.py out")
        script_order = [c[0] for c in self.calls]
        self.assertEqual(script_order[:4], ["apply_review.py", "metrics.py",
                                            "validate.py", "evaluate.py"])
        self.assertEqual(dict(self.calls)["evaluate.py"], ("--graph",))
        # decisions file was written for apply_review to read
        self.assertEqual(json.loads((self.tmp / "review_decisions.json")
                                    .read_text(encoding="utf-8")), self.DECISIONS)

    def test_failure_rolls_back_every_file(self):
        self.fail_at = "validate.py"
        status, doc = self.post(self.DECISIONS)
        self.assertEqual(status, 500)
        self.assertIn("rolled back", doc["error"])
        for n, p in self.files.items():
            self.assertEqual(p.read_text(encoding="utf-8"),
                             f'{{"pristine": "{n}"}}', n)

    def test_empty_export_rejected_without_running_anything(self):
        status, doc = self.post({"exported": "x", "decisions": {"sample": []}})
        self.assertEqual(status, 400)
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
