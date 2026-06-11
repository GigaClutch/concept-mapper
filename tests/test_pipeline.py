"""Unit tests for pipeline helpers (run: python -m unittest discover tests)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))

import validate  # noqa: E402
from scrape_sep import ContentsParser, TextExtractor  # noqa: E402


class TestNorm(unittest.TestCase):
    def test_collapses_whitespace(self):
        self.assertEqual(validate.norm("a\n  b\tc"), "a b c")

    def test_nbsp(self):
        self.assertEqual(validate.norm("a b"), "a b")

    def test_substring_check_survives_reflow(self):
        quote = "the supreme principle of morality"
        source = "argued that the supreme\n   principle of  morality is"
        self.assertIn(validate.norm(quote), validate.norm(source))


class TestEdgeKey(unittest.TestCase):
    def test_symmetric_unordered(self):
        self.assertEqual(validate.edge_key("a", "b", "CONTRASTS_WITH"),
                         validate.edge_key("b", "a", "CONTRASTS_WITH"))

    def test_directed_ordered(self):
        self.assertNotEqual(validate.edge_key("a", "b", "DEVELOPED_BY"),
                            validate.edge_key("b", "a", "DEVELOPED_BY"))


class TestEdgeTaxonomy(unittest.TestCase):
    def test_no_related_to(self):
        self.assertNotIn("RELATED_TO", validate.EDGE_TYPES)

    def test_families_complete(self):
        self.assertEqual(len(validate.EDGE_TYPES), 12)


class TestTextExtractor(unittest.TestCase):
    def test_inline_tags_do_not_split_words(self):
        ex = TextExtractor()
        ex.feed("<p>(hereafter, <em>Groundwork</em>), but</p>")
        self.assertEqual(ex.text(), "(hereafter, Groundwork), but")

    def test_script_and_style_dropped(self):
        ex = TextExtractor()
        ex.feed("<p>keep</p><script>drop()</script><style>.x{}</style><p> this</p>")
        self.assertEqual(ex.text(), "keep this")


class TestContentsParser(unittest.TestCase):
    def test_entry_links_and_dedup(self):
        p = ContentsParser()
        p.feed('<a href="entries/kant-moral/">Kant\'s Moral  Philosophy</a>'
               '<a href="entries/kant-moral/">see also dup</a>'
               '<a href="https://example.com/entries/x/">offsite</a>'
               '<a href="other.html">not an entry</a>')
        self.assertEqual(p.entries, {"kant-moral": "Kant's Moral Philosophy"})


if __name__ == "__main__":
    unittest.main()
