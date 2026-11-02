"""6週目：単元② 否定文の2週目「好き・ほしいに気をつけよう」

5週目で「好きではありません・ほしくありません」に be＋not を使ってしまう子がいたので、
同じ「ではありません／くありません」でも be＋not になる 親切（kind）・背が高い（tall）を
新しい単語に入れて、ならべてくらべる週にした。cook・swim は目的語なしで言える一般動詞。

次の週を作るときは、このファイルをコピーして W・TITLE・単語・問題の割り当てを書きかえる。
  python3 tools/week6.py [--html]
"""
import sys

from eigolib import (S, DONT, cn, esc, fix_list, header, html_doc, judge_table, meaning_list,
                     mini_quiz, opt, point_box, rb, reading, sec, shuffled, stop_box, word_table,
                     card_list, choose_list, write_pdfs)

W = 6
TITLE = "好き・ほしいに気をつけよう"
UNIT = "単元② 否定文（〜ではない・〜しない）"
WORDS = [("kind", "親切だ"), ("tall", "背が高い"), ("cook", "料理する"), ("swim", "泳ぐ"),
         ("like", "好きだ"), ("want", "ほしい"), ("not", "〜ではない"), ("don't", "〜しない")]

# ---------------------------------------------------------------- 文のストック
B = {  # be動詞＋not
    "kind_he": S("かれは 親切ではありません。", "He is not kind."),
    "kind_she": S("かのじょは 親切ではありません。", "She is not kind."),
    "kind_you": S("あなたは 親切ではありません。", "You are not kind."),
    "tall_i": S("わたしは 背が高くありません。", "I am not tall."),
    "tall_you": S("あなたは 背が高くありません。", "You are not tall."),
    "tall_he": S("かれは 背が高くありません。", "He is not tall."),
    "tall_she": S("かのじょは 背が高くありません。", "She is not tall."),
    "busy_i": S("わたしは いそがしくありません。", "I am not busy."),
    "sleepy_you": S("あなたは ねむくありません。", "You are not sleepy."),
    "happy_she": S("かのじょは うれしくありません。", "She is not happy."),
    "teacher_he": S("かれは 先生ではありません。", "He is not a teacher."),
    "student_she": S("かのじょは 生徒ではありません。", "She is not a student."),
    "friend_you": S("あなたは わたしの友だちではありません。", "You are not my friend."),
    "book_this": S("これは わたしの本ではありません。", "This is not my book."),
    "bag_this": S("これは わたしのかばんではありません。", "This is not my bag."),
}
D = {  # don't
    "like_tennis_i": S("わたしは テニスが 好きではありません。", "I don't like tennis."),
    "like_music_i": S("わたしは 音楽が 好きではありません。", "I don't like music."),
    "like_milk_i": S("わたしは 牛乳が 好きではありません。", "I don't like milk."),
    "like_milk_you": S("あなたは 牛乳が 好きではありません。", "You don't like milk."),
    "like_curry_you": S("あなたは カレーが 好きではありません。", "You don't like curry."),
    "like_soccer_you": S("あなたは サッカーが 好きではありません。", "You don't like soccer."),
    "want_bag_i": S("わたしは かばんが ほしくありません。", "I don't want a bag."),
    "want_comp_i": S("わたしは コンピューターが ほしくありません。", "I don't want a computer."),
    "want_book_you": S("あなたは 本が ほしくありません。", "You don't want a book."),
    "want_ramen_you": S("あなたは ラーメンが ほしくありません。", "You don't want ramen."),
    "cook_i": S("わたしは 料理を しません。", "I don't cook."),
    "cook_you": S("あなたは 料理を しません。", "You don't cook."),
    "swim_i": S("わたしは 泳ぎません。", "I don't swim."),
    "swim_you": S("あなたは 泳ぎません。", "You don't swim."),
    "water_i": S("わたしは 水を 飲みません。", "I don't drink water."),
    "tv_you": S("あなたは テレビを 見ません。", "You don't watch TV."),
    "english_i": S("わたしは 英語を 勉強しません。", "I don't study English."),
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
{sec("単語", "単語タイム", "先生のあとについて読む → 意味を見る。読めたら □ に1つチェック（3回まで）。kind・tall・cook・swim が新しい単語")}
{word_table(WORDS, "read")}
{point_box()}
</div>"""
    p2 = f"""<div class="page thu">{thu_hd(2)}
<div class="chant"><b>はじめの1分：声に出そう！</b>　{rb("I am not!")} {rb("You are not!")} {rb("I don't like!")} {rb("I don't want!")}<br>
<span class="small">先生「好きではありません」→ みんな「I don't like!」／先生「背が高くありません」→ みんな「I am not!」</span></div>
{sec("1", "先生と声に出して読もう → 意味を書こう", "ふつうの文と否定文をくらべよう")}
{read_table([("He is kind.", "かれは 親切です。", True),
             ("He is not kind.", "かれは 親切ではありません。", True),
             ("I like tennis.", "わたしは テニスが 好きです。", False),
             ("I don't like tennis.", "わたしは テニスが 好きではありません。", False),
             ("She is not tall.", "かのじょは 背が高くありません。", False),
             ("You don't want a book.", "あなたは 本が ほしくありません。", False),
             ("I don't swim.", "わたしは 泳ぎません。", False),
             ("You are not kind.", "あなたは 親切ではありません。", False)])}
{sec("2", "否定文にすると、正しいのはどっち？ ○ でかこもう")}
{to_neg_list(L("kind_you", "want_bag_i", "tall_she", "like_music_i", "tall_i"), "t2")}
</div>"""
    p3 = f"""<div class="page thu">{thu_hd(3)}
<div class="lead">まず先生が1番を声に出して解いてみせるよ（「最後は『ありません』…好き・ほしいじゃない…だから be動詞＋not！」）。2番は「好き」だから…？</div>
{sec("3", "日本語を見て、①→②→③の順に ○ でかこもう")}
{judge_table(L("tall_i", "like_tennis_i", "swim_you", "kind_he", "want_book_you", "happy_she"))}
{sec("4", "日本語に合うほうを えらぼう")}
{choose_list(L("kind_you", "want_comp_i", "tall_she", "cook_i", "like_milk_you", "teacher_he"), "t4")}
</div>"""
    p4 = f"""<div class="page thu">{thu_hd(4)}
{sec("5", "次の英文は間違っています。正しいのはどっち？ ○ でかこもう")}
{fix_list(L("like_curry_you", "kind_she", "want_comp_i"), "t5")}
{sec("6", "日本語に合うように、カードをならべて、英文を書こう", "さいしょは大文字、さいごに .")}
{card_list([C("tall_he", "He", "is", "not", "tall."),
            C("like_music_i", "I", "don't", "like", "music."),
            C("want_book_you", "You", "don't", "want", "a book.")], "t6")}
{sec("7", "英文を読んで、質問に答えよう")}
{reading("Hi! I am Mika. I am not tall. I like music. I don't like soccer.",
         [("ミカは 背が高い？", ("高い", "高くない"), "高くない"),
          ("ミカが 好きではないのは？", ("音楽", "サッカー"), "サッカー")])}
<div class="lead" style="margin-top:auto">このあと、ラスト5分で小テスト（何も見ないでとこう）。</div>
</div>"""
    return [p1, p2, p3, p4]


# ---------------------------------------------------------------- 木曜 小テスト
def thu_quiz_page():
    q = {"which": L("like_milk_i", "kind_he"),
         "choose": L("want_book_you", "tall_she"),
         "mean": L("kind_you", "swim_i")}
    one = mini_quiz("thu", "木曜<br>小テスト", W, UNIT, "ラスト5分・何も見ないでとこう", TITLE, q)
    return [f'<div class="page thu">{one}<div class="cut"><span>きりとり</span></div>{one}</div>']


# ---------------------------------------------------------------- 月曜 自習（8ページ）
MON_TAG = "月曜<br>じしゅう"

MON = {
    "A": dict(
        q1=L("like_music_i", "kind_she", "cook_i", "want_ramen_you", "tall_i", "teacher_he"),
        q2=L("like_milk_you", "tall_he", "swim_i", "kind_you", "want_comp_i", "book_this"),
        q3=L("want_bag_i", "sleepy_you", "like_tennis_i"),
        q4=L("like_curry_you", "tall_she", "want_book_you", "kind_he"),
        q5=[C("like_soccer_you", "You", "don't", "like", "soccer."),
            C("tall_you", "You", "are", "not", "tall."),
            C("want_comp_i", "I", "don't", "want", "a computer."),
            C("cook_you", "You", "don't", "cook.")],
        q6=("Hello! I am Aya. I am not tall. I like milk. I don't want a bag.",
            [("アヤは 背が高い？", ("高い", "高くない"), "高くない"),
             ("アヤが ほしくないものは？", ("牛乳", "かばん"), "かばん")]),
        q7=L("kind_you", "want_bag_i", "swim_you", "happy_she", "like_tennis_i", "tall_he"),
        q8=L("want_ramen_you", "kind_she", "english_i", "tall_i", "like_music_i", "friend_you"),
        q9=L("want_comp_i", "kind_he", "like_milk_you"),
        q10=L("like_music_i", "tall_you", "cook_i", "book_this"),
        q11=[C("kind_she", "She", "is", "not", "kind."),
             C("like_curry_you", "You", "don't", "like", "curry."),
             C("swim_i", "I", "don't", "swim."),
             C("want_book_you", "You", "don't", "want", "a book.")],
        q12=("Hi! I am Taku. I am not busy. I like baseball. I don't like tennis.",
             [("タクは いそがしい？", ("いそがしい", "いそがしくない"), "いそがしくない"),
              ("タクが 好きではないのは？", ("野球", "テニス"), "テニス")]),
    ),
    "B": dict(
        q1=L("tall_she", "like_curry_you", "cook_you", "kind_he", "want_comp_i", "busy_i"),
        q2=L("like_tennis_i", "kind_she", "tv_you", "tall_you", "want_book_you", "bag_this"),
        q3=L("want_ramen_you", "tall_i", "like_music_i"),
        q4=L("like_soccer_you", "tall_he", "want_bag_i", "kind_you"),
        q5=[C("like_tennis_i", "I", "don't", "like", "tennis."),
            C("kind_he", "He", "is", "not", "kind."),
            C("want_book_you", "You", "don't", "want", "a book."),
            C("cook_i", "I", "don't", "cook.")],
        q6=("Hello! I am Rina. I am not tall. I like curry. I don't like ramen.",
            [("リナが 好きではないのは？", ("カレー", "ラーメン"), "ラーメン"),
             ("リナは 背が高い？", ("高い", "高くない"), "高くない")]),
        q7=L("like_milk_i", "kind_she", "swim_i", "want_book_you", "tall_you", "bag_this"),
        q8=L("like_soccer_you", "tall_she", "water_i", "kind_you", "want_bag_i", "student_she"),
        q9=L("like_curry_you", "happy_she", "want_bag_i"),
        q10=L("want_ramen_you", "kind_she", "like_tennis_i", "swim_you"),
        q11=[C("tall_i", "I", "am", "not", "tall."),
             C("like_soccer_you", "You", "don't", "like", "soccer."),
             C("want_comp_i", "I", "don't", "want", "a computer."),
             C("kind_you", "You", "are", "not", "kind.")],
        q12=("Hi! I am Ken. I am not sleepy. I like music. I don't want a computer.",
             [("ケンは ねむい？", ("ねむい", "ねむくない"), "ねむくない"),
              ("ケンが ほしくないものは？", ("音楽", "コンピューター"), "コンピューター")]),
    ),
}


def mon_pages(pat):
    d = MON[pat]
    hd = lambda i: header("mon", MON_TAG, W, UNIT, f"パターン{pat}（{i}/8）", TITLE)
    steps = "".join(f"<div>□ {a}<br><small>{b}</small></div>" for a, b in
                    [("① 単語", "3分"), ("② ポイント", "3分"), ("③ その1", "12分"),
                     ("④ 丸つけ・分析", "5分"), ("⑤ その2", "12分"), ("⑥ 丸つけ・分析", "5分")])
    card_hint = '<div class="lead"><b style="color:#2a5ca6">【{0}】 手順カード③を見ながら、1問ずつ じっくり</b>　「好き」「ほしい」が出たら、とくに気をつけよう</div>'
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
    qa = {"which": L("like_soccer_you", "tall_i"), "choose": L("kind_he", "want_bag_i"),
          "mean": L("like_curry_you", "tall_she")}
    qb = {"which": L("like_music_i", "kind_she"), "choose": L("want_book_you", "tall_you"),
          "mean": L("swim_i", "kind_he")}
    a = mini_quiz("mon", tag, W, UNIT, "パターンA 小テスト（7週目の木曜のはじめにやる）", TITLE, qa, dow="木")
    b = mini_quiz("mon", tag, W, UNIT, "パターンB 小テスト（7週目の木曜のはじめにやる）", TITLE, qb, dow="木")
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
