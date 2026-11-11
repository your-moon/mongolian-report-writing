#!/usr/bin/env python3
"""bolor-toli.com lookup — check what a Mongolian word actually means before using it.

Why this exists: WORDS.md documents 28 measured calques. All of them were produced by a
model that had already read the rule telling it not to. The rule needs a fact it does not
have — what the Mongolian word means to a Mongolian reader. This fetches that fact.

Usage:
    bolor.py үйлдвэрлэл            # mn -> en: what does this word actually say?
    bolor.py production            # en -> mn: which words are on offer?
    bolor.py --scan draft.md       # check a finished draft; exit 1 on any ERROR
    bolor.py --scan draft.md --allow=хаалга   # a real door: skip one term or check name
    bolor.py --scan letter.md --setting=official   # official letter/report (default: dev note)
    bolor.py --term deploy         # how Mongolian text renders it, with evidence
    bolor.py -d 8 үйлдвэрлэл       # другое направление (8=ru, 3=de, 5=jp, 7=cn, 4=kr)

Endpoint is undocumented and same-origin to the site. Keep the volume at human pace —
one word at a time, results cached in ~/.cache/bolor-toli.json. Do not bulk-scrape it.
"""
import hashlib, json, os, re, sys, urllib.error, urllib.parse, urllib.request

CACHE = os.path.expanduser("~/.cache/bolor-toli.json")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"

# Measured calques from WORDS.md §2a-2d. Each one shipped in a real document.
# (regex over lowercased text, short name, why it is wrong)
CALQUES = [
    (r"хаалг",                      "хаалга",             "a physical door; a connection is холболт"),
    (r"холболт\w*\s+хаа",           "холболт хаах",       "connections are cut (таслах), not shut"),
    (r"дундаа\s+уулз",              "дундаа уулзах",      "people meeting in person; use дундын сервер дээр холбогдох"),
    (r"чимээгүй(?!хэн)",            "чимээгүй",           "silence of sound; use тогтмол / хариу өгөхөө больсон. чимээгүйхэн олгох is fine"),
    (r"дотор\s+(нь\s+)?ор",          "дотор орох",         "climbing inside the cabinet; use системд нэвтрэх"),
    (r"давалгаа",                   "давалгаа",           "an ocean wave; use үе шаттайгаар"),
    (r"гараар\s+хүрэлгүй",           "гараар хүрэлгүй",    "EN idiom; use газар дээр нь очилгүйгээр"),
    (r"уншуул",                     "уншуулах",           "have someone read aloud to you; use мэдэгдэх"),
    (r"тайлагд",                    "тайлагдах",          "deciphered / reported; use тодорхой"),
    (r"нарийсна",                   "нарийсна",           "EN geometry metaphor; use шатлан олгогдоно"),
    (r"санах\s+ой",                 "санах ой",           "computer RAM, not human memory; use хүн санаж хийх үйлдэл"),
    (r"өөрийгөө\s+зарла",           "өөрийгөө зарлах",    "advertise / proclaim publicly; use системд холбогдох"),
    (r"дахин\s+асаа",               "дахин асаах",        "flip the power on; reboot is дахин ачаалах"),
    (r"программ\w*\s+суу",          "программ суух",      "суух = sit down; use суулгагдсан"),
    (r"флот",                       "флот",               "a naval fleet; use нийт машин / бүх машин"),
    (r"үйлдвэрлэлийн\s+орчин",      "үйлдвэрлэлийн орчин","factory manufacturing; write prod / бодит орчин"),
    (r"зам\s+хоног",                "зам хоног",          "not a phrase; use замын зардал, цаг хугацаа"),
    (r"ил\s+нээлттэй",              "ил нээлттэй",        "redundant pair; use нээлттэй"),
    (r"хүний\s+ойлгох",             "хүний ойлгох",       "use хүнд ойлгомжтой"),
    (r"хандалт\w*\s+өг",            "хандалт өгөх",       "use хандалт олгох"),
]

# SKILL.md default 6: foreign product names stay in Latin script.
CYRILLIC_BRANDS = [
    (r"кь?ю\s?-?пэй",       "QPay"),
    (r"сошиал\s?-?пэй",     "SocialPay"),
    (r"мон\s?-?пэй",        "MonPay"),
    (r"ард\s?-?пэй",        "ArdPay"),
    (r"опен\s?(аи|эй\s?ай)", "OpenAI"),
]

# SKILL.md default 2. Quoted speech is stripped before this check.
FIRST_PERSON = (r"(?<!\w)(би|бид|бидэн|бидний|биднийг|бидэнд|биднээс|бидэнтэй|манай|манайх|"
                r"манайхан|миний|надад|намайг|надаас|надтай)(?!\w)")

# SKILL.md default 5: colloquial -чих contractions.
COLLOQUIAL = r"\w+чих(сан|сэн|сон|сөн|лаа|лээ|лоо|лөө|на|нэ|но|нө|аад|ээд|оод|өөд)(?!\w)"

# GRAMMAR.md §3: -жээ only when the sentence attributes the claim to a source.
EVIDENTIAL = r"(?<!\w)\w+?(жээ|чээ)(?!\w)"
NOT_EVIDENTIAL = ("хэмжээ",)           # WORDS.md §5: арга хэмжээ is a noun
ATTRIBUTION = r"гэж|гэв|гэсэн|мэдээл|мэдэгд|дагуу|дүгнэлт|эх сурвалж"

TERMS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "terms.json")
SETTINGS = ("dev", "official")


def load_terms(path: str = TERMS_FILE) -> list:
    """terms.json: how Mongolian technical writing actually renders each English term."""
    try:
        return json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return []


def term_findings(i: int, line: str, setting: str, terms: list) -> list:
    out, low = [], line.lower()
    has_cyrillic = re.search(r"[а-яөүё]", low)
    prose = re.sub(r"`[^`]*`", " ", low)          # `code` is never prose
    for e in terms:
        want = e[setting]
        level = "ERROR" if e.get("status") == "confirmed" else "WARN"
        for bad in e.get("avoid") or []:
            if bad and re.search(rf"(?<!\w){re.escape(bad.lower())}", low):
                out.append((i, level, "term", bad,
                            f"{e['en']}: write {want['write']} ({setting})"))
        if want["group"] == "english" or not has_cyrillic:
            continue
        for en in e["en"].split("/"):
            m = re.search(rf"(?<![a-z]){re.escape(en.strip())}(?![a-z])", prose)
            if m:
                out.append((i, "WARN", "term", m.group(),
                            f"Mongolian {setting} text writes {want['write']} ({want['group']})"))
                break
    return out


QUOTED = r'"[^"]*"|“[^”]*”|„[^“”]*[“”]|«[^»]*»'


def strip_quotes(line: str) -> str:
    return re.sub(QUOTED, lambda m: " " * len(m.group()), line)


def scan_text(text: str, allow=(), setting: str = "dev", terms=None) -> list:
    """Return findings as (line, level, check, term, why). level is ERROR or WARN."""
    out = []
    lines = text.splitlines()
    terms = load_terms() if terms is None else terms
    for i, line in enumerate(lines, 1):
        out += term_findings(i, line, setting, terms)
        low = line.lower()
        bare = strip_quotes(low)
        for rx, term, why in CALQUES:
            if re.search(rx, low):
                out.append((i, "ERROR", "calque", term, why))
        for rx, name in CYRILLIC_BRANDS:
            m = re.search(rx, low)
            if m:
                out.append((i, "ERROR", "brand", m.group(), f"write {name} in Latin script"))
        for m in re.finditer(FIRST_PERSON, bare):
            out.append((i, "ERROR", "first-person", m.group(),
                        "no би/бид/манай; name the organization or write тус байгууллага"))
        for m in re.finditer(COLLOQUIAL, bare):
            out.append((i, "ERROR", "colloquial", m.group(), "spoken -чих form; drop it"))
        for sentence in re.split(r"(?<=[.!?])\s+", bare):
            if re.search(ATTRIBUTION, sentence):
                continue
            for m in re.finditer(EVIDENTIAL, sentence):
                if not m.group().startswith(NOT_EVIDENTIAL):
                    out.append((i, "WARN", "evidential", m.group(),
                                "-жээ with no cited source sounds secondhand; use -сан/-сэн "
                                "(ignore if it is a noun + reflexive -ээ, e.g. цээжээ)"))
        if "?" in bare:
            out.append((i, "WARN", "question", "?", "rhetorical questions are news voice"))
        m = re.search(r"[«»“”„]", line)
        if m:
            out.append((i, "WARN", "quotes", m.group(), 'the corpus uses straight " "'))
        m = re.search(r"(?<![А-ЯӨҮЁа-яөүё])[А-ЯӨҮЁ]\s+[А-ЯӨҮЁ][а-яөүё]{2,}", line)
        if m:
            out.append((i, "WARN", "initial", m.group(), "initial takes a period: Л.Оюун-Эрдэнэ"))

    # Whole-document consistency (GRAMMAR.md §6, WORDS.md §2c).
    def first_line(rx):
        for i, line in enumerate(lines, 1):
            if re.search(rx, line.lower()):
                return i
    comma = first_line(r"(?<![\d.,])\d{1,3}(,\d{3})+(?!\d)")
    space = first_line(r"(?<![\d.,])\d{1,3}([ \u00a0\u202f]\d{3})+(?![\d])")
    if comma and space:
        out.append((space, "ERROR", "numbers", "1,000 vs 1 000",
                    f"thousands separator is a comma on line {comma} and a space here; pick one"))
    pct, huvi = first_line(r"\d\s?%"), first_line(r"\d\s+хув[ьи]")
    if pct and huvi:
        out.append((huvi, "ERROR", "numbers", "% vs хувь",
                    f"percent is % on line {pct} and хувь here; pick one"))
    dash = first_line(r"хяналтын\s+самбар")
    board = first_line(r"(?<!хяналтын )самбар")
    if dash and board:
        out.append((board, "ERROR", "calque", "самбар",
                    f"самбар is the hardware board here but the dashboard on line {dash}; "
                    "call the dashboard нэгдсэн хяналтын дэлгэц"))

    return [f for f in out if f[2] not in allow and f[3] not in allow]


def api_key(payload: str) -> str:
    """API-Key = sha256(decimal sum of (codepoint+1) mod 10^10+8), per the site's bundle."""
    n, acc = 10**10 + 8, 0
    for ch in payload:
        acc = (acc + ord(ch) + 1) % n
    return hashlib.sha256(str(acc).encode()).hexdigest()


def fetch(word: str, direction: int = 1) -> dict:
    cache = {}
    if os.path.exists(CACHE):
        try:
            cache = json.load(open(CACHE, encoding="utf-8"))
        except Exception:
            cache = {}
    ck = f"{direction}:{word}"
    if ck in cache:
        return cache[ck]
    url = ("https://bolor-toli.com/pub/translate?word="
           + urllib.parse.quote(word) + f"&direction={direction}")
    req = urllib.request.Request(url, headers={
        "API-Key": api_key(f"{word}{direction}"), "User-Agent": UA,
        "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8"))
    cache[ck] = data
    try:
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    except OSError:
        pass                            # a lookup must not fail because the cache can't be saved
    return data


def senses(data: dict):
    """Yield (word, category, part-of-speech) for the far side of each entry."""
    to_mn = data.get("to_mn")
    for entry in data.get("er") or []:
        side = entry.get("w" if to_mn else "t") or {}
        for v in side.get("vars") or []:
            if v.get("acro") in ("mb",):      # traditional Mongolian script duplicate
                continue
            tags = v.get("tags") or {}
            yield v.get("w", ""), tags.get("category", ""), tags.get("class", "")


def report(word: str, direction: int) -> int:
    try:
        data = fetch(word, direction)
    except (urllib.error.URLError, OSError, ValueError) as e:
        print(f"{word}: lookup unavailable ({e}). Offline, or bolor-toli changed its API.\n"
              "--scan does not need the network and still works.")
        return 3
    rows, seen = [], set()
    for w, cat, cls in senses(data):
        if w and w not in seen:
            seen.add(w)
            rows.append((w, cat, cls))
    if not rows:
        print(f"{word}: no entry (check spelling, or it is not a dictionary word)")
        return 1
    side = "mn -> " if not data.get("to_mn") else "-> mn"
    print(f"{word}  [{side}, {data.get('er_cnt', len(rows))} entries]")
    for w, cat, cls in rows[:15]:
        tag = " ".join(t for t in (cat, cls) if t)
        print(f"  {w:<28}{tag}")
    print("\nAsk: is the sense you intend in this list? If not, the word is wrong.")
    return 0


def scan(path: str, allow=(), setting: str = "dev") -> int:
    findings = scan_text(open(path, encoding="utf-8").read(), allow, setting)
    for line, level, check, term, why in findings:
        print(f"{path}:{line}: {level} [{check}] {term} — {why}")
    errors = sum(1 for f in findings if f[1] == "ERROR")
    warns = len(findings) - errors
    print(f"\n{errors} error(s), {warns} warning(s)." if findings else "\nClean.")
    if warns:
        print("Warnings are heuristics: read each one; they do not fail the scan.")
    return 1 if errors else 0


def show_term(word: str) -> int:
    w = word.lower().strip()
    for e in load_terms():
        names = [n.strip() for n in e["en"].split("/")]
        if w in names or w in (e["dev"]["write"].lower(), e["official"]["write"].lower()):
            print(f"{e['en']}  [{e['status']}]")
            for s in SETTINGS:
                print(f"  {s:<9}{e[s]['write']}  ({e[s]['group']})")
            if e.get("avoid"):
                print(f"  avoid    {', '.join(e['avoid'])}")
            if e.get("note"):
                print(f"  note     {e['note']}")
            for ev in e.get("evidence") or []:
                print(f"  - {ev.get('url') or ev.get('source', '')}: {ev.get('quote', '')}")
            return 0
    print(f"{word}: not in terms.json. Look it up (bolor.py {word}) and check real usage.")
    return 1


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args[0] == "--scan":
        allow = [a.split("=", 1)[1] for a in args[2:] if a.startswith("--allow=")]
        setting = next((a.split("=", 1)[1] for a in args[2:] if a.startswith("--setting=")), "dev")
        if setting not in SETTINGS:
            print(f"--setting must be one of {', '.join(SETTINGS)}")
            return 2
        return scan(args[1], allow, setting)
    if args[0] == "--term":
        return show_term(" ".join(args[1:]))
    direction = 1
    if args[0] in ("-d", "--direction"):
        direction, args = int(args[1]), args[2:]
    return report(" ".join(args), direction)


if __name__ == "__main__":
    sys.exit(main())
