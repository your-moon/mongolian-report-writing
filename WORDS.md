# Word Choice — Calques That a Mongolian Reader Rejects

**Source: a real session, 2026-09-21.** An English-language product page (a
remote-access system for vending machines) was turned into a formal Mongolian report.
The register, the verb endings, and the би/бид rule were all correct — and the document
was still wrong, because English *metaphors* had been carried across word-for-word. A
Mongolian-native reader caught the first one ("хаалга = its physical door — not the
correct word") and a full re-read found **26 more of the same class**.

Every row below was produced by a model that had already read SKILL.md, STRUCTURE.md
and GRAMMAR.md. None of those files prevented it. That is why this file exists.

## 1. The failure mode, stated once

Formal Mongolian has no tolerance for a dead metaphor imported from English. Where
English says *open the door*, *meet in the middle*, *a quiet connection*, *get inside a
machine*, *a wave at a time*, the Mongolian word you reach for keeps its **physical,
literal meaning** and the sentence reads as nonsense or comedy. English has worn these
words smooth; Mongolian has not.

**The check, applied to every noun and verb before it goes in:** does this word have an
everyday physical sense? If yes — would a reader who speaks no English picture that
physical thing here? If yes, the word is wrong no matter how well it translates the
English.

## 2. The measured table

Left column is what the model wrote. It is not hypothetical.

### 2a. Metaphors carried across

| English source | Calque produced (wrong) | Correct Mongolian | Why it fails |
|---|---|---|---|
| open the door / a way in | **хаалга** нээх | **холболт** эхлүүлэх | хаалга = a physical door on hinges |
| the door closes itself | хаалгаа өөрөө **хаана** | холболтоо өөрөө **таслана** | a connection is cut (тасрах), not shut |
| both ends meet in the middle | хоёул **дундаа уулздаг** | хоёр тал **дундын сервер дээр хоорондоо холбогддог** | уулзах = people meeting in person |
| one quiet connection | **чимээгүй** холболт | **тогтмол** холболт | чимээгүй = making no sound |
| machines that have gone quiet | **чимээгүй болсон** машин | **хариу өгөхөө больсон** машин | same — silence of sound, not of traffic |
| get inside a machine | машин **дотор орох** | машины **системд нэвтрэх** | pictures a person climbing into the cabinet |
| work as if standing in front of it | машины **дотор орж** ажиллах | машины **удирдлагын системд нэвтэрч** ажиллах | same |
| ship a wave at a time | **давалгаа** тус бүрээр | **үе шаттайгаар** | давалгаа = an ocean wave |
| without touching the fleet | **гараар хүрэлгүйгээр** | **газар дээр нь очилгүйгээр** | "touching" is idiomatic in EN only |
| read the serial down the phone | утсаар **уншуулсны** дараа | утсаар **мэдэгдсэний** дараа | уншуулах = have someone read aloud to you |
| audit rows still resolve to a name | нэр **тайлагдсан** хэвээр | нэр **тодорхой** хэвээр | тайлагдах = be deciphered / be reported |
| three levels, and they only narrow | эрх зөвхөн **нарийсна** | эрх **шатлан олгогдоно** | the EN geometry metaphor conveys nothing |
| not off somebody remembering | **хүний санах ойд** бус | **хүн санаж хийх үйлдэлд** бус | санах ой = computer RAM |
| a new board announces itself | самбар **өөрийгөө зарлах** | самбар **системд холбогдох** | зарлах = to advertise / proclaim publicly |

### 2b. Physical verbs used for technical acts

| Wrong | Correct | Why |
|---|---|---|
| машиныг **дахин асаах** | машиныг **дахин ачаалах** | асаах = flip the power on. Reboot is ачаалах. |
| холболтыг **хаах** | холболтыг **таслах** | follows from хаалга above — keep it consistent |
| программ **суусан** | программ **суулгагдсан** | суух = to sit down |

### 2c. Loanwords that already mean something else

| Wrong | Correct | Why |
|---|---|---|
| **флот** (of machines) | **нийт машин** / **бүх машин** | флот = a naval fleet. Nothing else. |
| **хяналтын самбар** (dashboard) *next to* **самбар** (the hardware board) | dashboard → **нэгдсэн хяналтын дэлгэц** | one word was carrying two unrelated referents in one document |

### 2d. Phrases that simply do not exist

| Wrong | Correct |
|---|---|
| **зам хоног**, хүний нөөц зарцуулж | **замын зардал, цаг хугацаа**, хүний нөөц зарцуулж |
| **Ил нээлттэй** порт | **Нээлттэй** порт (redundant pair) |
| **хүний ойлгох** нэр | **хүнд ойлгомжтой** нэр |
| хандалт **өгөх** | хандалт **олгох** |

### 2e. Software-delivery terms — and the tool that settles them

**Source: a second session, same day (2026-09-21).** A ticket fix-note (an admin-panel
bug fix) was written *after* this file was loaded, and still rendered
*production environment* as **үйлдвэрлэлийн орчин**. The engineer rejected it on sight:
үйлдвэрлэл is factory manufacturing, so the sentence claimed a software fix had been
rolled out onto a plant floor. It had already been posted to a customer-visible ticket.

| English source | Calque produced (wrong) | Correct | Why it fails |
|---|---|---|---|
| production environment / prod | **үйлдвэрлэлийн** орчин | `prod` **орчин**; in running prose **бодит орчин** or **ашиглалтын орчин** | bolor-toli gives үйлдвэрлэл = output *(econ.)*, industry, manufacturing. "In live service" is not among its senses. |

**The default that removes the decision:** in a technical note, do not translate English
technical terms at all. If the tooling prints `prod-903f343d`, write `prod`. `staging`,
`pipeline`, `build`, `release`, `rollback`, `image` likewise. "Translate it, then check
its physical sense" needs judgment at every term; "don't translate it" needs none.

**Stop adding rows to this table.** Two independent sessions have now produced a calque
while this file was loaded — the table is consulted *while writing*, which is exactly
when it is not consulted. Two things that run without depending on that:

- `python3 ~/.claude/skills/mongolian-report-writing/bolor.py <үг>` — bolor-toli.com lookup. Prints what the Mongolian word actually
  means, with its domain tag. This is the fact the rule needs and does not have. Run it
  on any word you are about to use for a technical sense.
- `python3 ~/.claude/skills/mongolian-report-writing/bolor.py --scan <file>` — greps the measured blocklist over a finished draft. It
  needs no judgment and it goes red on the real fix-note text.

**Retraction, from running the lookup:** an earlier draft of this section claimed **дүрс**
was wrong for a Docker *image*. bolor-toli lists дүрс → image with a **comp.** tag, so
the claim is withdrawn. It was reasoned from the §1 physical-sense check and the check
was wrong. Two other guesses (staging → тайз, rollback → буцаах) were cut for the same
reason: nobody has shipped them, so they are not findings.

**Correct — do not "fix" these on a sweep:** **хөгжүүлэлтийн орчин** (dev) is the
established term. For *deploy*, both **ашиглалтад нэвтрүүлэх** and **серверт байршуулах**
are right; the fix-note's "нэвтрүүлсэн" was fine — only the noun beside it was wrong.

## 3. Brand names — the rule is already in SKILL.md §6 and was still broken

A Latin-script company name (e.g. **BrightLabs**) was written in Cyrillic (**БрайтЛабс**). Cyrillicizing a foreign
company or product name is the same error class: it produces a word that exists in no
register. Keep company names, product names, eBarimt, QPay as they are spelled at source.

Genuine Mongolian institution names still get STRUCTURE.md §5 treatment (full name
first, abbreviation in parentheses, short form after). Foreign names get nothing —
they are simply left alone.

## 4. What to do with the English source before translating

Do not translate the marketing sentence. **Translate what the system actually does.**

> EN: *"The system asks the machine to open a way in from its own side, and the machine
> shuts it whether you remembered to or not."*
>
> Wrong (translates the sentence): машинаас **хаалгаа** нээхийг хүсэж, машин түүнийг
> өөрөө **хаана**.
>
> Right (translates the mechanism): машинаас **холболтыг өөрийн талаас нь
> эхлүүлэхийг** хүснэ. Хугацаа дуусахад машин **холболтоо өөрөө таслана**.

The English page is written to be vivid. The Mongolian report is written to be exact.
They are not the same document and the second is not a translation of the first.

## 5. Also caught in the same pass — register, not vocabulary

- A colloquial quotation dropped into a report: *"яг одоо ямар байдалтай байна вэ" гэж
  асуухад* → **тухайн үеийн байдлыг шууд асуухад**. SKILL.md default 5 already bans
  news voice; a quoted question smuggles it back in.
- False positives to *not* "fix" on a grep sweep: **арга хэм-жээ** is a noun, not the
  `-жээ` evidential ending; **чимээгүйхэн олгох** (granted silently, without telling
  anyone) is correct and idiomatic — the ban is on чимээгүй for network traffic only.
