# mongolian-report-writing

A Claude Code skill for writing and reviewing formal Mongolian (Cyrillic/Khalkha) reports, post-mortems and official documents in the register Mongolian institutions actually use, not translated-sounding prose or news-story voice.

It is based on the MNS 5140 document standard and 90+ real government, corporate and news sources. It also lists calques that real drafts shipped and a Mongolian reader rejected.

## Install

```sh
git clone https://github.com/your-moon/mongolian-report-writing ~/.claude/skills/mongolian-report-writing
```

Claude Code loads it automatically when you ask for a Mongolian тайлан, албан бичиг or "proper Mongolian".

## Files

- `SKILL.md`: the seven defaults and a pre-send checklist
- `GRAMMAR.md`: verb endings and evidentiality, punctuation, numbers and dates
- `STRUCTURE.md`: MNS 5140 document structure, names and abbreviations
- `WORDS.md`: calques that were shipped and rejected, with the correct words
- `TERMS.md`, `terms.json`: 60 software terms, kept English, Cyrillic loanword or native word, for a dev note and for an official document, with evidence
- `bolor.py`: checks a draft and looks words up on bolor-toli.com. Python 3, standard library only.
- `test_bolor.py`: one known-bad sentence per check, plus correct sentences that must come back clean.

## Check a draft

```sh
python3 ~/.claude/skills/mongolian-report-writing/bolor.py --scan draft.md
```

```
draft.md:1: ERROR [calque] үйлдвэрлэлийн орчин — factory manufacturing; write prod / бодит орчин
draft.md:1: ERROR [first-person] бид — no би/бид/манай; name the organization or write тус байгууллага
draft.md:2: WARN [evidential] унтарчээ — -жээ with no cited source sounds secondhand; use -сан/-сэн
```

An ERROR fails the scan (exit 1): known calques, би/бид/манай outside quotes, colloquial -чих forms, Cyrillicized brand names (КьюПэй), and mixed number or percent formats in one document. A WARN is a heuristic to read, not to obey blindly. If a hit is right for your text, skip it with `--allow=хаалга`.

`bolor.py <үг>` prints what a word actually means on bolor-toli.com. Please keep lookups at human pace; results are cached in `~/.cache/bolor-toli.json`. Without a network the lookup says so, and the scan still works.

## Translate a technical term or not?

```sh
python3 ~/.claude/skills/mongolian-report-writing/bolor.py --term deploy
```

```
deploy  [unsure]
  dev      deploy  (english)
  official ашиглалтад нэвтрүүлэх  (native)
```

`--scan --setting=official` checks a letter or report against the official column. See `TERMS.md` for how the evidence was collected and how to add a term.

## Add a calque you caught

Add a line to `CALQUES` in `bolor.py`, add the bad sentence to `BAD` in `test_bolor.py`, and run `python3 -m unittest test_bolor`.
