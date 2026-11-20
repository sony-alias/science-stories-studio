"""I026 The Letter to Hardy, a Science Stories episode.

After R. Kanigel, The Man Who Knew Infinity (1991). Script and sources: episodes/I026_script.md

Render:  manim -qh --frame_rate 30 episodes/I026_ramanujan_letter.py LetterToHardy
Then:    scripts/finish_video.sh media/videos/I026_ramanujan_letter/1080p30/LetterToHardy.mp4 out/I026_ramanujan_letter.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

from mpmath import mp, mpf, factorial as mfact, sqrt as msqrt, pi as mpi  # noqa: E402

MONO = "DejaVu Sans Mono"
GREEN_INK = "#3f6b3a"
mp.dps = 60
PI_STR = mp.nstr(+mpi, 40, strip_zeros=False)          # 3.141592653589793238462643383279502884197


def note(text, size=17, color=FADED):
    return serif(text, size, color, italic=True)


def P(x, y):
    return np.array([x, y, 0.0])


def mono(text, size=20, color=INK):
    return Text(text, font=MONO, font_size=size, color=color)


def plain_cameo(scale=0.85):
    """Kit cameo with the moustache taken off (stylised, not a likeness)."""
    c = cameo("collar", scale)
    c[2][1][0].set_opacity(0)
    return c


def cameo_label(name, sub):
    return VGroup(serif(name, 20, INK), note(sub, 15)).arrange(DOWN, buff=0.05)


def ramanujan_partial(k):
    s = mpf(0)
    for j in range(k + 1):
        s += mfact(4 * j) * (1103 + 26390 * j) / (mfact(j) ** 4 * mpf(396) ** (4 * j))
    return 9801 / (2 * msqrt(2) * s)


def correct_digits(v):
    """Number of leading significant digits of v that agree with pi."""
    a = mp.nstr(v, 45, strip_zeros=False).replace(".", "")
    b = PI_STR.replace(".", "")
    n = 0
    while n < min(len(a), len(b)) and a[n] == b[n]:
        n += 1
    return n


def digit_line(value_str, good, size=26):
    """A number with its first `good` significant digits in ink and the rest in red."""
    chars = VGroup()
    count = 0
    for ch in value_str:
        if ch.isdigit():
            count += 1
            col = INK if count <= good else RED_INK
        else:
            col = INK
        chars.add(Text(ch, font=MONO, font_size=size, color=col))
    chars.arrange(RIGHT, buff=0.02, aligned_edge=DOWN)
    return chars


def envelope(w=3.2, h=2.0):
    body = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=2, fill_color="#e6d6b4", fill_opacity=1)
    flap = Polygon(P(-w / 2, h / 2), P(w / 2, h / 2), P(0, -0.1), stroke_color=INK, stroke_width=1.5,
                   fill_color=PAPER_DARK, fill_opacity=1)
    stampbox = Rectangle(width=0.5, height=0.6, stroke_color=RED_INK, stroke_width=1.5).move_to(
        P(w / 2 - 0.4, h / 2 - 0.45))
    post = Circle(radius=0.33, stroke_color=SEPIA, stroke_width=1.2).move_to(P(w / 2 - 0.85, h / 2 - 0.5))
    post_t = Text("MADRAS", font_size=9, color=SEPIA).move_to(post)
    addr = VGroup(*[Line(P(-0.9, y), P(0.9 - 0.3 * i, y), color=FADED, stroke_width=1.5)
                    for i, y in enumerate([-0.35, -0.55, -0.75])])
    return VGroup(body, flap, stampbox, post, post_t, addr)


def formula_page(seed, w=2.0, h=2.7):
    """A sheet with scribbled lines standing for written formulas (drawing, not the real pages)."""
    rng = np.random.default_rng(seed)
    sheet = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=1.5, fill_color="#f6eedb", fill_opacity=1)
    marks = VGroup()
    y = h / 2 - 0.3
    while y > -h / 2 + 0.25:
        x = -w / 2 + 0.2
        while x < w / 2 - 0.4:
            seg = rng.uniform(0.15, 0.5)
            marks.add(Line(P(x, y), P(min(x + seg, w / 2 - 0.2), y), color=SEPIA, stroke_width=1.6))
            x += seg + rng.uniform(0.06, 0.18)
        y -= rng.uniform(0.22, 0.32)
    return VGroup(sheet, marks)


def table(rows, col_w, row_h=0.42, size=16, header_color=SEPIA):
    """A small spreadsheet-looking grid; rows is a list of lists of strings, first row is the header."""
    g = VGroup()
    for r, row in enumerate(rows):
        x = 0
        for c, cell in enumerate(row):
            box = Rectangle(width=col_w[c], height=row_h, stroke_color=FADED, stroke_width=1,
                            fill_color=PAPER_DARK if r == 0 else "#f6eedb", fill_opacity=1)
            box.move_to(P(x + col_w[c] / 2, -r * row_h))
            t = Text(cell, font=MONO, font_size=size, color=header_color if r == 0 else INK)
            if t.width > col_w[c] - 0.12:
                t.scale_to_fit_width(col_w[c] - 0.12)
            t.move_to(box)
            g.add(VGroup(box, t))
            x += col_w[c]
    return g


class LetterToHardy(NarratedScene):
    def construct(self):
        self.camera.background_color = PAPER
        paper, frame = paper_background()
        self.add(paper)
        self.play(FadeIn(frame), run_time=0.8)

        caption = [None]

        def say(text):
            self.vo(text)
            lines = wrap_two(text) if NARRATE else [text]
            new = VGroup(*[serif(l, 22, FADED, italic=True) for l in lines]).arrange(DOWN, buff=0.06)
            if new.width > 12.6:
                new.scale_to_fit_width(12.6)
            new.move_to([0, -3.33 if len(lines) == 1 else -3.2, 0])
            if caption[0] is None:
                anim = FadeIn(new, shift=UP * 0.1)
            else:
                anim = AnimationGroup(FadeOut(caption[0], shift=UP * 0.1, run_time=0.3), FadeIn(new, shift=UP * 0.1),
                                      lag_ratio=0.55)
            caption[0] = new
            return anim

        def clear():
            self.vo_wait()
            if caption[0] is None:
                return Wait(0.01)
            old, caption[0] = caption[0], None
            return FadeOut(old)

        def line(text, *anims, run_time=0.8):
            self.play(say(text), *anims, run_time=run_time)

        # ================= title =================
        series = spaced("Science Stories", 22).move_to([0, 1.8, 0])
        orn1 = ornament(3.4).next_to(series, DOWN, buff=0.3)
        title = serif("The Letter to Hardy", 54).next_to(orn1, DOWN, buff=0.35)
        sub = serif("Ramanujan, and a series that hunts down pi", 26, FADED, italic=True).next_to(title, DOWN,
                                                                                                 buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("after R. Kanigel, The Man Who Knew Infinity (1991)", 16).move_to([0, -2.6, 0])
        self.vo("Science Stories. The letter to Hardy.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= the envelope =================
        hardy = plain_cameo(0.8).move_to(P(-4.6, 0.9))
        hardy_l = cameo_label("G. H. Hardy", "Trinity College, Cambridge").next_to(hardy, DOWN, buff=0.15)
        place = VGroup(spaced("Cambridge · early 1913", 18, SEPIA)).move_to(P(1.6, 3.0))
        env = envelope().move_to(P(1.6, 0.6))
        line("Cambridge, early 1913. The mathematician G. H. Hardy opens a letter from India.",
             FadeIn(hardy), FadeIn(hardy_l), FadeIn(place), FadeIn(env, shift=LEFT * 0.4), run_time=1.0)
        self.play(env[1].animate.rotate(PI, axis=RIGHT, about_point=env[1].get_top()), run_time=0.8)
        self.vo_wait()
        pages = VGroup(*[formula_page(s) for s in range(5)])
        for i, pg in enumerate(pages):
            pg.move_to(P(-0.6 + 0.9 * i, 0.55 - 0.08 * i)).rotate((i - 2) * 5 * DEGREES)
        sample = MathTex(r"1+2+3+4+\cdots = -\tfrac{1}{12}", font_size=30, color=INK)
        sample_card = ink_card(sample, pad=0.16).move_to(P(1.2, -1.75))
        sample_n = note("one of the letter's claims, true in a special sense", 14).next_to(sample_card, DOWN,
                                                                                          buff=0.08)
        pages_n = note("pages drawn schematically", 13).next_to(pages, UP, buff=0.12)
        line("Inside are pages of formulas. More than a hundred results, and almost no proofs.",
             FadeOut(env), LaggedStart(*[FadeIn(pg, shift=UP * 0.3) for pg in pages], lag_ratio=0.15),
             FadeIn(pages_n), run_time=1.6)
        self.play(FadeIn(sample_card), FadeIn(sample_n), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(pages, pages_n, sample_card, sample_n, place)), run_time=0.7)

        # ================= the opening sentence =================
        quote = VGroup(
            serif("“Dear Sir, I beg to introduce myself to you as a clerk in the", 20, INK, italic=True),
            serif("Accounts Department of the Port Trust Office at Madras", 20, INK, italic=True),
            serif("on a salary of only £20 per annum. I am now about 23 years of age.”", 20, INK, italic=True),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        qcard = ink_card(quote, pad=0.3).move_to(P(1.6, 1.75))
        q_src = note("from the letter, dated 16 January 1913", 14).next_to(qcard, DOWN, buff=0.1).align_to(qcard, LEFT)
        line("The letter begins: I beg to introduce myself to you as a clerk in the Accounts Department of the Port "
             "Trust Office at Madras, on a salary of only twenty pounds per annum.",
             FadeIn(qcard, shift=UP * 0.2), FadeIn(q_src), run_time=1.2)
        self.vo_wait()

        ram = plain_cameo(0.8).move_to(P(4.6, -1.15))
        ram_l = cameo_label("Srinivasa Ramanujan", "born 22 December 1887").next_to(ram, LEFT, buff=0.25)
        age_hi = qcard[2][2][-14:-12]      # the "23" in the last line
        cross = Line(age_hi.get_corner(DL), age_hi.get_corner(UR), color=RED_INK, stroke_width=4)
        real = VGroup(serif("in fact 25", 22, RED_INK, bold=True)).next_to(age_hi, DOWN, buff=0.45)
        line("The writer is Srinivasa Ramanujan. He says he is about twenty-three. By his birth date, he is in fact "
             "twenty-five.", FadeIn(ram), FadeIn(ram_l), run_time=1.0)
        self.wait(1.6)
        self.play(Create(cross), FadeIn(real, scale=1.4), run_time=0.8)
        self.vo_wait()

        # ================= no reply =================
        self.play(FadeOut(VGroup(qcard, q_src, cross, real)), run_time=0.6)
        letters = VGroup()
        for i, (nm, x) in enumerate([("to E. W. Hobson", -0.2), ("to H. F. Baker", 2.6)]):
            e = envelope(2.2, 1.35).move_to(P(x, 1.6))
            t = note(nm, 16).next_to(e, UP, buff=0.1)
            nr = serif("no reply", 22, RED_INK, italic=True).rotate(-6 * DEGREES).next_to(e, DOWN, buff=0.15)
            letters.add(VGroup(e, t, nr))
        no_deg = note("no university degree", 16, SEPIA).next_to(ram_l, DOWN, buff=0.1)
        line("He has no degree. He has already written to two other Cambridge mathematicians, Hobson and Baker. "
             "Neither replied.", FadeIn(no_deg), FadeIn(VGroup(letters[0][:2], letters[1][:2]), lag_ratio=0.3),
             run_time=1.0)
        self.wait(2.2)
        self.play(FadeIn(letters[0][2], scale=1.3), FadeIn(letters[1][2], scale=1.3), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(letters), run_time=0.6)

        # ================= the puzzle =================
        q1 = serif("genius", 40, BLUE_INK, italic=True)
        q2 = serif("or", 28, FADED, italic=True)
        q3 = serif("nonsense?", 40, RED_INK, italic=True)
        gq = VGroup(q1, q2, q3).arrange(RIGHT, buff=0.35).move_to(P(0.3, 1.9))
        facts = VGroup(note("a stranger", 18, INK), note("no training", 18, INK), note("no proofs", 18, INK)
                       ).arrange(RIGHT, buff=0.7).next_to(gq, DOWN, buff=0.5)
        line("So here is the puzzle Hardy faces. A stranger, with no training and no proofs. Is this genius, or "
             "nonsense?", FadeIn(facts, lag_ratio=0.3), run_time=1.0)
        self.wait(2.5)
        self.play(FadeIn(gq, lag_ratio=0.3), run_time=1.0)
        self.vo_wait()
        tray = VGroup(Rectangle(width=2.6, height=0.18, stroke_color=INK, stroke_width=1.5, fill_color=PAPER_DARK,
                                fill_opacity=1),
                      note("set aside", 15)).arrange(DOWN, buff=0.08).move_to(P(-1.0, -1.0))
        mini = formula_page(9, 1.2, 1.5).next_to(tray[0], UP, buff=0.02)
        line("The easy answer is to put the letter aside. Two professors already had.",
             FadeIn(tray), FadeIn(mini, shift=DOWN * 0.6), run_time=1.0)
        self.vo_wait()

        # ================= Hardy and Littlewood =================
        self.play(FadeOut(VGroup(gq, facts, tray, mini)), FadeOut(VGroup(ram, ram_l, no_deg)), run_time=0.6)
        little = plain_cameo(0.8).move_to(P(-1.9, 0.9))
        little_l = cameo_label("J. E. Littlewood", "Trinity College").next_to(little, DOWN, buff=0.15)
        line("Hardy does not. He sits down with his colleague, John Littlewood, and they go through it.",
             FadeIn(little), FadeIn(little_l), run_time=1.0)
        self.vo_wait()
        piles = VGroup()
        for i, (lab, col) in enumerate([("recognised", BLUE_INK), ("could prove", GREEN_INK),
                                        ("“defeated me completely”", RED_INK)]):
            stack = VGroup(*[formula_page(20 + 3 * i + j, 1.1, 1.4).shift(P(0.05 * j, 0.05 * j)) for j in range(3)])
            t = note(lab, 16, col).next_to(stack, DOWN, buff=0.12)
            piles.add(VGroup(stack, t))
        piles.arrange(RIGHT, buff=0.55).move_to(P(3.3, 1.2))
        line("Some formulas they recognise. Some they can prove. And some, Hardy later wrote, defeated him "
             "completely. He had never seen anything in the least like them.",
             FadeIn(piles[0], shift=UP * 0.2), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(piles[1], shift=UP * 0.2), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(piles[2], shift=UP * 0.2), run_time=0.8)
        self.vo_wait()
        verdict = VGroup(serif("“They must be true, because if they were not true,", 26, INK, italic=True),
                         serif("no one would have had the imagination to invent them.”", 26, INK, italic=True)
                         ).arrange(DOWN, buff=0.12)
        vcard = ink_card(verdict, pad=0.25).move_to(P(1.2, -1.75))
        v_src = note("G. H. Hardy, on the letter's formulas", 14).next_to(vcard, DOWN, buff=0.06)
        line("His verdict: they must be true, because if they were not true, no one would have had the imagination "
             "to invent them.", FadeIn(vcard, shift=UP * 0.2), FadeIn(v_src), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(hardy, hardy_l, little, little_l, piles, vcard, v_src)), run_time=0.8)

        # ================= pi =================
        circ = Circle(radius=1.1, color=INK, stroke_width=3).move_to(P(0, 1.0))
        diam = Line(circ.get_left(), circ.get_right(), color=SEPIA, stroke_width=2)
        pisym = MathTex(r"\pi", font_size=90, color=RED_INK).move_to(P(0, 1.0) + UP * 0.05)
        ratio = note("the distance round a circle, divided by the distance across", 17).next_to(circ, DOWN,
                                                                                                buff=0.25)
        line("To see what kind of mind this was, look at what Ramanujan did with one of the oldest problems there "
             "is. Pi.", Create(circ), Create(diam), run_time=1.2)
        self.play(FadeIn(ratio), run_time=0.6)
        self.play(FadeIn(pisym, scale=1.5), run_time=0.8)
        self.vo_wait()
        self.play(FadeOut(VGroup(circ, diam, ratio, pisym)), run_time=0.6)

        leib = MathTex(r"\pi", "=", r"4", r"-\frac{4}{3}", r"+\frac{4}{5}", r"-\frac{4}{7}", r"+\frac{4}{9}",
                       r"-\cdots", font_size=50, color=INK).move_to(P(0, 2.55))
        leib_n = note("a classic series, known for centuries", 15).next_to(leib, DOWN, buff=0.12)
        # partial sums plot
        N = 20
        sums = []
        s = 0.0
        for n in range(N):
            s += 4 * (-1) ** n / (2 * n + 1)
            sums.append(s)
        ax = Axes(x_range=[0, N, 5], y_range=[2.5, 4.2, 0.5], x_length=8.6, y_length=3.0,
                  x_axis_config={"decimal_number_config": {"color": INK, "num_decimal_places": 0}},
                  axis_config={"color": INK, "stroke_width": 2, "include_tip": False, "font_size": 18,
                               "decimal_number_config": {"color": INK, "num_decimal_places": 1}},
                  ).add_coordinates().move_to(P(-0.6, -0.1))
        ax_x = note("number of terms added", 14).next_to(ax.x_axis, DOWN, buff=0.38)
        ax_y = note("running total", 14).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.45)
        piline = DashedLine(ax.c2p(0, np.pi), ax.c2p(N, np.pi), color=RED_INK, stroke_width=2)
        pil = MathTex(r"\pi", font_size=30, color=RED_INK).next_to(piline, RIGHT, buff=0.1)
        dots = VGroup(*[Dot(ax.c2p(i + 1, v), radius=0.05, color=BLUE_INK) for i, v in enumerate(sums)])
        zig = VMobject(stroke_color=BLUE_INK, stroke_width=2).set_points_as_corners(
            [ax.c2p(i + 1, v) for i, v in enumerate(sums)])
        line("Pi can be written as an infinite sum. Here is a classic one: four, minus four thirds, plus four "
             "fifths, minus four sevenths, and on forever.", FadeIn(leib[:3]), FadeIn(leib_n), run_time=1.0)
        self.wait(1.2)
        for part in leib[3:]:
            self.play(FadeIn(part, shift=LEFT * 0.15), run_time=0.55)
        self.play(Create(ax), FadeIn(ax_x), FadeIn(ax_y), Create(piline), FadeIn(pil), run_time=1.0)
        self.vo_wait()

        line("Each new term pulls the total back and forth across pi. But it closes in painfully slowly.",
             run_time=0.6)
        self.play(Create(zig), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.12), run_time=3.0,
                  rate_func=linear)
        self.vo_wait()
        tally = VGroup(
            VGroup(note("after 10 terms", 18, INK), digit_line("3.0418", 1, 26)).arrange(RIGHT, buff=0.3),
            VGroup(note("after 1,000 terms", 18, INK), digit_line("3.1406", 3, 26)).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.18, aligned_edge=RIGHT)
        tcard = ink_card(tally, pad=0.2).move_to(P(3.9, 0.9))
        tkey = note("ink: digits that match pi · red: wrong", 13).next_to(tcard, DOWN, buff=0.08)
        line("After ten terms, you have three point oh four. After a thousand terms, you still only have three "
             "point one four.", FadeIn(tcard), FadeIn(tkey), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(ax, ax_x, ax_y, piline, pil, dots, zig, tcard, tkey, leib, leib_n)),
                  run_time=0.8)

        # ================= Ramanujan's series =================
        ram_f = MathTex(r"\frac{1}{\pi}", "=", r"\frac{2\sqrt{2}}{9801}", r"\sum_{k=0}^{\infty}",
                        r"\frac{(4k)!\,(1103+26390\,k)}{(k!)^4\;396^{4k}}", font_size=52, color=INK).move_to(P(0, 2.0))
        ram_n = note("S. Ramanujan, Modular equations and approximations to π, 1914", 15).next_to(ram_f, DOWN,
                                                                                                    buff=0.2)
        line("Now here is a series Ramanujan published in 1914, the year after his letter.",
             Write(ram_f), FadeIn(ram_n), run_time=2.0)
        self.vo_wait()
        hl = [SurroundingRectangle(ram_f[4][0:5], color=RED_INK, buff=0.06),
              SurroundingRectangle(ram_f[4][6:10], color=RED_INK, buff=0.06),
              SurroundingRectangle(ram_f[2][5:9], color=RED_INK, buff=0.06)]
        line("It looks like a monster. Factorials, the number eleven oh three, the number nine thousand eight "
             "hundred and one.", Create(hl[0]), run_time=0.8)
        self.wait(0.6)
        self.play(ReplacementTransform(hl[0], hl[1]), run_time=0.6)
        self.wait(0.6)
        self.play(ReplacementTransform(hl[1], hl[2]), run_time=0.6)
        self.vo_wait()
        self.play(FadeOut(hl[2]), run_time=0.3)
        line("But watch what happens when we add it up.", ram_f.animate.scale(0.75).move_to(P(0, 2.55)),
             ram_n.animate.move_to(P(0, 1.65)), run_time=1.0)
        self.vo_wait()

        rows = VGroup()
        goods = []
        for k in range(4):
            v = ramanujan_partial(k)
            g = correct_digits(v)
            goods.append(g)
            vs = mp.nstr(v, 36, strip_zeros=False)
            lab = note(f"{k + 1} term" + ("s" if k else ""), 17, INK)
            num = digit_line(vs, g, 22)
            cnt = serif(f"{g} digits", 18, BLUE_INK, italic=True)
            rows.add(VGroup(lab, num, cnt))
        for r in rows:
            r[0].move_to(P(-5.45, 0)).align_to(P(-6.1, 0), LEFT)
            r[1].next_to(P(-4.7, 0), RIGHT, buff=0)
            r[2].next_to(P(4.95, 0), RIGHT, buff=0)
        for i, r in enumerate(rows):
            r.shift(UP * (0.95 - 0.62 * i))
            r[1].align_to(r[0], DOWN)
            r[2].align_to(r[0], DOWN)
        truth = VGroup(note("π =", 17, RED_INK), digit_line(PI_STR[:36], 36, 22)).arrange(RIGHT, buff=0.15)
        truth.next_to(rows[3][1], DOWN, buff=0.35).align_to(rows[3][1], LEFT)
        truth[0].next_to(truth[1], LEFT, buff=0.15)
        line("The first term alone gives three point one four one five nine two. Seven correct digits.",
             FadeIn(rows[0][0]), FadeIn(rows[0][1], lag_ratio=0.05), FadeIn(truth), run_time=1.6)
        self.play(FadeIn(rows[0][2]), run_time=0.5)
        self.vo_wait()
        line("Add a second term, and sixteen digits are right.", FadeIn(rows[1][0]),
             FadeIn(rows[1][1], lag_ratio=0.03), run_time=1.4)
        self.play(FadeIn(rows[1][2]), run_time=0.5)
        self.vo_wait()
        line("Every new term adds about eight more correct digits. Where the classic series crawls, this one leaps.",
             FadeIn(rows[2]), run_time=1.2)
        self.play(FadeIn(rows[3]), run_time=1.2)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(rows, truth)), run_time=0.7)

        # ================= what came after =================
        gos = VGroup(spaced("1985", 20, SEPIA), serif("Bill Gosper: over 17,000,000 digits of π", 30, INK),
                     note("computed with this series", 16)).arrange(DOWN, buff=0.15).move_to(P(0, 0.4))
        line("Ramanujan gave no proof of it. Seventy years later, in 1985, Bill Gosper used this series to compute "
             "more than seventeen million digits of pi.", FadeIn(gos[0]), run_time=0.8)
        self.wait(2.0)
        self.play(FadeIn(gos[1:], shift=UP * 0.15), run_time=0.9)
        self.vo_wait()
        self.play(FadeOut(gos), FadeOut(VGroup(ram_f, ram_n)), run_time=0.6)

        tl = NumberLine(x_range=[1912, 1921, 1], length=11.0, color=INK, include_numbers=True,
                        decimal_number_config={"group_with_commas": False, "color": INK, "num_decimal_places": 0},
                        font_size=20).move_to(P(0, 0.2))
        events = [(1913.04, "16 Jan 1913: the letter", DOWN, 0.8), (1913.1, "8 Feb: Hardy replies", UP, 0.9),
                  (1914.28, "Apr 1914: arrives in England", DOWN, 1.5), (1914.5, "1914: the π paper", UP, 1.6),
                  (1918.33, "May 1918: Fellow of the Royal Society", UP, 0.9),
                  (1920.32, "Apr 1920: dies in India, aged 32", DOWN, 1.0)]
        evm = VGroup()
        for x, txt, d, off in events:
            p = tl.n2p(x)
            tick = Dot(p, radius=0.07, color=RED_INK)
            lab = note(txt, 15, INK)
            lab.move_to(p + d * off)
            con = Line(p + d * 0.1, lab.get_edge_center(-d) - d * 0.05, color=FADED, stroke_width=1)
            evm.add(VGroup(tick, con, lab))
        for m, (x, _, d, _) in zip(evm, events):
            if m[2].get_left()[0] < -6.3:
                m[2].shift(RIGHT * (-6.3 - m[2].get_left()[0]))
            if m[2].get_right()[0] > 6.3:
                m[2].shift(LEFT * (m[2].get_right()[0] - 6.3))
            p = tl.n2p(x)
            edge_y = m[2].get_edge_center(-d)[1] - d[1] * 0.05
            m[1].put_start_and_end_on(p + d * 0.1, np.array([p[0], edge_y, 0]))
        line("And Hardy? He replied to the letter in February 1913, and in April 1914 Ramanujan arrived in "
             "England.", Create(tl), FadeIn(evm[0]), run_time=1.0)
        self.play(FadeIn(evm[1]), run_time=0.6)
        self.wait(1.2)
        self.play(FadeIn(evm[2]), FadeIn(evm[3]), run_time=0.7)
        self.vo_wait()
        line("In 1918 he was elected a Fellow of the Royal Society. Two years later, back in India, he died. He was "
             "thirty-two.", FadeIn(evm[4]), run_time=0.8)
        self.wait(2.0)
        self.play(FadeIn(evm[5]), run_time=0.8)
        self.vo_wait()
        today = VGroup(serif("Series built on his ideas", 34, INK),
                       serif("still chase digits of π today.", 34, RED_INK)).arrange(DOWN, buff=0.2).move_to(P(0, 0.8))
        today_n = note("e.g. the Chudnovsky series (1988), used in record computations", 15).next_to(today, DOWN,
                                                                                                    buff=0.3)
        line("Series built on his ideas are still used to chase digits of pi today.", FadeOut(VGroup(tl, evm)),
             FadeIn(today, lag_ratio=0.2), FadeIn(today_n), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(today, today_n)), run_time=0.7)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 22, RED_INK).move_to(P(0, 3.15))
        left_rows = [["n", "term", "running total"]]
        tot = 0.0
        for n in range(6):
            t = 4 * (-1) ** n / (2 * n + 1)
            tot += t
            left_rows.append([str(n), f"{t:+.4f}", f"{tot:.10f}"])
        tl_tab = table(left_rows, [0.55, 1.35, 2.2], size=15).move_to(P(-3.3, 0.85))
        tl_t = serif("classic series", 20, BLUE_INK).next_to(tl_tab, UP, buff=0.15)
        tl_f = mono("term = 4*(-1)^n/(2*n+1)", 14, FADED).next_to(tl_tab, DOWN, buff=0.15)
        r_rows = [["k", "π from the first k+1 terms"]]
        for k in range(2):
            r_rows.append([str(k), mp.nstr(ramanujan_partial(k), 15, strip_zeros=False)])
        tr_tab = table(r_rows, [0.55, 3.5], size=15).move_to(P(3.2, 1.45))
        tr_t = serif("Ramanujan's series", 20, RED_INK).next_to(tr_tab, UP, buff=0.15)
        tr_f = VGroup(mono("term = FACT(4*k)*(1103+26390*k)", 13, FADED),
                      mono("       /(FACT(k)^4*396^(4*k))", 13, FADED),
                      mono("π = 9801/(2*SQRT(2)*sum of terms)", 13, FADED)).arrange(DOWN, buff=0.06,
                                                                                    aligned_edge=LEFT)
        tr_f.next_to(tr_tab, DOWN, buff=0.15)
        line("Try it yourself. Open a spreadsheet. In one column, add up the classic series, term by term.",
             FadeIn(tiy), FadeIn(tl_t), FadeIn(tl_tab[:3]), FadeIn(tl_f), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(tl_tab[i:i + 3]) for i in range(3, len(tl_tab), 3)], lag_ratio=0.3),
                  run_time=2.4)
        self.vo_wait()
        limit = note("a spreadsheet keeps about 15 significant digits,\nso two terms already fill it", 15, SEPIA)
        limit.next_to(tr_f, DOWN, buff=0.2)
        line("In another, add up Ramanujan's series. You will only need two rows. By then, the spreadsheet has run "
             "out of digits.", FadeIn(tr_t), FadeIn(tr_tab[:2]), FadeIn(tr_f), run_time=1.0)
        self.play(FadeIn(tr_tab[2:4]), run_time=0.6)
        self.play(FadeIn(tr_tab[4:6]), run_time=0.6)
        self.wait(0.6)
        self.play(FadeIn(limit), run_time=0.6)
        self.vo_wait()
        crawl = serif("crawls", 26, BLUE_INK, italic=True).next_to(tl_f, DOWN, buff=0.35)
        leap = serif("leaps", 26, RED_INK, italic=True).next_to(limit, RIGHT, buff=0.4)
        line("Then count how many digits each one gets right. One crawls. One leaps.", run_time=0.6)
        self.wait(1.6)
        self.play(FadeIn(crawl, scale=1.2), run_time=0.5)
        self.play(FadeIn(leap, scale=1.2), run_time=0.5)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tiy, tl_tab, tl_t, tl_f, tr_tab, tr_t, tr_f, limit, crawl, leap)),
                  run_time=0.8)

        # ================= close =================
        env2 = envelope(2.4, 1.5).move_to(P(0, 1.9))
        last = VGroup(serif("A clerk's letter, a reader willing to take it seriously,", 30, INK),
                      serif("and an idea that still runs on our computers.", 30, RED_INK)).arrange(DOWN, buff=0.22)
        last.move_to(P(0, -0.3))
        line("A clerk's letter, a reader willing to take it seriously, and an idea that still runs on our computers.",
             FadeIn(env2), FadeIn(last, lag_ratio=0.2), run_time=1.2)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(last, env2)), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after R. Kanigel, The Man Who Knew Infinity (1991) · sources in the episode notes", 17),
                     note("facts checked against MacTutor, S. Wolfram (2016), A. Rice (IMA, 2020), Hardy's Twelve "
                          "Lectures, J. M. Borwein (2012) and Bhavana", 17),
                     note("silhouettes stylised, not likenesses · letter pages drawn schematically · digits computed "
                          "with mpmath · Manim · synthetic narration", 15)
                     ).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        for m in end:
            if m.width > 12.8:
                m.scale_to_fit_width(12.8)
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(3.0)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)
