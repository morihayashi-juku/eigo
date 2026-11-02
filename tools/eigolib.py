"""中1英語 教材棚 — プリント生成の共通部品。

各週のスクリプト（tools/week6.py など）が、問題データを書いて
このモジュールの部品で HTML を組み、Playwright（Chromium）で A4 PDF にする。

  python3 tools/week6.py          → pdf/w6_*.pdf を作る
  python3 tools/week6.py --html   → 確認用に HTML も tools/out/ に残す

決まり（CLAUDE.md と同じ）
- A4 縦。日本語 Noto Sans CJK JP、英語 Liberation Sans。
- 木曜は緑、月曜は青の見出し帯。各ページ右上に 月 日・名前欄。
- 英単語には必ずカタカナの読み（ruby）を付ける。READ に無い単語はエラーにする。
- こたえは同じページを answers=True で描き、正解を赤で囲む／赤字で書く。
"""
from __future__ import annotations

import html
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "pdf"

# ---------------------------------------------------------------- 読み（ルビ）
READ = {
    "i": "アイ", "am": "アム", "are": "アー", "is": "イズ", "a": "ア",
    "you": "ユー", "he": "ヒー", "she": "シー", "this": "ディス", "my": "マイ",
    "not": "ノット", "don't": "ドント", "do": "ドゥー",
    "student": "ステューデント", "teacher": "ティーチャー", "friend": "フレンド",
    "play": "プレイ", "like": "ライク", "eat": "イート", "have": "ハヴ",
    "study": "スタディ", "watch": "ウォッチ", "want": "ウォント",
    "speak": "スピーク", "read": "リード", "drink": "ドリンク", "use": "ユーズ",
    "know": "ノウ", "make": "メイク", "clean": "クリーン",
    "cook": "クック", "swim": "スイム",
    "soccer": "サッカー", "tennis": "テニス", "music": "ミュージック",
    "ramen": "ラーメン", "english": "イングリッシュ", "tv": "ティーヴィー",
    "baseball": "ベースボール", "bag": "バッグ", "japanese": "ジャパニーズ",
    "book": "ブック", "milk": "ミルク", "water": "ウォーター", "curry": "カレー",
    "room": "ルーム", "pen": "ペン", "computer": "コンピューター",
    "busy": "ビズィー", "sleepy": "スリーピー", "happy": "ハッピー",
    "kind": "カインド", "tall": "トール",
    "hi": "ハイ", "hello": "ハロー",
    "ken": "ケン", "yuki": "ユキ", "sho": "ショウ", "mika": "ミカ",
    "aya": "アヤ", "taku": "タク", "rina": "リナ",
}


DONT = "don't"


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def rb(sentence: str) -> str:
    """英文の各単語にカタカナのルビを付ける。"""
    out = []
    for tok in sentence.split():
        core = re.sub(r"^[^\w']+|[^\w']+$", "", tok)
        key = core.lower()
        if key not in READ:
            raise KeyError(f"読みが未登録: {core!r}（eigolib.READ に足してください）")
        out.append(f"<ruby>{esc(tok)}<rt>{READ[key]}</rt></ruby>")
    return '<span class="en">' + " ".join(out) + "</span>"


# ---------------------------------------------------------------- 文の型
class S:
    """否定文1つ分。kind は 'be'（be動詞＋not）か 'do'（don't）。"""

    def __init__(self, jp: str, en: str):
        self.jp = jp
        self.en = en
        self.kind = "do" if " don't " in f" {en} " else "be"
        assert self.kind == "do" or " not " in en, en

    # 日本語の最後（①）と、好き・ほしい（②）
    @property
    def end(self) -> str:
        return "ありません" if self.jp.rstrip("。").endswith("ありません") else "ません"

    @property
    def sukihoshi(self) -> bool:
        j = self.jp
        return "好きではありません" in j or "ほしくありません" in j

    @property
    def subj(self) -> str:
        return self.en.split()[0]

    @property
    def be(self) -> str:
        return {"I": "am", "You": "are"}.get(self.subj, "is")

    @property
    def rest(self) -> str:
        """主語と not / don't をのぞいたうしろ（例: 'kind.'、'like tennis.'）"""
        w = self.en.split()
        return " ".join(w[3:] if self.kind == "be" else w[2:])

    @property
    def pos_en(self) -> str:
        if self.kind == "be":
            return self.en.replace(" not ", " ", 1)
        return self.en.replace(" don't ", " ", 1)

    @property
    def pos_jp(self) -> str:
        j = self.jp
        if j.endswith("ではありません。"):
            return j[: -len("ではありません。")] + "です。"
        if j.endswith("くありません。"):
            return j[: -len("くありません。")] + "いです。"
        assert j.endswith("ません。"), j
        return j[: -len("ません。")] + "ます。"

    # よくある間違いの形
    def wrong(self) -> str:
        if self.kind == "be":
            return f"{self.subj} don't {self.rest}"
        return f"{self.subj} {self.be} not {self.rest}"

    def other_wrong(self) -> str:
        if self.kind == "be":
            return f"{self.subj} not {self.rest}"
        return f"{self.subj} not {self.rest}"

    def choices3(self) -> tuple[list[str], str]:
        """( ___ ) に入れる3択と正解。"""
        if self.kind == "be":
            ok = f"{self.be} not"
            opts = [ok, f"not {self.be}", "don't"]
        else:
            ok = "don't"
            opts = [ok, "not", f"{self.be} not"]
        return opts, ok


def shuffled(items, seed, keep_not_first=False):
    r = random.Random(str(seed))
    items = list(items)
    first = items[0]
    for _ in range(20):
        r.shuffle(items)
        if not keep_not_first or items[0] != first:
            break
    return items


# ---------------------------------------------------------------- ページの枠
CSS = r"""
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: "Noto Sans CJK JP", sans-serif; color: #1b1f24; font-size: 10.5pt; line-height: 1.5;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; padding: 9mm 11mm 8mm; position: relative; overflow: hidden;
  page-break-after: always; break-after: page; display: flex; flex-direction: column; gap: 3.4mm; }
.page:last-child { page-break-after: auto; break-after: auto; }
.thu { --c: #2c7a52; --soft: #e6f3ec; }
.mon { --c: #2a5ca6; --soft: #e6eef9; }
.en { font-family: "Liberation Sans", "Noto Sans CJK JP", sans-serif; }
ruby { ruby-position: over; }
rt { font-family: "Noto Sans CJK JP", sans-serif; font-size: 6.4pt; color: #6b7480; font-weight: 400; letter-spacing: .02em; }

/* 見出し帯 */
.hd { display: grid; grid-template-columns: 21mm 1fr 52mm; border: 1.6px solid var(--c); border-radius: 3mm; overflow: hidden; min-height: 21mm; flex: none; }
.hd .tag { background: var(--c); color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; line-height: 1.15; }
.hd .tag .d { font-size: 7.5pt; font-weight: 700; text-align: center; }
.hd .tag .no { font-size: 15pt; font-weight: 900; font-family: "Liberation Sans", sans-serif; margin-top: 1mm; }
.hd .mid { padding: 2.2mm 3.5mm; display: flex; flex-direction: column; justify-content: center; }
.hd .mid .sub { font-size: 7.2pt; color: var(--c); font-weight: 700; }
.hd .mid .ttl { font-size: 13.5pt; font-weight: 900; line-height: 1.25; margin-top: .5mm; }
.hd .nm { border-left: 1px solid #c9d0d8; padding: 1.8mm 2.5mm; font-size: 7.5pt; display: grid; grid-template-rows: 1fr 1fr; }
.hd .nm div { border-bottom: 1px solid #9aa3ad; }

/* セクション見出し */
.sec { display: flex; align-items: baseline; gap: 2mm; font-weight: 700; font-size: 11pt; margin-top: 1.4mm; flex: none; }
.sec .num { background: #f2a64b; color: #fff; border-radius: 99px; padding: 0 2.6mm; font-size: 8.5pt; font-weight: 900; white-space: nowrap; }
.sec .s { font-size: 7.3pt; color: #5d6670; font-weight: 400; }
.sec .pt { margin-left: auto; font-size: 7.3pt; color: #5d6670; font-weight: 400; white-space: nowrap; }
.lead { font-size: 9pt; color: #333; }
.small { font-size: 8pt; color: #5d6670; }
.cn { display: inline-flex; width: 4.6mm; height: 4.6mm; border: 1px solid #333; border-radius: 50%; align-items: center; justify-content: center; font-size: 7pt; flex: none; }

/* 表 */
table.t { width: 100%; border-collapse: collapse; }
table.t th { background: #eef1f5; font-size: 7.3pt; font-weight: 700; padding: 1.2mm 1.5mm; border: 1px solid #c7ced6; }
table.t td { border: 1px solid #c7ced6; padding: 1mm 2mm; vertical-align: middle; }
table.t td.no { width: 6mm; text-align: center; font-size: 7.5pt; color: #555; }
.word { font-family: "Liberation Sans", sans-serif; font-weight: 700; font-size: 15pt; }
.boxes { color: #9aa3ad; letter-spacing: 1.2mm; font-size: 9pt; white-space: nowrap; }
.wt td { height: 11.4mm; font-size: 9.8pt; }
.wt td.word { font-size: 16pt; }

/* ポイント */
.point { border: 1.6px solid #e2483d; border-radius: 3mm; padding: 5mm 4.5mm 4mm; position: relative; flex: none; }
.point > .lab { position: absolute; top: -2.6mm; left: 4mm; background: #e2483d; color: #fff; font-weight: 900; font-size: 7.6pt; padding: .2mm 3mm; border-radius: 99px; }
.point .big { font-weight: 900; font-size: 12pt; margin-bottom: 1.6mm; }
.red { color: #e2483d; }
.cmp { width: 100%; border-collapse: collapse; font-size: 9.4pt; }
.cmp th { font-size: 7.6pt; padding: 1mm 1.5mm; }
.cmp th.be { background: #e8f1fb; color: #2a5ca6; }
.cmp th.do { background: #fdf0e4; color: #c2410c; }
.cmp td { border: 1px solid #d5dbe2; padding: 2mm 2.4mm; vertical-align: top; }
.cmp td.k { background: #f6f7f9; font-weight: 700; white-space: nowrap; width: 26mm; }
.cmp .en { font-size: 13pt; }
.why { margin-top: 2.4mm; font-size: 9.2pt; display: grid; gap: 1.4mm; }
.why .ic { display: inline-flex; width: 4.4mm; height: 4.4mm; border-radius: 50%; background: #f2c94c; color: #fff; font-weight: 900; justify-content: center; align-items: center; font-size: 7pt; margin-right: 1.5mm; }
.ng { color: #e2483d; }
.why .ng { font-family: "Liberation Sans", sans-serif; }

/* 文と選択肢 */
.q { display: grid; grid-template-columns: 6mm 1fr; column-gap: 1.5mm; align-items: start; }
.q .jp { font-size: 9.6pt; }
.line-en { font-size: 14pt; margin: .6mm 0 0 3mm; }
.opt { display: inline-block; padding: 0 1.2mm; border-radius: 99px; }
.par { white-space: nowrap; }
.bg { font-size: 9pt; white-space: nowrap; }
.answers .c { box-shadow: 0 0 0 1.4px #e11d2e; color: #e11d2e; }
.answers .page::after { content: "こたえ"; position: absolute; top: 2.2mm; left: 50%; transform: translateX(-50%);
  color: #e11d2e; border: 1.4px solid #e11d2e; border-radius: 99px; padding: 0 4mm; font-size: 8pt; font-weight: 900; background: #fff; }
.fill { display: none; }
.answers .fill { display: inline; color: #e11d2e; font-weight: 700; }
.answers .fillblock { display: block; }
.wline { border-bottom: 1px solid #555; min-height: 10mm; display: flex; align-items: flex-end; padding: 0 1mm .6mm; }

/* カード */
.cards { display: flex; gap: 1.6mm; flex-wrap: wrap; align-items: flex-end; }
.card { border: 1px solid #8b949e; border-radius: 1.4mm; padding: 0 2.2mm .6mm; background: #fff; font-size: 13.5pt; box-shadow: 0 .4mm 0 #c9d0d8; }
.cardq { display: grid; grid-template-columns: 6mm 56mm 1fr; column-gap: 2mm; align-items: start; }
.ansline { grid-column: 2 / 4; border-bottom: 1px solid #555; height: 14mm; display: flex; align-items: flex-end; padding: 0 2mm 1mm; font-size: 14pt; }

/* 判断の表（①②③） */
.judge td { height: 11.6mm; font-size: 9.6pt; }
.judge td.ch { text-align: center; white-space: nowrap; }
.judge td.ch .opt { margin: 0 .6mm; }
.skip { display: none; }
.answers .skip { display: inline; color: #e11d2e; font-weight: 700; font-size: 8pt; }
.answers .hide-if-skip { display: none; }

/* 読む文 */
.read { border: 1.6px solid #8b6bd1; background: #f6f2fd; border-radius: 3mm; padding: 2.6mm 4mm; font-size: 14pt; line-height: 2.3; flex: none; }
.rq { display: grid; grid-template-columns: 6mm 1fr 1fr; gap: 1.5mm; align-items: center; font-size: 10pt; }

/* ストップ・まとめ */
.stop { border: 1.8px solid #e8711a; background: #fff8f0; border-radius: 3mm; padding: 2.8mm 4mm; font-size: 9.4pt; line-height: 1.7; margin-top: auto; flex: none; }
.stop b.h { color: #e8711a; font-size: 10pt; margin-right: 3mm; }
.blank { display: inline-block; border-bottom: 1px solid #333; min-width: 13mm; text-align: center; }
.steps { display: grid; grid-template-columns: repeat(6, 1fr); gap: 1.4mm; flex: none; }
.steps div { border: 1px solid #b9c2cc; border-radius: 1.6mm; text-align: center; font-size: 7.3pt; padding: .8mm 0; line-height: 1.3; }
.steps small { color: #6b7480; font-size: 6.6pt; }
.howto { border: 1.6px dashed var(--c); border-radius: 3mm; padding: 3mm 4mm; font-size: 9pt; margin-top: auto; display: grid; grid-template-columns: 1fr auto; gap: 1.2mm 4mm; }
.howto .score { grid-row: 1 / 3; grid-column: 2; align-self: start; border: 1.6px solid var(--c); border-radius: 2mm; padding: 1.2mm 3mm; font-weight: 900; font-size: 10pt; }
.memo { grid-column: 1 / 3; border: 1px solid #b9c2cc; border-radius: 1.6mm; height: 8mm; font-size: 6.8pt; color: #8a939d; padding: .6mm 1.6mm; }
.chant { border: 1.6px solid var(--c); background: var(--soft); border-radius: 3mm; padding: 2.2mm 4mm; font-size: 9.4pt; flex: none; }
.chant b { color: var(--c); }
.chant .en { font-size: 13pt; margin-right: 2.6mm; }

/* 小テスト（A4に上下2つ） */
.half { height: calc((297mm - 17mm) / 2 - 4mm); display: flex; flex-direction: column; gap: 2mm; position: relative; }
.cut { text-align: center; font-size: 7pt; color: #8a939d; border-top: 1.4px dashed #9aa3ad; margin: 2mm 0; line-height: 0; flex: none; }
.cut span { background: #fff; padding: 0 3mm; position: relative; top: -.2mm; }
.scorebox { align-self: flex-end; margin-top: auto; border: 1.6px solid var(--c); border-radius: 2mm; padding: 1mm 3mm; font-weight: 900; font-size: 10pt; white-space: nowrap; }
.mq { display: grid; grid-template-columns: 6mm 52mm 1fr; column-gap: 2mm; align-items: center; font-size: 9pt; }
.mq .en { font-size: 12pt; }
"""


def header(day: str, kind_label: str, no: int, unit: str, sub: str, title: str, dow: str | None = None) -> str:
    """kind_label は「木曜<br>じゅぎょう」のような HTML。dow は日付欄の曜日（省略時は day から）。"""
    dow = dow or {"thu": "木", "mon": "月"}[day]
    date = f"月　　日（{dow}）"
    return f"""
<div class="hd"><div class="tag"><div class="d">{kind_label}</div><div class="no">No.{no}</div></div>
<div class="mid"><div class="sub">{esc(unit)}　{esc(sub)}</div><div class="ttl">{esc(title)}</div></div>
<div class="nm"><div>{date}</div><div>名前</div></div></div>"""


def sec(num: str, text: str, s: str = "", pt: str = "") -> str:
    return (f'<div class="sec"><span class="num">{esc(num)}</span><span>{text}</span>'
            + (f'<span class="s">{s}</span>' if s else "")
            + (f'<span class="pt">{esc(pt)}</span>' if pt else "") + "</div>")


def cn(i: int) -> str:
    return f'<span class="cn">{i}</span>'


def opt(text: str, correct: bool, en: bool = False) -> str:
    inner = rb(text) if en else esc(text)
    return f'<span class="opt{" c" if correct else ""}">{inner}</span>'


# ---------------------------------------------------------------- 部品
def word_table(words, mode: str, seed=0) -> str:
    """words: [(英語, 意味)]。mode='read'（読めた□□□）か 'choose'（意味を3択）"""
    if mode == "read":
        rows = "".join(
            f'<tr><td class="no">{i}</td><td class="word">{esc(w)}</td><td>{READ[w.lower()]}</td>'
            f'<td>{esc(m)}</td><td class="boxes">□□□</td></tr>'
            for i, (w, m) in enumerate(words, 1))
        head = "<th></th><th>英語</th><th>読み</th><th>意味</th><th>読めた</th>"
        return f'<table class="t wt"><colgroup><col><col style="width:30mm"><col style="width:28mm"><col><col style="width:22mm"></colgroup><tr>{head}</tr>{rows}</table>'
    allm = [m for _, m in words]
    rows = ""
    for i, (w, m) in enumerate(words, 1):
        r = random.Random(f"{seed}-{w}")
        others = [x for x in allm if x != m]
        ch = r.sample(others, 2)
        ch.insert((i + len(str(seed))) % 3, m)  # 正解の位置を 1→2→3 と順にずらす
        cells = " ／ ".join(opt(x, x == m) for x in ch)
        rows += (f'<tr><td class="no">{i}</td><td class="word">{esc(w)}</td><td>{READ[w.lower()]}</td>'
                 f'<td class="par">（ {cells} ）</td></tr>')
    head = "<th></th><th>英語</th><th>読み</th><th>意味はどれ？ ○ でかこもう</th>"
    return f'<table class="t wt"><colgroup><col><col style="width:30mm"><col style="width:28mm"><col></colgroup><tr>{head}</tr>{rows}</table>'


def point_box(label="ポイント") -> str:
    return f"""
<div class="point"><span class="lab">{label}</span>
<div class="big">「好き」「ほしい」だけは、「ありません」でも <span class="red">don't</span>！</div>
<table class="cmp">
<tr><th></th><th class="be">be動詞＋not になる</th><th class="do">don't になる（例外はこの2つ）</th></tr>
<tr><td class="k">〜ではありません</td>
<td>かれは 親切ではありません。<br>{rb("He is not kind.")}</td>
<td>わたしは テニスが <b>好き</b>ではありません。<br>{rb("I don't like tennis.")}</td></tr>
<tr><td class="k">〜くありません</td>
<td>わたしは 背が高くありません。<br>{rb("I am not tall.")}</td>
<td>わたしは かばんが <b>ほしく</b>ありません。<br>{rb("I don't want a bag.")}</td></tr>
</table>
<div class="why">
<div><span class="ic">?</span><b>どうして？</b>「好き」は <b>like</b>、「ほしい」は <b>want</b>。英語では<b>動詞（一般動詞）</b>だから、be動詞は使わない。</div>
<div><span class="ic">?</span><b>見分けかた</b>：① 最後が「〜ません」（しません・泳ぎません）→ don't　② 「ありません」なら、好き・ほしい？ → はい なら don't　③ それ以外の「ありません」→ be動詞＋not</div>
<div><span class="ic">!</span><b>よくあるまちがい</b>：<span class="ng">× I am not like tennis.　× I am not want a bag.　× He don't kind.</span></div>
</div></div>"""


def judge_table(items: list[S]) -> str:
    rows = ""
    for i, s in enumerate(items, 1):
        e = s.end
        if e == "ません":
            q2 = ('<span class="hide-if-skip">はい ／ いいえ</span><span class="skip">とばす</span>')
        else:
            q2 = f'{opt("はい", s.sukihoshi)} ／ {opt("いいえ", not s.sukihoshi)}'
        rows += (f'<tr><td class="no">{i}</td><td>{esc(s.jp)}</td>'
                 f'<td class="ch">{opt("ありません", e == "ありません")} ／ {opt("ません", e == "ません")}</td>'
                 f'<td class="ch">{q2}</td>'
                 f'<td class="ch">{opt("be＋not", s.kind == "be")} ／ {opt(DONT, s.kind == "do")}</td></tr>')
    head = ('<th></th><th>日本語</th><th>① 最後は？</th>'
            '<th>② 好き・ほしい？<br><span style="font-weight:400">（「ありません」のときだけ）</span></th><th>③ どっち？</th>')
    return (f'<table class="t judge"><colgroup><col><col><col style="width:30mm"><col style="width:30mm"><col style="width:28mm"></colgroup>'
            f'<tr>{head}</tr>{rows}</table>'
            '<div class="small">①が「ません」（しません・泳ぎません など）なら②はとばして③へ。①〜③が全部合って1点。</div>')


def choose_list(items: list[S], seed) -> str:
    out = []
    for i, s in enumerate(items, 1):
        opts, ok = s.choices3()
        opts = shuffled(opts, f"{seed}-{i}-{s.en}")
        cells = " ／ ".join(opt(o, o == ok, en=True) for o in opts)
        bg = f'（ {opt("be", s.kind == "be")} ・ {opt("一般", s.kind == "do")} ）'
        out.append(
            f'<div class="q">{cn(i)}<div><div style="display:flex;justify-content:space-between"><span class="jp">{esc(s.jp)}</span><span class="bg">{bg}</span></div>'
            f'<div class="line-en">{rb(s.subj)} <span class="par">( {cells} )</span> {rb(s.rest)}</div></div></div>')
    return ('<div style="display:grid;gap:2.6mm">' + "".join(out) + "</div>"
            '<div class="small">先に（be・一般）を ○ してから、答えを ○。両方合って1点。</div>')


def fix_list(items: list[S], seed) -> str:
    out = []
    for i, s in enumerate(items, 1):
        pair = shuffled([s.en, s.other_wrong()], f"{seed}-{i}")
        a, b = pair
        out.append(
            f'<div class="q">{cn(i)}<div><div style="display:grid;grid-template-columns:66mm 1fr;align-items:end">'
            f'<span class="jp">{esc(s.jp)}</span><span class="line-en" style="margin:0"><span class="ng">× </span>{rb(s.wrong())}</span></div>'
            f'<div class="line-en" style="margin-top:1.4mm">→ <span style="font-size:9pt">正しいのは</span>　'
            f'{opt("ア", a == s.en)} {rb(a)}　　{opt("イ", b == s.en)} {rb(b)}</div></div></div>')
    return '<div style="display:grid;gap:4mm">' + "".join(out) + "</div>"


def meaning_list(items: list[S]) -> str:
    out = []
    for i, s in enumerate(items, 1):
        out.append(f'<div class="q" style="grid-template-columns:6mm 70mm 1fr;align-items:end">{cn(i)}'
                   f'<div class="line-en" style="margin:0">{rb(s.en)}</div>'
                   f'<div class="wline"><span class="fill">{esc(s.jp)}</span></div></div>')
    return '<div style="display:grid;gap:3.4mm">' + "".join(out) + "</div>"


def card_list(items: list[tuple[S, list[str]]], seed) -> str:
    out = []
    for i, (s, chunks) in enumerate(items, 1):
        assert " ".join(chunks) == s.en, (chunks, s.en)
        cards = shuffled(chunks, f"{seed}-{i}", keep_not_first=True)
        if cards == chunks:
            cards = cards[1:] + cards[:1]
        c = "".join(f'<span class="card">{rb(x)}</span>' for x in cards)
        out.append(f'<div class="cardq">{cn(i)}<span class="jp" style="font-size:8.6pt">{esc(s.jp)}</span>'
                   f'<div class="cards">{c}</div><div class="ansline"><span class="fill en">{esc(s.en)}</span></div></div>')
    return '<div style="display:grid;gap:3.6mm">' + "".join(out) + "</div>"


def reading(text: str, qs) -> str:
    """qs: [(質問, [選択肢2つ], 正解)]"""
    rows = "".join(
        f'<div class="rq">{cn(i)}<span>{esc(q)}</span><span>（ {opt(a, a == ok)} ／ {opt(b, b == ok)} ）</span></div>'
        for i, (q, (a, b), ok) in enumerate(qs, 1))
    return f'<div class="read">{rb(text)}</div><div style="display:grid;gap:3.4mm;padding:0 2mm">{rows}</div>'


def stop_box(part: str) -> str:
    return f"""<div class="stop"><b class="h">ストップ！ ここで丸つけ</b>{part}の点数 <span class="blank"></span>／25<br>
まちがいが <b>2つ以上</b> → まちがい分析シートで <b>1問</b> えらんで、ノートに5行で書いてから次へ。<br>
□ 丸つけした　　□ ノートに書いた（まちがい1つ以下ならとばしてOK）</div>"""


# ---------------------------------------------------------------- 小テスト（6問）
def mini_quiz(day: str, kind_label: str, no: int, unit: str, sub: str, title: str, q, dow: str | None = None) -> str:
    """q = {'which':[S,S], 'choose':[S,S], 'mean':[S,S]}"""
    which = "".join(
        f'<div class="q" style="grid-template-columns:6mm 1fr 44mm">{cn(i)}<span class="jp">{esc(s.jp)}</span>'
        f'<span class="par">（ {opt("be＋not", s.kind == "be")} ／ {opt(DONT, s.kind == "do")} ）</span></div>'
        for i, s in enumerate(q["which"], 1))
    mean = ""
    for i, s in enumerate(q["mean"], 1):
        a, b = (s.jp, s.pos_jp) if (i + len(sub)) % 2 else (s.pos_jp, s.jp)  # 正解がア・イ交互になるように
        mean += (f'<div class="mq">{cn(i)}{rb(s.en)}<span>{opt("ア", a == s.jp)} {esc(a)}　{opt("イ", b == s.jp)} {esc(b)}</span></div>')
    return f"""<div class="half">{header(day, kind_label, no, unit, sub, title, dow)}
{sec("1", "否定文にするとき、どっちを使う？ ○ でかこもう")}
<div style="display:grid;gap:1.4mm">{which}</div>
{sec("2", "日本語に合うほうを ○ でかこもう")}
{choose_list(q["choose"], f"q{no}{sub}")}
{sec("3", "英文を読んで、意味はどっち？ ア・イ を ○")}
<div style="display:grid;gap:1.6mm">{mean}</div>
<div class="scorebox">点数 <span class="blank"></span> / 6</div></div>"""


# ---------------------------------------------------------------- PDF
def html_doc(pages: list[str], answers=False) -> str:
    return (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body class="{"answers" if answers else ""}">' + "".join(pages) + "</body></html>")


def write_pdfs(jobs: dict[str, str], keep_html=False):
    from playwright.sync_api import sync_playwright
    out_html = Path(__file__).resolve().parent / "out"
    if keep_html:
        out_html.mkdir(exist_ok=True)
    PDF_DIR.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for name, doc in jobs.items():
            if keep_html:
                (out_html / (name.replace(".pdf", ".html"))).write_text(doc, encoding="utf-8")
            pg.set_content(doc, wait_until="load")
            pg.evaluate("document.fonts.ready")
            # はみ出しチェック
            over = pg.evaluate("""() => [...document.querySelectorAll('.page')].map((p,i)=>
                [i+1, p.scrollHeight - p.clientHeight]).filter(x=>x[1]>1)""")
            if over:
                print(f"  !! {name}: はみ出し {over}")
            pg.pdf(path=str(PDF_DIR / name), format="A4", print_background=True,
                   margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            print("  wrote", name)
        b.close()
