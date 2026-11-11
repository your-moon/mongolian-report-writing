---
name: mongolian-report-writing
description: Write or review formal Mongolian (Cyrillic/Khalkha) reports, incident post-mortems, and official/business documents in the actual register Mongolian institutions use — not translated-sounding prose and not news-story voice. Use whenever asked to write, translate, or check a Mongolian-language report, тайлан, албан бичиг, or when told to write "proper Mongolian."
---

# Mongolian Report Writing

Grounded in Mongolia's actual document standard (MNS 5140) and 90+ real government, corporate, and news sources — not generic textbook Mongolian. Report register is deliberately different from news-story register; don't reach for журналист voice by default.

## The seven defaults

1. **Verb endings carry evidentiality — pick on purpose.**
   `-сан/-сэн` = the report's own asserted/verified fact (default for findings). `-жээ`/`-сан байна` = ONLY when explicitly attributing to a cited external source ("...гэж мэдээлжээ", "...тогтоожээ"). `-лаа/-в` = the issuing body's own immediate completed action. `-на/-нэ` = scheduled/future/procedural effect. Never let `-жээ` leak into the report's own direct claims — it reads as secondhand and undercuts authority. See GRAMMAR.md §3.

2. **No би/бид/манай.** Confirmed by grepping real government guides and statements (zero hits across seven independent primary sources) — not one quotable ban, but a consistent, universal genre norm. Refer to the organization by name or "тус байгууллага" instead. Even corporate reports (APU JSC) confine "бид" to marketing preamble, never to findings/numbers — keep findings impersonal regardless of register. See STRUCTURE.md §4.

3. **Two-part body, not a fixed heading template.** MNS 5140 mandates: Part 1 (optional) states purpose/basis; Part 2 (required) states the conclusion/decision/recommendation. Narrative reports conventionally close on a **ДҮГНЭЛТ** section. Don't force "Удиртгал/Үндэслэл/Дүгнэлт/Санал зөвлөмж" onto every document — the heading set varies by genre (scholarly paper, resolution, functional report). See STRUCTURE.md §2.

4. **Pick one number/date/currency convention and hold it.** Real Mongolian sources are genuinely inconsistent (comma vs. space thousands separators, % vs. хувь, dotted vs. spelled-out dates) — that's a documented finding, not something to copy. A report must be internally consistent even where the wild corpus isn't. See GRAMMAR.md §6 and STRUCTURE.md §6 for the actual conventions to choose from.

5. **Cut news-story voice.** No rhetorical questions, no idioms ("гал дээр тос нэмэх"), no colloquial contractions (-чихсон), no bare first-person quotes dropped into narration. Attribute institutionally in third person (ablative: "ХХХ-аас мэдээлэв") or by title+name+reporting-verb, never as inner monologue. See STYLE.md §3 for the full formal-vs-news contrast table.

6. **Don't translate the non-translatable.** Proper names — product/brand/system names (eBarimt, QPay, SocialPay, iPhone, OpenAI), company names, payment-method names — stay in their original script, never forced into a Cyrillic calque or invented Mongolian equivalent. Real corpus usage confirms this: "iPhone Duo", "OpenAI", "Bank of China", "CIFIT 2026" all appear in Latin script inside otherwise-Cyrillic sentences. This is distinct from ordinary organization names, which the standard *does* want spelled out in full + abbreviated (STRUCTURE.md §5) — that rule is for genuine Mongolian institutional names, not foreign product/brand names.
   **In a technical note, do not translate English technical terms at all** — `prod`,
   `staging`, `pipeline`, `build`, `release`, `rollback`. If the tooling prints
   `prod-903f343d`, write `prod`. Measured failure: *production environment* →
   **үйлдвэрлэлийн орчин**, which says a factory. See WORDS.md §2e.

7. **Translate the mechanism, not the metaphor — this is the failure that survives every other rule.**
   A document can pass every check above and still be wrong, because English metaphors were
   carried across word-for-word. Measured 2026-09-21 on a real product-page→report translation:
   **27 instances in one document**, caught only when a native reader read it. `хаалга нээх`
   for *open a way in* (хаалга = a physical door), `дундаа уулздаг` for *meet in the middle*,
   `чимээгүй холболт` for *a quiet connection*, `давалгаа` for *a wave of updates*,
   `дахин асаах` for *reboot* (= flip the power on; reboot is `дахин ачаалах`), `флот` for
   *fleet* (= a naval fleet). **The check: does this word have an everyday physical sense, and
   would a reader who speaks no English picture that physical thing here?** Never translate the
   English sentence — write what the system actually does. See WORDS.md for the full measured
   table and the correct replacements.

## Workflow

- [ ] Structure: two-part body present? Narrative report ends on ДҮГНЭЛТ?
- [ ] Every verb ending deliberate (not defaulted to -лаа/-жээ out of habit) — GRAMMAR.md §3
- [ ] Zero би/бид/манай anywhere, including in a translated "we found..." sentence
- [ ] Acronyms/org names spelled out in full once, abbreviation in parens, short form after — STRUCTURE.md §5
- [ ] Case endings match each word's own vowel class (don't copy the previous word's suffix) — GRAMMAR.md §1-2
- [ ] Numbers/dates/currency use one consistent convention throughout — GRAMMAR.md §6
- [ ] No news-register leakage (idiom, rhetorical question, colloquial contraction) — STYLE.md §3
- [ ] Every noun/verb checked against WORDS.md §2 — no English metaphor carried across word-for-word (хаалга/давалгаа/чимээгүй/дотор орох/флот/дахин асаах class)
- [ ] Product/brand/system names left untranslated in original script (eBarimt, QPay, iPhone, etc.); only genuine Mongolian org names get the spell-out-then-abbreviate treatment
- [ ] English technical terms left untranslated (`prod`, `staging`, `pipeline`, `build`)
- [ ] `./bolor.py <үг>` run on any Mongolian word used for a technical sense — it prints
      what the word actually means, which is the fact the physical-sense check lacks
- [ ] `./bolor.py --scan <draft>` run on the finished draft; it must exit 0
- [ ] **Outward-facing Mongolian (ticket, PR description, customer doc) is shown in the
      terminal and posted only after the user says so.** Both measured calque batches were
      caught by a human reading the text; one reached a customer-visible ticket
      because it was posted unreviewed. This gate is the only thing with a 100% catch rate.
- [ ] Punctuation: straight quotes " ", period after name-initials (Л.Оюун-Эрдэнэ), comma before fronted subordinate clauses — GRAMMAR.md §5

## Reference files

- **STRUCTURE.md** — MNS 5140 standard, document structure, resolution/academic templates, verb mood/voice, first-person avoidance, terminology/acronyms, formatting, anti-patterns.
- **GRAMMAR.md** — the 8 noun cases, vowel harmony, verb tense/evidentiality in depth, common mistakes, punctuation, numbers/dates/units.
- **WORDS.md** — the calque table: 27 measured English-metaphor errors from a real translation, with correct replacements; term collisions; how to translate a marketing sentence into a report sentence.
- **bolor.py** — bolor-toli.com lookup and blocklist scanner. `./bolor.py <үг>` prints a
  word's real senses with domain tags; `./bolor.py --scan <file>` greps the measured
  calques over a draft and exits non-zero on a hit. Use it instead of adding table rows.
- **STYLE.md** — connective/transition words, attribution patterns, sentence/paragraph rhythm, and the formal-report-vs-news-story contrast table.

Every rule in these files traces to a real cited source (government PDF, legalinfo.mn, montsame.mn, corpus article) or is explicitly marked as reasoned synthesis rather than a quoted rule — check the citation if something looks off rather than assuming it's settled.
