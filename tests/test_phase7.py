"""Phase 7 tests: the mutating pipeline paths (run: python -m unittest discover tests).

Fixture-based, no network, no .env, no cache/ — every test runs against a
temporary copy of synthetic data with the modules' path constants patched.
"""

import http.client
import json
import shutil
import sys
import tempfile
import threading
import types
import unittest
from functools import partial
from http.server import HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))

import build_review_data  # noqa: E402
import common  # noqa: E402
import ground  # noqa: E402
import merge  # noqa: E402
import serve  # noqa: E402


def write(path: Path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")


class TestWeightParity(unittest.TestCase):
    """common.edge_weight must reproduce validate.py's reference exactly."""

    def test_matches_validate_reference(self):
        cases = [("backbone", 0), ("backbone", 1), ("backbone", 3),
                 ("research", 0), ("research", 1), ("research", 2),
                 ("grounding", 1), ("", 0)]
        for origin, n_ev in cases:
            e = {"origin": origin, "evidence": [{"article_id": f"a{i}", "quote": "q"}
                                                for i in range(n_ev)]}
            n = (1 if origin == "backbone" else 0) + n_ev
            expected = 1 - 0.5 ** max(n, 1)
            self.assertEqual(common.edge_weight(e), expected,
                             f"origin={origin!r} evidence={n_ev}")

    def test_recompute_in_place(self):
        edges = [{"origin": "backbone", "evidence": [], "weight": -1}]
        out = common.recompute_weights(edges)
        self.assertIs(out, edges)
        self.assertEqual(edges[0]["weight"], 0.5)


class PatchedDirsMixin:
    """Temp data dir + saved/restored module path constants."""

    PATCH = ()  # (module, attr, relative-path-under-tmp)

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self._saved = []
        for mod, attr, rel in self.PATCH:
            self._saved.append((mod, attr, getattr(mod, attr)))
            setattr(mod, attr, self.tmp / rel)

    def tearDown(self):
        for mod, attr, val in self._saved:
            setattr(mod, attr, val)
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestGroundApplyIdempotent(PatchedDirsMixin, unittest.TestCase):
    PATCH = ((ground, "DATA", "data"),
             (ground, "RESPONSE_DIR", "data/ground/responses"),
             (ground, "PROPOSED_EDGES", "data/quarantine/proposed_edges.json"),
             (ground, "ARTICLE_CACHE", "cache/sep/articles"))

    def setUp(self):
        super().setUp()
        d = self.tmp / "data"
        write(d / "graph.json", {
            "meta": {"built": "2026-01-01"},
            "nodes": [{"id": i, "label": i, "type": "concept"} for i in ("a", "b", "c")],
            "edges": [
                {"source": "a", "type": "DEVELOPED_BY", "target": "b", "weight": 0.5,
                 "origin": "backbone", "evidence": [], "status": "unverified"},
                # research-origin edge citing an article with NO response file:
                # the pre-fix rebuild dropped 'ghost' from graph.articles
                {"source": "c", "type": "IS_A", "target": "a", "weight": 0.5,
                 "origin": "research", "evidence": [{"article_id": "ghost", "quote": "gq"}],
                 "status": "unverified"},
            ],
            "articles": [{"id": "ghost", "title": "Ghost", "url": "u",
                          "retrieved": "2026-01-02", "grounded_edges": 1,
                          "proposed_edges": 0}],
        })
        write(d / "registry.json", {"nodes": [
            {"id": "a", "label": "A", "type": "concept"},
            {"id": "b", "label": "B", "type": "person"},
            {"id": "c", "label": "C", "type": "concept"}]})
        write(d / "corpus.json", {
            "meta": {"built": "2026-01-01", "count": 1},
            "articles": [{"id": "art1", "title": "Article One", "url": "u1",
                          "priority": 1, "retrieved": "", "grounded_edges": 0,
                          "proposed_edges": 0}]})
        write(d / "ground" / "responses" / "art1.json", {
            "meta": {"article_id": "art1", "date": "2026-01-03"},
            "groundings": [{"source": "a", "type": "DEVELOPED_BY", "target": "b",
                            "quote": "hello world"}],
            "proposed_edges": [{"source": "a", "type": "CRITIQUES", "target": "c",
                                "quote": "prop quote"}]})
        # an already-reviewed proposal whose status must survive re-apply
        write(self.tmp / "data" / "quarantine" / "proposed_edges.json", {
            "meta": {"built": "2026-01-03"},
            "proposals": [{"source": "a", "type": "CRITIQUES", "target": "c",
                           "quote": "prop quote", "article_id": "art1",
                           "status": "accepted"}]})
        (self.tmp / "cache" / "sep" / "articles").mkdir(parents=True)
        (self.tmp / "cache" / "sep" / "articles" / "art1.txt").write_text("x", encoding="utf-8")

    def read_all(self):
        d = self.tmp / "data"
        return {p.name: p.read_text(encoding="utf-8")
                for p in (d / "graph.json", d / "corpus.json",
                          d / "quarantine" / "proposed_edges.json")}

    def test_apply_twice_is_stable_and_lossless(self):
        ground.cmd_apply(None)
        first = self.read_all()
        graph = json.loads(first["graph.json"])
        # the research-cited article survives the rebuild
        self.assertIn("ghost", [a["id"] for a in graph["articles"]])
        # origin-aware weights: backbone edge gained 1 quote -> n=2 -> 0.75;
        # research edge keeps n=1 -> 0.5 (the stale formula said 0.75)
        w = {(e["source"], e["target"]): e["weight"] for e in graph["edges"]}
        self.assertEqual(w[("a", "b")], 0.75)
        self.assertEqual(w[("c", "a")], 0.5)
        # review-written status survives the quarantine rewrite
        quar = json.loads(first["proposed_edges.json"])
        self.assertEqual(quar["proposals"][0]["status"], "accepted")
        ground.cmd_apply(None)
        self.assertEqual(self.read_all(), first, "second apply changed bytes")


class TestMergePreservesProvisional(PatchedDirsMixin, unittest.TestCase):
    PATCH = ((merge, "DATA", "data"), (merge, "ROOT", "."))

    def setUp(self):
        super().setUp()
        d = self.tmp / "data"
        write(d / "seeds.json", {
            "meta": {"version": "t", "domain": "Ethics"},
            "concepts": [{"id": "a", "label": "A"}],
            "persons": [], "schools": [], "works": [],
            "sep_corpus": [{"id": "art1", "priority": 1}]})
        write(d / "wikidata_enrichment.json", {"entries": [
            {"id": "a", "wikidata_qid": "Q1", "qid_source": "curated-verified",
             "wd_description": "", "wd_aliases": []}]})
        write(d / "sep_contents.json", {"entries": [{"id": "art1", "title": "Article One"}]})
        write(d / "registry.json", {"meta": {"built": "2026-01-01"}, "nodes": [
            {"id": "a", "label": "A", "type": "concept", "status": "registry"},
            {"id": "prov1", "label": "Prov", "type": "concept",
             "status": "provisional", "qid_source": "unresolved",
             "wikidata_qid": "", "aliases": []}]})
        write(d / "corpus.json", {"meta": {"built": "2026-01-01", "count": 1},
                                  "articles": [{"id": "art1", "title": "Article One",
                                                "url": "u", "priority": 1,
                                                "retrieved": "2026-01-05",
                                                "grounded_edges": 7, "proposed_edges": 2}]})
        write(d / "graph.json", {"nodes": [{"id": "a"}, {"id": "prov1"}], "edges": []})

    def test_provisional_rows_and_bookkeeping_survive_reruns(self):
        merge.main()
        reg1 = (self.tmp / "data" / "registry.json").read_text(encoding="utf-8")
        cor1 = (self.tmp / "data" / "corpus.json").read_text(encoding="utf-8")
        self.assertIn("prov1", {r["id"] for r in json.loads(reg1)["nodes"]})
        art = json.loads(cor1)["articles"][0]
        self.assertEqual((art["retrieved"], art["grounded_edges"]), ("2026-01-05", 7))
        merge.main()
        self.assertEqual((self.tmp / "data" / "registry.json").read_text(encoding="utf-8"), reg1)
        self.assertEqual((self.tmp / "data" / "corpus.json").read_text(encoding="utf-8"), cor1)

    def test_failed_coverage_check_writes_nothing(self):
        d = self.tmp / "data"
        write(d / "graph.json", {"nodes": [{"id": "a"}, {"id": "prov1"},
                                           {"id": "zzz"}], "edges": []})
        before_reg = (d / "registry.json").read_text(encoding="utf-8")
        before_cor = (d / "corpus.json").read_text(encoding="utf-8")
        with self.assertRaises(SystemExit):
            merge.main()
        self.assertEqual((d / "registry.json").read_text(encoding="utf-8"), before_reg)
        self.assertEqual((d / "corpus.json").read_text(encoding="utf-8"), before_cor)


class TestReviewBundleDeterminism(PatchedDirsMixin, unittest.TestCase):
    PATCH = ((build_review_data, "DATA", "data"),
             (build_review_data, "ROOT", "."))

    def setUp(self):
        super().setUp()
        d = self.tmp / "data"
        (self.tmp / "viewer").mkdir()
        write(d / "registry.json", {"nodes": [
            {"id": "a", "label": "A", "type": "concept"},
            {"id": "b", "label": "B", "type": "person"}]})
        write(d / "corpus.json", {"articles": [{"id": "art1", "title": "T", "url": "u"}]})
        write(d / "graph.json", {"nodes": [], "edges": []})
        write(d / "verification_sample.json", {"sample": [
            {"source": "a", "type": "DEVELOPED_BY", "target": "b", "verdict": ""}]})
        write(d / "quarantine" / "proposed_edges.json", {"proposals": [
            {"source": "a", "type": "CRITIQUES", "target": "b", "quote": "q",
             "article_id": "art1", "status": "quarantined"}]})
        write(d / "quarantine" / "proposed_nodes.json", {"proposed_nodes": []})

    def bundle(self):
        build_review_data.main()
        return (self.tmp / "viewer" / "review.data.js").read_text(encoding="utf-8")

    def test_identical_inputs_identical_bytes(self):
        self.assertEqual(self.bundle(), self.bundle())

    def test_keys_and_fingerprint(self):
        doc = json.loads(self.bundle().split("=", 1)[1].rstrip().rstrip(";"))
        self.assertEqual(doc["sample"][0]["key"], "a|DEVELOPED_BY|b")
        self.assertEqual(doc["proposed_edges"][0]["key"], "a|CRITIQUES|b|art1")
        fp1 = doc["fingerprint"]
        write(self.tmp / "data" / "quarantine" / "proposed_nodes.json",
              {"proposed_nodes": [{"label": "New Thing", "type": "concept"}]})
        doc2 = json.loads(self.bundle().split("=", 1)[1].rstrip().rstrip(";"))
        self.assertNotEqual(doc2["fingerprint"], fp1,
                            "fingerprint must change when the queue changes")


class TestServeRollback(PatchedDirsMixin, unittest.TestCase):
    """A research pass that corrupts the data and dies with SystemExit must
    leave the server alive, the files restored byte-for-byte, and the spend
    accounted for."""

    PATCH = ()

    def setUp(self):
        super().setUp()
        self.g = self.tmp / "graph.json"
        self.r = self.tmp / "registry.json"
        self.g.write_text('{"good": "graph"}', encoding="utf-8")
        self.r.write_text('{"good": "registry"}', encoding="utf-8")
        self._snap = serve.SNAPSHOT_FILES
        self._run = serve.run_script
        self._research = sys.modules.get("research")
        serve.SNAPSHOT_FILES = (self.g, self.r)
        serve.run_script = lambda name: types.SimpleNamespace(returncode=0,
                                                              stdout="", stderr="")
        stub = types.ModuleType("research")
        stub.LAST_COST = 0.0
        tmp = self.tmp

        def research_node(node_id):
            stub.LAST_COST = 0.042  # spend happened before the crash
            (tmp / "graph.json").write_text("CORRUPT", encoding="utf-8")
            raise SystemExit("no ANTHROPIC_API_KEY in environment or .env")

        stub.research_node = research_node
        sys.modules["research"] = stub
        serve.state.update({"spent": 0.0, "cap": 1.50})
        self.server = HTTPServer(("127.0.0.1", 0),
                                 partial(serve.Handler, directory=str(self.tmp)))
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        serve.SNAPSHOT_FILES = self._snap
        serve.run_script = self._run
        if self._research is not None:
            sys.modules["research"] = self._research
        else:
            sys.modules.pop("research", None)
        super().tearDown()

    def post(self, body, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=10)
        conn.request("POST", "/api/research", body,
                     {"Content-Type": "application/json", **(headers or {})})
        resp = conn.getresponse()
        out = (resp.status, json.loads(resp.read().decode("utf-8")))
        conn.close()
        return out

    def test_systemexit_rolls_back_and_server_survives(self):
        status, doc = self.post(json.dumps({"id": "any"}))
        self.assertEqual(status, 500)
        self.assertIn("research failed", doc["error"])
        self.assertEqual(self.g.read_text(encoding="utf-8"), '{"good": "graph"}')
        self.assertEqual(self.r.read_text(encoding="utf-8"), '{"good": "registry"}')
        self.assertAlmostEqual(serve.state["spent"], 0.042)
        # server is still alive and answering
        status2, _ = self.post(json.dumps({"id": "again"}))
        self.assertEqual(status2, 500)

    def test_cross_origin_post_rejected_before_any_work(self):
        status, doc = self.post(json.dumps({"id": "any"}),
                                {"Origin": "http://evil.example"})
        self.assertEqual(status, 403)
        self.assertEqual(self.g.read_text(encoding="utf-8"), '{"good": "graph"}')

    def test_oversized_body_rejected(self):
        status, _ = self.post("x" * 5000)
        self.assertEqual(status, 413)


if __name__ == "__main__":
    unittest.main()
