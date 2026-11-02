"""新しく入った子 n01 の宿題（be動詞・一般動詞の否定文と疑問文）。

形（先生と決めたこと）
- 木曜の授業のあと、金〜水の6日分。1日の量は自学ノート（大学ノート）に半ページ。
- プリントは問題だけ。答えはノートに書く（英文は文全体を書く）。
- 本人が毎日こたえを見て自分で丸つけ・直しをする。

A4 1枚に2日分 × 3枚。こたえは同じレイアウトに赤で答えを入れて出す。

  python3 tools/n01_homework.py          → pdf/n01_homework.pdf, pdf/n01_homework_answers.pdf
  python3 tools/n01_homework.py --html   → 確認用 HTML も tools/out/ に
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eigolib import PDF_DIR, esc  # noqa: E402

OUT = "n01_homework"
UNIT = "be動詞・一般動詞の否定文と疑問文"

# ---------------------------------------------------------------- 6日分のデータ
# section: (指示, 型, [(問題, こたえ)])
#   型 "row"  … 短い答えを1行にまとめて書く（ウォームアップ）
#   型 "list" … 1問1行（2行）で書く
DAYS = [
    dict(
        no=1, dow="金", title="be動詞の否定文と疑問文",
        hint="am / is / are の文<br>・否定文 → be動詞の<b>うしろ</b>に <b>not</b><br>・疑問文 → be動詞を<b>文の頭</b>へ<br>"
             "・you で聞かれたら I で答える",
        words=[("from", "フロム", "〜出身の"), ("classroom", "クラスルーム", "教室"), ("hungry", "ハングリー", "おなかがすいた")],
        secs=[
            ("be動詞の文？ 一般動詞の文？ 「be」か「一般」と書こう。", "row", [
                ("Mai is my sister.", "be"),
                ("I watch TV.", "一般"),
                ("They are tall.", "be"),
            ]),
            ("否定文にして、文全体を書こう。", "list", [
                ("I am busy.", "I am not busy."),
                ("Ken is from Osaka.", "Ken is not from Osaka."),
                ("We are in the classroom.", "We are not in the classroom."),
            ]),
            ("疑問文にして、答えも書こう。Yes / No は書いてあるとおりに。", "list", [
                ("Mai is a student.　（Yes）", "Is Mai a student? — Yes, she is."),
                ("You are hungry.　（No）", "Are you hungry? — No, I'm not."),
                ("They are friends.　（No）", "Are they friends? — No, they aren't."),
            ]),
        ]),
    dict(
        no=2, dow="土", title="一般動詞の否定文と疑問文",
        hint="am / is / are がない文<br>・I / you / we / they<br>　→ <b>don't</b> ／ <b>Do</b><br>・he / she / Ken など<br>　→ <b>doesn't</b> ／ <b>Does</b><br>"
             "・does のときは動詞の <b>s をとる</b><br>（likes → like, has → have）",
        words=[("piano", "ピアノ", "ピアノ"), ("fish", "フィッシュ", "魚"), ("math", "マス", "数学"), ("live in", "リヴ イン", "〜に住む")],
        secs=[
            ("be動詞の文？ 一般動詞の文？ 「be」か「一般」と書こう。", "row", [
                ("Ken has a bike.", "一般"),
                ("I am tired.", "be"),
                ("She likes cats.", "一般"),
            ]),
            ("否定文にして、文全体を書こう。", "list", [
                ("I play the piano.", "I don't play the piano."),
                ("They watch TV.", "They don't watch TV."),
                ("Mai likes fish.", "Mai doesn't like fish."),
                ("He has a dog.", "He doesn't have a dog."),
            ]),
            ("疑問文にして、答えも書こう。Yes / No は書いてあるとおりに。", "list", [
                ("You study math.　（Yes）", "Do you study math? — Yes, I do."),
                ("Ken lives in Tokyo.　（No）", "Does Ken live in Tokyo? — No, he doesn't."),
            ]),
        ]),
    dict(
        no=3, dow="日", title="どっち？ 否定文",
        hint="文に am / is / are がある？<br>・<b>ある</b> → be動詞のうしろに <b>not</b><br>・<b>ない</b> → 動詞の前に <b>don't / doesn't</b><br>"
             "・まぜない！<br>× Ken isn't play tennis.",
        words=[("brother", "ブラザー", "兄・弟"), ("every day", "エヴリ デイ", "毎日"), ("cook", "クック", "料理する")],
        secs=[
            ("まず「be」か「一般」を書いてから、否定文にしよう。<br>（ノートには「1　be　Ken is not 〜」のように1行で）", "list", [
                ("Ken is my brother.", "be　Ken is not my brother."),
                ("Ken speaks English.", "一般　Ken doesn't speak English."),
                ("I am a teacher.", "be　I am not a teacher."),
                ("I cook every day.", "一般　I don't cook every day."),
                ("They are tired.", "be　They are not tired."),
                ("They play baseball.", "一般　They don't play baseball."),
            ]),
            ("（　）に入るほうをノートに書こう。", "row", [
                ("She ( isn't / doesn't ) hungry.", "isn't"),
                ("We ( aren't / don't ) like math.", "don't"),
                ("My mother ( isn't / doesn't ) watch TV.", "doesn't"),
            ]),
        ]),
    dict(
        no=4, dow="月", title="どっち？ 疑問文",
        hint="文に am / is / are がある？<br>・<b>ある</b> → be動詞を文の頭へ<br>・<b>ない</b> → <b>Do / Does</b> を文の頭へ<br>"
             "・答えは聞かれたもので<br>Is 〜? → is / isn't<br>Does 〜? → does / doesn't",
        words=[("park", "パーク", "公園"), ("pen", "ペン", "ペン")],
        secs=[
            ("まず「be」か「一般」を書いてから、疑問文にして答えも書こう。", "list", [
                ("Mai is tired.　（No）", "be　Is Mai tired? — No, she isn't."),
                ("Mai likes music.　（Yes）", "一般　Does Mai like music? — Yes, she does."),
                ("You are from Osaka.　（Yes）", "be　Are you from Osaka? — Yes, I am."),
                ("You have a pen.　（No）", "一般　Do you have a pen? — No, I don't."),
                ("They are in the park.　（Yes）", "be　Are they in the park? — Yes, they are."),
            ]),
            ("（　）に入るほうをノートに書こう。", "row", [
                ("( Are / Do ) you play tennis?", "Do"),
                ("( Is / Does ) she your sister?", "Is"),
                ("( Is / Does ) Ken study English?", "Does"),
            ]),
        ]),
    dict(
        no=5, dow="火", title="まちがい直し",
        hint="・be動詞と do / does は<br>　<b>いっしょに使わない</b><br>・動詞（play, like…）がない文<br>　→ be動詞の文<br>"
             "・Does / doesn't のあとは<br>　動詞に s をつけない",
        words=[("bike", "バイク", "自転車")],
        secs=[
            ("日本語を英語にするとき、使うのは「be」？「一般」？", "row", [
                ("わたしはテニスが好きです。", "一般"),
                ("ケンは今、部屋にいます。", "be"),
                ("彼は背が高いです。", "be"),
            ]),
            ("まちがいが1つある。正しい文をノートに書こう。", "list", [
                ("I'm not play soccer.", "I don't play soccer."),
                ("Does she busy?", "Is she busy?"),
                ("Are you study English?", "Do you study English?"),
                ("Ken don't like cats.", "Ken doesn't like cats."),
                ("Does Mai has a bike?", "Does Mai have a bike?"),
                ("They doesn't live in Tokyo.", "They don't live in Tokyo."),
                ("He not is a teacher.", "He is not a teacher."),
            ]),
        ]),
    dict(
        no=6, dow="水", title="総まとめ 日本語を英語に",
        hint="書く前に3つチェック<br>① be動詞？ 一般動詞？<br>② 主語はだれ？<br>　am / is / are, do / does<br>③ 否定文？ 疑問文？<br>"
             "「好きです」は like（一般動詞）！",
        words=[("sister", "シスター", "姉・妹"), ("mother", "マザー", "母"), ("have", "ハヴ", "持っている・飼っている")],
        secs=[
            ("日本語を英語にしよう。", "list", [
                ("わたしは疲れていません。", "I am not tired."),
                ("あなたは音楽が好きですか。 ― はい、好きです。", "Do you like music? — Yes, I do."),
                ("ケンは英語を勉強しません。", "Ken doesn't study English."),
                ("マイはあなたのお姉さんですか。 ― いいえ、ちがいます。", "Is Mai your sister? — No, she isn't."),
                ("彼らはサッカーをしますか。 ― はい、します。", "Do they play soccer? — Yes, they do."),
                ("わたしの母は忙しくありません。", "My mother is not busy."),
                ("彼女はねこを飼っていません。", "She doesn't have a cat."),
            ]),
        ]),
]

# ---------------------------------------------------------------- 見た目
CSS = r"""
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: "Noto Sans CJK JP", sans-serif; color: #1b1f24; font-size: 10pt; line-height: 1.5;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
  --c: #2c6e4f; --soft: #eef5f0; --line: #c9d6ce; --red: #e11d2e; }
.page { width: 210mm; height: 297mm; padding: 10mm 12mm 8mm; position: relative; overflow: hidden;
  page-break-after: always; break-after: page; display: flex; flex-direction: column; gap: 3.2mm; }
.page:last-child { page-break-after: auto; break-after: auto; }
.en { font-family: "Liberation Sans", "Noto Sans CJK JP", sans-serif; }

.hd { display: flex; align-items: center; gap: 4mm; border-bottom: 2px solid var(--c); padding-bottom: 2.4mm; flex: none; }
.hd .tag { background: var(--c); color: #fff; font-weight: 900; font-size: 9.5pt; padding: 1.6mm 3.4mm; border-radius: 1.8mm; white-space: nowrap; }
.hd .ttl { font-size: 15pt; font-weight: 900; line-height: 1.2; }
.hd .sub { font-size: 7.6pt; color: #5d6670; }
.hd .nm { margin-left: auto; font-size: 8pt; width: 50mm; border-bottom: 1px solid #333; padding-bottom: .4mm; }
.answers .hd .nm { visibility: hidden; }
.answers .page::before { content: "【こたえ】"; position: absolute; top: 3.4mm; right: 12mm; color: var(--red); font-weight: 900; font-size: 9pt; }

.howto { border: 1.6px dashed var(--c); border-radius: 3mm; padding: 2.4mm 4mm; display: grid; grid-template-columns: 1fr 58mm; gap: 4mm; font-size: 8.6pt; line-height: 1.55; flex: none; }
.howto b.h { color: var(--c); font-size: 9.6pt; display: block; margin-bottom: .6mm; }
.howto ol { margin: 0; padding-left: 4.6mm; }
.note { border: 1px solid #b9c2cc; border-radius: 1.4mm; background: repeating-linear-gradient(#fff 0 5.3mm, #aac4e6 5.3mm 5.5mm); padding: .4mm 2.4mm 0 7mm; font-size: 8pt; line-height: 5.5mm; position: relative; align-self: start; }
.note::before { content: ""; position: absolute; left: 4.6mm; top: 0; bottom: 0; border-left: 1px solid #e6a3a3; }
.note .r { color: var(--red); }
.notewrap .cap { font-size: 7pt; color: #5d6670; display: block; margin-bottom: .6mm; }

.day { flex: 1 1 0; min-height: 0; border: 1.6px solid var(--c); border-radius: 3mm; overflow: hidden; display: flex; flex-direction: column; }
.day .bar { display: flex; align-items: center; gap: 3mm; background: var(--soft); border-bottom: 1px solid var(--line); padding: 1.6mm 3.4mm; flex: none; }
.day .bar .d { background: var(--c); color: #fff; font-weight: 900; font-size: 10.5pt; padding: .3mm 3mm; border-radius: 99px; white-space: nowrap; }
.day .bar .dt { font-size: 8.6pt; white-space: nowrap; }
.day .bar .tt { font-weight: 900; font-size: 11.5pt; }
.day .bar .ck { margin-left: auto; font-size: 8pt; color: #333; white-space: nowrap; letter-spacing: .02em; }
.day .in { flex: 1; min-height: 0; display: grid; grid-template-columns: 1fr 52mm; }
.day .qs { padding: 2.2mm 3.6mm 2mm; display: flex; flex-direction: column; gap: 1.8mm; overflow: hidden; }
.day .side { background: #f6faf7; border-left: 1px solid var(--line); padding: 2.4mm 3mm; font-size: 8.2pt; line-height: 1.55; display: flex; flex-direction: column; gap: 2.4mm; }
.side .lab { color: var(--c); font-weight: 900; font-size: 8.4pt; border-bottom: 1px dashed var(--c); margin-bottom: .8mm; }
.side .w { display: grid; grid-template-columns: auto 1fr; column-gap: 2mm; }
.side .w .en { font-weight: 700; }

.sec { display: flex; gap: 1.8mm; align-items: baseline; font-weight: 700; font-size: 9.4pt; line-height: 1.4; }
.sec .n { flex: none; display: inline-flex; width: 4.8mm; height: 4.8mm; border-radius: 50%; background: var(--c); color: #fff; font-size: 7.6pt; font-weight: 900; align-items: center; justify-content: center; transform: translateY(.6mm); }
.sec .s { font-weight: 400; font-size: 7.6pt; color: #5d6670; }
.items { display: grid; gap: .5mm; padding-left: 6.6mm; }
.items .it { display: flex; flex-wrap: wrap; column-gap: 1.6mm; align-items: baseline; }
.answers .items { gap: 0; line-height: 1.38; }
.answers .day .qs { gap: 1.2mm; }
.items .no { width: 4mm; flex: none; font-size: 8.6pt; color: #444; }
.items .p { font-size: 11pt; }
.items .p.jp { font-size: 9.6pt; }
.row { display: flex; flex-wrap: wrap; gap: .6mm 6mm; padding-left: 6.6mm; }
.row .it { display: flex; gap: 1.4mm; align-items: baseline; }
.row .no { font-size: 8.6pt; color: #444; }
.row .p { font-size: 10.6pt; }
.row .p.jp { font-size: 9.4pt; }
.a { display: none; }
.answers .a { display: inline; color: var(--red); font-weight: 700; font-size: 10pt; }
.answers .items .a { flex-basis: 100%; padding-left: 5.6mm; font-size: 9.6pt; }
.answers .items .a::before { content: "→ "; }
.answers .row .a::before { content: "→ "; }

.foot { position: absolute; bottom: 4mm; right: 12mm; font-size: 7pt; color: #8a939d; }
.end { flex: none; text-align: center; font-size: 8.6pt; color: var(--c); font-weight: 700; }
.grade { border: 1.6px solid var(--red); border-radius: 3mm; padding: 2.2mm 4mm; font-size: 8.6pt; line-height: 1.6; flex: none; }
.grade b.h { color: var(--red); font-size: 9.6pt; margin-right: 2mm; }
"""

DATE = "　　月　　日"


def is_jp(s: str) -> bool:
    return any("぀" <= ch <= "鿿" for ch in s.split("（")[0])


def ptxt(s: str) -> str:
    cls = "p jp" if is_jp(s) else "p en"
    # （Yes）のような日本語カッコは日本語フォントで
    return f'<span class="{cls}">{esc(s).replace("（", "<span style=\"font-family:Noto Sans CJK JP;font-size:8.6pt;color:#555\">（").replace("）", "）</span>")}</span>'


def section(i: int, text: str, kind: str, items) -> str:
    head = f'<div class="sec"><span class="n">{i}</span><span>{text}</span></div>'
    if kind == "row":
        body = "".join(f'<span class="it"><span class="no">({k})</span>{ptxt(q)}<span class="a en">{esc(a)}</span></span>'
                       for k, (q, a) in enumerate(items, 1))
        return head + f'<div class="row">{body}</div>'
    body = "".join(f'<div class="it"><span class="no">{k}.</span>{ptxt(q)}<span class="a en">{esc(a)}</span></div>'
                   for k, (q, a) in enumerate(items, 1))
    return head + f'<div class="items">{body}</div>'


def day_box(d) -> str:
    secs = "".join(section(i, *s) for i, s in enumerate(d["secs"], 1))
    words = "".join(f'<span class="en">{esc(e)}</span><span>{esc(r)}　{esc(j)}</span>' for e, r, j in d["words"])
    return f"""<div class="day">
<div class="bar"><span class="d">{d["no"]}日目</span><span class="dt">{DATE}（{d["dow"]}）</span><span class="tt">{esc(d["title"])}</span>
<span class="ck">□ やった　□ 丸つけ　□ 直し</span></div>
<div class="in"><div class="qs">{secs}</div>
<div class="side"><div><div class="lab">ヒント</div>{d["hint"]}</div>
<div><div class="lab">単語</div><div class="w">{words}</div></div></div></div></div>"""


HOWTO = """<div class="howto"><div><b class="h">宿題のやりかた（自学ノートに 1日 半ページ）</b>
<ol><li>ノートに <b>日付</b> と「<b>○日目</b>」を書く。</li>
<li>問題の番号を書いてから答える。英文は <b>文全体</b> を書く。</li>
<li>1日分おわったら、すぐ <b>こたえ</b> を見て赤ペンで丸つけ。</li>
<li>まちがえた問題は、正しい文をその下に <b>もう一度書く</b>（直し）。</li>
<li>このプリントの □ に ✓ を入れる。</li></ol></div>
<div class="notewrap"><span class="cap">ノートの書き方（例）</span><div class="note">
11/6（金）　1日目<br>① (1) be　(2) 一般　(3) be<br>② 1. I am not busy.　<span class="r">○</span><br>　 2. Ken is not from Osaka.　<span class="r">○</span></div></div></div>"""

GRADE = """<div class="grade"><b class="h">丸つけのしかた</b>合っていたら ○、ちがっていたら ✓。✓ の問題は正しい文をノートにもう一度書こう。<br>
isn't / is not、don't / do not、I'm not / I am not は、<b>短い形でも長い形でもどちらも ○</b>。「be」「一般」の判断がちがっていたら、文が合っていても直しをしよう。</div>"""


def page(n: int, total: int, days, first: bool, answers: bool) -> str:
    top = (GRADE if answers else HOWTO) if first else ""
    end = '<div class="end">6日間おつかれさま！ 木曜はこのノートを持ってこよう。</div>' if n == total and not answers else ""
    return f"""<div class="page">
<div class="hd"><span class="tag">宿題</span><div><div class="ttl">否定文と疑問文　毎日コツコツ</div>
<div class="sub">n01「{UNIT}」の復習　{n}枚目（{days[0]["no"]}〜{days[-1]["no"]}日目）</div></div><div class="nm">名前</div></div>
{top}{"".join(day_box(d) for d in days)}{end}
<div class="foot">中1英語　n01 宿題　{n}／{total}</div></div>"""


def doc(answers: bool) -> str:
    pages = [page(i // 2 + 1, 3, DAYS[i:i + 2], i == 0, answers) for i in range(0, 6, 2)]
    return (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>n01 宿題</title><style>{CSS}</style></head>'
            f'<body class="{"answers" if answers else ""}">' + "".join(pages) + "</body></html>")


def main():
    keep_html = "--html" in sys.argv
    jobs = {f"{OUT}.pdf": doc(False), f"{OUT}_answers.pdf": doc(True)}
    from playwright.sync_api import sync_playwright
    out_html = Path(__file__).resolve().parent / "out"
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for name, html in jobs.items():
            if keep_html:
                out_html.mkdir(exist_ok=True)
                (out_html / name.replace(".pdf", ".html")).write_text(html, encoding="utf-8")
            pg.set_content(html, wait_until="load")
            pg.evaluate("document.fonts.ready")
            over = pg.evaluate("""() => [...document.querySelectorAll('.page, .day .qs, .day .side')]
                .map((e,i)=>[e.className, e.scrollHeight - e.clientHeight]).filter(x=>x[1]>1)""")
            if over:
                print(f"  !! {name}: はみ出し {over}")
            pg.pdf(path=str(PDF_DIR / name), format="A4", print_background=True,
                   margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            print("  wrote", name)
        b.close()


if __name__ == "__main__":
    main()
