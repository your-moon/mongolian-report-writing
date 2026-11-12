#!/usr/bin/env python3
"""EXPERIMENT. It failed its evaluation (5/12 held-out confirmed terms): use it for example
sentences when reviewing a term, never to choose one. See docs/research/term-picker-eval.md.

pick_terms.py - choose how Mongolian text renders each English software term, from data.

    pick_terms.py download          # corpora -> ~/.cache/mongolian-terms/ (parallel ranged, resumable)
    pick_terms.py index             # mine candidates + count signals -> ~/.cache/mongolian-terms/index.json
    pick_terms.py pick              # docs/research/term-picks.{json,md}   (--blind: ignore terms.json renderings)
    pick_terms.py eval              # docs/research/term-picker-eval.md    (tunes weights on half A only)

Signals per candidate (reported separately, never merged into one opaque score in the output):
  ui    association (Dice) in software-UI translations (translatewiki, GNOME, Ubuntu)
  web   association (Dice) in OPUS CCAligned web pairs
  corpus  frequency in CC-100 sentences that carry a technology anchor word, and its share of all uses
  sense bolor-toli mn->en senses for the top candidates (bolor.fetch / bolor.senses, cached, 2 s apart)
  collision  the same rendering is the pick for two terms
Python 3 stdlib only. Mongolian is agglutinative, so candidates are keyed on a 5-letter stem per word.
"""
import argparse, collections, concurrent.futures as cf, json, lzma, math, multiprocessing as mp
import os, re, sys, threading, time, urllib.request, zipfile

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # repo root
sys.path.insert(0, HERE)
CACHE = os.path.expanduser("~/.cache/mongolian-terms")
INDEX = os.path.join(CACHE, "index.json")
OUT = os.path.join(HERE, "docs", "research")
PARAMS = os.path.join(OUT, "term-picker-params.json")
STEM = 5

SOURCES = [  # name, url, kind
    ("OPUS-translatewiki", "https://object.pouta.csc.fi/OPUS-translatewiki/v2026-07-01/moses/en-mn.txt.zip", "ui"),
    ("OPUS-GNOME", "https://object.pouta.csc.fi/OPUS-GNOME/v1/moses/en-mn.txt.zip", "ui"),
    ("OPUS-Ubuntu", "https://object.pouta.csc.fi/OPUS-Ubuntu/v14.10/moses/en-mn.txt.zip", "ui"),
    ("OPUS-CCAligned", "https://object.pouta.csc.fi/OPUS-CCAligned/v1/moses/en-mn.txt.zip", "web"),
    ("mn.txt", "https://data.statmt.org/cc-100/mn.txt.xz", "cc100"),
]
ANCHOR = re.compile(r"^(?:сервер|систем|программ|програм|интернэт|интернет|компьютер|вэб|өгөгдөл|файл"
                    r"|аппликэйш|апп(?:ы|д|ын|аас|аар|тай|уу)?$)")
DEFAULT = {"w_ui": 1.0, "w_web": 1.0, "w_corp": 0.0, "tau_ui": 0.2, "tau_web": 0.1, "margin": 1.3,
           "min_ui": 1, "min_web": 2}


# ------------------------------------------------------------------ download
def _ranged(url, dest, workers=24, chunk=4 << 20):
    total = int(urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30)
                .headers["Content-Length"])
    if os.path.exists(dest) and os.path.getsize(dest) == total:
        return f"{os.path.basename(dest)}: have {total} bytes"
    part, state = dest + ".part", dest + ".state"
    done = set(json.load(open(state))) if os.path.exists(state) and os.path.exists(part) else set()
    fd = os.open(part, os.O_RDWR | os.O_CREAT)
    os.ftruncate(fd, total)
    lock = threading.Lock()

    def get(i):
        a, b = i * chunk, min(total, (i + 1) * chunk) - 1
        for attempt in range(5):
            try:
                req = urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}"})
                data = urllib.request.urlopen(req, timeout=60).read()
                if len(data) == b - a + 1:
                    os.pwrite(fd, data, a)
                    with lock:
                        done.add(i)
                        if len(done) % 8 == 0:
                            json.dump(sorted(done), open(state, "w"))
                    return
            except Exception:
                time.sleep(1 + attempt)
        raise RuntimeError(f"chunk {i} of {url} failed")

    todo = [i for i in range((total + chunk - 1) // chunk) if i not in done]
    with cf.ThreadPoolExecutor(workers) as ex:
        list(ex.map(get, todo))
    os.close(fd)
    os.replace(part, dest)
    if os.path.exists(state):
        os.remove(state)
    return f"{os.path.basename(dest)}: {total} bytes"


def cmd_download(a):
    os.makedirs(CACHE, exist_ok=True)
    for name, url, kind in SOURCES:
        if a.only and a.only != name:
            continue
        t = time.time()
        dest = os.path.join(CACHE, name + (".xz" if kind == "cc100" else ".zip"))
        print(_ranged(url, dest), f"({time.time() - t:.0f} s)", flush=True)
        if kind != "cc100":
            d = os.path.join(CACHE, "raw", name)
            if not os.path.isdir(d):
                zipfile.ZipFile(dest).extractall(d)


# ------------------------------------------------------------------ text helpers
TOK = re.compile(r"[а-яёөү]+|[a-z]+")
CLAUSE = re.compile(r"[.,;:!?()\[\]{}\"«»…|/\\–—\n]+")


def clauses(text):
    """Lowercased word lists, one per clause, so n-grams never cross punctuation."""
    return [w for w in (TOK.findall(c) for c in CLAUSE.split(text.lower())) if w]


def stem(w):
    return "l:" + w if "a" <= w[0] <= "z" else w[:STEM]


def ngrams(cl, latin, nmax=3):
    """Yield (stem-tuple, surface-tuple). Latin words only as unigrams equal to a term word."""
    for ws in cl:
        st = [stem(w) for w in ws]
        for i in range(len(ws)):
            for n in range(1, nmax + 1):
                if i + n > len(ws):
                    break
                g = st[i:i + n]
                if any(s[0] == "l" and s[1] == ":" for s in g):
                    if n == 1 and ws[i] in latin:
                        yield tuple(g), tuple(ws[i:i + 1])
                    break
                yield tuple(g), tuple(ws[i:i + n])


def key_s(k):
    return " ".join(k)


def term_words(en):
    return [w for w in re.split(r"[/\s]+", en.lower()) if w]


def variants(w):
    v = {w, w + "s", w + "es", w + "ed", w + "d", w + "ing", w + w[-1] + "ed", w + w[-1] + "ing"}
    if w.endswith("e"):
        v.add(w[:-1] + "ing")
    if w.endswith("s") and len(w) > 4:
        v.add(w[:-1])
    return v


def load_terms():
    return json.load(open(os.path.join(HERE, "terms.json"), encoding="utf-8"))


def renderings(t):
    out = {}
    for side in ("dev", "official"):
        w = t[side]["write"]
        out[w] = side
    return out  # write -> side (last wins; only used to seed candidates)


def read_pairs(name):
    d = os.path.join(CACHE, "raw", name)
    en = [f for f in os.listdir(d) if f.endswith(".en")][0]
    mn = en[:-3] + ".mn"
    with open(os.path.join(d, en), encoding="utf-8", errors="replace") as fe, \
            open(os.path.join(d, mn), encoding="utf-8", errors="replace") as fm:
        for e, m in zip(fe, fm):
            yield e.rstrip("\n"), m.rstrip("\n")


# ------------------------------------------------------------------ index
def cmd_index(a):
    t0 = time.time()
    terms = load_terms()
    ens = [t["en"] for t in terms]
    var2t = collections.defaultdict(set)
    latin = set()
    for i, t in enumerate(terms):
        for w in term_words(t["en"]):
            latin.add(w)
            for v in variants(w):
                var2t[v].add(i)
    forced = collections.defaultdict(dict)  # term idx -> key -> tag
    for i, t in enumerate(terms):
        for w, side in renderings(t).items():
            cl = clauses(w)
            if len(cl) == 1 and cl[0] and "l:" not in key_s(tuple(stem(x) for x in cl[0])):
                forced[i][tuple(stem(x) for x in cl[0])] = "rendering"
        for w in term_words(t["en"]):
            forced[i][("l:" + w,)] = "latin"

    corp = {"ui": ["OPUS-translatewiki", "OPUS-GNOME", "OPUS-Ubuntu"], "web": ["OPUS-CCAligned"]}
    data = {}
    for kind, names in corp.items():
        # pass A: aligned pairs + cooccurrence
        aligned, n_pairs = [], 0
        c_t = collections.Counter()
        cooc = collections.defaultdict(collections.Counter)
        for name in names:
            for e, m in read_pairs(name):
                n_pairs += 1
                hit = set()
                for w in re.findall(r"[a-z]+", e.lower()):
                    if w in var2t:
                        hit |= var2t[w]
                if not hit:
                    continue
                cl = clauses(m)
                grams = {g for g, _ in ngrams(cl, latin)}
                aligned.append((e, m, cl, grams, hit))
                for i in hit:
                    c_t[i] += 1
                    cooc[i].update(grams)
        print(f"{kind}: {n_pairs} pairs, {len(aligned)} aligned, passA {time.time() - t0:.0f} s", flush=True)
        minc = DEFAULT["min_" + kind]
        sel = collections.defaultdict(dict)  # term -> key -> tag
        for i, cnt in cooc.items():
            for g, c in cnt.items():
                if c < minc or (g[0][:2] == "l:" and len(g) == 1 and g[0][2:] not in term_words(ens[i])):
                    continue
                if 2 * c / (c_t[i] + c) < 0.04:
                    continue
                sel[i][g] = "mined"
        # pass B: global document frequency of every key we may score
        want = set()
        for i in sel:
            want |= set(sel[i])
        for i in forced:
            want |= set(forced[i])
        c_g, surf = collections.Counter(), collections.defaultdict(collections.Counter)
        for name in names:
            for e, m in read_pairs(name):
                seen = set()
                for g, s in ngrams(clauses(m), latin):
                    if g in want:
                        surf[g][s] += 1
                        seen.add(g)
                c_g.update(seen)
        # forced keys (may be longer than 3 words): direct scan in aligned pairs
        data[kind] = dict(aligned=aligned, c_t=c_t, cooc=cooc, c_g=c_g, surf=surf, n_pairs=n_pairs, sel=sel)
        print(f"{kind}: passB {time.time() - t0:.0f} s", flush=True)

    # assemble per-term candidates
    def dice(kind, i, g):
        D = data[kind]
        co = D["cooc"][i].get(g, 0)
        return co, D["c_g"].get(g, 0), (2 * co / (D["c_t"][i] + D["c_g"].get(g, 0)) if co else 0.0)

    def suppress(cands, kind, i):
        """Rank by Dice, drop contiguous sub/super n-grams of an already kept better one."""
        ranked = sorted(cands, key=lambda g: (-dice(kind, i, g)[2], -len(g)))
        kept = []
        for g in ranked:
            rel = False
            for k in kept:
                s, l = (g, k) if len(g) <= len(k) else (k, g)
                if any(l[j:j + len(s)] == s for j in range(len(l) - len(s) + 1)):
                    rel = True
                    break
            if not rel:
                kept.append(g)
        return kept

    out = {"terms": {}, "meta": {}}
    cc_keys = set()
    for i, t in enumerate(terms):
        cand = {}
        for kind in ("ui", "web"):
            D = data[kind]
            pool = [g for g in D["sel"].get(i, {}) if g[0][:2] != "l:" or True]
            for g in suppress(pool, kind, i)[:12]:
                cand[g] = "mined"
        for g, tag in forced[i].items():
            cand.setdefault(g, tag)
            if cand[g] == "mined" and tag == "rendering":
                cand[g] = "mined+rendering"
        rec = {"c_t": {k: int(data[k]["c_t"].get(i, 0)) for k in ("ui", "web")}, "cands": {}}
        for g, tag in cand.items():
            c = {"tag": tag, "len": len(g)}
            for kind in ("ui", "web"):
                D = data[kind]
                co = D["cooc"][i].get(g, 0)
                if co == 0 and len(g) > 3:  # forced long rendering: direct scan
                    co = sum(1 for (_, _, cl, _, hit) in D["aligned"] if i in hit and _contains(cl, g))
                cg = D["c_g"].get(g, 0)
                c[kind] = {"cooc": co, "c_g": cg, "dice": round(2 * co / (D["c_t"][i] + cg), 5) if co else 0.0}
            allsurf = collections.Counter()
            for kind in ("ui", "web"):
                allsurf.update(data[kind]["surf"].get(g, {}))
            if allsurf:
                # most common form, but prefer the shortest form of the same length-in-words that is at least a
                # fifth as common: the bare stem (сүлжээ) is what bolor-toli knows, not сүлжээний
                top = allsurf.most_common(1)[0]
                near = [sf for sf, n in allsurf.items() if len(sf) == len(top[0]) and n >= 0.2 * top[1]]
                c["surface"] = " ".join(min(near, key=lambda sf: sum(map(len, sf))))
            else:
                c["surface"] = key_s(g)
            c["ex"] = {}
            for kind in ("ui", "web"):
                rows = [(len(e) + len(m), e, m) for (e, m, cl, grams, hit) in data[kind]["aligned"]
                        if i in hit and (g in grams or (len(g) > 3 and _contains(cl, g))) and len(e) > 12]
                rows.sort()
                c["ex"][kind] = [[e, m] for _, e, m in rows[:2]]
            rec["cands"][key_s(g)] = c
            cc_keys.add(g)
        out["terms"][t["en"]] = rec

    # CC-100
    xz = os.path.join(CACHE, "mn.txt.xz")
    if a.skip_cc:
        out["meta"]["cc100"] = {"sentences": 1, "tech_sentences": 0, "lines_read": 0, "truncated": False,
                                "seconds": 0, "counts": {}}
    else:
        out["meta"]["cc100"] = cc100_count(xz, cc_keys, latin, a.cc_limit)
    for rec in out["terms"].values():
        for k, c in rec["cands"].items():
            c["corpus"] = out["meta"]["cc100"]["counts"].get(k, [0, 0])
    out["meta"].update(n_pairs={k: data[k]["n_pairs"] for k in data}, aligned={k: len(data[k]["aligned"]) for k in data},
                       stem=STEM, built=time.strftime("%Y-%m-%d"), seconds=round(time.time() - t0))
    json.dump(out, open(INDEX, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"index written {INDEX} in {time.time() - t0:.0f} s")


def _contains(cl, g):
    for ws in cl:
        st = [stem(w) for w in ws]
        for i in range(len(st) - len(g) + 1):
            if tuple(st[i:i + len(g)]) == g:
                return True
    return False


# ---- CC-100 pass (multiprocess, streaming)
_G = {}


def _init(keys, latin):
    first = collections.defaultdict(list)
    for k in keys:
        first[k[0]].append(k)
    _G["first"], _G["latin"] = first, latin


def _work(lines):
    first, latin = _G["first"], _G["latin"]
    tech, allc, n, nt = collections.Counter(), collections.Counter(), 0, 0
    for line in lines:
        cl = clauses(line)
        if not cl:
            continue
        n += 1
        # anchor positions as (clause, index)
        anc = {(ci, wi) for ci, ws in enumerate(cl) for wi, w in enumerate(ws) if ANCHOR.match(w)}
        if anc:
            nt += 1
        for ci, ws in enumerate(cl):
            st = [stem(w) for w in ws]
            seen = {}
            for i, s in enumerate(st):
                for k in first.get(s, ()):
                    if tuple(st[i:i + len(k)]) == k:
                        cover = {(ci, j) for j in range(i, i + len(k))}
                        is_t = bool(anc - cover)
                        seen[k] = seen.get(k, False) or is_t
            for k, is_t in seen.items():
                allc[k] += 1
                if is_t:
                    tech[k] += 1
    return tech, allc, n, nt


def cc100_count(path, keys, latin, limit_mb):
    t = time.time()
    tech, allc, n, nt, lines_read = collections.Counter(), collections.Counter(), 0, 0, 0
    truncated = False
    with mp.Pool(max(2, (os.cpu_count() or 4) - 1), _init, (keys, latin)) as pool:
        def batches():
            nonlocal truncated, lines_read
            f = lzma.open(path, "rt", encoding="utf-8", errors="replace")
            buf = []
            try:
                for line in f:
                    lines_read += 1
                    buf.append(line)
                    if len(buf) >= 4000:
                        yield buf
                        buf = []
                        if limit_mb and lines_read * 120 > limit_mb * 1e6:
                            return
            except (lzma.LZMAError, EOFError):
                truncated = True
            if buf:
                yield buf
        for tc, ac, nn, tt in pool.imap_unordered(_work, batches(), chunksize=1):
            tech.update(tc), allc.update(ac)
            n += nn
            nt += tt
    counts = {key_s(k): [tech[k], allc[k]] for k in keys}
    return {"sentences": n, "tech_sentences": nt, "lines_read": lines_read, "truncated": truncated,
            "seconds": round(time.time() - t), "counts": counts}


# ------------------------------------------------------------------ picking
def params():
    p = dict(DEFAULT)
    if os.path.exists(PARAMS):
        p.update(json.load(open(PARAMS))["params"])
    return p


def load_index():
    return json.load(open(INDEX, encoding="utf-8"))


def score_term(rec, base_share, p, blind=False):
    rows = []
    for k, c in rec["cands"].items():
        if blind and "mined" not in c["tag"]:
            continue
        if blind and c["tag"] == "latin":
            continue
        ui = c["ui"]["dice"] if c["ui"]["cooc"] >= p["min_ui"] else 0.0
        web = c["web"]["dice"] if c["web"]["cooc"] >= p["min_web"] else 0.0
        tech, allc = c["corpus"]
        share = tech / allc if allc else 0.0
        corp = share * min(1.0, math.log10(1 + tech) / 4)
        s = p["w_ui"] * ui + p["w_web"] * web + p["w_corp"] * corp
        rows.append(dict(key=k, surface=c["surface"].replace("l:", ""), tag=c["tag"], score=s, ui=ui, web=web, ui_cooc=c["ui"]["cooc"],
                         web_cooc=c["web"]["cooc"], tech=tech, all=allc, share=share,
                         lift=(share / base_share if base_share else 0.0), len=c["len"], ex=c["ex"]))
    rows.sort(key=lambda r: (-r["score"], -r["len"]))
    return rows


def top_of(rows, f):
    r = sorted([x for x in rows if x[f] > 0], key=lambda x: (-x[f], -x["len"]))
    return r


def decide_signals(rows, p):
    """Agreement part of the decision (no sense, no collision)."""
    if not rows or rows[0]["score"] <= 0:
        return "review", "no data"
    tu, tw = top_of(rows, "ui"), top_of(rows, "web")

    def decisive(lst, f, tau):
        return lst and lst[0][f] >= tau and (len(lst) == 1 or lst[0][f] >= p["margin"] * lst[1][f])
    pick = rows[0]["key"]
    if tu and tw:
        if tu[0]["key"] == tw[0]["key"] == pick:
            return "auto", "ui and web agree"
        return "review", f"ui top {tu[0]['surface']} vs web top {tw[0]['surface']}"
    if tw and not tu:
        return ("auto", "web only, decisive") if decisive(tw, "web", p["tau_web"]) and tw[0]["key"] == pick \
            else ("review", "web only, not decisive")
    if tu and not tw:
        return ("auto", "ui only, decisive") if decisive(tu, "ui", p["tau_ui"]) and tu[0]["key"] == pick \
            else ("review", "ui only, not decisive")
    return "review", "pick has no ui or web support"


def words_match(a, b):
    """Same Mongolian word up to inflection: one is a prefix of the other with a suffix of at most 3 letters, or they share all but 1 letter
    of the shorter one (шинэчлэл / шинэчлэгдсэн). The 5-letter index stem is NOT used here: it conflates
    хэрэглэгч with хэрэгсэл."""
    if a == b:
        return True
    s, l = sorted((a, b), key=len)
    if len(s) >= 4 and l.startswith(s) and len(l) - len(s) <= 3:
        return True
    cp = 0
    while cp < len(s) and s[cp] == l[cp]:
        cp += 1
    return cp >= 6 and cp >= len(s) - 1


def _ws(s):
    return [w for cl in clauses(s) for w in cl]


def _eq(x, y):
    return len(x) == len(y) and all(words_match(p, q) for p, q in zip(x, y))


def _sub(s, l):
    return any(_eq(s, l[j:j + len(s)]) for j in range(len(l) - len(s) + 1))


def agrees(surface, term, side="official"):
    """(strict, lenient). strict: same words; lenient: pick is a contiguous part of the reference, or contains it."""
    if not surface:
        return False, False
    pk, ref = _ws(surface), _ws(term[side]["write"])
    strict = _eq(pk, ref)
    return strict, strict or _sub(pk, ref) or _sub(ref, pk)


# ---- sense
def sense_check(surface, en):
    import bolor
    key = surface
    if surface.isascii():
        return {"status": "n/a", "note": "Latin form", "senses": []}
    last = getattr(sense_check, "_last", 0)
    cached = os.path.exists(bolor.CACHE) and f"1:{key}" in json.load(open(bolor.CACHE, encoding="utf-8"))
    if not cached:
        wait = 2.0 - (time.time() - last)
        if wait > 0:
            time.sleep(wait)
    try:
        d = bolor.fetch(key)
    except Exception as e:
        return {"status": "error", "note": str(e)[:60], "senses": []}
    finally:
        sense_check._last = time.time()
    rows, seen = [], set()
    for w, cat, cls in bolor.senses(d):
        if w and w not in seen:
            seen.add(w)
            rows.append((w, cat, cls))
    if not rows:
        return {"status": "none", "note": "no bolor-toli entry", "senses": []}
    words = set(term_words(en)) | {v for w in term_words(en) for v in variants(w)}
    tech = [r for r in rows if re.search(r"comp|tech", r[1].lower())]
    match = [r for r in rows if set(re.findall(r"[a-z]+", r[0].lower())) & words]
    first = rows[0]
    if match or tech:
        st = "pass"
    elif not re.search(r"comp|tech", first[1].lower()):
        st = "flag"
    else:
        st = "pass"
    note = ("matches term" if match else "") + (" tech tag" if tech else "")
    if st == "flag":
        note = f"first sense '{first[0]}' non-technical"
    return {"status": st, "note": note.strip(), "senses": [f"{w} ({cat})" if cat else w for w, cat, _ in rows[:4]]}


def run_picks(terms, idx, p, blind=False, sense=True, nsense=5):
    base = idx["meta"]["cc100"]["tech_sentences"] / max(1, idx["meta"]["cc100"]["sentences"])
    res = {}
    for t in terms:
        rec = idx["terms"][t["en"]]
        rows = score_term(rec, base, p, blind)
        dec, why = decide_signals(rows, p)
        e = dict(en=t["en"], rows=rows, signal_decision=dec, why=why, pick=rows[0]["key"] if rows and rows[0]["score"] > 0 else None)
        res[t["en"]] = e
    # collisions on picks
    owners = collections.defaultdict(list)
    for en, e in res.items():
        if e["pick"]:
            owners[e["pick"]].append(en)
    for en, e in res.items():
        e["collision"] = [o for o in owners.get(e["pick"], []) if o != en] if e["pick"] else []
    if sense:
        for t in terms:
            e = res[t["en"]]
            e["sense"] = {}
            for r in e["rows"][:nsense]:
                e["sense"][r["key"]] = sense_check(r["surface"], t["en"])
    for en, e in res.items():
        d, why = e["signal_decision"], e["why"]
        if e["pick"] and sense:
            s = e["sense"].get(e["pick"], {"status": "none"})
            if s["status"] not in ("pass", "n/a"):
                d, why = "review", f"sense {s['status']}: {s.get('note', '')}"
        if e["collision"]:
            d, why = "review", f"collision with {', '.join(e['collision'])}"
        e["decision"], e["decision_why"] = d, why
    return res


def cmd_pick(a):
    terms, idx, p = load_terms(), load_index(), params()
    res = run_picks(terms, idx, p, blind=a.blind)
    os.makedirs(OUT, exist_ok=True)
    js, md = [], []
    cc = idx["meta"]["cc100"]
    md.append("# Term picks from data\n")
    md.append(f"Generated by `python3 pick_terms.py pick` from index built {idx['meta']['built']}. "
              f"Params: `{json.dumps(p)}`. CC-100: {cc['sentences']} sentences read, "
              f"{cc['tech_sentences']} with a technology anchor ({100 * cc['tech_sentences'] / max(1, cc['sentences']):.1f}%)"
              f"{', file truncated' if cc['truncated'] else ''}.\n")
    md.append("The data is mostly customer/official register (web pages, UI strings, news), so compare "
              "the pick with the **official** column. Signals: ui/web = Dice association (n pairs), "
              "corpus = tech sentences / all sentences (share, lift over the all-sentence tech rate).\n")
    md.append("| term | official now | pick | decision | top 3 candidates: ui / web / corpus | why |")
    md.append("|---|---|---|---|---|---|")
    ex_lines = []
    for t in terms:
        e = res[t["en"]]
        top3 = e["rows"][:3]
        cell = "<br>".join(
            f"**{r['surface']}** ui {r['ui']:.2f} ({r['ui_cooc']}) / web {r['web']:.2f} ({r['web_cooc']}) / "
            f"corp {r['tech']}/{r['all']} ({r['share']:.0%}, lift {r['lift']:.1f}x)" for r in top3) or "no data"
        pick = next((r["surface"] for r in e["rows"] if r["key"] == e["pick"]), "-")
        md.append(f"| {t['en']} | {t['official']['write']} | {pick} | {e['decision']} | {cell} | {e['decision_why']} |")
        top = e["rows"][0] if e["pick"] else None
        if top:
            exs = (top["ex"]["ui"][:1] + top["ex"]["web"][:1])[:2]
            for en_s, mn_s in exs:
                ex_lines.append(f"- **{t['en']}** -> {pick}: {en_s[:140]} / {mn_s[:160]}")
        js.append(dict(term=t["en"], status=t["status"], official=t["official"]["write"], dev=t["dev"]["write"],
                       pick=pick if e["pick"] else None, decision=e["decision"], why=e["decision_why"],
                       collision=e["collision"], top=[{k: r[k] for k in ("surface", "ui", "ui_cooc", "web", "web_cooc",
                                                                        "tech", "all", "share", "lift", "tag")}
                                                      for r in top3],
                       sense={k: v for k, v in (e.get("sense") or {}).items() if k in [r["key"] for r in top3]},
                       examples=(top["ex"] if top else {})))
    md.append("\n## Example sentence pairs for each pick\n")
    md += ex_lines
    json.dump(js, open(os.path.join(OUT, "term-picks.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(OUT, "term-picks.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(collections.Counter(x["decision"] for x in js))


# ------------------------------------------------------------------ eval
def halves(terms):
    conf = sorted([t for t in terms if t["status"] == "confirmed"], key=lambda t: t["en"].lower())
    return conf[0::2], conf[1::2]


def agreement(terms, idx, p, blind):
    res = run_picks(terms, idx, p, blind=blind, sense=False)
    s = l = d = 0
    rows = []
    for t in terms:
        e = res[t["en"]]
        surf = next((r["surface"] for r in e["rows"] if r["key"] == e["pick"]), None)
        st, le = agrees(surf, t)
        s += st
        l += le
        d += agrees(surf, t, "dev")[0]
        rows.append((t, e, st, le))
    return s, l, d, rows, res


def cmd_eval(a):
    import itertools
    terms, idx = load_terms(), load_index()
    A, B = halves(terms)
    grid = dict(w_ui=[0.0, 0.5, 1.0, 2.0], w_web=[0.5, 1.0, 2.0], w_corp=[0.0, 0.25, 0.5, 1.0],
                min_ui=[1, 2, 3, 5], min_web=[2, 3, 5])
    best = None
    t0 = time.time()
    for wu, ww, wc, mu, mw in itertools.product(grid["w_ui"], grid["w_web"], grid["w_corp"],
                                                grid["min_ui"], grid["min_web"]):
        p = dict(DEFAULT, w_ui=wu, w_web=ww, w_corp=wc, min_ui=mu, min_web=mw)
        s, l, _, _, _ = agreement(A, idx, p, True)
        key = (s, l, -abs(wu - 1) - abs(ww - 1) - abs(wc) - 0.01 * (mu + mw))
        if best is None or key > best[0]:
            best = (key, p)
    p = best[1]
    # decision thresholds: tuned on A for auto-precision, then coverage
    bt = None
    for tu, tw, mg in itertools.product([0.1, 0.2, 0.3], [0.05, 0.1, 0.2], [1.0, 1.3, 2.0]):
        q = dict(p, tau_ui=tu, tau_web=tw, margin=mg)
        _, _, _, rows, res = agreement(A, idx, q, True)
        auto = [(st, le) for (t, e, st, le) in rows if e["signal_decision"] == "auto"]
        good = sum(le for st, le in auto)
        bad = len(auto) - good
        key = (good - 2 * bad, good)
        if bt is None or key > bt[0]:
            bt = (key, q)
    p = bt[1]
    os.makedirs(OUT, exist_ok=True)
    json.dump({"params": p, "tuned_on": [t["en"] for t in A], "grid": grid}, open(PARAMS, "w"), indent=1)
    out = []
    cmdline = "python3 pick_terms.py eval"
    out.append("# Term picker evaluation\n")
    out.append(f"Produced by `{cmdline}` (index built {idx['meta']['built']}; tuning took {time.time() - t0:.0f} s). "
               "Every number below is printed by that command.\n")
    out.append("## Setup\n")
    out.append(f"- 24 confirmed terms sorted alphabetically (case-insensitive) and split by alternating position: "
               f"half A = positions 0,2,4,..; half B = 1,3,5,... A: {', '.join(t['en'] for t in A)}. "
               f"B: {', '.join(t['en'] for t in B)}.")
    out.append(f"- Weights and thresholds were tuned on **A only** (grid in `{os.path.relpath(PARAMS, HERE)}`): `{json.dumps(p)}`. "
               "B was not looked at during tuning.")
    out.append("- Truth is `terms.json` **official** write. *strict* = same words as the official rendering, up to inflection (`words_match`); "
               "*lenient* = pick is a contiguous sub/super n-gram of it (e.g. `татаж` for `татаж авах`).")
    out.append("- **Blind** = candidates come only from mining (terms.json renderings and the Latin form are not allowed to compete); "
               "this is the honest test, because seeding the answer into the pool is circular. **Seeded** = the production mode.\n")
    for mode, blind in (("Blind (mined only)", True), ("Seeded (production)", False)):
        out.append(f"## {mode}\n")
        out.append("| set | strict | lenient | matches dev column |")
        out.append("|---|---|---|---|")
        for nm, T in (("Half B (held out)", B), ("Half A (tuned)", A), ("All 24", A + B)):
            s, l, d, _, _ = agreement(T, idx, p, blind)
            out.append(f"| {nm} | {s}/{len(T)} | {l}/{len(T)} | {d}/{len(T)} |")
        out.append("")
        # auto precision
        for nm, T in (("B", B), ("A", A)):
            _, _, _, rows, _ = agreement(T, idx, p, blind)
            auto = [r for r in rows if r[1]["signal_decision"] == "auto"]
            out.append(f"- half {nm}: {len(auto)} of {len(T)} would be `auto` (ui/web agreement only); "
                       f"of those {sum(r[3] for r in auto)} are lenient-correct, {sum(r[2] for r in auto)} strict-correct.")
        out.append("")
    # per-term table B and A (blind)
    out.append("## Per-term picks, blind mode\n")
    out.append("| half | term | official | blind pick | strict | lenient | signal decision |")
    out.append("|---|---|---|---|---|---|---|")
    for nm, T in (("B", B), ("A", A)):
        _, _, _, rows, _ = agreement(T, idx, p, True)
        for t, e, st, le in rows:
            pk = next((r["surface"] for r in e["rows"] if r["key"] == e["pick"]), "-")
            out.append(f"| {nm} | {t['en']} | {t['official']['write']} | {pk} | {'yes' if st else 'no'} | {'yes' if le else 'no'} | {e['signal_decision']} |")
    # reworked + unsure from production picks file
    picks = json.load(open(os.path.join(OUT, "term-picks.json"), encoding="utf-8")) if os.path.exists(
        os.path.join(OUT, "term-picks.json")) else []
    byt = {x["term"]: x for x in picks}
    out.append("\n## The 9 reworked terms (production picks, `term-picks.json`)\n")
    out.append("| term | official now | pick | decision | why |")
    out.append("|---|---|---|---|---|")
    for en in ("session", "crash", "log", "account", "build", "feature", "role", "incident", "cloud"):
        x = byt.get(en)
        if x:
            out.append(f"| {en} | {x['official']} | {x['pick']} | {x['decision']} | {x['why']} |")
    uns = [x for x in picks if x["status"] != "confirmed"]
    cnt = collections.Counter(x["decision"] for x in uns)
    out.append(f"\n## The {len(uns)} unsure terms (production picks)\n")
    out.append(f"auto: {cnt['auto']}, review: {cnt['review']}.")
    tmap = {t["en"]: t for t in terms}
    conf_p = [x for x in picks if x["status"] == "confirmed"]
    c_auto = [x for x in conf_p if x["decision"] == "auto"]
    c_ok = sum(agrees(x["pick"], tmap[x["term"]])[1] for x in c_auto)
    wo = [x for x in picks if x["why"].startswith("web only")]
    wo_ok = sum(agrees(x["pick"], tmap[x["term"]])[1] for x in wo if x["status"] == "confirmed")
    wo_c = sum(1 for x in wo if x["status"] == "confirmed")
    sn = sum(1 for x in picks if x["why"].startswith("sense none"))
    out.append("\n## Reading the numbers\n")
    out.append(f"- Production `auto` on the confirmed terms: {len(c_auto)} are auto, {c_ok} of those match the official "
               f"column leniently. Of the {wo_c} confirmed terms decided by 'web only, decisive', {wo_ok} match.")
    out.append(f"- {sn} of {len(picks)} production picks end in review only because bolor-toli has no entry for the "
               "surface form (junk n-gram, or a loanword the dictionary lacks).")
    out.append("- Seeded and blind agree because a rendering with no data cannot win; seeding only helps when "
               "the data is silent, and then the pick is empty rather than the old answer.")
    out.append("- Matcher history: `words_match` was tightened twice after the first run showed false agreements "
               "(хэрэглэгч vs хэрэгсэл, тохиргоо vs тохиромжтой, user vs хэрэг). The final matcher is the one scored above; "
               "the tuned parameters were re-fitted on A with it.")
    open(os.path.join(OUT, "term-picker-eval.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    d = sp.add_parser("download")
    d.add_argument("--only")
    i = sp.add_parser("index")
    i.add_argument("--cc-limit", type=int, default=0, help="read only ~N MB of CC-100 text (0 = all)")
    i.add_argument("--skip-cc", action="store_true", help="development only: no corpus counts")
    p = sp.add_parser("pick")
    p.add_argument("--blind", action="store_true")
    sp.add_parser("eval")
    a = ap.parse_args()
    {"download": cmd_download, "index": cmd_index, "pick": cmd_pick, "eval": cmd_eval}[a.cmd](a)


if __name__ == "__main__":
    main()
