# Term picker evaluation

Produced by `python3 pick_terms.py eval` (index built 2026-11-12; tuning took 0 s). Every number below is printed by that command.

## Setup

- 24 confirmed terms sorted alphabetically (case-insensitive) and split by alternating position: half A = positions 0,2,4,..; half B = 1,3,5,... A: access/permission, bug, database, error, firewall, install, network, outage/downtime, server, token, upgrade, version. B: app/application, cloud, download, file, fix, login, notification, password, settings, update, user, website.
- Weights and thresholds were tuned on **A only** (grid in `docs/research/term-picker-params.json`): `{"w_ui": 1.0, "w_web": 1.0, "w_corp": 0.0, "tau_ui": 0.1, "tau_web": 0.2, "margin": 1.0, "min_ui": 3, "min_web": 2}`. B was not looked at during tuning.
- Truth is `terms.json` **official** write. *strict* = same words as the official rendering, up to inflection (`words_match`); *lenient* = pick is a contiguous sub/super n-gram of it (e.g. `татаж` for `татаж авах`).
- **Blind** = candidates come only from mining (terms.json renderings and the Latin form are not allowed to compete); this is the honest test, because seeding the answer into the pool is circular. **Seeded** = the production mode.

## Blind (mined only)

| set | strict | lenient | matches dev column |
|---|---|---|---|
| Half B (held out) | 5/12 | 7/12 | 5/12 |
| Half A (tuned) | 8/12 | 9/12 | 7/12 |
| All 24 | 13/24 | 16/24 | 12/24 |

- half B: 6 of 12 would be `auto` (ui/web agreement only); of those 3 are lenient-correct, 2 strict-correct.
- half A: 8 of 12 would be `auto` (ui/web agreement only); of those 8 are lenient-correct, 7 strict-correct.

## Seeded (production)

| set | strict | lenient | matches dev column |
|---|---|---|---|
| Half B (held out) | 5/12 | 7/12 | 5/12 |
| Half A (tuned) | 8/12 | 9/12 | 7/12 |
| All 24 | 13/24 | 16/24 | 12/24 |

- half B: 6 of 12 would be `auto` (ui/web agreement only); of those 3 are lenient-correct, 2 strict-correct.
- half A: 8 of 12 would be `auto` (ui/web agreement only); of those 8 are lenient-correct, 7 strict-correct.

## Per-term picks, blind mode

| half | term | official | blind pick | strict | lenient | signal decision |
|---|---|---|---|---|---|---|
| B | app/application | аппликэйшн | програм | no | no | auto |
| B | cloud | үүлэн технологи | cloud | no | no | auto |
| B | download | татаж авах | татаж авах | yes | yes | review |
| B | file | файл | файл | yes | yes | review |
| B | fix | засвар | тогтмол | no | no | auto |
| B | login | нэвтрэх | нэвтрэх | yes | yes | review |
| B | notification | мэдэгдэл | хүлээн авах болно | no | no | review |
| B | password | нууц үг | нууц | no | yes | review |
| B | settings | тохиргоо | тохиргоо | yes | yes | auto |
| B | update | шинэчлэл | шинэчлэх | yes | yes | auto |
| B | user | хэрэглэгч | хэрэг | no | no | review |
| B | website | вэб сайт | вэб | no | yes | auto |
| A | access/permission | хандалт | хандах | no | no | review |
| A | bug | алдаа | алдаа | yes | yes | review |
| A | database | өгөгдлийн сан | мэдээллийн сан | no | no | review |
| A | error | алдаа | алдаа | yes | yes | auto |
| A | firewall | галт хана | галт хана | yes | yes | auto |
| A | install | суулгах | суулгах | yes | yes | auto |
| A | network | сүлжээ | сүлжээ | yes | yes | auto |
| A | outage/downtime | үйлчилгээний тасалдал | цахилгаан тасарсан | no | no | review |
| A | server | сервер | сервер | yes | yes | auto |
| A | token | токен | токен | yes | yes | auto |
| A | upgrade | шинэчлэл | өгөгдлийг шинэчлэх | no | yes | auto |
| A | version | хувилбар | хувилбар | yes | yes | auto |

## The 9 reworked terms (production picks, `term-picks.json`)

| term | official now | pick | decision | why |
|---|---|---|---|---|
| session | нэвтрэлт | мэдээлэл алдагдав | review | sense none: no bolor-toli entry |
| crash | ажиллахаа зогсох | сүйрэл | auto | web only, decisive |
| log | системийн лог | лог | review | sense none: no bolor-toli entry |
| account | хэрэглэгчийн бүртгэл | бүртгэл | review | ui top бүртгэл vs web top данс |
| build | хувилбар | картуудыг хоосон тайзны | review | sense none: no bolor-toli entry |
| feature | боломж | функцийг ашиглаж | review | sense none: no bolor-toli entry |
| role | эрхийн түвшин | үүрэг | auto | web only, decisive |
| incident | саатал | ослын | review | sense flag: first sense 'bailout' non-technical |
| cloud | үүлэн технологи | cloud | auto | web only, decisive |

## The 36 unsure terms (production picks)

auto: 10, review: 26.

## Reading the numbers

- Production `auto` on the confirmed terms: 10 are auto, 8 of those match the official column leniently. Of the 5 confirmed terms decided by 'web only, decisive', 3 match.
- 17 of 60 production picks end in review only because bolor-toli has no entry for the surface form (junk n-gram, or a loanword the dictionary lacks).
- Seeded and blind agree because a rendering with no data cannot win; seeding only helps when the data is silent, and then the pick is empty rather than the old answer.
- Matcher history: `words_match` was tightened twice after the first run showed false agreements (хэрэглэгч vs хэрэгсэл, тохиргоо vs тохиромжтой, user vs хэрэг). The final matcher is the one scored above; the tuned parameters were re-fitted on A with it.
