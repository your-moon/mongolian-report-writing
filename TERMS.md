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

## Add or correct a term

1. `python3 ~/.claude/skills/mongolian-report-writing/bolor.py <english word>` for the dictionary senses (go slowly; the API is undocumented).
2. Find the term in at least one real Mongolian page and copy a short quote with its URL.
3. Add or edit the entry in `terms.json`. Set `status` to confirmed only by the rule above.
4. Put a wrong rendering in `avoid` only if it is wrong for the technical sense *and* not an
   ordinary correct word elsewhere. Dictionary senses alone are not enough: тогтоох, шалгалт,
   салбар are dictionary senses of fix, test and branch, and correct words in every report.
5. Run `python3 -m unittest test_bolor`.
