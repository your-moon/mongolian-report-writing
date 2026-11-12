# How Mongolian writes technical vocabulary: four sources compared (2026-11-12)

## Sources

| Source | What it is | Coverage of our 60 terms | Limits |
|---|---|---|---|
| toli.gov.mn | Official orthography dictionary (Хэлний бодлогын үндэсний зөвлөл) | Spelling only; most tech loanwords absent (файл, апп, токен, кэш, порт, сервер) | No meanings for loans; copying the data is prohibited, single lookups only |
| Microsoft Terminology (MONGOLIAN.tbx, 6,256 terms) | Professional localization glossary | 20 of the 24 confirmed terms | Windows-era wording; spells програм, интернет |
| Android `values-mn/strings.xml` (2,292 strings aligned by id) | Professional UI translation | UI terms only | Some calques (Reboot → Дахин асаах) |
| CC-100 Mongolian (15.1M web sentences, ~2018 crawl) | What people actually write | Everything | Includes spam and machine-translated pages |

Agreement with the 24 confirmed terms: **Microsoft 16 of 20** (80%); the automatic picker
(`pick_terms.py`) 5 of 12 held out. Microsoft's 4 differences are dated or unused wording:
хамгаалалттай гарц for firewall (0 corpus hits; галт хана has 140), үүл for cloud, програм for app,
сайжруулах for upgrade.

## Two loanword layers: Russian and English

Soviet-era words came through Russian and keep Russian spelling. Newer English words are spelled
by sound with э. Usage still mixes both, and the official dictionary often disagrees with the
majority. Counts from `layers.py` over CC-100:

| Word | Russian-route spelling | Mongolian/English-route spelling | Official (toli.gov.mn) |
|---|---|---|---|
| program | програм 34,157 / программ 17,426 | | **программ** |
| internet | интернет 30,951 | интернэт 22,581 | **интернэт** |
| web | веб 12,490 | вэб 62,720 | (no entry) |
| server | сервер 5,355 | сэрвэр 175, сервэр 171 | (no entry) |
| account | аккаунт 656 | акаунт 253 | (no entry) |
| application | аппликейшн 3,946 | аппликэйшн 1,899 | (no entry) |
| computer | компьютер 37,805 | компьютэр 174 | |

Even an English-era word like account is mostly written the Russian way (аккаунт). Rule for a
report: use the official spelling where toli.gov.mn has one (программ, интернэт, сайт, админ);
elsewhere use the majority spelling (вэб, сервер, компьютер).

## Competing words for the same thing

| Term | Counts (tech sentences) | Reading |
|---|---|---|
| reboot/restart | дахин эхлүүлэх 71 · дахин ачаалах 79 · дахин асаах 7 | дахин асаах is rare, so the WORDS.md ban holds by usage, though Android uses it |
| session | нэвтрэлт 142 · сесс 21 · сеанс 14 | нэвтрэлт is what people write |
| account | аккаунт/акаунт 482 · хэрэглэгчийн бүртгэл 284 | dev and informal: аккаунт; official: хэрэглэгчийн бүртгэл (also Microsoft) |
| browser | хөтөч 1,401 · браузер 440 · броузер 92 | "интернэт хөтөч" is common; хөтөч alone also means a guide, so write вэб хөтөч (also Microsoft) |
| firewall | галт хана 76 · хамгаалалттай гарц 0 | галт хана |
| crash | гацсан/гацах 250 · унтарсан 65 · ажиллахаа зогсох 5 | гацах is how people say an app crashed or froze |
| incident/failure | доголдол 398 · саатал 280 | системийн доголдол is the common phrase |
| feature | онцлог 4,936 · функц 1,432 | онцлог is also generic "characteristic"; Android and Microsoft both use онцлог |
| encryption | шифрлэх 513 · нууцлах 2,274 | нууцлах is general secrecy; шифрлэх is the technical act |
| cloud | клауд 55 · үүлэн технологи 139 · үүлэн үйлчилгээ 19 | үүлэн технологи |
| log | лог 120 · системийн бүртгэл 33 | лог is used ("лог мэдээлэл"), though the native word лог means a crucible or rubbish |

## What can be automated, and what can't

Automatable, with measured support:
- **Spelling of a loanword**: toli.gov.mn lookup, one word at a time.
- **Usage counts of competing words**: `layers.py`, about 3 min over CC-100. This settles
  "which word do people write" for the competing words listed above.
- **A first candidate**: Microsoft Terminology, 80% agreement with confirmed terms. A Microsoft
  term with zero corpus hits is dated and should be dropped.
- **Detecting known errors in a draft**: `bolor.py --scan`.

Not automatable:
- **Mining a rendering from parallel text**: `pick_terms.py`, 5 of 12.
- **Choosing between words that are both in use** (онцлог or функц, саатал or доголдол): the
  counts show both are real. Which one fits a given document is a reader's call.
