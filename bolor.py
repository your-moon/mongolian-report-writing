#!/usr/bin/env python3
"""bolor-toli.com lookup — check what a Mongolian word actually means before using it.

Why this exists: WORDS.md documents 28 measured calques. All of them were produced by a
model that had already read the rule telling it not to. The rule needs a fact it does not
have — what the Mongolian word means to a Mongolian reader. This fetches that fact.

Usage:
    bolor.py үйлдвэрлэл            # mn -> en: what does this word actually say?
    bolor.py production            # en -> mn: which words are on offer?
    bolor.py --scan draft.md       # flag every blocklisted calque in a draft
    bolor.py -d 8 үйлдвэрлэл       # другое направление (8=ru, 3=de, 5=jp, 7=cn, 4=kr)

Endpoint is undocumented and same-origin to the site. Keep the volume at human pace —
one word at a time, results cached in ~/.cache/bolor-toli.json. Do not bulk-scrape it.
"""
import hashlib, json, os, re, sys, urllib.parse, urllib.request

CACHE = os.path.expanduser("~/.cache/bolor-toli.json")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"

# Measured calques from WORDS.md §2a-2e. Each shipped in a real document.
BLOCKLIST = [
    ("хаалга",        "door — use холболт for a connection"),
    ("давалгаа",      "ocean wave — use үе шаттайгаар for staged rollout"),
    ("чимээгүй",      "silent (sound) — use тогтмол; NB чимээгүйхэн олгох is correct"),
    ("дотор орох",    "climbing inside — use системд нэвтрэх"),
    ("санах ой",      "computer RAM — not human memory"),
    ("флот",          "naval fleet — use нийт машин"),
    ("дахин асаах",   "flip the power on — reboot is дахин ачаалах"),
    ("дундаа уулз",   "people meeting in person"),
    ("үйлдвэрлэлийн", "factory manufacturing — prod is not үйлдвэрлэл"),
    ("тайлагдсан",    "deciphered — use тодорхой"),
    ("зам хоног",     "not a phrase — use замын зардал, цаг хугацаа"),
]


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
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
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
    data = fetch(word, direction)
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


def scan(path: str) -> int:
    text = open(path, encoding="utf-8").read()
    hits = 0
    for i, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        for term, why in BLOCKLIST:
            if term in low:
                if term == "чимээгүй" and "чимээгүйхэн" in low:
                    continue
                print(f"{path}:{i}: {term} — {why}")
                hits += 1
    print(f"\n{hits} blocked word(s)." if hits else "\nNo blocklisted calques.")
    return 1 if hits else 0


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    if args[0] == "--scan":
        return scan(args[1])
    direction = 1
    if args[0] in ("-d", "--direction"):
        direction, args = int(args[1]), args[2:]
    return report(" ".join(args), direction)


if __name__ == "__main__":
    sys.exit(main())
