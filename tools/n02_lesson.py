"""新しく入った子 n02 の授業プリント（n01「be動詞・一般動詞の否定文と疑問文」の復習・定着）。

木曜40分・4ページ。n01 と同じ見た目（左に問題、右にヒントの帯）で、問題はすべて新しい文。
こたえは同じページに赤で答えを入れて出すので、問題とこたえがずれない。

  python3 tools/n02_lesson.py          → pdf/n02_fukushu.pdf, pdf/n02_fukushu_answers.pdf
  python3 tools/n02_lesson.py --html   → 確認用 HTML も tools/out/ に
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "pdf"
OUT = "n02_fukushu"
FOOT = "中1英語　否定文と疑問文の復習（n02）"


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- 部品
def ch(*opts, ok: str) -> str:
    """( A / B ) の2択。こたえでは正解を赤丸で囲む。"""
    assert ok in opts, (opts, ok)
    inner = " / ".join(f'<span class="o{" c" if o == ok else ""}">{esc(o)}</span>' for o in opts)
    return f'<span class="par">( {inner} )</span>'


def bg(ok: str) -> str:
    return ch("be動詞", "一般動詞", ok={"be": "be動詞", "do": "一般動詞"}[ok])


def line(answer: str, label: str = "", short: bool = False) -> str:
    lab = f'<span class="lab">{esc(label)}</span>' if label else ""
    return (f'<div class="ln{" short" if short else ""}">{lab}<div class="u"><span class="a">{esc(answer)}</span></div></div>')


def sec(n: int, text: str, s: str = "") -> str:
    return (f'<div class="sec"><span class="n">{n}</span><span>{text}</span>'
            + (f'<span class="s">{s}</span>' if s else "") + "</div>")


def item(no: int, body: str, after: str = "") -> str:
    return f'<div class="it"><span class="no">{no}.</span><div class="b"><div class="q">{body}</div>{after}</div></div>'


def side_box(title: str, body: str, cls: str = "") -> str:
    return f'<div class="box {cls}"><div class="bt">{title}</div>{body}</div>'


def words(ws) -> str:
    rows = "".join(f'<span class="en we">{esc(e)}</span><span>{esc(r)}　{esc(j)}</span>' for e, r, j in ws)
    return f'<div class="box plain"><div class="bt">使う単語</div><div class="wl">{rows}</div></div>'


def page(no: int, title: str, sub: str, left: str, side: str) -> str:
    return f"""<div class="page">
<div class="hd"><span class="tag">否定・疑問<br>復習 {no}</span>
<div class="tt"><div class="ttl">{esc(title)}</div><div class="sub">{esc(sub)}</div></div>
<div class="nm"><div>月　　日（木）</div><div>名前</div></div></div>
<div class="main"><div class="left">{left}</div><div class="side">{side}</div></div>
<div class="foot">{FOOT}　{no}／4</div></div>"""


# ---------------------------------------------------------------- 1ページ目：作り分け
P1_MAKE = [  # (文, 種類, 否定文, 疑問文)
    ("Mai is a teacher.", "be", "Mai is not a teacher.", "Is Mai a teacher?"),
    ("Ken plays the piano.", "do", "Ken doesn't play the piano.", "Does Ken play the piano?"),
    ("You are hungry.", "be", "You are not hungry.", "Are you hungry?"),
    ("They have a dog.", "do", "They don't have a dog.", "Do they have a dog?"),
    ("Aya studies math.", "do", "Aya doesn't study math.", "Does Aya study math?"),
]
P1_CHOOSE = [
    ("My father", ("isn't", "doesn't"), "isn't", "busy."),
    ("", ("Are", "Do"), "Do", "they live in Osaka?"),
    ("She", ("don't", "doesn't"), "doesn't", "have a bike."),
    ("", ("Is", "Does"), "Is", "your sister a student?"),
]


def p1() -> str:
    make = "".join(item(i, f'<span class="en big">{esc(s)}</span>　{bg(k)}',
                        line(neg, "否定文") + line(q, "疑問文"))
                   for i, (s, k, neg, q) in enumerate(P1_MAKE, 1))
    choose = "".join(item(i, f'<span class="en big">{esc(a)} {ch(*o, ok=ok)} {esc(b)}</span>')
                     for i, (a, o, ok, b) in enumerate(P1_CHOOSE, 1))
    left = (sec(1, "be動詞か一般動詞かを ○ でかこみ，否定文と疑問文を書こう。")
            + f'<div class="list">{make}</div>'
            + sec(2, "正しいほうを ○ でかこもう。")
            + f'<div class="list tight">{choose}</div>')
    side = (side_box("まず「どっちの文？」", '文に <b>am / is / are</b> がある？'
                     '<div class="yn"><div class="y"><b>ある</b><br>be動詞の文</div><div class="n"><b>ない</b><br>一般動詞の文</div></div>')
            + side_box("文の形 まとめ",
                       '<div class="fm"><b>be動詞</b><br>否定：主語 + be + <span class="r">not</span> ～.<br>疑問：<span class="r">Be</span> + 主語 ～?</div>'
                       '<div class="fm"><b>一般動詞</b><br>否定：主語 + <span class="r">don\'t / doesn\'t</span> + 動詞.<br>疑問：<span class="r">Do / Does</span> + 主語 + 動詞 ～?</div>')
            + side_box("does のときは s をとる！",
                       '<span class="en">Ken plays</span> → <span class="en">Ken doesn\'t <b>play</b></span><br>'
                       '<span class="en">Aya studies</span> → <span class="en">Does Aya <b>study</b> ～?</span><br>'
                       '<span class="en">She has</span> → <span class="en">She doesn\'t <b>have</b></span>', "warn")
            + words([("piano", "ピアノ", "ピアノ"), ("math", "マス", "数学"), ("live in", "リヴ イン", "〜に住む"),
                     ("father", "ファーザー", "父"), ("sister", "シスター", "姉・妹")]))
    return page(1, "作り分けよう", "n01 のふりかえり　否定文と疑問文を両方書く", left, side)


# ---------------------------------------------------------------- 2ページ目：答え方
P2_ANSWER = [  # (質問, Yes/No, こたえ)
    ("Are you a student?", "Yes", "Yes, I am."),
    ("Is Ken your friend?", "No", "No, he isn't."),
    ("Do you like soccer?", "Yes", "Yes, I do."),
    ("Does Mai play tennis?", "No", "No, she doesn't."),
    ("Are they in the park?", "Yes", "Yes, they are."),
    ("Does your mother cook?", "Yes", "Yes, she does."),
    ("Is this your bag?", "No", "No, it isn't."),
    ("Do Ken and Mai study English?", "No", "No, they don't."),
]
P2_FILL = [  # (前, うしろ, 種類, こたえ)
    ("", "you like music?", "疑問文", "Do"),
    ("", "Ken tall?", "疑問文", "Is"),
    ("", "your sister swim?", "疑問文", "Does"),
    ("We", "busy.", "否定文", "aren't"),
    ("I", "have a pen.", "否定文", "don't"),
    ("My father", "watch TV.", "否定文", "doesn't"),
]


def p2() -> str:
    ans = "".join(
        item(i, f'<span class="en big">{esc(q)}</span>　<span class="yn-tag">（{yn}）</span>',
             f'<div class="ln short"><span class="lab en">— </span><div class="u"><span class="a">{esc(a)}</span></div></div>')
        for i, (q, yn, a) in enumerate(P2_ANSWER, 1))
    fill = "".join(
        item(i, (f'<span class="en big">{esc(a)} <span class="bl"><span class="a">{esc(x)}</span></span> {esc(b)}</span>'
                 f'　<span class="yn-tag">（{k}）</span>'))
        for i, (a, b, k, x) in enumerate(P2_FILL, 1))
    left = (sec(1, "質問に答えよう。（　）の Yes / No で答える。")
            + f'<div class="list ans">{ans}</div>'
            + sec(2, "＿＿ に入る語を，下の語から えらんで書こう。")
            + '<div class="pool en">am　is　are　do　does　aren\'t　don\'t　doesn\'t</div>'
            + f'<div class="list tight">{fill}</div>')
    side = (side_box("聞かれたもので答える",
                     '<table class="mt"><tr><th>質問</th><th>答え</th></tr>'
                     '<tr><td>Are you ～?</td><td>I am. / I\'m not.</td></tr>'
                     '<tr><td>Is he ～?</td><td>he is. / he isn\'t.</td></tr>'
                     '<tr><td>Do you ～?</td><td>I do. / I don\'t.</td></tr>'
                     '<tr><td>Does she ～?</td><td>she does. / she doesn\'t.</td></tr></table>')
            + side_box("主語の言いかえ",
                       '<div class="sw"><span class="en">you</span>→<span class="en"><b>I</b></span>'
                       '<span class="en">Ken</span>→<span class="en"><b>he</b></span>'
                       '<span class="en">Mai / your mother</span>→<span class="en"><b>she</b></span>'
                       '<span class="en">this</span>→<span class="en"><b>it</b></span>'
                       '<span class="en">Ken and Mai</span>→<span class="en"><b>they</b></span></div>', "warn")
            + side_box("2 のコツ", "①「どっちの文？」を決める<br>② 主語を見て do / does，am / is / are を決める")
            + words([("park", "パーク", "公園"), ("mother", "マザー", "母"), ("cook", "クック", "料理する"),
                     ("swim", "スイム", "泳ぐ"), ("tall", "トール", "背が高い")]))
    return page(2, "答え方をマスターしよう", "主語を言いかえて，聞かれたもので答える", left, side)


# ---------------------------------------------------------------- 3ページ目：まちがい直し・ならべかえ
P3_FIX = [  # (まちがい, 線を引くところ, 正しい文)
    ("Ken isn't like dogs.", "isn't", "Ken doesn't like dogs."),
    ("Do you hungry?", "Do", "Are you hungry?"),
    ("Does she has a cat?", "has", "Does she have a cat?"),
    ("I am not play the piano.", "am not", "I don't play the piano."),
    ("Is Mai speak English?", "Is", "Does Mai speak English?"),
    ("They doesn't live in Osaka.", "doesn't", "They don't live in Osaka."),
    ("Are you a student? — Yes, you are.", "you are", "Yes, I am."),
]
P3_ORDER = [  # (日本語, カード, 正しい文, いらない語)
    ("あなたは忙しいですか。", ["are", "busy", "do", "you"], "Are you busy?", "do"),
    ("ケンは野球をしません。", ["baseball", "doesn't", "isn't", "Ken", "play"], "Ken doesn't play baseball.", "isn't"),
    ("マイはわたしの姉ではありません。", ["Mai", "my", "not", "is", "sister", "doesn't"], "Mai is not my sister.", "doesn't"),
    ("彼らはテレビを見ますか。", ["they", "TV", "do", "watch", "are"], "Do they watch TV?", "are"),
]


def p3() -> str:
    fix = ""
    for i, (w, mark, ok) in enumerate(P3_FIX, 1):
        shown = esc(w).replace(esc(mark), f'<span class="mk">{esc(mark)}</span>', 1)
        fix += item(i, f'<span class="en big">{shown}</span>', line(ok, "正しくは"))
    order = ""
    for i, (jp, cards, ok, extra) in enumerate(P3_ORDER, 1):
        assert extra in cards and all(c.lower().strip("?.") in ok.lower() or c == extra for c in cards), (ok, cards)
        c = "".join(f'<span class="card en{" x" if x == extra else ""}">{esc(x)}</span>' for x in cards)
        order += item(i, f'<span class="jp">{esc(jp)}</span><span class="cards">{c}</span>', line(ok))
    left = (sec(1, "まちがいが1つずつある。まちがいに線を引き，正しい文を書こう。", "7は答えの文だけ直す")
            + f'<div class="list">{fix}</div>'
            + sec(2, "ならべかえて英文を書こう。", "いらない語が1つずつある。文の最後に . か ? をつける")
            + f'<div class="list">{order}</div>')
    side = (side_box("まぜない！", 'be動詞と do / does は<br><b>いっしょに使わない</b>。'
                     '<div class="ng en">× Ken isn\'t like dogs.<br>× Do you hungry?<br>× I am not play ～.</div>', "warn")
            + side_box("does / doesn't のあと", '動詞は <b>s のつかない形</b>。<div class="ng en">× Does she has ～?<br>○ Does she have ～?</div>')
            + side_box("いらない語の見つけ方", "① 日本語を見て「どっちの文？」<br>② 使わないほうの be動詞 / do が<br>　いらない語")
            + words([("dog", "ドッグ", "犬"), ("cat", "キャット", "ねこ"), ("speak", "スピーク", "話す"),
                     ("baseball", "ベースボール", "野球"), ("watch", "ウォッチ", "見る")]))
    return page(3, "まちがい直しとならべかえ", "どこがおかしいか，「どっちの文？」で考える", left, side)


# ---------------------------------------------------------------- 4ページ目：日本語を英語に
P4_JE = [  # (日本語, 英語, 答えの英語 or None)
    ("ケンは疲れていません。", "Ken is not tired.", None),
    ("あなたは数学が好きですか。 ― はい，好きです。", "Do you like math?", "Yes, I do."),
    ("わたしの妹はピアノをひきません。", "My sister doesn't play the piano.", None),
    ("彼らは公園にいますか。 ― いいえ，いません。", "Are they in the park?", "No, they aren't."),
    ("わたしは自転車を持っていません。", "I don't have a bike.", None),
    ("マイは毎日料理をしますか。 ― はい，します。", "Does Mai cook every day?", "Yes, she does."),
    ("これはあなたのかばんですか。 ― いいえ，ちがいます。", "Is this your bag?", "No, it isn't."),
]
CHECK = [
    "be動詞か一般動詞かを，書く前に決められた",
    "he / she / Ken のとき，doesn't / Does にできた",
    "does / doesn't のあと，動詞の s をとれた",
    "答えの主語を言いかえられた（Ken → he など）",
]


def p4() -> str:
    je = ""
    for i, (jp, en, a) in enumerate(P4_JE, 1):
        after = line(en)
        if a:
            yn = a.split(",")[0]
            rest = a[len(yn) + 2:]
            after += (f'<div class="ln short"><span class="lab en">— {yn},</span><div class="u"><span class="a">{esc(rest)}</span></div></div>')
        je += item(i, f'<span class="jp">{esc(jp)}</span>', after)
    chk = "".join(f"<div>□ {esc(c)}</div>" for c in CHECK)
    left = (sec(1, "日本語を英語にしよう。", "is not → isn't など短い形でもOK")
            + f'<div class="list">{je}</div>'
            + sec(2, "ふりかえり　できたら □ に ✓")
            + f'<div class="chk">{chk}</div>')
    side = (side_box("書く前に3つチェック",
                     '<div class="st">① be動詞？ 一般動詞？</div><div class="ar">▼</div>'
                     '<div class="st">② 主語はだれ？<br><small>am / is / are，do / does</small></div><div class="ar">▼</div>'
                     '<div class="st">③ 否定文？ 疑問文？</div>')
            + side_box("ひっかけ注意", "「好きです」→ <b>like</b>（一般動詞）<br>「持っています」→ <b>have</b>（一般動詞）<br>"
                       "「疲れて<b>います</b>」→ <b>tired</b>（be動詞）<br>「公園に<b>います</b>」→ <b>be動詞</b>", "warn")
            + words([("tired", "タイアード", "疲れた"), ("bike", "バイク", "自転車"), ("bag", "バッグ", "かばん"),
                     ("every day", "エヴリ デイ", "毎日"), ("this", "ディス", "これ")]))
    return page(4, "日本語を英語にしよう", "3つチェックしてから書く", left, side)


# ---------------------------------------------------------------- 見た目
CSS = r"""
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: "Noto Sans CJK JP", sans-serif; color: #1b1f24; font-size: 10pt; line-height: 1.5;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; --c: #2c6e4f; --soft: #eef5f0; --red: #e11d2e; }
.en { font-family: "Liberation Sans", "Noto Sans CJK JP", sans-serif; }
.page { width: 210mm; height: 297mm; padding: 10mm 12mm 9mm; position: relative; overflow: hidden;
  page-break-after: always; break-after: page; display: flex; flex-direction: column; gap: 3mm; }
.page:last-child { page-break-after: auto; break-after: auto; }
.hd { display: flex; align-items: center; gap: 4mm; border-bottom: 2px solid var(--c); padding-bottom: 2.4mm; flex: none; }
.hd .tag { background: var(--c); color: #fff; font-weight: 900; font-size: 8.6pt; line-height: 1.25; padding: 1.4mm 3.2mm; border-radius: 1.8mm; text-align: center; }
.hd .ttl { font-size: 16pt; font-weight: 900; line-height: 1.2; }
.hd .sub { font-size: 7.8pt; color: #5d6670; }
.hd .nm { margin-left: auto; width: 52mm; font-size: 8pt; display: grid; gap: 2.2mm; }
.hd .nm div { border-bottom: 1px solid #333; padding-bottom: .3mm; }
.answers .hd .nm { visibility: hidden; }
.answers .page::before { content: "【こたえ】"; position: absolute; top: 3.4mm; right: 12mm; color: var(--red); font-weight: 900; font-size: 9pt; }
.main { flex: 1; min-height: 0; display: grid; grid-template-columns: 1fr 56mm; gap: 5mm; }
.left { display: flex; flex-direction: column; gap: 2.2mm; min-height: 0; overflow: hidden; }
.side { background: var(--soft); border-left: 2px solid var(--c); border-radius: 0 3mm 3mm 0; padding: 3mm 3mm; display: flex; flex-direction: column; gap: 2.6mm; font-size: 8.2pt; line-height: 1.55; overflow: hidden; }
.foot { position: absolute; bottom: 4mm; right: 12mm; font-size: 7pt; color: #8a939d; }

.sec { display: flex; gap: 2mm; align-items: baseline; font-weight: 700; font-size: 10pt; line-height: 1.4; flex-wrap: wrap; margin-top: 1mm; }
.sec .n { flex: none; display: inline-flex; width: 5.4mm; height: 5.4mm; border-radius: 50%; background: var(--c); color: #fff; font-size: 8.4pt; font-weight: 900; align-items: center; justify-content: center; transform: translateY(.8mm); }
.sec .s { font-weight: 400; font-size: 7.8pt; color: #5d6670; flex-basis: 100%; padding-left: 7.4mm; margin-top: -.6mm; }
.list { display: grid; gap: 2.8mm; padding-left: 1mm; }
.list.tight { gap: 3.6mm; }
.list.ans { gap: 1.8mm; }
.it { display: grid; grid-template-columns: 5.4mm 1fr; align-items: start; }
.it .no { font-size: 9pt; color: #444; padding-top: .5mm; }
.it .q { font-size: 9.6pt; display: flex; flex-wrap: wrap; align-items: baseline; gap: 1mm 2mm; }
.big { font-size: 12pt; }
.jp { font-size: 10pt; }
.par { white-space: nowrap; font-size: 9pt; }
.big .par { font-size: 12pt; }
.o { padding: 0 1.2mm; border-radius: 99px; }
.answers .o.c { box-shadow: 0 0 0 1.4px var(--red); color: var(--red); }
.yn-tag { font-size: 8.4pt; color: #555; }

.ln { display: flex; align-items: flex-end; gap: 2mm; margin-top: .8mm; }
.ln .lab { flex: none; font-size: 7.6pt; color: var(--c); font-weight: 700; width: 11mm; padding-bottom: .8mm; }
.ln .lab.en { font-size: 10.5pt; color: #1b1f24; font-weight: 400; width: auto; }
.ln .u { flex: 1; border-bottom: 1px solid #555; height: 10.6mm; display: flex; align-items: flex-end; padding: 0 1.5mm .6mm; }
.ln.short .u { flex: 0 0 56mm; height: 9.4mm; }
.a { visibility: hidden; font-family: "Liberation Sans", "Noto Sans CJK JP", sans-serif; font-size: 11pt; color: var(--red); font-weight: 700; }
.answers .a { visibility: visible; }
.bl { display: inline-block; min-width: 20mm; border-bottom: 1px solid #333; text-align: center; }
.bl .a { font-size: 11pt; }
.pool { border: 1px dashed #9aa3ad; border-radius: 2mm; padding: 1mm 3mm; font-size: 11pt; text-align: center; letter-spacing: .02em; margin-left: 6.4mm; }
.mk { }
.answers .mk { text-decoration: underline; text-decoration-color: var(--red); text-decoration-thickness: 1.6px; text-underline-offset: 1mm; }
.cards { display: inline-flex; flex-wrap: wrap; gap: 1.4mm; margin-left: 1mm; }
.card { border: 1px solid #8b949e; border-radius: 1.2mm; padding: 0 2mm; font-size: 11pt; background: #fff; box-shadow: 0 .4mm 0 #c9d0d8; }
.answers .card.x { text-decoration: line-through; text-decoration-color: var(--red); text-decoration-thickness: 1.6px; color: var(--red); }
.chk { border: 1.4px solid var(--c); border-radius: 2.4mm; padding: 2mm 4mm; display: grid; grid-template-columns: 1fr; gap: 1.2mm; font-size: 9.4pt; }

.box { background: #fff; border-radius: 2mm; padding: 2mm 2.6mm; }
.box .bt { color: var(--c); font-weight: 900; font-size: 8.6pt; border-bottom: 1px dashed var(--c); margin-bottom: 1.2mm; }
.box.plain { background: transparent; padding: 0; }
.box.warn { background: #fff4ef; border: 1px solid #f0b8a5; }
.box.warn .bt { color: #c2410c; border-color: #e0a58f; }
.r { color: var(--red); font-weight: 700; }
.yn { display: grid; grid-template-columns: 1fr 1fr; gap: 1.4mm; margin-top: 1.2mm; text-align: center; }
.yn div { border-radius: 1.6mm; padding: 1mm; font-size: 7.8pt; }
.yn .y { background: #fde8e4; } .yn .n { background: #e6eef9; }
.fm { margin-bottom: 1.2mm; font-size: 7.8pt; }
.mt { width: 100%; border-collapse: collapse; font-size: 7.6pt; font-family: "Liberation Sans", "Noto Sans CJK JP", sans-serif; }
.mt th { background: #eef1f5; font-family: "Noto Sans CJK JP"; font-weight: 700; padding: .4mm; }
.mt td { border-top: 1px solid #dde2e8; padding: .6mm .8mm; }
.sw { display: grid; grid-template-columns: auto auto 1fr; gap: .4mm 1.4mm; }
.ng { margin-top: 1mm; color: var(--red); font-size: 8.2pt; }
.st { border: 1px solid var(--c); border-radius: 1.6mm; padding: .8mm 2mm; text-align: center; font-size: 8pt; background: #fff; }
.st small { font-size: 7pt; color: #555; }
.ar { text-align: center; color: var(--c); font-size: 7pt; line-height: 1.2; }
.wl { display: grid; grid-template-columns: auto 1fr; gap: .2mm 2mm; font-size: 7.8pt; }
.we { font-weight: 700; }
"""


def doc(answers: bool) -> str:
    pages = [p1(), p2(), p3(), p4()]
    return (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>n02 復習</title><style>{CSS}</style></head>'
            f'<body class="{"answers" if answers else ""}">' + "".join(pages) + "</body></html>")


def main():
    keep_html = "--html" in sys.argv
    jobs = {f"{OUT}.pdf": doc(False), f"{OUT}_answers.pdf": doc(True)}
    from playwright.sync_api import sync_playwright
    out_html = Path(__file__).resolve().parent / "out"
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for name, h in jobs.items():
            if keep_html:
                out_html.mkdir(exist_ok=True)
                (out_html / name.replace(".pdf", ".html")).write_text(h, encoding="utf-8")
            pg.set_content(h, wait_until="load")
            pg.evaluate("document.fonts.ready")
            over = pg.evaluate("""() => [...document.querySelectorAll('.page, .left, .side')]
                .map(e=>[e.className, e.scrollHeight - e.clientHeight]).filter(x=>x[1]>1)""")
            if over:
                print(f"  !! {name}: はみ出し {over}")
            pg.pdf(path=str(PDF_DIR / name), format="A4", print_background=True,
                   margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            print("  wrote", name)
        b.close()


if __name__ == "__main__":
    main()
