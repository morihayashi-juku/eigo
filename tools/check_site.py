"""サイトのデータ（data/*.json）と pdf/ が合っているか確かめる。push の前に実行する。

  python3 tools/check_site.py

- JSON が読めるか
- 書いてある PDF が pdf/ にあるか、ファイル名が英数字だけか
- ページ数が PDF の本当のページ数と同じか（pdfinfo を使う）
- units が data/common.json の単元にあるか、id がかぶっていないか、cur（今ここ）が1つか
- pdf/ にあるのにどこにも書かれていない PDF（警告だけ）
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
err, warn = [], []


def load(name):
    try:
        return json.loads((ROOT / "data" / f"{name}.json").read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        err.append(f"data/{name}.json が読めません: {e}")
        return None


def pages(f):
    try:
        out = subprocess.run(["pdfinfo", str(ROOT / "pdf" / f)], capture_output=True, text=True).stdout
        m = re.search(r"^Pages:\s+(\d+)", out, re.M)
        return int(m.group(1)) if m else None
    except FileNotFoundError:
        return None


common = load("common")
units = {u["id"] for u in (common or {}).get("units", [])}
used = set()
for track in ("futari", "hitori"):
    d = load(track)
    if not d:
        continue
    items = [("ずっと使うもの", it) for it in d.get("common", [])] + [("過去の版", it) for it in d.get("old", [])]
    ids = [s["id"] for s in d["sets"]]
    if len(ids) != len(set(ids)):
        err.append(f"{track}: sets の id がかぶっています {ids}")
    curs = [s["id"] for s in d["sets"] if s.get("cur")]
    if len(curs) > 1:
        err.append(f"{track}: cur（今ここ）が2つ以上あります {curs}")
    for s in d["sets"]:
        for u in s.get("units", []):
            if u not in units:
                err.append(f"{track} {s['label']}: 単元 {u!r} が data/common.json にありません")
        for g in s["groups"]:
            items += [(f"{s['label']} {g['label']}", it) for it in g["items"]]
    for where, it in items:
        f = it["file"]
        used.add(f)
        if not re.fullmatch(r"[A-Za-z0-9_.\-]+\.pdf", f):
            err.append(f"{track} {where}: ファイル名は英数字だけにする: {f}")
        if not (ROOT / "pdf" / f).exists():
            err.append(f"{track} {where}: pdf/{f} がありません")
            continue
        n = pages(f)
        if n is not None and n != it.get("pages"):
            err.append(f"{track} {where}: {f} のページ数は {n} です（JSON は {it.get('pages')}）")

for p in sorted((ROOT / "pdf").glob("*.pdf")):
    if p.name not in used:
        warn.append(f"pdf/{p.name} はどこにも書かれていません")

for w in warn:
    print("注意:", w)
for e in err:
    print("エラー:", e)
print("OK" if not err else f"{len(err)} 件のエラー")
sys.exit(1 if err else 0)
