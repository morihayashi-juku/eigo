"""新しく入った子 n02 の宿題（n01 の復習・定着。授業プリント n02_fukushu と同じ週）。

n01_homework.py をコピーして DAYS を書きかえたもの。形は n01 と同じ。

形（先生と決めたこと）
- 木曜の授業のあと、金〜水の6日分。1日の量は自学ノート（大学ノート）に半ページ。
- プリントは問題だけ。答えはノートに書く（英文は文全体を書く）。
- 本人が毎日こたえを見て自分で丸つけ・直しをする。

A4 1枚に2日分 × 3枚。こたえは同じレイアウトに赤で答えを入れて出す。

  python3 tools/n02_homework.py          → pdf/n02_homework.pdf, pdf/n02_homework_answers.pdf
  python3 tools/n02_homework.py --html   → 確認用 HTML も tools/out/ に
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eigolib import PDF_DIR, esc  # noqa: E402

OUT = "n02_homework"
UNIT = "be動詞・一般動詞の否定文と疑問文"
SUB = "n02「否定文と疑問文の復習」"
TITLE = "否定文と疑問文　もう一度コツコツ"


# ---------------------------------------------------------------- 6日分のデータ
DAYS = [
    dict(
        no=1, dow="金", title="作り分け　否定文",
        hint="文に am / is / are がある？<br>・<b>ある</b> → be動詞のうしろに <b>not</b><br>・<b>ない</b> → 動詞の前に<br>　<b>don't / doesn't</b><br>"
             "・doesn't のあとは s をとる<br>（has → have）",
        words=[("from", "フロム", "〜出身の"), ("speak", "スピーク", "話す"), ("brother", "ブラザー", "兄・弟"), ("bike", "バイク", "自転車")],
        secs=[
            ("be動詞の文？ 一般動詞の文？ 「be」か「一般」と書こう。", "row", [
                ("My sister is a student.", "be"),
                ("They watch TV every day.", "一般"),
                ("I am in my room.", "be"),
            ]),
            ("否定文にして、文全体を書こう。", "list", [
                ("I am from Tokyo.", "I am not from Tokyo."),
                ("Mai plays tennis.", "Mai doesn't play tennis."),
                ("We are in the park.", "We are not in the park."),
                ("You speak English.", "You don't speak English."),
                ("My brother has a bike.", "My brother doesn't have a bike."),
                ("This is my pen.", "This is not my pen."),
            ]),
        ]),
    dict(
        no=2, dow="土", title="作り分け　疑問文と答え",
        hint="文に am / is / are がある？<br>・<b>ある</b> → be動詞を文の頭へ<br>・<b>ない</b> → <b>Do / Does</b> を文の頭へ<br>"
             "・Does のあとは s をとる<br>（likes → like）<br>・答えの主語を言いかえる<br>（Ken → he）",
        words=[("baseball", "ベースボール", "野球"), ("father", "ファーザー", "父"), ("cook", "クック", "料理する"), ("every day", "エヴリ デイ", "毎日")],
        secs=[
            ("疑問文にして、答えも書こう。Yes / No は書いてあるとおりに。", "list", [
                ("Ken is busy.　（Yes）", "Is Ken busy? — Yes, he is."),
                ("You play baseball.　（No）", "Do you play baseball? — No, I don't."),
                ("Mai likes music.　（Yes）", "Does Mai like music? — Yes, she does."),
                ("They are from Osaka.　（No）", "Are they from Osaka? — No, they aren't."),
                ("Your father cooks every day.　（Yes）", "Does your father cook every day? — Yes, he does."),
            ]),
            ("（　）に入るほうをノートに書こう。", "row", [
                ("( Are / Do ) you tired?", "Are"),
                ("( Is / Does ) Aya have a dog?", "Does"),
                ("( Do / Does ) they study math?", "Do"),
            ]),
        ]),
    dict(
        no=3, dow="日", title="答え方",
        hint="聞かれたもので答える<br>Are you 〜? → I am / I'm not<br>Does she 〜? → she does<br>　/ she doesn't<br>"
             "主語の言いかえ<br>Ken → he　Mai → she<br>this → it<br>Ken and Mai → they<br><b>you and Mai → we</b>（新しい！）",
        words=[("hungry", "ハングリー", "おなかがすいた"), ("book", "ブック", "本"), ("swim", "スイム", "泳ぐ"), ("classroom", "クラスルーム", "教室")],
        secs=[
            ("質問に答えよう。（　）の Yes / No で答える。答えの文だけ書けばOK。", "list", [
                ("Are you hungry?　（No）", "No, I'm not."),
                ("Does Ken like cats?　（Yes）", "Yes, he does."),
                ("Is your mother busy?　（Yes）", "Yes, she is."),
                ("Do you and Mai play tennis?　（Yes）", "Yes, we do."),
                ("Is this your book?　（No）", "No, it isn't."),
                ("Do they live in Tokyo?　（No）", "No, they don't."),
                ("Does Aya swim?　（No）", "No, she doesn't."),
                ("Is Ken in the classroom?　（Yes）", "Yes, he is."),
            ]),
        ]),
    dict(
        no=4, dow="月", title="＿＿ に入る語",
        hint="① どっちの文？<br>　be動詞？ 一般動詞？<br>② 主語はだれ？<br>　I → am / do<br>　you・we・they → are / do<br>"
             "　he・she・Ken → is / does",
        words=[("piano", "ピアノ", "ピアノ"), ("bag", "バッグ", "かばん"), ("fish", "フィッシュ", "魚"), ("tall", "トール", "背が高い")],
        secs=[
            ("＿＿ に入る語を、下からえらんでノートに書こう。<br><span class=\"en\" style=\"font-weight:400\">am　is　are　do　does　isn't　don't　doesn't</span>", "list", [
                ("＿＿ you from Osaka?", "Are"),
                ("＿＿ she play the piano?", "Does"),
                ("＿＿ this your bag?", "Is"),
                ("＿＿ you have a pen?", "Do"),
                ("They ＿＿ like fish.　（否定文）", "don't"),
                ("Ken ＿＿ tall.　（否定文）", "isn't"),
                ("My father ＿＿ speak English.　（否定文）", "doesn't"),
                ("I ＿＿ not busy.", "am"),
            ]),
        ]),
    dict(
        no=5, dow="火", title="まちがい直し",
        hint="・be動詞と do / does は<br>　<b>いっしょに使わない</b><br>・動詞（play, like…）がない<br>　→ be動詞の文<br>"
             "・Does / doesn't のあとは<br>　動詞に s をつけない<br>・7 は答えの文を直す",
        words=[("soccer", "サッカー", "サッカー"), ("study", "スタディ", "勉強する"), ("dog", "ドッグ", "犬")],
        secs=[
            ("まちがいが1つある。正しい文をノートに書こう。", "list", [
                ("Mai isn't play soccer.", "Mai doesn't play soccer."),
                ("Do she like music?", "Does she like music?"),
                ("Are you have a dog?", "Do you have a dog?"),
                ("Ken doesn't busy.", "Ken isn't busy."),
                ("Does Aya studies English?", "Does Aya study English?"),
                ("I not am hungry.", "I am not hungry."),
                ("Is Ken your brother? — No, he doesn't.", "No, he isn't."),
            ]),
        ]),
    dict(
        no=6, dow="水", title="総まとめ　ならべかえと英作文",
        hint="書く前に3つチェック<br>① be動詞？ 一般動詞？<br>② 主語はだれ？<br>③ 否定文？ 疑問文？<br>"
             "ならべかえは、使わないほうの<br>be動詞 / do が「いらない語」",
        words=[("sister", "シスター", "姉・妹"), ("cat", "キャット", "ねこ"), ("have", "ハヴ", "持っている・飼っている")],
        secs=[
            ("ならべかえて英文を書こう。いらない語が1つずつある。", "list", [
                ("あなたはテニスが好きですか。　[ like / are / you / tennis / do ]", "Do you like tennis?　（いらない語：are）"),
                ("ケンは教室にいません。　[ in / Ken / isn't / doesn't / the classroom ]", "Ken isn't in the classroom.　（いらない語：doesn't）"),
                ("彼女はねこを飼っていますか。　[ she / a cat / does / is / have ]", "Does she have a cat?　（いらない語：is）"),
            ]),
            ("日本語を英語にしよう。", "list", [
                ("わたしは忙しくありません。", "I am not busy."),
                ("あなたの妹は泳ぎますか。 ― いいえ、泳ぎません。", "Does your sister swim? — No, she doesn't."),
                ("彼らは野球をしません。", "They don't play baseball."),
                ("マイはおなかがすいていますか。 ― はい、すいています。", "Is Mai hungry? — Yes, she is."),
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
11/20（金）　1日目<br>① (1) be　(2) 一般　(3) be<br>② 1. I am not from Tokyo.　<span class="r">○</span><br>　 2. Mai doesn't play tennis.　<span class="r">○</span></div></div></div>"""

GRADE = """<div class="grade"><b class="h">丸つけのしかた</b>合っていたら ○、ちがっていたら ✓。✓ の問題は正しい文をノートにもう一度書こう。<br>
isn't / is not、don't / do not、I'm not / I am not は、<b>短い形でも長い形でもどちらも ○</b>。「be」「一般」の判断がちがっていたら、文が合っていても直しをしよう。</div>"""


def page(n: int, total: int, days, first: bool, answers: bool) -> str:
    top = (GRADE if answers else HOWTO) if first else ""
    end = '<div class="end">6日間おつかれさま！ 木曜はこのノートを持ってこよう。</div>' if n == total and not answers else ""
    return f"""<div class="page">
<div class="hd"><span class="tag">宿題</span><div><div class="ttl">{TITLE}</div>
<div class="sub">{SUB}　{n}枚目（{days[0]["no"]}〜{days[-1]["no"]}日目）</div></div><div class="nm">名前</div></div>
{top}{"".join(day_box(d) for d in days)}{end}
<div class="foot">中1英語　n02 宿題　{n}／{total}</div></div>"""


def doc(answers: bool) -> str:
    pages = [page(i // 2 + 1, 3, DAYS[i:i + 2], i == 0, answers) for i in range(0, 6, 2)]
    return (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>n02 宿題</title><style>{CSS}</style></head>'
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
