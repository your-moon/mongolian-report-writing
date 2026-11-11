# Structure & Standard — Mongolian Formal Documents

Sourced from MNS 5140-2:2021 (official PDF, extracted via `pdftotext`, not a summarizer), two legalinfo.mn instruments (Төрийн албан хэрэг хөтлөх үндсэн заавар; Албан хэрэг хөтлөлтийн нийтлэг журам — both downloaded as raw HTML and grepped for verification), real government resolutions, and real corporate/central-bank reports.

## 1. The governing standard

Mongolia's document-writing standard is **MNS 5140** ("Баримт бичгийн стандарт"), issued by the Standards and Metrology Agency, in three parts:
- MNS 5140-1 — document names/types/definitions
- MNS 5140-2 — composition and requirements ("Баримт бичгийн бүрдэл, тэдгээрт тавих шаардлага")
- MNS 5140-3 — printed-sheet layout requirements

It sits alongside two legal-instrument-level guides: **"Төрийн албан хэрэг хөтлөх үндсэн заавар"** and **"Албан хэрэг хөтлөлтийн нийтлэг журам"** (legalinfo.mn).

The standard classifies **Тайлан (report)** as one of 17 named "organizational document" types (Зохион байгуулалтын баримт бичиг), alongside Акт, Албан бичиг, Гэрээ, Дүгнэлт, Дүрэм, Журам, Заавар, Зөвлөмж, Санал, Санамж бичиг, Төлөвлөгөө, Төсөл, Удирдамж, Хөтөлбөр, Хурлын тэмдэглэл (verified from the standard's own classification table).

## 2. Structure: a universal two-part body, not one fixed heading set

The standard does **not** mandate "Удиртгал/Үндэслэл/Дүгнэлт/Санал зөвлөмж" for every document. What it mandates is a two-part body:

> "Баримт бичгийн агуулга нь үндсэн хоёр хэсгээс бүрдэнэ. Нэг дэх буюу тэмдэглэх хэсэгт уг баримт бичгийг боловсруулсан зорилго, үндэслэл, шаардлагыг зааж, хоёр дахь хэсэгт санал, хүсэлт, дүгнэлт, шийдвэр, зөвлөмжийн талаар бичнэ. Зарим тохиолдолд бичвэр нь тэмдэглэх хэсэггүйгээр зөвхөн хоёр дахь хэсгээс бүрдэнэ."
> (Part 1 states purpose/basis/rationale; Part 2 states the recommendation, request, conclusion, decision, or recommendation. Some documents skip Part 1 entirely.)
> — MNS 5140-2:2021 PDF

For **narrative reports**, two independent sources both close on **ДҮГНЭЛТ** (conclusion) as the final required section, preceded by topic-organized body sections (not a generic "Main Body" label) — e.g. a functional/library-report template runs: ТАЙЛАН ГЭЖ ЮУ ВЭ → ТАЙЛАНГИЙН ХУГАЦАА → [topic sections specific to the reporting unit] → ТӨЛБӨР ТООЦОО (ТӨСӨВ) → **ДҮГНЭЛТ**. (Source: a SlideShare deck — arrived through a fetch tool wrapped in a suspicious JSON header; only the substantive heading list was used, treat as lower-confidence than the pdftotext sources, though consistent with the independently-confirmed ДҮГНЭЛТ convention below.)

### 2a. Academic-report structure (Эрдэм шинжилгээний өгүүлэл)

A distinct, internationally-styled structure (source: nairuulga.mn — Хэлний бодлогын үндэсний зөвлөл, quotes re-verified against raw HTML):

Гарчиг ("Гарчиг нь өгүүллийн гол санааг агуулсан товч, тодорхой, оновчтой томьёологдсон байх ёстой", all-caps, distinct font) → Зохиогчийн хаяг → Хураангуй (8–12 lines, required in Russian and English too) → Түлхүүр үг → Удиртгал (methodology, objectives, hypotheses) → Үндсэн хэсэг → Судалгааны үр дүн → Хязгаарлалт (limitations, future directions) → Дүгнэлт & Ном зүй. Formatting: Times New Roman 10pt, single spacing, A4, margins top/bottom 1.5cm, left 3cm, right 1.5cm.

### 2b. Government resolutions (Тогтоол) — a distinct, formulaic sub-genre

Confirmed identically across two real, unrelated draft resolutions (downloaded PDFs from two different ministries):

```
МОНГОЛ УЛСЫН ЗАСГИЙН ГАЗРЫН ТОГТООЛ
[он] оны ... дугаар сарын ...-ны өдөр      Дугаар ....      Улаанбаатар хот
[SUBJECT IN CAPS] ТУХАЙ
[Legal citation] ... заасныг үндэслэн Монгол Улсын Засгийн газраас ТОГТООХ нь:
1. ... баталсугай.
2. ... даалгасугай.
```

Note the archaic optative/hortative suffix **-сугай** (баталсугай, даалгасугай) — specific to this genre, not general report writing.

## 3. Verb mood/voice — impersonal, non-agentive, evidential-past

Three real, distinct patterns, all avoiding a human "doer" as grammatical subject:

- **-сугай** in resolutions (see 2b above) — genre-specific, not for general reports.
- **-лаа/-лээ/-в** in press releases/policy statements — an outcome described as observed fact, never "бид шийдсэн": "Бодлогын хүүг 12 хувьд хэвээр хадгалах ... шийдвэрлэлээ." (Монголбанк, two independent statements cross-checked, same register both times).
- **Institution-as-subject narrative**: "Тэргүүн шадар сайд Л.Гантөмөр ... тогтоолын төслийг ... өргөн барилаа." — the named official appears only as the formal actor of an institutional act, never reporting in first person (mongolia.gov.mn).

The standard's own prose is self-referentially impersonal too: "Баримт бичиг зохион бүрдүүлж, албан ёсны болгоход дараах 28 бүрдлийг ашиглана" — never "бид ашиглана".

## 4. First person — avoided in government register; contrast in corporate register

**Evidence, stated honestly:** grepping the entire ~230KB raw text of the main official document-writing guide for би/бид/манай returns **zero occurrences**. Combined with zero first-person occurrences across every other primary source checked (two resolutions, two Монголбанк statements, a Ministry of Finance release, a PM's-office release), this is strong, multiply-corroborated evidence for the convention — but it's enforced through consistent genre usage, not one single explicit "no би/бид" prohibition sentence found in the accessible guide text. Don't claim there's one banning sentence; the evidence is the consistent absence.

Institutional self-reference instead uses the organization's proper name or **"тус"**, e.g. "тус байгууллага", "Монголбанкны Мөнгөний бодлогын хороо".

**Corporate contrast:** APU JSC's real 2023 half-year report *does* use "бид" — but only in the marketing/values preamble ("ҮЗЭЛ БАРИМТЛАЛ": "Бид бүхий л түвшинд чанарыг эрхэмлэж..."). Its actual financial-reporting language reverts to the same impersonal register as government documents: "цэвэр борлуулалтын орлого 32%-иар өссөн ба цэвэр ашиг ... 13%-иар буурсан үзүүлэлттэй байна." **Rule: findings and numbers stay impersonal even in corporate register; "бид" is confined to vision/brand copy, never to a reported fact.**

## 5. Terminology precision / acronyms

Directly from the standard:

> "...байгууллага, түүний зохион байгуулалтын нэгжийн нэр дахин давтагдахаар бол тэдгээрийн нэрийг эхний удаа бүтнээр бичээд, товчилсон нэрийг хаалтад бичиж, цаашид товчилсон нэрээр бичнэ. Жишээ нь: Иргэний нисэхийн ерөнхий газар (цаашид "ИНЕГ" гэх)"
> — MNS 5140-2:2021 PDF

**Rule: spell the organization/term out in full on first use, give the abbreviation in parentheses, use only the short form thereafter.** This applies to genuine Mongolian institutional names (Иргэний нисэхийн ерөнхий газар → ИНЕГ).

**Foreign/technical/brand names — do not translate.** No formal rule exists in MNS 5140 or either legalinfo.mn guide on this (that gap was real when first researched), but real corpus usage is unambiguous and consistent: product, brand, system, and payment-method names are kept in their **original script**, never forced into a Cyrillic calque or invented Mongolian equivalent — "iPhone Duo", "OpenAI", "Bank of China", "CIFIT 2026" all appear in Latin script inside otherwise fully-Cyrillic sentences (ikon.mn, zindaa.mn corpus). **Apply the same treatment to eBarimt, QPay, SocialPay, MonPay, ArdPay, and similar system/product names — write them as-is, don't Cyrillicize or translate them.** Genuine Mongolian institution names still get the spell-out-then-abbreviate treatment above; this rule is specifically for names that originate outside Mongolian.

## 6. Formatting conventions

- **Dates** — two real, distinct formats coexist by context:
  - Numeric, dot-separated, for headers/letterheads: "Он, сар, өдрийн тоог цэгээр зааглан ... Жишээ нь: 2007.03.06"
  - Spelled-word form for running text: "2023 оны 01 сарын 14 өдөр"
- **Money** — numeral + parenthetical spelled-out form: "3,603,000 (гурван сая зургаан зуун гурван мянга)"
- **Decimals** — period-separated, spelled with "бүхэл...-ийн": "3,568.58 (гурван мянга таван зуун жаран найман бүхэл зууны тавин найм)"
- **Percentages** — suffix directly on the numeral, no spelled-out form needed (unlike currency): "8.2 хувь", "32%-иар өссөн"
- **Fonts/margins** — Arial 11–12pt or Times New Roman 12–14pt body (9–11pt tables); A4, margins top 20mm / bottom 15–20mm / left 20–30mm / right 15–20mm; line spacing 1.5
- **Page numbering** — Arabic numerals from page 2 onward, centered, 10mm from top edge
- **Headlines** in real government press releases render in ALL CAPS: "АРАБЫН НЭГДСЭН ЭМИРАТ УЛСТАЙ ЭРЧИМ ХҮЧНИЙ САЛБАРТ ХАМТРАН АЖИЛЛАХ ТУХАЙ САНАМЖ БИЧИГТ ГАРЫН ҮСЭГ ЗУРАВ"

## 7. Style / anti-pattern warnings (from the standard and legalinfo.mn, verbatim-confirmed)

> "...энгийн, тодорхой, хоёрдмол утгагүй, аман ярианы болон нутгийн аялга хэлц, этгээд, бүдүүлэг үг хэрэглээгүй, санаагаа зөв илэрхийлсэн байх" — simple, clear, unambiguous; no colloquial/dialectal/vulgar language.

> "Гарын үсэг зурагдсан баримт бичигт ямар нэг засвар, өөрчлөлт хийхийг хориглоно." — no edits to a signed document.

> "Огноо байхгүй, бүртгэлийн дугаар аваагүй баримт бичгийг гадагш явуулахыг хориглоно." — undated/unregistered documents may not be sent out.

> "оноосон нэрийн эхний үсгийг том үсгээр эхэлж бичнэ. Жишээ нь: Дамдины Сүхбаатар, Улаанбаатар хот..." — capitalize the first letter of proper nouns.

> "бичвэрийн дунд нэг үеийг хоёр мөрөнд хувааж бичихгүй" — never break a syllable across two lines.

## Explicit gaps — do not assert these as rules

- No single universally-mandated heading set ("Удиртгал/Үндэслэл/Дүгнэлт/Санал зөвлөмж") across all report genres — only the two-part body is actually mandated; named headings vary by genre.
- The first-person-avoidance convention is evidenced by consistent absence, not one quotable prohibition sentence.
