"""7週目：単元② 否定文の3週目「好き・ほしいをもう一度」

6週目でも「好きではありません・ほしくありません」に be＋not を使うまちがいが残ったので、
同じ型でもう1週。新しい単語は入れず、「〜くありません」（いそがしく・ねむく・うれしく・背が高く）を多めにして
「ほしくありません」とならべてくらべる。

  python3 tools/week7.py [--html]
"""
import sys

from eigolib import (S, DONT, cn, esc, fix_list, header, html_doc, judge_table, meaning_list,
                     mini_quiz, opt, point_box, rb, reading, sec, shuffled, stop_box, word_table,
                     card_list, choose_list, write_pdfs)

W = 7
TITLE = "好き・ほしいをもう一度"
UNIT = "単元② 否定文（〜ではない・〜しない）"
WORDS = [("like", "好きだ"), ("want", "ほしい"), ("busy", "いそがしい"), ("sleepy", "ねむい"),
         ("happy", "うれしい"), ("kind", "親切だ"), ("cook", "料理する"), ("swim", "泳ぐ")]

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
}
X = {**B, **D}


def L(*keys):
    return [X[k] for k in keys]


def C(key, *chunks):
    return (X[key], list(chunks))


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
{sec("単語", "単語タイム", "先生のあとについて読む → 意味を見る。読めたら □ に1つチェック（3回まで）。今週は新しい単語なし")}
{word_table(WORDS, "read")}
{point_box()}
</div>"""
    p2 = f"""<div class="page thu">{thu_hd(2)}
<div class="chant"><b>はじめの1分：声に出そう！</b>　{rb("I don't like!")} {rb("I don't want!")} {rb("I am not!")} {rb("You are not!")}<br>
<span class="small">先生「ほしくありません」→ みんな「I don't want!」／先生「ねむくありません」→ みんな「I am not!」／先生「好きではありません」→ みんな「I don't like!」</span></div>
{sec("1", "先生と声に出して読もう → 意味を書こう", "ふつうの文と否定文をくらべよう")}
{read_table([("I am sleepy.", "わたしは ねむいです。", True),
             ("I am not sleepy.", "わたしは ねむくありません。", True),
             ("I want milk.", "わたしは 牛乳が ほしいです。", False),
             ("I don't want milk.", "わたしは 牛乳が ほしくありません。", False),
             ("You are not busy.", "あなたは いそがしくありません。", False),
             ("You don't like English.", "あなたは 英語が 好きではありません。", False),
             ("He is not happy.", "かれは うれしくありません。", False),
             ("I don't play soccer.", "わたしは サッカーを しません。", False)])}
{sec("2", "否定文にすると、正しいのはどっち？ ○ でかこもう")}
{to_neg_list(L("busy_you", "want_milk_i", "happy_he", "like_english_you", "sleepy_i"), "t2")}
</div>"""
    p3 = f"""<div class="page thu">{thu_hd(3)}
<div class="lead">まず先生が1番を声に出して解いてみせるよ（「ねむ<b>く</b>ありません…『く』があっても、好き・ほしいじゃない…だから be動詞＋not！」）。2番は「ほし<b>く</b>ありません」。同じ「く」だけど…？</div>
{sec("3", "日本語を見て、①→②→③の順に ○ でかこもう")}
{judge_table(L("sleepy_i", "want_pen_i", "busy_he", "like_baseball_i", "cook_you", "kind_she"))}
{sec("4", "日本語に合うほうを えらぼう")}
{choose_list(L("happy_i", "like_tennis_you", "tall_he", "want_comp_you", "swim_i", "student_he"), "t4")}
</div>"""
    p4 = f"""<div class="page thu">{thu_hd(4)}
{sec("5", "次の英文は間違っています。正しいのはどっち？ ○ でかこもう")}
{fix_list(L("want_water_you", "sleepy_she", "like_ramen_i"), "t5")}
{sec("6", "日本語に合うように、カードをならべて、英文を書こう", "さいしょは大文字、さいごに .")}
{card_list([C("busy_he", "He", "is", "not", "busy."),
            C("want_milk_i", "I", "don't", "want", "milk."),
            C("like_english_you", "You", "don't", "like", "English.")], "t6")}
{sec("7", "英文を読んで、質問に答えよう")}
{reading("Hi! I am Sho. I am not busy. I like baseball. I don't want a computer.",
         [("ショウは いそがしい？", ("いそがしい", "いそがしくない"), "いそがしくない"),
          ("ショウが ほしくないものは？", ("野球", "コンピューター"), "コンピューター")])}
<div class="lead" style="margin-top:auto">このあと、ラスト5分で小テスト（何も見ないでとこう）。</div>
</div>"""
    return [p1, p2, p3, p4]


# ---------------------------------------------------------------- 木曜 小テスト
def thu_quiz_page():
    q = {"which": L("want_water_you", "sleepy_i"),
         "choose": L("like_english_you", "happy_he"),
         "mean": L("busy_you", "like_baseball_i")}
    one = mini_quiz("thu", "木曜<br>小テスト", W, UNIT, "ラスト5分・何も見ないでとこう", TITLE, q)
    return [f'<div class="page thu">{one}<div class="cut"><span>きりとり</span></div>{one}</div>']


# ---------------------------------------------------------------- 月曜 自習（8ページ）
MON_TAG = "月曜<br>じしゅう"

MON = {
    "A": dict(
        q1=L("want_pen_i", "sleepy_she", "like_english_you", "busy_he", "swim_i", "happy_i"),
        q2=L("like_baseball_i", "tall_you", "want_water_you", "kind_she", "ramen_you", "teacher_she"),
        q3=L("want_milk_i", "busy_you", "like_music_you"),
        q4=L("like_ramen_i", "sleepy_i", "want_bag_you", "happy_he"),
        q5=[C("want_pen_i", "I", "don't", "want", "a pen."),
            C("busy_he", "He", "is", "not", "busy."),
            C("like_english_you", "You", "don't", "like", "English."),
            C("swim_you", "You", "don't", "swim.")],
        q6=("Hello! I am Yuki. I am not sleepy. I like milk. I don't want water.",
            [("ユキは ねむい？", ("ねむい", "ねむくない"), "ねむくない"),
             ("ユキが ほしくないものは？", ("牛乳", "水"), "水")]),
        q7=L("like_tennis_you", "kind_he", "want_comp_you", "sleepy_i", "cook_i", "student_he"),
        q8=L("want_book_i", "happy_he", "like_curry_i", "busy_you", "soccer_i", "pen_this"),
        q9=L("like_baseball_i", "sleepy_she", "want_water_you"),
        q10=L("want_comp_you", "tall_he", "like_music_you", "cook_you"),
        q11=[C("happy_i", "I", "am", "not", "happy."),
             C("like_ramen_i", "I", "don't", "like", "ramen."),
             C("want_milk_i", "I", "don't", "want", "milk."),
             C("kind_you", "You", "are", "not", "kind.")],
        q12=("Hi! I am Rina. I am not busy. I like tennis. I don't like curry.",
             [("リナは いそがしい？", ("いそがしい", "いそがしくない"), "いそがしくない"),
              ("リナが 好きではないのは？", ("テニス", "カレー"), "カレー")]),
    ),
    "B": dict(
        q1=L("like_ramen_i", "busy_you", "want_comp_you", "happy_he", "cook_you", "kind_she"),
        q2=L("want_milk_i", "sleepy_i", "like_tennis_you", "tall_he", "tv_i", "student_he"),
        q3=L("want_water_you", "happy_i", "like_baseball_i"),
        q4=L("like_english_you", "busy_he", "want_pen_i", "kind_you"),
        q5=[C("like_music_you", "You", "don't", "like", "music."),
            C("sleepy_she", "She", "is", "not", "sleepy."),
            C("want_book_i", "I", "don't", "want", "a book."),
            C("cook_i", "I", "don't", "cook.")],
        q6=("Hello! I am Ken. I am not happy. I like English. I don't want a pen.",
            [("ケンは うれしい？", ("うれしい", "うれしくない"), "うれしくない"),
             ("ケンが ほしくないものは？", ("英語", "ペン"), "ペン")]),
        q7=L("want_bag_you", "tall_you", "like_curry_i", "sleepy_she", "swim_you", "friend_he"),
        q8=L("like_music_you", "kind_he", "want_water_you", "happy_i", "ramen_you", "book_this"),
        q9=L("like_english_you", "busy_he", "want_comp_you"),
        q10=L("want_milk_i", "sleepy_she", "like_tennis_you", "swim_i"),
        q11=[C("busy_you", "You", "are", "not", "busy."),
             C("want_water_you", "You", "don't", "want", "water."),
             C("like_baseball_i", "I", "don't", "like", "baseball."),
             C("tall_he", "He", "is", "not", "tall.")],
        q12=("Hi! I am Aya. I am not sleepy. I like baseball. I don't like milk.",
             [("アヤは ねむい？", ("ねむい", "ねむくない"), "ねむくない"),
              ("アヤが 好きではないのは？", ("野球", "牛乳"), "牛乳")]),
    ),
}


def mon_pages(pat):
    d = MON[pat]
    hd = lambda i: header("mon", MON_TAG, W, UNIT, f"パターン{pat}（{i}/8）", TITLE)
    steps = "".join(f"<div>□ {a}<br><small>{b}</small></div>" for a, b in
                    [("① 単語", "3分"), ("② ポイント", "3分"), ("③ その1", "12分"),
                     ("④ 丸つけ・分析", "5分"), ("⑤ その2", "12分"), ("⑥ 丸つけ・分析", "5分")])
    card_hint = '<div class="lead"><b style="color:#2a5ca6">【{0}】 手順カード③を見ながら、1問ずつ じっくり</b>　「〜くありません」が出たら、ほしくありません？ それとも ねむく・いそがしく…？</div>'
    words2 = shuffled(WORDS, f"w{pat}2")
    p = []
    p.append(f"""<div class="page mon">{hd(1)}<div class="steps">{steps}</div>
{sec("①", "単語タイム", "声に出して読む → 意味を ○ でかこむ（点数は別）", "／8")}
{word_table(shuffled(WORDS, f"w{pat}1"), "choose", seed=f"{pat}1")}
{point_box("② ポイント")}</div>""")
    p.append(f"""<div class="page mon">{hd(2)}{card_hint.format("その1")}
{sec("問1", "日本語を見て、①→②→③の順に ○ でかこもう", pt="1点×6")}{judge_table(d["q1"])}
{sec("問2", "日本語に合うほうを えらぼう", pt="1点×6")}{choose_list(d["q2"], pat + "2")}</div>""")
    p.append(f"""<div class="page mon">{hd(3)}
{sec("問3", "次の英文は間違っています。正しいのはどっち？ ○ でかこもう", pt="1点×3")}{fix_list(d["q3"], pat + "3")}
{sec("問4", "英文を読んで、意味を日本語で書こう", "not・don't の意味に気をつけよう", "1点×4")}{meaning_list(d["q4"])}</div>""")
    p.append(f"""<div class="page mon">{hd(4)}
{sec("問5", "日本語に合うように、カードをならべて、英文を書こう", "さいしょは大文字、さいごに .", "1点×4")}{card_list(d["q5"], pat + "5")}
{sec("問6", "英文を読んで、質問に答えよう", pt="1点×2")}{reading(*d["q6"])}
{stop_box("その1")}</div>""")
    p.append(f"""<div class="page mon">{hd(5)}{card_hint.format("その2")}
{sec("問7", "日本語を見て、①→②→③の順に ○ でかこもう", pt="1点×6")}{judge_table(d["q7"])}
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
    qa = {"which": L("like_ramen_i", "busy_he"), "choose": L("want_pen_i", "tall_you"),
          "mean": L("sleepy_she", "want_book_i")}
    qb = {"which": L("want_milk_i", "kind_she"), "choose": L("like_tennis_you", "sleepy_i"),
          "mean": L("happy_he", "like_curry_i")}
    a = mini_quiz("mon", tag, W, UNIT, "パターンA 小テスト（8週目の木曜のはじめにやる）", TITLE, qa, dow="木")
    b = mini_quiz("mon", tag, W, UNIT, "パターンB 小テスト（8週目の木曜のはじめにやる）", TITLE, qb, dow="木")
    return [f'<div class="page mon">{a}<div class="cut"><span>きりとり</span></div>{b}</div>']


# ---------------------------------------------------------------- 書き出し
def main():
    les, quiz, ma, mb, rev = lesson_pages(), thu_quiz_page(), mon_pages("A"), mon_pages("B"), review_page()
    f = lambda n: f"w{W}_{n}.pdf"
    jobs = {
        f("1_Thu_lesson"): html_doc(les),
        f("2_Thu_quiz"): html_doc(quiz),
        f("3_Mon_selfstudy_A"): html_doc(ma),
        f("4_Mon_selfstudy_B"): html_doc(mb),
        f("5_Mon_review_quiz_AB"): html_doc(rev),
        f("6_answers"): html_doc(les + quiz + ma + mb + rev, answers=True),
    }
    write_pdfs(jobs, keep_html="--html" in sys.argv)


if __name__ == "__main__":
    main()
