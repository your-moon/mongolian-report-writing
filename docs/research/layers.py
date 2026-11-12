import lzma, re, sys, collections, json, os
PAIRS = {  # pairs/groups of competing spellings or words; counted as whole-word stems
 "program":   [r"программ", r"програм(?!м)"],
 "internet":  [r"интернэт", r"интернет"],
 "system":    [r"систем(?!ат)", r"систэм"],
 "web":       [r"вэб", r"веб"],
 "computer":  [r"компьютер", r"компьютэр", r"компютер"],
 "server":    [r"сервер", r"сэрвэр", r"сервэр"],
 "reboot":    [r"дахин асаа", r"дахин ачаал", r"дахин эхлүүл", r"перезагруз"],
 "session":   [r"сесс", r"сеанс", r"нэвтрэлт", r"логик холболт"],
 "account":   [r"акаунт", r"аккаунт", r"хэрэглэгчийн бүртгэл"],
 "browser":   [r"браузер", r"броузер", r"хөтөч"],
 "firewall":  [r"галт хана", r"хамгаалалттай гарц", r"брандмауэр"],
 "feature":   [r"онцлог", r"функц"],
 "encryption":[r"шифрлэ", r"нууцла"],
 "log":       [r"лог(?![иоу])", r"системийн бүртгэл"],
 "cloud":     [r"үүлэн технологи", r"үүлэн үйлчилгээ", r"клауд"],
 "crash":     [r"гацс", r"гацах", r"ажиллахаа зогс", r"унтарс"],
 "incident":  [r"саатал", r"доголдол", r"зөрчил"],
 "update":    [r"шинэчлэлт", r"шинэчлэл(?!т)"],
 "app":       [r"апп(?!лик)", r"аппликэйшн", r"аппликейшн", r"программ хангамж"],
}
TECH = re.compile(r"сервер|систем|программ|програм|апп|интернэт|интернет|компьютер|вэб|веб|өгөгдөл|файл|утас|хэрэглэгч")
rx = {k: [re.compile(r"(?<![а-яөүё])" + p) for p in v] for k, v in PAIRS.items()}
cnt = {k: [[0, 0] for _ in v] for k, v in PAIRS.items()}   # [all, tech]
ex = {k: [None for _ in v] for k, v in PAIRS.items()}
n = 0
with lzma.open(sys.argv[1], "rt", encoding="utf-8", errors="ignore") as f:
    for line in f:
        n += 1
        low = line.lower()
        tech = bool(TECH.search(low))
        for k, rs in rx.items():
            for i, r in enumerate(rs):
                if r.search(low):
                    cnt[k][i][0] += 1
                    if tech:
                        cnt[k][i][1] += 1
                        if ex[k][i] is None and len(line) < 200: ex[k][i] = line.strip()
print(f"{n} sentences")
for k, v in PAIRS.items():
    print(f"\n{k}")
    for i, p in enumerate(v):
        print(f"  {p:<24} all={cnt[k][i][0]:>7}  tech={cnt[k][i][1]:>7}   {(ex[k][i] or '')[:110]}")
