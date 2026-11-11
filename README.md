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
- `bolor.py`: looks up a word on bolor-toli.com (`bolor.py үг`) and scans a draft for known calques (`bolor.py --scan draft.md`). Python 3, standard library only. Please keep lookups at human pace.
