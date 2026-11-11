"""Run: python3 -m unittest test_bolor  (from this folder)."""
import unittest
from bolor import scan_text

# Each bad line comes from a real failure in WORDS.md or a rule in SKILL.md / GRAMMAR.md.
BAD = [
    ("calque", "Машинаас хаалгаа нээхийг хүснэ."),
    ("calque", "Хоёр тал дундаа уулздаг."),
    ("calque", "Нэг чимээгүй холболт ашиглана."),
    ("calque", "Шинэчлэлийг давалгаа тус бүрээр гаргасан."),
    ("calque", "Засварыг үйлдвэрлэлийн орчинд нэвтрүүлсэн."),
    ("calque", "Машиныг дахин асаасан."),
    ("calque", "Нийт флот хэвийн ажилласан."),
    ("calque", "Хэрэглэгчид хандалт өгсөн."),
    ("calque", "Хяналтын самбар дээр харагдана. Самбар солигдсон."),
    ("brand", "Төлбөрийг КьюПэй-ээр хийсэн."),
    ("first-person", "Бид алдааг 14:00 цагт засварласан."),
    ("first-person", "Манай систем хэвийн ажилласан."),
    ("colloquial", "Сервер унтарчихсан байсан."),
    ("evidential", "Сервер 14:00 цагт унтарчээ."),
    ("question", "Яагаад ийм алдаа гарсан бэ?"),
    ("quotes", "«Хууль» батлагдсан."),
    ("initial", "Л Оюун-Эрдэнэ хэлэв."),
    ("numbers", "Нийт 3,603,000 төгрөг. Үлдэгдэл 12 500 төгрөг."),
    ("numbers", "Борлуулалт 6.4 хувиар өссөн. Зардал 3%-иар буурсан."),
]

# Correct text from GRAMMAR.md, STRUCTURE.md and WORDS.md. Must produce no findings.
GOOD = """Хууль батлагдсан өдрөөсөө хэрэгжинэ.
...баривчлагдсан тухай ТАСС агентлаг өчигдөр мэдээлжээ.
Хяналтын шалгалтаар зөрчлийг тогтоосон тухай аудитын дүгнэлтэд тогтоожээ.
110 гишүүн оролцсоноос 90 гишүүн буюу 81.8 хувь нь баталлаа.
Нийт 3,603,000 (гурван сая зургаан зуун гурван мянга) төгрөг зарцуулсан.
Л.Оюун-Эрдэнэ "бид дэмжинэ" гэж мэдэгдэв.
Машинаас холболтыг өөрийн талаас нь эхлүүлэхийг хүснэ.
Хугацаа дуусахад машин холболтоо өөрөө таслана.
Тус байгууллага арга хэмжээ авсан.
Эрхийг чимээгүйхэн олгосон.
Төлбөрийг QPay-ээр хийсэн.
Засварыг prod орчинд нэвтрүүлсэн.
Машиныг дахин ачаалсан.
"""


TERMS = [
    {"en": "production/prod", "status": "confirmed",
     "dev": {"group": "english", "write": "prod"},
     "official": {"group": "native", "write": "ашиглалтын орчин"},
     "avoid": ["үйлдвэрлэлийн орчин"], "evidence": []},
    {"en": "server", "status": "confirmed",
     "dev": {"group": "loan", "write": "сервер"},
     "official": {"group": "loan", "write": "сервер"}, "avoid": [], "evidence": []},
    {"en": "dashboard", "status": "unsure",
     "dev": {"group": "english", "write": "dashboard"},
     "official": {"group": "native", "write": "хяналтын дэлгэц"},
     "avoid": ["хяналтын самбар"], "evidence": []},
]


class TermTest(unittest.TestCase):
    def checks(self, text, setting="dev"):
        return [(f[1], f[3]) for f in scan_text(text, setting=setting, terms=TERMS)
                if f[2] == "term"]

    def test_confirmed_avoid_is_an_error(self):
        self.assertIn(("ERROR", "үйлдвэрлэлийн орчин"), self.checks("Засварыг үйлдвэрлэлийн орчинд гаргасан."))

    def test_unsure_avoid_is_only_a_warning(self):
        self.assertIn(("WARN", "хяналтын самбар"), self.checks("Хяналтын самбарт харагдана."))

    def test_avoid_matches_only_at_a_word_start(self):
        terms = [dict(TERMS[1], avoid=["тор"])]
        self.assertEqual([f for f in scan_text("Мотор эвдэрсэн.", terms=terms) if f[2] == "term"], [])

    def test_bundled_terms_do_not_flag_correct_report_text(self):
        from bolor import load_terms
        text = ("Зөрчлийг тогтоосон. Тус салбараас шалгалт хийж, үр дүнг хэвлэлд мэдээлсэн. "
                "Машиныг дахин ачаалсан. Харилцаа холбооны сүлжээ хэвийн. Мотор солигдсон. "
                "Үйлдвэрлэлийн хэмжээ өссөн. Хуралдаан болсон.")
        self.assertEqual([f for f in scan_text(text, terms=load_terms()) if f[2] == "term"], [])

    def test_latin_word_with_a_loanword_warns(self):
        self.assertIn(("WARN", "server"), self.checks("Server унтарсан."))

    def test_english_group_stays_latin_in_dev(self):
        self.assertEqual(self.checks("Засварыг prod орчинд гаргасан."), [])

    def test_same_word_warns_in_official(self):
        self.assertIn(("WARN", "prod"), self.checks("Засварыг prod орчинд гаргасан.", "official"))

    def test_code_and_english_only_lines_are_ignored(self):
        self.assertEqual(self.checks("Run `server start` дараа нь шалгасан."), [])
        self.assertEqual(self.checks("The server is down."), [])

    def test_bundled_terms_file_is_valid(self):
        from bolor import load_terms, SETTINGS
        for e in load_terms():
            with self.subTest(term=e.get("en")):
                self.assertIn(e["status"], ("confirmed", "unsure"))
                for s in SETTINGS:
                    self.assertIn(e[s]["group"], ("english", "loan", "native"))
                    self.assertTrue(e[s]["write"])
                if e["status"] == "confirmed":
                    self.assertTrue(e["evidence"], "confirmed needs evidence")


class ScanTest(unittest.TestCase):
    def test_each_bad_line_trips_its_check(self):
        for check, line in BAD:
            with self.subTest(line=line):
                self.assertIn(check, [f[2] for f in scan_text(line, terms=[])])

    def test_correct_text_is_clean(self):
        self.assertEqual(scan_text(GOOD, terms=[]), [])

    def test_allow_skips_a_term(self):
        self.assertEqual(scan_text("Хаалга эвдэрсэн.", allow=("хаалга",), terms=[]), [])


if __name__ == "__main__":
    unittest.main()
