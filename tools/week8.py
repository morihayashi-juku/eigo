"""8週目：単元② 否定文の4週目「好き・ほしいは 動詞グループ」

6・7週目と同じ形（日本語の「ありません」から考える）では、「好きではありません・ほしくありません」の
まちがいが残った。そこで見方を変えて、英語の単語を
  動詞グループ（like want cook swim play eat …）／ようす・ものグループ（busy sleepy happy kind tall a teacher …）
に分け、「カギの単語」のグループで be＋not／don't を決める週にした。
日本語の「好きだ・ほしい」は「ねむい」と同じ形に見えるが、英語の like・want は play と同じ動詞、という点をくり返す。

  python3 tools/week8.py [--html]
"""
import sys

from eigolib import (READ, S, DONT, cn, esc, fix_list, header, html_doc, judge_table, meaning_list,
                     mini_quiz, opt, point_box, rb, reading, sec, shuffled, stop_box, word_table,
                     card_list, choose_list, write_pdfs)

W = 8
TITLE = "好き・ほしいは 動詞グループ"
UNIT = "単元② 否定文（〜ではない・〜しない）"
WORDS = [("like", "好きだ"), ("want", "ほしい"), ("cook", "料理する"), ("swim", "泳ぐ"),
         ("busy", "いそがしい"), ("sleepy", "ねむい"), ("happy", "うれしい"), ("kind", "親切だ")]
VERB = {"like", "want", "cook", "swim", "play", "eat", "watch", "drink", "study"}  # 動詞グループ

# ---------------------------------------------------------------- 文のストック
B = {  # be動詞＋not（「〜くありません」をわざと多めにして「ほしくありません」とくらべる）
    "busy_you": S("あなたは いそがしくありません。", "You are not busy."),
    "busy_he": S("かれは いそがしくありません。", "He is not busy."),
    "sleepy_i": S("わたしは ねむくありません。", "I am not sleepy."),
    "sleepy_she": S("かのじょは ねむくありません。", "She is not sleepy."),
    "happy_i": S("わたしは うれしくありません。", "I am not happy."),
    "happy_he": S("かれは うれしくありません。", "He is not happy."),
    "tall_you": S("あなたは 背が高くありません。", "You are not tall."),
    "tall_he": S("かれは 背が高くありません。", "He is not tall."),
    "kind_she": S("かのじょは 親切ではありません。", "She is not kind."),
    "kind_he": S("かれは 親切ではありません。", "He is not kind."),
    "kind_you": S("あなたは 親切ではありません。", "You are not kind."),
    "teacher_she": S("かのじょは 先生ではありません。", "She is not a teacher."),
    "student_he": S("かれは 生徒ではありません。", "He is not a student."),
    "friend_he": S("かれは わたしの友だちではありません。", "He is not my friend."),
    "pen_this": S("これは わたしのペンではありません。", "This is not my pen."),
    "book_this": S("これは わたしの本ではありません。", "This is not my book."),
    "tall_i": S("わたしは 背が高くありません。", "I am not tall."),
}
D = {  # don't
    "like_baseball_i": S("わたしは 野球が 好きではありません。", "I don't like baseball."),
    "like_ramen_i": S("わたしは ラーメンが 好きではありません。", "I don't like ramen."),
    "like_curry_i": S("わたしは カレーが 好きではありません。", "I don't like curry."),
    "like_english_you": S("あなたは 英語が 好きではありません。", "You don't like English."),
    "like_tennis_you": S("あなたは テニスが 好きではありません。", "You don't like tennis."),
    "like_music_you": S("あなたは 音楽が 好きではありません。", "You don't like music."),
    "want_pen_i": S("わたしは ペンが ほしくありません。", "I don't want a pen."),
    "want_milk_i": S("わたしは 牛乳が ほしくありません。", "I don't want milk."),
    "want_book_i": S("わたしは 本が ほしくありません。", "I don't want a book."),
    "want_water_you": S("あなたは 水が ほしくありません。", "You don't want water."),
    "want_bag_you": S("あなたは かばんが ほしくありません。", "You don't want a bag."),
    "want_comp_you": S("あなたは コンピューターが ほしくありません。", "You don't want a computer."),
    "cook_i": S("わたしは 料理を しません。", "I don't cook."),
    "cook_you": S("あなたは 料理を しません。", "You don't cook."),
    "swim_i": S("わたしは 泳ぎません。", "I don't swim."),
    "swim_you": S("あなたは 泳ぎません。", "You don't swim."),
    "soccer_i": S("わたしは サッカーを しません。", "I don't play soccer."),
    "ramen_you": S("あなたは ラーメンを 食べません。", "You don't eat ramen."),
    "tv_i": S("わたしは テレビを 見ません。", "I don't watch TV."),
    "like_soccer_you": S("あなたは サッカーが 好きではありません。", "You don't like soccer."),
    "like_milk_you": S("あなたは 牛乳が 好きではありません。", "You don't like milk."),
    "want_ramen_i": S("わたしは ラーメンが ほしくありません。", "I don't want ramen."),
}
X = {**B, **D}


def L(*keys):
    return [X[k] for k in keys]


def C(key, *chunks):
    return (X[key], list(chunks))


# ---------------------------------------------------------------- 8週目の新しい部品
OTHER_BE = ["busy", "sleepy", "happy", "kind", "tall"]
OTHER_DO = ["like", "want", "cook", "swim", "play"]


def key_of(x):
    """カギの単語（be の文は busy・teacher など、do の文は like・want など）"""
    w = [t.strip(".") for t in x.en.split()]
    if x.kind == "do":
        return w[2]
    rest = [t for t in w[3:] if t.lower() not in ("a", "my")]
    return rest[0]


def grp_opts(is_verb):
    return f'{opt("動詞", is_verb)} ／ {opt("ようす・もの", not is_verb)}'


def key_table(items, seed):
    """① カギの単語（2択）→ ② グループ → ③ be＋not／don't"""
    rows = ""
    for i, x in enumerate(items, 1):
        k = key_of(x)
        pool = OTHER_BE if x.kind == "do" else OTHER_DO
        other = shuffled([p for p in pool if p != k], f"{seed}{i}")[0]
        a, b = (k, other) if (i + len(str(seed))) % 2 else (other, k)
        rows += (f'<tr><td class="no">{i}</td><td>{esc(x.jp)}</td>'
                 f'<td class="ch">{opt(a, a == k, en=True)} ／ {opt(b, b == k, en=True)}</td>'
                 f'<td class="ch">{grp_opts(x.kind == "do")}</td>'
                 f'<td class="ch">{opt("be＋not", x.kind == "be")} ／ {opt(DONT, x.kind == "do")}</td></tr>')
    head = ('<th></th><th>日本語</th><th>① カギの単語は？</th><th>② グループは？</th><th>③ どっち？</th>')
    return (f'<table class="t judge"><colgroup><col><col><col style="width:34mm"><col style="width:36mm"><col style="width:28mm"></colgroup>'
            f'<tr>{head}</tr>{rows}</table>'
            '<div class="small">② が「動詞」なら don\'t、「ようす・もの」なら be動詞＋not。①〜③が全部合って1点。</div>')


def sort_words(words, seed):
    """単語の仲間分け：[(英語, 意味)] → 動詞／ようす・もの"""
    cells = ""
    for i, (w, m) in enumerate(words, 1):
        cells += (f'<div class="q" style="grid-template-columns:6mm 30mm 34mm 1fr;align-items:center;column-gap:2mm">{cn(i)}'
                  f'<span class="word" style="font-size:14pt">{rb(w)}</span><span style="font-size:9.6pt">{esc(m)}</span>'
                  f'<span class="par" style="font-size:9.6pt">（ {grp_opts(w.lower() in VERB)} ）</span></div>')
    return f'<div style="display:grid;gap:1.6mm">{cells}</div>'


def group_point(label="ポイント"):
    v = [("like", "好きだ"), ("want", "ほしい"), ("cook", "料理する"), ("swim", "泳ぐ"), ("play", "する")]
    y = [("busy", "いそがしい"), ("sleepy", "ねむい"), ("happy", "うれしい"), ("kind", "親切だ"), ("a teacher", "先生")]
    one = lambda w, m, h: (f'<span style="display:inline-block;white-space:nowrap;margin:0 3.2mm .6mm 0">'
                           + (f'<b style="color:#c2410c">{rb(w)} {esc(m)}</b>' if h else f'{rb(w)} <span style="font-size:8.6pt">{esc(m)}</span>')
                           + '</span>')
    li = lambda xs, hi: "".join(one(w, m, w in hi) for w, m in xs)
    return f"""
<div class="point"><span class="lab">{label}</span>
<div class="big">「好き（like）」「ほしい（want）」は、英語では <span class="red">動詞グループ</span>！</div>
<table class="cmp">
<tr><th></th><th class="do">動詞グループ → <b>don't</b>＋動詞</th><th class="be">ようす・ものグループ → <b>am / are / is ＋ not</b></th></tr>
<tr><td class="k">なかま</td><td>{li(v, {"like", "want"})}</td><td>{li(y, set())}</td></tr>
<tr><td class="k">否定文</td><td>わたしは 牛乳が <b>ほしく</b>ありません。<br>{rb("I don't want milk.")}</td>
<td>わたしは <b>ねむく</b>ありません。<br>{rb("I am not sleepy.")}</td></tr>
</table>
<div class="why">
<div><span class="ic">?</span><b>どうして？</b>日本語の「ほしい」は「ねむい」と同じ形に見えるけど、英語の <b>want</b> は <b>play</b> と同じ 動詞。動詞の文に am はいらない → 否定文は don't。</div>
<div><span class="ic">?</span><b>コツ</b>：日本語の文の中の <b>カギの単語</b>（好き→like、ねむい→sleepy）を英語にして、どっちのグループか見る。</div>
<div><span class="ic">!</span><b>よくあるまちがい</b>：<span class="ng">× I am not like milk.　× I am not want a pen.　× I don't sleepy.</span></div>
</div></div>"""


# ---------------------------------------------------------------- 木曜 授業（4ページ）
THU_TAG = "木曜<br>じゅぎょう"


def thu_hd(i):
    return header("thu", THU_TAG, W, UNIT, f"（{i}/4）" if i else "（こたえ）", TITLE)


def read_table(rows):
    """[(英文, 日本語, 意味を見本で見せるか)]"""
    out = ""
    for i, (en, jp, show) in enumerate(rows, 1):
        mean = esc(jp) if show else f'<span class="fill">{esc(jp)}</span>'
        out += (f'<tr><td class="no">{i}</td><td><span class="en" style="font-size:14pt">{rb(en)}</span></td>'
                f'<td class="boxes">□□□</td><td style="font-size:9.6pt">{mean}</td></tr>')
    return ('<table class="t wt"><colgroup><col><col style="width:68mm"><col style="width:20mm"><col></colgroup>'
            '<tr><th></th><th>英文（声に出して読もう）</th><th>読めた</th><th>意味</th></tr>' + out + "</table>")


def to_neg_list(items, seed):
    out = []
    for i, s in enumerate(items, 1):
        wrong = s.wrong()
        a, b = shuffled([s.en, wrong], f"{seed}-{i}")
        out.append(f'<div class="q">{cn(i)}<div><div class="line-en" style="margin:0">{rb(s.pos_en)} '
                   f'<span style="font-size:8.6pt">→ 否定文にすると？</span></div>'
                   f'<div class="line-en" style="margin-left:6mm">{opt("ア", a == s.en)} {rb(a)}　　{opt("イ", b == s.en)} {rb(b)}</div></div></div>')
    return '<div style="display:grid;gap:3.4mm">' + "".join(out) + "</div>"


def lesson_pages():
    p1 = f"""<div class="page thu">{thu_hd(1)}
{sec("単語", "単語タイム", "先生のあとについて読む → 意味を見る。読めたら □ に1つチェック（3回まで）。今週は新しい単語なし。上の4つが動詞グループ")}
{word_table(WORDS, "read")}
{group_point()}
</div>"""
    p2 = f"""<div class="page thu">{thu_hd(2)}
<div class="chant"><b>はじめの1分：声に出そう！</b>　{rb("like!")} {rb("want!")} {rb("play!")} → 動詞！　{rb("busy!")} {rb("sleepy!")} {rb("happy!")} → ようす！<br>
<span class="small">先生「like は？」→ みんな「動詞！ だから I don't like!」／先生「sleepy は？」→ みんな「ようす！ だから I am not sleepy!」</span></div>
{sec("1", "単語の仲間分け：動詞グループ？ ようす・ものグループ？ ○ でかこもう", "意味を声に出して読んでから")}
{sort_words(shuffled([("like", "好きだ"), ("busy", "いそがしい"), ("want", "ほしい"), ("cook", "料理する"),
                      ("sleepy", "ねむい"), ("happy", "うれしい"), ("swim", "泳ぐ"), ("kind", "親切だ"),
                      ("play", "する"), ("tall", "背が高い")], "s1"), "s1")}
{sec("2", "先生と声に出して読もう → 意味を書こう", "カギの単語に気をつけよう")}
{read_table([("I want a pen.", "わたしは ペンが ほしいです。", True),
             ("I don't want a pen.", "わたしは ペンが ほしくありません。", True),
             ("I am happy.", "わたしは うれしいです。", False),
             ("I am not happy.", "わたしは うれしくありません。", False),
             ("You don't like soccer.", "あなたは サッカーが 好きではありません。", False),
             ("She is not busy.", "かのじょは いそがしくありません。", False)])}
</div>"""
    p3 = f"""<div class="page thu">{thu_hd(3)}
<div class="lead">まず先生が1番を声に出して解いてみせるよ（「ほしくありません…カギの単語は『ほしい』＝ want…want は動詞グループ…だから don't！」）。2番は「ねむい」＝ sleepy。sleepy は…？</div>
{sec("3", "日本語を見て、①→②→③の順に ○ でかこもう")}
{key_table(L("want_milk_i", "sleepy_she", "like_tennis_you", "busy_he", "want_comp_you", "happy_i"), "t3")}
{sec("4", "日本語に合うほうを えらぼう")}
{choose_list(L("like_soccer_you", "tall_i", "want_ramen_i", "kind_she", "like_milk_you", "sleepy_i"), "t4")}
</div>"""
    p4 = f"""<div class="page thu">{thu_hd(4)}
{sec("5", "次の英文は間違っています。正しいのはどっち？ ○ でかこもう")}
{fix_list(L("like_baseball_i", "happy_he", "want_pen_i"), "t5")}
{sec("6", "日本語に合うように、カードをならべて、英文を書こう", "さいしょは大文字、さいごに .")}
{card_list([C("want_ramen_i", "I", "don't", "want", "ramen."),
            C("sleepy_she", "She", "is", "not", "sleepy."),
            C("like_soccer_you", "You", "don't", "like", "soccer.")], "t6")}
{sec("7", "英文を読んで、質問に答えよう")}
{reading("Hi! I am Mika. I am not sleepy. I like music. I don't want a bag.",
         [("ミカは ねむい？", ("ねむい", "ねむくない"), "ねむくない"),
          ("ミカが ほしくないものは？", ("音楽", "かばん"), "かばん")])}
<div class="lead" style="margin-top:auto">このあと、ラスト5分で小テスト（何も見ないでとこう）。</div>
</div>"""
    return [p1, p2, p3, p4]

# ---------------------------------------------------------------- 木曜 小テスト
def thu_quiz_page():
    q = {"which": L("like_milk_you", "happy_he"),
         "choose": L("want_pen_i", "busy_you"),
         "mean": L("sleepy_she", "want_ramen_i")}
    one = mini_quiz("thu", "木曜<br>小テスト", W, UNIT, "ラスト5分・何も見ないでとこう", TITLE, q)
    return [f'<div class="page thu">{one}<div class="cut"><span>きりとり</span></div>{one}</div>']


# ---------------------------------------------------------------- 月曜 自習（8ページ）
MON_TAG = "月曜<br>じしゅう"

MON = {
    "A": dict(
        q1=L("like_soccer_you", "busy_he", "want_book_i", "sleepy_she", "cook_you", "kind_he"),
        q2=L("want_water_you", "happy_i", "like_curry_i", "tall_you", "swim_i", "teacher_she"),
        q3=L("want_ramen_i", "sleepy_i", "like_music_you"),
        q4=L("like_milk_you", "busy_you", "want_pen_i", "happy_he"),
        q5=[C("want_water_you", "You", "don't", "want", "water."),
            C("happy_i", "I", "am", "not", "happy."),
            C("like_baseball_i", "I", "don't", "like", "baseball."),
            C("cook_i", "I", "don't", "cook.")],
        q6=("Hello! I am Taku. I am not tall. I like soccer. I don't like milk.",
            [("タクは 背が高い？", ("高い", "高くない"), "高くない"),
             ("タクが 好きではないのは？", ("サッカー", "牛乳"), "牛乳")]),
        q7=L("want_comp_you", "happy_he", "like_ramen_i", "busy_you", "swim_you", "student_he"),
        q8=L("like_english_you", "sleepy_she", "want_milk_i", "kind_you", "soccer_i", "pen_this"),
        q9=L("like_soccer_you", "busy_he", "want_bag_you"),
        q10=L("want_book_i", "sleepy_she", "like_tennis_you", "cook_you"),
        q11=[C("busy_he", "He", "is", "not", "busy."),
             C("want_ramen_i", "I", "don't", "want", "ramen."),
             C("like_milk_you", "You", "don't", "like", "milk."),
             C("tall_i", "I", "am", "not", "tall.")],
        q12=("Hi! I am Aya. I am not busy. I like curry. I don't want ramen.",
             [("アヤは いそがしい？", ("いそがしい", "いそがしくない"), "いそがしくない"),
              ("アヤが ほしくないものは？", ("カレー", "ラーメン"), "ラーメン")]),
    ),
    "B": dict(
        q1=L("want_pen_i", "sleepy_i", "like_milk_you", "happy_he", "swim_i", "kind_she"),
        q2=L("like_baseball_i", "busy_you", "want_comp_you", "tall_he", "ramen_you", "student_he"),
        q3=L("like_soccer_you", "happy_i", "want_water_you"),
        q4=L("want_ramen_i", "sleepy_she", "like_curry_i", "busy_he"),
        q5=[C("like_tennis_you", "You", "don't", "like", "tennis."),
            C("busy_you", "You", "are", "not", "busy."),
            C("want_milk_i", "I", "don't", "want", "milk."),
            C("swim_you", "You", "don't", "swim.")],
        q6=("Hello! I am Sho. I am not happy. I like tennis. I don't want a pen.",
            [("ショウは うれしい？", ("うれしい", "うれしくない"), "うれしくない"),
             ("ショウが ほしくないものは？", ("テニス", "ペン"), "ペン")]),
        q7=L("like_curry_i", "busy_he", "want_bag_you", "sleepy_she", "cook_i", "friend_he"),
        q8=L("want_ramen_i", "happy_he", "like_soccer_you", "tall_i", "tv_i", "book_this"),
        q9=L("like_milk_you", "sleepy_i", "want_book_i"),
        q10=L("like_english_you", "happy_i", "want_water_you", "swim_you"),
        q11=[C("sleepy_i", "I", "am", "not", "sleepy."),
             C("like_music_you", "You", "don't", "like", "music."),
             C("want_pen_i", "I", "don't", "want", "a pen."),
             C("kind_he", "He", "is", "not", "kind.")],
        q12=("Hi! I am Yuki. I am not sleepy. I like English. I don't like baseball.",
             [("ユキは ねむい？", ("ねむい", "ねむくない"), "ねむくない"),
              ("ユキが 好きではないのは？", ("英語", "野球"), "野球")]),
    ),
}


def mon_pages(pat):
    d = MON[pat]
    hd = lambda i: header("mon", MON_TAG, W, UNIT, f"パターン{pat}（{i}/8）", TITLE)
    steps = "".join(f"<div>□ {a}<br><small>{b}</small></div>" for a, b in
                    [("① 単語", "3分"), ("② ポイント", "3分"), ("③ その1", "12分"),
                     ("④ 丸つけ・分析", "5分"), ("⑤ その2", "12分"), ("⑥ 丸つけ・分析", "5分")])
    card_hint = '<div class="lead"><b style="color:#2a5ca6">【{0}】 手順カード③を見ながら、1問ずつ じっくり</b>　カギの単語は 動詞グループ？ ようす・ものグループ？</div>'
    words2 = shuffled(WORDS, f"w{pat}2")
    p = []
    p.append(f"""<div class="page mon">{hd(1)}<div class="steps">{steps}</div>
{sec("①", "単語タイム", "声に出して読む → 意味を ○ でかこむ（点数は別）", "／8")}
{word_table(shuffled(WORDS, f"w{pat}1"), "choose", seed=f"{pat}1")}
{group_point("② ポイント")}</div>""")
    p.append(f"""<div class="page mon">{hd(2)}{card_hint.format("その1")}
{sec("問1", "日本語を見て、①→②→③の順に ○ でかこもう", pt="1点×6")}{key_table(d["q1"], pat + "1")}
{sec("問2", "日本語に合うほうを えらぼう", pt="1点×6")}{choose_list(d["q2"], pat + "2")}</div>""")
    p.append(f"""<div class="page mon">{hd(3)}
{sec("問3", "次の英文は間違っています。正しいのはどっち？ ○ でかこもう", pt="1点×3")}{fix_list(d["q3"], pat + "3")}
{sec("問4", "英文を読んで、意味を日本語で書こう", "not・don't の意味に気をつけよう", "1点×4")}{meaning_list(d["q4"])}</div>""")
    p.append(f"""<div class="page mon">{hd(4)}
{sec("問5", "日本語に合うように、カードをならべて、英文を書こう", "さいしょは大文字、さいごに .", "1点×4")}{card_list(d["q5"], pat + "5")}
{sec("問6", "英文を読んで、質問に答えよう", pt="1点×2")}{reading(*d["q6"])}
{stop_box("その1")}</div>""")
    p.append(f"""<div class="page mon">{hd(5)}{card_hint.format("その2")}
{sec("問7", "日本語を見て、①→②→③の順に ○ でかこもう", pt="1点×6")}{key_table(d["q7"], pat + "7")}
{sec("問8", "日本語に合うほうを えらぼう", pt="1点×6")}{choose_list(d["q8"], pat + "8")}</div>""")
    p.append(f"""<div class="page mon">{hd(6)}
{sec("問9", "次の英文は間違っています。正しいのはどっち？ ○ でかこもう", pt="1点×3")}{fix_list(d["q9"], pat + "9")}
{sec("問10", "英文を読んで、意味を日本語で書こう", "not・don't の意味に気をつけよう", "1点×4")}{meaning_list(d["q10"])}</div>""")
    p.append(f"""<div class="page mon">{hd(7)}
{sec("問11", "日本語に合うように、カードをならべて、英文を書こう", "さいしょは大文字、さいごに .", "1点×4")}{card_list(d["q11"], pat + "11")}
{sec("問12", "英文を読んで、質問に答えよう", pt="1点×2")}{reading(*d["q12"])}
{stop_box("その2")}</div>""")
    p.append(f"""<div class="page mon">{hd(8)}
{sec("仕上げ", "単語タイム もう一度", "何も見ないで、意味を ○ でかこもう（点数は別）", "／8")}
{word_table(words2, "choose", seed=f"{pat}8")}
<div style="font-size:9pt;margin-top:2mm">点数のまとめ：　その1 <span class="blank"></span> ／25　　その2 <span class="blank"></span> ／25</div>
<div style="font-size:8.6pt">□ 判断（be＋not・don't）を全部書いた → 先生からスタンプ！</div>
<div class="howto"><div><b>④ 丸つけのしかた</b>：前の机の「こたえ」を見て、<b>赤ペン</b>で丸つけ。<br>まちがえたところは、正しい答えを赤で書いておこう。消しゴムで消さない！</div>
<div class="score">点数 <span class="blank"></span> / 50</div>
<div><b>⑤ ふりかえり</b>　◎ よくわかった　○ だいたいOK　△ むずかしかった　（どれかに○）</div>
<div class="memo">木曜に先生に聞きたいこと（なければ空欄でOK）</div></div></div>""")
    return p


# ---------------------------------------------------------------- 月曜のふくしゅう小テスト
def review_page():
    tag = "月曜の<br>ふくしゅう"
    qa = {"which": L("want_book_i", "sleepy_she"), "choose": L("like_curry_i", "busy_he"),
          "mean": L("happy_i", "like_soccer_you")}
    qb = {"which": L("like_milk_you", "tall_he"), "choose": L("want_water_you", "happy_he"),
          "mean": L("busy_you", "want_pen_i")}
    a = mini_quiz("mon", tag, W, UNIT, "パターンA 小テスト（9週目の木曜のはじめにやる）", TITLE, qa, dow="木")
    b = mini_quiz("mon", tag, W, UNIT, "パターンB 小テスト（9週目の木曜のはじめにやる）", TITLE, qb, dow="木")
    return [f'<div class="page mon">{a}<div class="cut"><span>きりとり</span></div>{b}</div>']



# ---------------------------------------------------------------- 宿題（金〜水の6日分・1日半ページ・A4 3枚）
# 2人の宿題の決まり（11/19 決定）：毎日5分。プリントに直接書く。先生が回収して丸つけ（こたえは先生用だけ）。
HW_CSS = """<style>
.hw { --c: #a35d0b; --soft: #fbefdc; }
.day { border: 1.6px solid var(--c); border-radius: 3mm; padding: 3mm 4mm 3.4mm; display: flex; flex-direction: column; gap: 2.4mm; flex: 1; }
.day + .day { margin-top: 1mm; }
.dayhd { display: flex; align-items: center; gap: 3mm; }
.dayhd .dn { background: var(--c); color: #fff; font-weight: 900; border-radius: 99px; padding: .3mm 4mm; font-size: 10.5pt; }
.dayhd .dd { font-size: 9pt; }
.dayhd .ok { margin-left: auto; font-size: 9pt; }
.hwrow { display: grid; grid-template-columns: 6mm 22mm 20mm 1fr 34mm; align-items: center; column-gap: 2mm; font-size: 9.6pt; min-height: 8mm; }
.hwrow .word { font-size: 14pt; }
.wq { display: grid; grid-template-columns: 6mm 1fr 46mm; align-items: center; column-gap: 2mm; font-size: 9.6pt; min-height: 8mm; }
.hwsec { font-weight: 700; font-size: 9.6pt; display: flex; gap: 2mm; align-items: baseline; }
.hwsec .k { color: var(--c); }
.hwsec .s { font-size: 7.8pt; color: #5d6670; font-weight: 400; }
.hwmq { display: grid; grid-template-columns: 6mm 58mm 1fr; column-gap: 2mm; align-items: center; font-size: 9.4pt; min-height: 10mm; }
.hwmq .en { font-size: 13pt; }
</style>"""
ALL_MEAN = [m for _, m in WORDS]
DAYS = [  # (曜日, 単語3つ, 見分け3つ, ("choose"|"mean", 2つ))
    ("金", ["want", "sleepy", "cook"], ["like_curry_i", "busy_you", "want_pen_i"], ("choose", ["sleepy_she", "like_soccer_you"])),
    ("土", ["like", "happy", "swim"], ["want_water_you", "happy_he", "like_music_you"], ("choose", ["want_ramen_i", "tall_you"])),
    ("日", ["busy", "want", "kind"], ["sleepy_i", "like_milk_you", "want_book_i"], ("choose", ["busy_he", "like_english_you"])),
    ("月", ["cook", "like", "sleepy"], ["want_comp_you", "kind_she", "like_ramen_i"], ("mean", ["want_milk_i", "happy_i"])),
    ("火", ["swim", "happy", "want"], ["like_tennis_you", "sleepy_she", "want_bag_you"], ("mean", ["like_baseball_i", "busy_he"])),
    ("水", ["kind", "busy", "like"], ["want_pen_i", "happy_i", "like_soccer_you"], ("mean", ["sleepy_i", "want_water_you"])),
]


def hw_words(ws, seed):
    mean = dict(WORDS)
    out = ""
    for i, w in enumerate(ws, 1):
        others = [m for m in ALL_MEAN if m != mean[w]]
        ch = shuffled(others, f"{seed}{w}")[:2]
        ch.insert((i + len(seed)) % 3, mean[w])
        cells = " ／ ".join(opt(m, m == mean[w]) for m in ch)
        out += (f'<div class="hwrow">{cn(i)}<span class="word">{esc(w)}</span><span>{READ[w.lower()]}</span>'
                f'<span class="par">（ {cells} ）</span><span class="par" style="font-size:8.6pt">（ {opt("動詞", w in VERB)} ・ {opt("ようす", w not in VERB)} ）</span></div>')
    return out


def hw_which(items):
    return "".join(
        f'<div class="wq">{cn(i)}<span>{esc(x.jp)}</span>'
        f'<span class="par">（ {opt("be＋not", x.kind == "be")} ／ {opt(DONT, x.kind == "do")} ）</span></div>'
        for i, x in enumerate(items, 1))


def hw_mean(items, seed):
    out = ""
    for i, x in enumerate(items, 1):
        a, b = (x.jp, x.pos_jp) if (i + len(seed)) % 2 else (x.pos_jp, x.jp)
        out += (f'<div class="hwmq">{cn(i)}{rb(x.en)}<span>{opt("ア", a == x.jp)} {esc(a)}<br>{opt("イ", b == x.jp)} {esc(b)}</span></div>')
    return out


def hw_day(n, day):
    dow, ws, which, (kind, last) = day
    if kind == "choose":
        third = (f'<div class="hwsec"><span class="k">③</span>日本語に合うほうを ○ でかこもう'
                 f'<span class="s">先に（be・一般）を ○</span></div>' + choose_list(L(*last), f"hw{n}").replace(
                     '<div class="small">先に（be・一般）を ○ してから、答えを ○。両方合って1点。</div>', ""))
    else:
        third = (f'<div class="hwsec"><span class="k">③</span>英文を読んで、意味はどっち？ ア・イ を ○'
                 f'<span class="s">not・don\'t の意味に気をつけよう</span></div>' + hw_mean(L(*last), f"hw{n}"))
    return f"""<div class="day">
<div class="dayhd"><span class="dn">{n}日目（{dow}）</span><span class="dd">やった日　　月　　日</span><span class="ok">□ できた（5分）</span></div>
<div class="hwsec"><span class="k">①</span>単語：声に出して読んで、意味と グループを ○ でかこもう</div>
<div>{hw_words(ws, f"d{n}")}</div>
<div class="hwsec"><span class="k">②</span>否定文にするとき、どっちを使う？ ○ でかこもう<span class="s">好き（like）・ほしい（want）は 動詞グループ → don't！</span></div>
<div>{hw_which(L(*which))}</div>
{third}
</div>"""


def homework_pages():
    pages = []
    for k in range(3):
        a, b = DAYS[2 * k], DAYS[2 * k + 1]
        hd = header("thu", "宿題", W, "単元② 否定文", f"{k + 1}枚目（{a[0]}・{b[0]}）　1日5分・月曜と木曜に持ってこよう", TITLE, dow="　")
        pages.append(f'<div class="page hw">{HW_CSS if k == 0 else ""}{hd}{hw_day(2 * k + 1, a)}{hw_day(2 * k + 2, b)}</div>')
    return pages

# ---------------------------------------------------------------- 書き出し
def main():
    les, quiz, ma, mb, rev = lesson_pages(), thu_quiz_page(), mon_pages("A"), mon_pages("B"), review_page()
    hw = homework_pages()
    f = lambda n: f"w{W}_{n}.pdf"
    jobs = {
        f("1_Thu_lesson"): html_doc(les),
        f("2_Thu_quiz"): html_doc(quiz),
        f("3_Mon_selfstudy_A"): html_doc(ma),
        f("4_Mon_selfstudy_B"): html_doc(mb),
        f("5_Mon_review_quiz_AB"): html_doc(rev),
        f("6_answers"): html_doc(les + quiz + ma + mb + rev, answers=True),
        f("7_homework"): html_doc(hw),
        f("8_homework_answers"): html_doc(hw, answers=True),
    }
    write_pdfs(jobs, keep_html="--html" in sys.argv)


if __name__ == "__main__":
    main()
