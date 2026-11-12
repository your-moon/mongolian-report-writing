# Technical Terms: Translate, Loanword, or Keep English?

A dictionary says what a word *can* mean. Only real Mongolian text shows how people *write*
the term. `terms.json` records both for 60 common software terms, separately for two settings:

- **dev**: ticket, PR, developer chat
- **official**: a letter or report to a government body, bank, or customer

Each setting puts the term in one group:

| Group | Write it | Example |
|---|---|---|
| english | Latin script, untranslated | `prod`, `commit`, `pipeline` |
| loan | Cyrillic loanword | сервер, файл, апп |
| native | the Mongolian word in use | нууц үг, хэрэглэгч, тохиргоо |

The same term can change group by setting: `deploy` in a ticket, **ашиглалтад нэвтрүүлэх** in
an official report.

## Look one up

```sh
python3 ~/.claude/skills/mongolian-report-writing/bolor.py --term deploy
```

It prints both settings, the wrong renderings to avoid, and every piece of evidence with its URL.

## What "confirmed" means

- **confirmed**: bolor-toli supports it and a real Mongolian page uses it, or two independent
  pages use it. A wrong rendering of a confirmed term fails `--scan`.
- **unsure**: dictionary-only, or the sources disagree. The scan only warns. Most dev-pipeline
  terms (deploy, build, commit, cache, session) are unsure because the public corpus (bank and
  telecom help pages, ikon.mn, unread.today, gogo.mn, mn.wikipedia) is customer-facing text.
  Mongolian developer writing is mostly in closed chats.

The evidence was collected 2026-11-11: 60 terms, 24 confirmed, 36 unsure.

## Where the dictionary and real usage disagreed

- **browser**: bolor-toli gives хөтөч (comp.), but хөтөч also means a guide; Wikipedia writes броузер.
- **encryption**: bolor-toli gives нууцлал, but a bank uses нууцлал for confidentiality. Write шифрлэлт.
- **upgrade**: bolor-toli prefers сайжруулалт; TDB announces an upgrade as СИСТЕМИЙН ШИНЭЧЛЭЛ.
- **bug**: bolor-toli gives согог; the media write алдаа.
- **account**: данс is a money account on every bank page. A login account is бүртгэл.

Trust real usage over the dictionary when they disagree.

## Choosing from data was tried, and it does not work

`docs/research/pick_terms.py` (2026-11-12) mined renderings from software UI translations
(translatewiki, GNOME, Ubuntu: about 8k sentence pairs), 567k English–Mongolian web pairs (OPUS
CCAligned) and 14M CC-100 Mongolian sentences, then checked each pick against bolor-toli.

It reproduced **5 of 12** held-out confirmed terms. Some picks it marked confident were worse
than a guess: crash → сүйрэл (catastrophe), fix → тогтмол, role → үүрэг. Reasons, from
`docs/research/term-picker-eval.md`:

- The Mongolian data is customer-facing text. Developer terms (build, session, deploy, commit)
  have no data or produce junk n-grams.
- Agreement between the UI and web data is not a safe signal; on the held-out half, 3 of 6
  agreed picks were right.
- bolor-toli has no entry for inflected, multi-word or loanword forms, so the sense check is
  blind on about a third of the picks.

A native reader decides. The script is still useful for one thing: real sentence pairs showing
how a term was translated, to look at while deciding.

```sh
python3 docs/research/pick_terms.py download   # ~460 MB into ~/.cache/mongolian-terms/
python3 docs/research/pick_terms.py index
python3 docs/research/pick_terms.py pick       # docs/research/term-picks.md has example pairs per term
```

## Add or correct a term

1. `python3 ~/.claude/skills/mongolian-report-writing/bolor.py <english word>` for the dictionary senses (go slowly; the API is undocumented).
2. Find the term in at least one real Mongolian page and copy a short quote with its URL.
3. Add or edit the entry in `terms.json`. Set `status` to confirmed only by the rule above.
4. Put a wrong rendering in `avoid` only if it is wrong for the technical sense *and* not an
   ordinary correct word elsewhere. Dictionary senses alone are not enough: тогтоох, шалгалт,
   салбар are dictionary senses of fix, test and branch, and correct words in every report.
5. Run `python3 -m unittest test_bolor`.
