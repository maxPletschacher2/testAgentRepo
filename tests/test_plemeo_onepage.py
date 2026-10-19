from pathlib import Path
from html.parser import HTMLParser
import unittest


class PlemeoHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.forms = []
        self.inputs = []
        self.textareas = []
        self.buttons = []
        self.headers = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        elif tag == "form":
            self.forms.append(attrs)
        elif tag == "input":
            self.inputs.append(attrs)
        elif tag == "textarea":
            self.textareas.append(attrs)
        elif tag == "button":
            self.buttons.append(attrs)
        elif tag in {"h1", "h2", "h3"}:
            self.headers.append((tag, attrs))


class TestPlemeoOnePage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.index_path = cls.root / "index.html"
        cls.html = cls.index_path.read_text(encoding="utf-8")
        cls.parser = PlemeoHtmlParser()
        cls.parser.feed(cls.html)

    def test_index_html_exists(self):
        self.assertTrue(self.index_path.exists(), "index.html fehlt im Repository-Root")

    def test_contains_required_sections(self):
        html = self.html.lower()
        self.assertIn("plemeo.ai", html)
        self.assertIn('id="produkt"', html)
        self.assertIn('id="kontakt"', html)
        self.assertIn("produkt", html)
        self.assertIn("kontaktformular", html)

    def test_contact_form_is_at_the_end(self):
        html = self.html
        form_pos = html.rfind('<form class="contact-card" id="contact-form">')
        footer_pos = html.rfind("<footer>")
        self.assertGreater(form_pos, 0, "Das Kontaktformular wurde nicht gefunden")
        self.assertGreater(footer_pos, form_pos, "Das Kontaktformular soll am Seitenende vor dem Footer stehen")

    def test_contact_form_fields_are_present(self):
        self.assertEqual(len(self.parser.forms), 1)
        self.assertGreaterEqual(len(self.parser.inputs), 3)
        self.assertEqual(len(self.parser.textareas), 1)
        self.assertGreaterEqual(len(self.parser.buttons), 1)

        names = {attrs.get("name") for attrs in self.parser.inputs}
        self.assertIn("name", names)
        self.assertIn("email", names)
        self.assertIn("subject", names)
        self.assertIn("message", {attrs.get("name") for attrs in self.parser.textareas})

    def test_navigation_targets(self):
        self.assertIn("#produkt", self.parser.links)
        self.assertIn("#vorteile", self.parser.links)
        self.assertIn("#ablauf", self.parser.links)
        self.assertIn("#kontakt", self.parser.links)
        self.assertIn("kontaktformular", self.html.lower())

    def test_static_page_has_client_side_feedback(self):
        self.assertIn("form-status", self.html)
        self.assertIn("Danke!", self.html)


if __name__ == "__main__":
    unittest.main()
