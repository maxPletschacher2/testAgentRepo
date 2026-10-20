from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "index.html"


class SimpleHTMLSanityParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms = 0
        self.headers = []
        self.links = []
        self.inputs = []
        self.textareas = 0
        self.selects = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "form":
            self.forms += 1
        elif tag in {"h1", "h2", "h3"}:
            self.headers.append(tag)
        elif tag == "a":
            self.links.append(attrs.get("href", ""))
        elif tag == "input":
            self.inputs.append(attrs)
        elif tag == "textarea":
            self.textareas += 1
        elif tag == "select":
            self.selects += 1


class TestBMW4erLandingPage(unittest.TestCase):
    def setUp(self):
        self.html = INDEX_PATH.read_text(encoding="utf-8")

    def test_index_exists(self):
        self.assertTrue(INDEX_PATH.exists(), "index.html fehlt im Projektstamm")

    def test_contains_expected_sections_and_form(self):
        parser = SimpleHTMLSanityParser()
        parser.feed(self.html)

        self.assertIn("BMW 4er", self.html)
        self.assertIn('id="highlights"', self.html)
        self.assertIn('id="modelle"', self.html)
        self.assertIn('id="technik"', self.html)
        self.assertIn('id="kontakt"', self.html)
        self.assertGreaterEqual(parser.forms, 1)
        self.assertGreaterEqual(parser.selects, 1)
        self.assertGreaterEqual(parser.textareas, 1)

        input_types = {attrs.get("type") for attrs in parser.inputs}
        self.assertIn("text", input_types)
        self.assertIn("email", input_types)
        self.assertIn("checkbox", input_types)

    def test_navigation_targets_match_sections(self):
        self.assertIn('#highlights', self.html)
        self.assertIn('#modelle', self.html)
        self.assertIn('#technik', self.html)
        self.assertIn('#kontakt', self.html)
        self.assertIn("Anfrage abschicken", self.html)
        self.assertIn("class=\"status\"", self.html)


if __name__ == "__main__":
    unittest.main()
