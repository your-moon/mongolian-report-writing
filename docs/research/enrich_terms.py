"""Add Microsoft Terminology renderings to terms.json, dropping any with zero CC-100 sentences.

Usage counts for competing words are hand-written patterns in layers.py; automatic stems
miscounted (see stem()).

Usage: python3 docs/research/enrich_terms.py MONGOLIAN.tbx ~/.cache/mongolian-terms/mn.txt.xz
A Microsoft rendering with zero corpus hits is recorded as dropped, not as evidence.
"""
import collections, html, json, lzma, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TERMS = os.path.join(ROOT, "terms.json")


def microsoft(tbx):
    t = open(tbx, encoding="utf-8").read()
    out = collections.defaultdict(list)
    for e in re.findall(r"<termEntry.*?</termEntry>", t, re.S):
        langs = {l.lower()[:2]: [html.unescape(x) for x in re.findall(r'<term id="\d+">(.*?)</term>', b)]
                 for l, b in re.findall(r'<langSet xml:lang="([^"]+)">(.*?)</langSet>', e, re.S)}
        for en in langs.get("en", []):
            for mn in langs.get("mn", []):
                if mn.lower() not in out[en.lower()]:
                    out[en.lower()].append(mn.lower())
    return out


def stem(phrase):
    """Exact phrase; only the last word's ending may vary (last 2 letters free).

    Looser stems overcounted badly: "гац" for гацах matched 12,831 sentences against 250
    hand-checked, and хамгаалалттай гарц matched unrelated хамгаалалт... гар... text.
    """
    words = phrase.lower().split()
    last = words[-1] if len(words[-1]) <= 3 else words[-1][:max(3, len(words[-1]) - 2)]
    return r"\s+".join(map(re.escape, words[:-1] + [last]))


def count(corpus, phrases):
    """One combined regex per line; 200 separate searches took 20+ min over 15M lines."""
    keys = {}
    for p in phrases:
        keys.setdefault(stem(p), []).append(p)
    big = re.compile(r"(?<![а-яөүёa-z])(?:" + "|".join(sorted(keys, key=len, reverse=True)) + ")")
    exact = [(re.compile(k), ps) for k, ps in keys.items()]
    n = collections.Counter()
    with lzma.open(corpus, "rt", encoding="utf-8", errors="ignore") as f:
        for line in f:
            hits = {m.group() for m in big.finditer(line.lower())}
            if not hits:
                continue
            for r, ps in exact:
                if any(r.match(h) for h in hits):
                    for p in ps:
                        n[p] += 1
    return n


def main(tbx, corpus):
    terms = json.load(open(TERMS, encoding="utf-8"))
    ms = microsoft(tbx)
    per_term = {}
    phrases = set()
    for e in terms:
        names = [x.strip().lower() for x in e["en"].split("/")]
        cands = [c for n in names for c in ms.get(n, [])]
        per_term[e["en"]] = cands
        phrases |= set(cands) | {e["dev"]["write"].lower(), e["official"]["write"].lower()}
    phrases = {p for p in phrases if re.search(r"[а-яөүё]", p)}
    n = count(corpus, phrases)
    for e in terms:
        ev = [x for x in e.get("evidence") or [] if x.get("source") not in ("microsoft", "cc-100")]
        for c in per_term[e["en"]]:
            if n[c] or not re.search(r"[а-яөүё]", c):   # Latin forms are not counted
                ev.append({"source": "microsoft", "quote": f"{e['en']} -> {c}"})
            else:
                ev.append({"source": "microsoft", "quote": f"{e['en']} -> {c} (dropped: 0 CC-100 sentences)"})
        e["evidence"] = ev
    json.dump(terms, open(TERMS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(terms)} terms enriched; {sum(1 for c in phrases if n[c] == 0)} phrases with zero hits")


if __name__ == "__main__":
    main(*sys.argv[1:3])
