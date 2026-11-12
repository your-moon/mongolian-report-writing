---
name: mongolian-report-writing
description: Write or review formal Mongolian (Cyrillic/Khalkha) reports, incident post-mortems, and official/business documents in the actual register Mongolian institutions use — not translated-sounding prose and not news-story voice. Use whenever asked to write, translate, or check a Mongolian-language report, тайлан, албан бичиг, or when told to write "proper Mongolian."
---

# Mongolian Report Writing

Grounded in Mongolia's actual document standard (MNS 5140) and 90+ real government, corporate, and news sources — not generic textbook Mongolian. Report register is deliberately different from news-story register; don't reach for журналист voice by default.

## Quick use

Three commands. Run them in this order on every Mongolian draft:

```sh
python3 ~/.claude/skills/mongolian-report-writing/bolor.py --term deploy session crash         # 1. before writing: how to render each technical term
python3 ~/.claude/skills/mongolian-report-writing/bolor.py --scan draft.md --setting=dev       # 2. after writing: must exit 0 (official: --setting=official)
python3 ~/.claude/skills/mongolian-report-writing/bolor.py үйлдвэрлэл                          # 3. any word you are unsure of: what it really means
```

- Add `--json` to `--term` or `--scan` for machine-readable output.
- Exit codes: `--scan` 0 = clean, 1 = errors. `--term` 1 = a term is not listed. The lookup
  prints "lookup unavailable" when offline (exit 3); the scan still works.
- `--setting=dev` is a ticket, PR or chat; `--setting=official` is a letter or report to a
  government body, bank or customer.
- A term not in the list: keep it in English in a dev note, and look it up before translating
  it in an official document.
- Show the finished Mongolian to the user before posting it anywhere.

## The seven defaults

1. **Verb endings carry evidentiality — pick on purpose.**
   `-сан/-сэн` = the report's own asserted/verified fact (default for findings). `-жээ`/`-сан байна` = ONLY when explicitly attributing to a cited external source ("...гэж мэдээлжээ", "...тогтоожээ"). `-лаа/-в` = the issuing body's own immediate completed action. `-на/-нэ` = scheduled/future/procedural effect. Never let `-жээ` leak into the report's own direct claims — it reads as secondhand and undercuts authority. See GRAMMAR.md §3.

2. **No би/бид/манай.** Confirmed by grepping real government guides and statements (zero hits across seven independent primary sources) — not one quotable ban, but a consistent, universal genre norm. Refer to the organization by name or "тус байгууллага" instead. Even corporate reports (APU JSC) confine "бид" to marketing preamble, never to findings/numbers — keep findings impersonal regardless of register. See STRUCTURE.md §4.

3. **Two-part body, not a fixed heading template.** MNS 5140 mandates: Part 1 (optional) states purpose/basis; Part 2 (required) states the conclusion/decision/recommendation. Narrative reports conventionally close on a **ДҮГНЭЛТ** section. Don't force "Удиртгал/Үндэслэл/Дүгнэлт/Санал зөвлөмж" onto every document — the heading set varies by genre (scholarly paper, resolution, functional report). See STRUCTURE.md §2.

4. **Pick one number/date/currency convention and hold it.** Real Mongolian sources are genuinely inconsistent (comma vs. space thousands separators, % vs. хувь, dotted vs. spelled-out dates) — that's a documented finding, not something to copy. A report must be internally consistent even where the wild corpus isn't. See GRAMMAR.md §6 and STRUCTURE.md §6 for the actual conventions to choose from.

5. **Cut news-story voice.** No rhetorical questions, no idioms ("гал дээр тос нэмэх"), no colloquial contractions (-чихсон), no bare first-person quotes dropped into narration. Attribute institutionally in third person (ablative: "ХХХ-аас мэдээлэв") or by title+name+reporting-verb, never as inner monologue. See STRUCTURE.md §7 and WORDS.md §5.

6. **Don't translate the non-translatable.** Proper names — product/brand/system names (eBarimt, QPay, SocialPay, iPhone, OpenAI), company names, payment-method names — stay in their original script, never forced into a Cyrillic calque or invented Mongolian equivalent. Real corpus usage confirms this: "iPhone Duo", "OpenAI", "Bank of China", "CIFIT 2026" all appear in Latin script inside otherwise-Cyrillic sentences. This is distinct from ordinary organization names, which the standard *does* want spelled out in full + abbreviated (STRUCTURE.md §5) — that rule is for genuine Mongolian institutional names, not foreign product/brand names.
   **Check how Mongolian text actually writes a technical term: `python3 ~/.claude/skills/mongolian-report-writing/bolor.py --term <word>`.**
   It says whether the term stays English, becomes a Cyrillic loanword (сервер) or has a native
   word in use (нууц үг), separately for a dev note and an official document, with evidence.
   See TERMS.md. For a term not listed, the default below holds.
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

1. Write the draft to a file and run the scanner on it. It must exit 0:

   ```sh
   python3 ~/.claude/skills/mongolian-report-writing/bolor.py --scan draft.md --setting=dev
   ```

   Use `--setting=official` for a letter or report to a government body, bank or customer:
   the term checks (TERMS.md) then expect the official rendering.

   ERROR lines fail the scan: measured calques (WORDS.md §2), би/бид/манай outside quotes,
   colloquial -чих forms, Cyrillicized brand names, and mixed number or percent formats.
   WARN lines are heuristics to read, not to obey blindly: -жээ with no cited source
   (GRAMMAR.md §3), question marks, « » quotes, initials with no period. If a hit is right
   for this text (a real door), pass `--allow=хаалга`.

2. Look up every Mongolian word you chose for a technical sense:
   `python3 ~/.claude/skills/mongolian-report-writing/bolor.py <үг>` prints what the word actually means, with domain tags.

3. Check by reading what no script can:
- [ ] Structure: two-part body present? Narrative report ends on ДҮГНЭЛТ? (STRUCTURE.md §2)
- [ ] Every verb ending deliberate: -сан/-сэн for the report's own findings — GRAMMAR.md §3
- [ ] No English metaphor carried across that the scanner doesn't know yet: does this word have an everyday physical sense a reader would picture here? (default 7)
- [ ] Acronyms/org names spelled out in full once, abbreviation in parens, short form after — STRUCTURE.md §5
- [ ] Case endings match each word's own vowel class — GRAMMAR.md §1-2
- [ ] Every technical term rendered as TERMS.md says for this setting; terms not listed stay English in a dev note
- [ ] **Outward-facing Mongolian (ticket, PR description, customer doc) is shown in the
      terminal and posted only after the user says so.** Both measured calque batches were
      caught by a human reading the text; one reached a customer-visible ticket
      because it was posted unreviewed. This gate is the only thing with a 100% catch rate.

## Reference files

- **STRUCTURE.md** — MNS 5140 standard, document structure, resolution/academic templates, verb mood/voice, first-person avoidance, terminology/acronyms, formatting, anti-patterns.
- **GRAMMAR.md** — the 8 noun cases, vowel harmony, verb tense/evidentiality in depth, common mistakes, punctuation, numbers/dates/units.
- **WORDS.md** — the calque table: 27 measured English-metaphor errors from a real translation, with correct replacements; term collisions; how to translate a marketing sentence into a report sentence.
- **TERMS.md** + `terms.json` — 60 software terms: English, Cyrillic loanword, or native word, per setting, with dictionary and real-usage evidence.
- **bolor.py** — bolor-toli.com lookup and blocklist scanner. `bolor.py <үг>` prints a word's real
  senses with domain tags; `bolor.py --scan <file>` runs every scriptable check and exits
  non-zero on an ERROR. Add a new calque to its `CALQUES` list and a test line to
  `test_bolor.py`, instead of only adding a table row.

Every rule in these files traces to a real cited source (government PDF, legalinfo.mn, montsame.mn, corpus article) or is explicitly marked as reasoned synthesis rather than a quoted rule — check the citation if something looks off rather than assuming it's settled.
