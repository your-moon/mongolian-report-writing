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


class ScanTest(unittest.TestCase):
    def test_each_bad_line_trips_its_check(self):
        for check, line in BAD:
            with self.subTest(line=line):
                self.assertIn(check, [f[2] for f in scan_text(line)])

    def test_correct_text_is_clean(self):
        self.assertEqual(scan_text(GOOD), [])

    def test_allow_skips_a_term(self):
        self.assertEqual(scan_text("Хаалга эвдэрсэн.", allow=("хаалга",)), [])


if __name__ == "__main__":
    unittest.main()
