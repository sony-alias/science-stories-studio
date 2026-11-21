"""I030 Seven Years in Secret, a Science Stories episode.

After S. Singh, Fermat's Enigma (1997). Script and sources: episodes/I030_script.md

Render:  manim -qh --frame_rate 30 episodes/I030_wiles_fermat.py SevenYearsInSecret
Then:    scripts/finish_video.sh media/videos/I030_wiles_fermat/1080p30/SevenYearsInSecret.mp4 out/I030_wiles_fermat.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

MONO = "DejaVu Sans Mono"
GREEN_INK = "#3f6b3a"
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


# ---------------- the exact mathematics shown on screen ----------------
def curve_ok(x, y, p):
    """y^2 + y = x^3 - x^2  (mod p)   -- LMFDB curve 11.a3, conductor 11."""
    return (y * y + y - x ** 3 + x * x) % p == 0


def solutions(p):
    return [(x, y) for x in range(p) for y in range(p) if curve_ok(x, y, p)]


def form_coeffs(n_max=60):
    """Coefficients of q * prod_{n>=1} (1-q^n)^2 (1-q^{11n})^2  (LMFDB modular form 11.2.a.a)."""
    poly = [0] * n_max
    poly[0] = 1
    for n in range(1, n_max):
        for k in [n, n] + ([11 * n, 11 * n] if 11 * n < n_max else []):
            new = poly[:]
            for i in range(k, n_max):
                new[i] -= poly[i - k]
            poly = new
    return [0] + poly[:n_max - 1]


COEF = form_coeffs()
A_P = {p: p - len(solutions(p)) for p in PRIMES}
for _p in PRIMES:
    assert A_P[_p] == COEF[_p], _p          # the match the video claims, checked at render time


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


def bookshelf(w=4.6, h=3.6, seed=3):
    rng = np.random.default_rng(seed)
    frame = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=2.5, fill_color=PAPER_DARK, fill_opacity=1)
    g = VGroup(frame)
    books = VGroup()
    shelves = 3
    for s in range(shelves):
        y0 = -h / 2 + s * h / shelves
        g.add(Line(P(-w / 2, y0), P(w / 2, y0), color=INK, stroke_width=2))
        x = -w / 2 + 0.12
        while x < w / 2 - 0.3:
            bw = rng.uniform(0.16, 0.3)
            bh = rng.uniform(0.7, 1.0) * (h / shelves - 0.15)
            col = [SEPIA, FADED, "#6b4a2b", BLUE_INK, "#a07850"][rng.integers(0, 5)]
            b = Rectangle(width=bw, height=bh, stroke_color=INK, stroke_width=1, fill_color=col, fill_opacity=0.85)
            b.move_to(P(x + bw / 2, y0 + bh / 2 + 0.02))
            books.add(b)
            x += bw + 0.03
    g.add(books)
    return g, books


def text_page(seed, w=3.0, h=3.6, margin=0.9, rows=11):
    """A printed page (drawn, not the real book): text block on the left, blank margin on the right."""
    rng = np.random.default_rng(seed)
    sheet = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=1.5, fill_color="#f6eedb", fill_opacity=1)
    marks = VGroup()
    top = h / 2 - 0.35
    for r in range(rows):
        y = top - r * (h - 0.7) / rows
        x = -w / 2 + 0.2
        while x < w / 2 - margin - 0.1:
            seg = rng.uniform(0.12, 0.42)
            marks.add(Line(P(x, y), P(min(x + seg, w / 2 - margin), y), color=FADED, stroke_width=2))
            x += seg + rng.uniform(0.05, 0.12)
    return VGroup(sheet, marks)


def scribble(p0, width, rows=4, seed=9, color=SEPIA):
    rng = np.random.default_rng(seed)
    g = VGroup()
    for r in range(rows):
        xs = np.linspace(0, width, 26)
        ys = 0.04 * np.sin(xs * 22 + rng.uniform(0, 6)) + rng.normal(0, 0.008, xs.size)
        pts = [p0 + P(x, -0.2 * r + y) for x, y in zip(xs, ys)]
        g.add(VMobject(color=color, stroke_width=1.6).set_points_smoothly(pts))
    return g


def tile_square(n, unit, color):
    sq = VGroup(*[Square(unit, stroke_color=INK, stroke_width=0.8, fill_color=color, fill_opacity=0.55)
                  .move_to(P((i + 0.5) * unit, (j + 0.5) * unit)) for i in range(n) for j in range(n)])
    return sq


def mod_grid(p, cell, origin):
    """p x p dots; returns (dots dict, group with axes numbers)."""
    dots = {}
    g = VGroup()
    for x in range(p):
        for y in range(p):
            d = Dot(origin + P(x * cell, y * cell), radius=0.055, color=FADED)
            dots[(x, y)] = d
            g.add(d)
    for x in range(p):
        g.add(mono(str(x), 15, SEPIA).move_to(origin + P(x * cell, -0.4)))
    for y in range(p):
        g.add(mono(str(y), 15, SEPIA).move_to(origin + P(-0.4, y * cell)))
    g.add(mono("x", 16, INK).move_to(origin + P((p - 1) * cell / 2, -0.75)))
    g.add(mono("y", 16, INK).move_to(origin + P(-0.75, (p - 1) * cell / 2)))
    return dots, g


def table(rows, col_w, row_h=0.44, size=17, colors=None):
    g = VGroup()
    for r, row in enumerate(rows):
        x = 0
        for c, cell in enumerate(row):
            box = Rectangle(width=col_w[c], height=row_h, stroke_color=FADED, stroke_width=1,
                            fill_color=PAPER_DARK if c == 0 else "#f6eedb", fill_opacity=1)
            box.move_to(P(x + col_w[c] / 2, -r * row_h))
            col = (colors[r] if colors else INK) if c > 0 else SEPIA
            t = mono(cell, size, col)
            if t.width > col_w[c] - 0.1:
                t.scale_to_fit_width(col_w[c] - 0.1)
            t.move_to(box)
            g.add(VGroup(box, t))
            x += col_w[c]
    return g


class SevenYearsInSecret(NarratedScene):
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
        title = serif("Seven Years in Secret", 54).next_to(orn1, DOWN, buff=0.35)
        sub = serif("Andrew Wiles and the bridge to Fermat", 26, FADED, italic=True).next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("after S. Singh, Fermat's Enigma (1997)", 16).move_to([0, -2.6, 0])
        self.vo("Science Stories. Seven years in secret.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= the library, 1963 =================
        shelf, books = bookshelf()
        shelf.move_to(P(-2.6, 0.45))
        place = spaced("Cambridge · 1963", 18, SEPIA).move_to(P(0, 3.05))
        boy = plain_cameo(0.7).move_to(P(3.6, 0.85))
        boy_l = cameo_label("Andrew Wiles", "aged ten").next_to(boy, DOWN, buff=0.15)
        line("Cambridge, England, 1963. A ten-year-old boy is browsing the maths shelf of his local library.",
             FadeIn(place), FadeIn(shelf), FadeIn(boy), FadeIn(boy_l), run_time=1.2)
        self.vo_wait()
        pick = books[len(books) // 2 + 3]
        book = Rectangle(width=1.6, height=2.2, stroke_color=INK, stroke_width=2, fill_color=RED_INK,
                         fill_opacity=0.85).move_to(P(0.9, 0.6))
        book_t = VGroup(serif("The Last", 18, PAPER), serif("Problem", 18, PAPER)).arrange(DOWN, buff=0.05)
        book_t.move_to(book).shift(UP * 0.35)
        book_a = serif("E. T. Bell", 14, PAPER, italic=True).move_to(book).shift(DOWN * 0.6)
        book_n = note("the book MacTutor names; cover drawn, not the real one", 13).move_to(P(0.9, -1.75))
        line("His name is Andrew Wiles, and he has found a book about a single problem.",
             pick.animate.set_fill(RED_INK, 1), run_time=0.8)
        self.play(ReplacementTransform(pick.copy(), book), run_time=0.9)
        self.play(FadeIn(book_t), FadeIn(book_a), FadeIn(book_n), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(shelf, book, book_t, book_a, book_n, place)),
                  VGroup(boy, boy_l).animate.set_opacity(0), run_time=0.8)
        self.remove(boy, boy_l)

        # ================= the equation =================
        eq = MathTex("x^n", "+", "y^n", "=", "z^n", font_size=72, color=INK).move_to(P(0, 2.3))
        eq2 = MathTex("3^2", "+", "4^2", "=", "5^2", font_size=56, color=INK).move_to(P(-3.0, 1.0))
        u = 0.22
        s3 = tile_square(3, u, BLUE_INK).move_to(P(-4.9, -1.05))
        s4 = tile_square(4, u, SEPIA).move_to(P(-3.6, -0.95))
        s5 = tile_square(5, u, GREEN_INK).move_to(P(-1.6, -0.85))
        plus = MathTex("+", font_size=40, color=INK).move_to(P(-4.3, -1.0))
        eqs = MathTex("=", font_size=40, color=INK).move_to(P(-2.65, -1.0))
        cnt = note("9 + 16 = 25 tiles", 15).next_to(s5, DOWN, buff=0.2).set_x(-3.3)
        line("Take whole numbers x, y and z. With squares there are plenty of answers. "
             "Three squared plus four squared is five squared.", Write(eq), run_time=1.2)
        self.play(FadeIn(eq2), run_time=0.6)
        self.play(LaggedStart(FadeIn(s3), FadeIn(plus), FadeIn(s4), FadeIn(eqs), FadeIn(s5), lag_ratio=0.3),
                  FadeIn(cnt), run_time=1.6)
        self.vo_wait()
        higher = VGroup(
            MathTex("x^3+y^3=z^3", font_size=40, color=INK),
            MathTex("x^4+y^4=z^4", font_size=40, color=INK),
            MathTex("x^5+y^5=z^5", font_size=40, color=INK),
            MathTex(r"\vdots", font_size=40, color=INK),
        ).arrange(DOWN, buff=0.25).move_to(P(1.6, 0.0))
        qmarks = VGroup(*[serif("no answer found", 18, RED_INK, italic=True).next_to(m, RIGHT, buff=0.3)
                          for m in higher[:3]])
        line("But with cubes, or any higher power, no one had ever found a single answer.",
             LaggedStart(*[FadeIn(m) for m in higher], lag_ratio=0.25), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(q) for q in qmarks], lag_ratio=0.3), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(eq2, s3, s4, s5, plus, eqs, cnt, higher, qmarks)),
                  eq.animate.scale(0.6).move_to(P(-4.4, 2.9)), run_time=0.8)

        # ================= Fermat's margin =================
        page = text_page(5).move_to(P(-2.6, 0.2))
        book_l = note("Diophantus, Arithmetica (Bachet's Latin edition, 1621) · page drawn schematically", 14)
        book_l.next_to(page, DOWN, buff=0.15)
        fermat = cameo("wig", 0.62).move_to(P(4.5, 1.6))
        fermat_l = cameo_label("Pierre de Fermat", "c. 1637").next_to(fermat, DOWN, buff=0.12)
        mark = scribble(page[0].get_corner(UR) + P(-0.82, -0.6), 0.7, rows=8)
        line("Around 1637, Pierre de Fermat wrote in the margin of an ancient book, the Arithmetica, that none exist.", FadeIn(page), FadeIn(book_l), FadeIn(fermat), FadeIn(fermat_l), run_time=1.0)
        self.play(Create(mark), run_time=2.0)
        self.vo_wait()
        quote = VGroup(serif("“I have discovered a truly remarkable proof", 22, INK, italic=True),
                       serif("which this margin is too small to contain.”", 22, INK, italic=True),
                       note("Fermat's note, in MacTutor's translation", 14)).arrange(DOWN, buff=0.1)
        qcard = ink_card(quote, pad=0.25).move_to(P(2.6, -1.0))
        line("And he added: I have discovered a truly remarkable proof, which this margin is too small to contain.",
             FadeIn(qcard, shift=UP * 0.2), run_time=1.0)
        self.vo_wait()
        tl = Line(P(-5.6, -2.45), P(5.6, -2.45), color=SEPIA, stroke_width=2)
        ticks = VGroup()
        for yr, x in [(1637, -5.2), (1670, -4.2), (1800, -1.0), (1900, 1.4), (1986, 4.8)]:
            ticks.add(VGroup(Line(P(x, -2.35), P(x, -2.55), color=SEPIA, stroke_width=2),
                             mono(str(yr), 15, SEPIA).move_to(P(x, -2.2))))
        line("Historians now doubt he really had one. For more than three centuries, no one could find a proof.",
             FadeOut(VGroup(page, book_l, mark)), qcard.animate.move_to(P(-1.6, 1.0)), run_time=1.0)
        self.play(Create(tl), LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.25), run_time=1.6)
        gap = Line(P(-4.2, -2.45), P(4.8, -2.45), color=RED_INK, stroke_width=6)
        gap_t = note("unproved", 16, RED_INK).move_to(P(0.2, -1.95))
        self.play(Create(gap), FadeIn(gap_t), run_time=2.0)
        self.vo_wait()

        boy2 = plain_cameo(0.7).move_to(P(4.5, 1.6))
        boy2_l = cameo_label("Andrew Wiles", "recalling 1963").next_to(boy2, DOWN, buff=0.12)
        q2 = VGroup(serif("“I knew from that moment", 24, INK, italic=True),
                    serif("that I would never let it go.”", 24, INK, italic=True),
                    note("Wiles, NOVA interview (2000)", 14)).arrange(DOWN, buff=0.1)
        q2card = ink_card(q2, pad=0.25).move_to(P(-1.2, 0.5))
        line("Wiles later said: I knew from that moment that I would never let it go.",
             FadeOut(VGroup(fermat, fermat_l, qcard)), FadeIn(boy2), FadeIn(boy2_l), FadeIn(q2card), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(q2card, tl, ticks, gap, gap_t, eq)), run_time=0.7)

        # ================= 1986 =================
        place2 = spaced("Princeton · summer 1986", 18, SEPIA).move_to(P(0, 3.05))
        boy2_l2 = cameo_label("Andrew Wiles", "now at Princeton").move_to(boy2_l)
        line("One summer evening in 1986, at a friend's house, Wiles, now a mathematician, heard some news.", FadeIn(place2), Transform(boy2_l, boy2_l2), run_time=1.0)
        cup = VGroup(Polygon(P(-0.35, 0.45), P(0.35, 0.45), P(0.25, -0.45), P(-0.25, -0.45),
                             stroke_color=INK, stroke_width=2, fill_color="#c8a46a", fill_opacity=0.5),
                     Line(P(0.12, 0.3), P(0.3, 0.85), color=SEPIA, stroke_width=3)).move_to(P(1.6, 0.6))
        cup_l = note("iced tea, as Wiles told it", 14).next_to(cup, DOWN, buff=0.12)
        self.play(FadeIn(cup), FadeIn(cup_l), run_time=0.8)
        self.vo_wait()
        news = VGroup(serif("Ken Ribet has proved it:", 24, INK),
                      serif("Fermat ⟸ Taniyama–Shimura", 28, RED_INK)).arrange(DOWN, buff=0.15)
        ncard = ink_card(news, pad=0.25).move_to(P(-2.2, 0.8))
        elec = note("“I was electrified.”  (NOVA, 2000)", 17, RED_INK).next_to(ncard, DOWN, buff=0.3)
        line("Ken Ribet had proved that Fermat's problem was tied to another puzzle, the Taniyama–Shimura "
             "conjecture. Wiles said he was electrified.", FadeIn(ncard, shift=UP * 0.2), run_time=1.0)
        self.wait(3.2)
        self.play(FadeIn(elec), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(ncard, elec, cup, cup_l, place2, boy2, boy2_l)), run_time=0.7)

        # ================= the chain of logic =================
        b1 = ink_card(VGroup(note("suppose", 15), MathTex("a^p+b^p=c^p", font_size=36, color=INK))
                      .arrange(DOWN, buff=0.08), pad=0.2).move_to(P(-4.6, 1.6))
        b2 = ink_card(VGroup(note("Frey's curve", 15), MathTex("y^2=x(x-a^p)(x+b^p)", font_size=32, color=INK))
                      .arrange(DOWN, buff=0.08), pad=0.2).move_to(P(0.0, 1.6))
        b3 = ink_card(VGroup(note("Ribet, 1986", 15), serif("not modular", 26, RED_INK))
                      .arrange(DOWN, buff=0.08), pad=0.2).move_to(P(4.6, 1.6))
        a12 = Arrow(b1.get_right(), b2.get_left(), buff=0.12, color=SEPIA, stroke_width=3)
        a23 = Arrow(b2.get_right(), b3.get_left(), buff=0.12, color=SEPIA, stroke_width=3)
        pnote = note("p a prime above 2 (enough to settle every power)", 14).next_to(b1, DOWN, buff=0.15)
        line("Suppose Fermat was wrong, and some numbers a, b and c did work.",
             FadeIn(b1), FadeIn(pnote), run_time=0.9)
        self.vo_wait()
        line("Gerhard Frey, building on earlier work, showed how to turn them into an elliptic curve with very "
             "strange properties.", GrowArrow(a12), FadeIn(b2), run_time=1.0)
        self.vo_wait()
        line("Ribet proved that such a curve could not be what mathematicians call modular.",
             GrowArrow(a23), FadeIn(b3), run_time=0.9)
        self.vo_wait()
        b4 = ink_card(VGroup(note("Taniyama and Shimura, 1950s–60s", 15),
                             serif("every elliptic curve is modular", 24, BLUE_INK)).arrange(DOWN, buff=0.08),
                      pad=0.2).move_to(P(2.3, -0.6))
        guess = note("a guess, not yet a theorem", 14, BLUE_INK).next_to(b4, DOWN, buff=0.1)
        line("But Taniyama and Shimura had guessed, in the 1950s and 60s, that every elliptic curve is modular.",
             FadeIn(b4, shift=UP * 0.2), FadeIn(guess), run_time=1.0)
        self.vo_wait()
        clash = Line(b3.get_bottom() + DOWN * 0.05, b4.get_top() + RIGHT * 1.4 + UP * 0.05, color=RED_INK,
                     stroke_width=4)
        boom = stamp(r"\text{contradiction}", size=28).move_to(P(5.2, 0.35))
        concl = ink_card(VGroup(serif("so no such a, b, c", 26, INK),
                                note("if the guess holds for curves like Frey's", 14)).arrange(DOWN, buff=0.06),
                         pad=0.2).move_to(P(-3.6, -1.0))
        line("So prove their guess, at least for curves like Frey's, and the numbers a, b and c cannot exist.",
             Create(clash), run_time=0.8)
        self.play(FadeIn(boom, scale=1.3), run_time=0.5)
        x1 = Cross(b1, stroke_color=RED_INK, stroke_width=4)
        self.play(FadeIn(concl, shift=UP * 0.2), Create(x1), run_time=0.9)
        self.vo_wait()
        chain = VGroup(b1, b2, b3, a12, a23, pnote, b4, guess, clash, boom, concl, x1)
        self.play(clear(), FadeOut(chain), run_time=0.8)

        # ================= seven years =================
        desk = VGroup(Line(P(-5.4, -1.2), P(-1.4, -1.2), color=INK, stroke_width=4),
                      Line(P(-5.1, -1.2), P(-5.1, -2.5), color=INK, stroke_width=3),
                      Line(P(-1.7, -1.2), P(-1.7, -2.5), color=INK, stroke_width=3))
        stack = VGroup()
        wiles = plain_cameo(0.7).move_to(P(-3.4, 1.6))
        wiles_l = cameo_label("Andrew Wiles", "working alone").next_to(wiles, DOWN, buff=0.1)
        line("No one knew where to begin. Wiles set almost everything else aside, and told almost no one but his wife.", FadeIn(desk), FadeIn(wiles), FadeIn(wiles_l),
             run_time=1.0)
        for i in range(7):
            sh = Rectangle(width=2.2, height=0.06, stroke_color=INK, stroke_width=0.8, fill_color="#f6eedb",
                           fill_opacity=1).move_to(P(-3.4 + 0.05 * ((-1) ** i), -1.13 + 0.07 * (i + 1)))
            stack.add(sh)
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in stack], lag_ratio=0.3), run_time=2.0)
        self.vo_wait()
        counter = VGroup()
        years = list(range(1986, 1994))
        yr_mobs = [mono(str(y), 54, INK).move_to(P(2.8, 1.6)) for y in years]
        seven = serif("seven years", 30, RED_INK, italic=True).move_to(P(2.8, 0.6))
        line("It took him seven years.", FadeIn(yr_mobs[0]), run_time=0.5)
        for a, b in zip(yr_mobs[:-1], yr_mobs[1:]):
            self.play(FadeOut(a, shift=UP * 0.2), FadeIn(b, shift=UP * 0.2), run_time=0.22)
        self.play(FadeIn(seven), run_time=0.5)
        self.vo_wait()
        rooms = VGroup(*[Rectangle(width=0.95, height=0.95, stroke_color=INK, stroke_width=2,
                                   fill_color="#3a3024", fill_opacity=0.9) for _ in range(6)])
        rooms.arrange_in_grid(2, 3, buff=0.08).move_to(P(2.8, -0.9))
        mansion_l = note("“a journey through a dark unexplored mansion” — Wiles, NOVA (2000)", 14)
        mansion_l.next_to(rooms, DOWN, buff=0.15)
        line("He compared it to a dark mansion: months stumbling in one room, until you find the light switch.", FadeOut(yr_mobs[-1]), seven.animate.move_to(P(2.8, 1.5)),
             FadeIn(rooms), FadeIn(mansion_l), run_time=1.0)
        self.wait(2.0)
        for r in rooms[:4]:
            self.play(r.animate.set_fill("#f3e2a8", 1), run_time=0.45)
            self.wait(0.35)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(desk, stack, wiles, wiles_l, seven, rooms, mansion_l)), run_time=0.8)

        # ================= what "modular" means: the curve =================
        head = spaced("What does modular mean?", 18, SEPIA).move_to(P(0, 3.05))
        ceq = MathTex("y^2+y=x^3-x^2", font_size=44, color=INK).move_to(P(-3.4, 2.3))
        ax = Axes(x_range=[-1, 2.2, 1], y_range=[-2.6, 1.8, 1], x_length=4.6, y_length=3.6,
                  axis_config={"color": FADED, "stroke_width": 1.5, "include_ticks": True, "tip_length": 0.15})
        ax.move_to(P(-3.4, -0.3))

        x0 = min(self._roots())
        xs = np.concatenate([x0 + (np.linspace(0, 1, 120) ** 2) * (2.0 - x0)])
        up = [ax.c2p(x, (-1 + np.sqrt(max(0, 1 + 4 * (x ** 3 - x ** 2)))) / 2) for x in xs]
        lo = [ax.c2p(x, (-1 - np.sqrt(max(0, 1 + 4 * (x ** 3 - x ** 2)))) / 2) for x in xs]
        curve = VMobject(color=RED_INK, stroke_width=3).set_points_smoothly(lo[::-1] + up[1:])
        joins = VGroup()
        ec_l = note("an elliptic curve (LMFDB 11.a3), over the real numbers", 14).next_to(ax, DOWN, buff=0.05)
        line("So what does modular mean? Take this elliptic curve: y squared plus y equals x cubed minus x squared.",
             FadeIn(head), Write(ceq), FadeIn(ax), run_time=1.2)
        self.play(Create(curve), FadeIn(joins), FadeIn(ec_l), run_time=1.8)
        self.vo_wait()

        # ---- modulo 5
        dots5, g5 = mod_grid(5, 0.62, P(1.3, -1.4))
        clock = VGroup(*[mono(str(k), 16, SEPIA).move_to(P(5.6, 1.4) + 0.55 * np.array(
            [np.sin(2 * PI * k / 5), np.cos(2 * PI * k / 5), 0])) for k in range(5)])
        ring = Circle(radius=0.75, color=SEPIA, stroke_width=1.5).move_to(P(5.6, 1.4))
        clock_l = note("mod 5: 4 + 3 = 2", 14).next_to(ring, DOWN, buff=0.12)
        line("Now count on a clock. Modulo five there are only five numbers, so test every pair.",
             FadeIn(g5), FadeIn(ring), FadeIn(clock), FadeIn(clock_l), run_time=1.0)
        self.vo_wait()
        sol5 = solutions(5)
        hits5 = VGroup(*[Dot(dots5[s].get_center(), radius=0.12, color=RED_INK) for s in sol5])
        tally5 = MathTex(r"5-", str(len(sol5)), "=", str(5 - len(sol5)), font_size=44, color=INK).move_to(P(4.9, -0.6))
        tally5[3].set_color(RED_INK)
        line("Four pairs work. Five minus four is one.",
             LaggedStart(*[GrowFromCenter(h) for h in hits5], lag_ratio=0.25), run_time=1.2)
        self.play(FadeIn(tally5), run_time=0.6)
        self.vo_wait()

        # ---- modulo 7
        dots7, g7 = mod_grid(7, 0.44, P(1.3, -1.4))
        sol7 = solutions(7)
        hits7 = VGroup(*[Dot(dots7[s].get_center(), radius=0.1, color=RED_INK) for s in sol7])
        tally7 = MathTex(r"7-", str(len(sol7)), "=", str(7 - len(sol7)), font_size=44, color=INK).move_to(P(4.9, -1.5))
        tally7[3].set_color(RED_INK)
        keep5 = MathTex(r"p=5:\ 1", font_size=34, color=INK).move_to(P(4.9, -0.6))
        line("Modulo seven, nine pairs work. Seven minus nine is minus two.",
             FadeOut(g5), FadeOut(hits5), FadeOut(clock), FadeOut(ring), FadeOut(clock_l), ReplacementTransform(tally5, keep5),
             run_time=0.6)
        self.play(FadeIn(g7), run_time=0.5)
        self.play(LaggedStart(*[GrowFromCenter(h) for h in hits7], lag_ratio=0.15), run_time=1.4)
        self.play(FadeIn(tally7), run_time=0.6)
        self.vo_wait()
        keep7 = MathTex(r"p=7:\ -2", font_size=34, color=INK).next_to(keep5, DOWN, buff=0.2, aligned_edge=LEFT)
        counts = VGroup(keep5, keep7)
        self.play(clear(), FadeOut(VGroup(g7, hits7, ax, curve, joins, ec_l)), ReplacementTransform(tally7, keep7),
                  run_time=0.8)
        self.play(ceq.animate.scale(0.8).move_to(P(-4.3, 2.35)),
                  counts.animate.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(P(-4.3, 1.25)), run_time=0.8)
        cnote = note("p minus the number of pairs", 14).next_to(counts, DOWN, buff=0.15)
        self.play(FadeIn(cnote), run_time=0.4)

        # ================= the modular form =================
        prod = MathTex(r"q\prod_{n\ge1}(1-q^{n})^{2}(1-q^{11n})^{2}", font_size=42, color=BLUE_INK).move_to(P(1.6, 2.2))
        form_l = note("a modular form (LMFDB 11.2.a.a)", 14).next_to(prod, DOWN, buff=0.12)
        line("Now a series built from a product with deep symmetry: a modular form.", Write(prod), FadeIn(form_l), run_time=1.6)
        self.vo_wait()

        def term(n, c):
            if n == 1:
                return "q"
            sgn = "-" if c < 0 else "+"
            mag = "" if abs(c) == 1 else str(abs(c))
            return f"{sgn}{mag}q^{{{n}}}" if c != 0 else ""

        parts = [term(n, COEF[n]) for n in range(1, 9)]
        parts = [t for t in parts if t] + [r"+\cdots"]
        ser = MathTex(*parts, font_size=40, color=INK).move_to(P(1.6, 0.55))
        eqsign = MathTex("=", font_size=40, color=INK).next_to(ser, LEFT, buff=0.2)
        line("Multiply it out, and read off the numbers.",
             FadeIn(eqsign), LaggedStart(*[FadeIn(t) for t in ser], lag_ratio=0.15), run_time=2.0)
        self.vo_wait()
        idx = {n: i for i, n in enumerate([n for n in range(1, 9) if COEF[n] != 0])}
        box5 = SurroundingRectangle(ser[idx[5]], color=RED_INK, buff=0.07)
        box7 = SurroundingRectangle(ser[idx[7]], color=RED_INK, buff=0.07)
        l5 = MathTex(r"q^5:\ +1", font_size=30, color=RED_INK).next_to(box5, DOWN, buff=0.3)
        l7 = MathTex(r"q^7:\ -2", font_size=30, color=RED_INK).next_to(box7, DOWN, buff=0.3)
        line("In front of q to the fifth: one. In front of q to the seventh: minus two.",
             Create(box5), FadeIn(l5), run_time=0.8)
        self.wait(1.2)
        self.play(Create(box7), FadeIn(l7), run_time=0.8)
        self.vo_wait()

        rows = [["p"] + [str(p) for p in PRIMES],
                ["curve"] + [str(A_P[p]) for p in PRIMES],
                ["series"] + [str(COEF[p]) for p in PRIMES]]
        tab = table(rows, [1.2] + [0.62] * len(PRIMES), colors=[SEPIA, RED_INK, BLUE_INK]).move_to(P(0.6, -1.3))
        ncol = len(PRIMES) + 1
        tab_l = note("curve: p minus pairs, counted by the episode's code · series: coefficient of q^p", 13)
        tab_l.next_to(tab, DOWN, buff=0.1)
        line("The same numbers. Prime after prime, they keep matching.",
             FadeIn(VGroup(tab[0], tab[ncol], tab[2 * ncol])), FadeIn(tab_l), run_time=0.8)
        for c in range(1, ncol):
            self.play(FadeIn(VGroup(tab[c], tab[ncol + c], tab[2 * ncol + c]), shift=DOWN * 0.1), run_time=0.28)
        self.vo_wait()
        twin = VGroup(serif("curve", 24, RED_INK), MathTex(r"\longleftrightarrow", font_size=40, color=INK),
                      serif("modular form", 24, BLUE_INK)).arrange(RIGHT, buff=0.25)
        tcard = ink_card(VGroup(twin, note("Taniyama–Shimura: every elliptic curve has such a twin", 14))
                         .arrange(DOWN, buff=0.1), pad=0.2).move_to(P(-3.9, -0.15))
        line("That is what modular means: the curve's counts are secretly the coefficients of a modular form. "
             "Taniyama and Shimura guessed every elliptic curve has such a twin.",
             FadeOut(VGroup(box5, box7, l5, l7)), run_time=0.6)
        self.play(tab.animate.shift(DOWN * 0.15), tab_l.animate.shift(DOWN * 0.15), run_time=0.4)
        self.play(FadeIn(tcard, shift=UP * 0.2), FadeOut(cnote), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(head, ceq, counts, prod, form_l, ser, eqsign, tab, tab_l, tcard)),
                  run_time=0.8)

        # ================= Cambridge, June 1993 =================
        board = Rectangle(width=7.0, height=3.4, stroke_color="#5a4632", stroke_width=8, fill_color="#2f3a33",
                          fill_opacity=1).move_to(P(-1.2, 0.9))
        chalk = "#ece6d6"
        btitle = VGroup(Text("Modular Forms, Elliptic Curves", font_size=22, color=chalk),
                        Text("and Galois Representations", font_size=22, color=chalk)).arrange(DOWN, buff=0.08)
        btitle.move_to(board.get_top() + DOWN * 0.55)
        place3 = spaced("Isaac Newton Institute · June 1993", 18, SEPIA).move_to(P(0, 3.05))
        wiles3 = plain_cameo(0.6).move_to(P(4.6, 1.75))
        wiles3_l = cameo_label("Andrew Wiles", "three lectures").next_to(wiles3, DOWN, buff=0.1)
        line("In June 1993, back in Cambridge, Wiles gave three lectures without saying where they were going.", FadeIn(place3), FadeIn(board), FadeIn(wiles3), FadeIn(wiles3_l),
             run_time=1.0)
        self.play(Write(btitle), run_time=1.6)
        self.vo_wait()
        bline = MathTex(r"\Rightarrow\ \text{Fermat's Last Theorem}", font_size=40, color=chalk)
        bline.move_to(board.get_center() + DOWN * 0.5)
        date = note("23 June 1993, end of the last lecture", 15, SEPIA).next_to(board, DOWN, buff=0.15)
        claps = VGroup()
        rng = np.random.default_rng(4)
        for i in range(22):
            x = rng.uniform(-5.6, 5.6)
            y = rng.uniform(-2.75, -2.35)
            if abs(x + 1.2) < 2.0:
                y -= 0.05
            claps.add(Arc(radius=0.12, start_angle=PI / 4, angle=PI / 2, color=SEPIA, stroke_width=2).move_to(P(x, y)))
        line("At the end of the last one, on the 23rd of June, he wrote Fermat's Last Theorem on the board. "
             "The room broke into applause.", FadeIn(date), run_time=0.6)
        self.play(Write(bline), run_time=1.8)
        self.play(LaggedStart(*[FadeIn(c, scale=1.6) for c in claps], lag_ratio=0.05), run_time=1.4)
        self.vo_wait()

        # ================= the gap =================
        crack = VMobject(color=RED_INK, stroke_width=6).set_points_as_corners(
            [board.get_center() + P(x, y) for x, y in [(-1.6, 0.6), (-1.0, 0.1), (-0.6, 0.35), (-0.1, -0.15),
                                                       (0.4, 0.1), (0.9, -0.4)]])
        gap_l = note("September 1993: a gap in one crucial step", 16, RED_INK).move_to(date)
        line("But later that year, as the proof was checked, a gap turned up in one crucial step.",
             FadeOut(claps), FadeOut(date), run_time=0.5)
        self.play(Create(crack), FadeIn(gap_l), run_time=1.2)
        self.vo_wait()
        taylor = plain_cameo(0.6).move_to(P(4.6, -0.95))
        taylor_l = serif("Richard Taylor", 20, INK).next_to(taylor, DOWN, buff=0.1)
        wiles3_l2 = cameo_label("Andrew Wiles", "a year of repair").move_to(wiles3_l)
        line("Wiles worked for another year to repair it, helped by Richard Taylor.",
             FadeIn(taylor), FadeIn(taylor_l), Transform(wiles3_l, wiles3_l2), run_time=1.0)
        self.vo_wait()
        mend = crack.copy().set_color(GREEN_INK)
        rev = VGroup(serif("“suddenly, totally unexpectedly,", 20, INK, italic=True),
                     serif("I had this incredible revelation”", 20, INK, italic=True),
                     note("Wiles, as quoted by MacTutor", 13)).arrange(DOWN, buff=0.08)
        rcard = ink_card(rev, pad=0.2).move_to(P(-1.2, -1.95))
        place4 = spaced("19 September 1994", 18, SEPIA).move_to(P(0, 3.05))
        line("On the 19th of September 1994, close to giving up, he took one last look, and saw how to make it work.",
             FadeOut(place3), FadeIn(place4), FadeOut(gap_l), run_time=0.8)
        self.play(ReplacementTransform(crack, mend), FadeIn(rcard, shift=UP * 0.2), run_time=1.4)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(board, btitle, bline, mend, rcard, wiles3, wiles3_l, taylor, taylor_l,
                                          place4)), run_time=0.8)

        # ================= 1995, 2001, the bridge =================
        def journal(t1, t2, pages):
            body = Rectangle(width=2.6, height=3.3, stroke_color=INK, stroke_width=2, fill_color="#e8dcc0",
                             fill_opacity=1)
            g = VGroup(body,
                       serif("ANNALS OF", 15, SEPIA), serif("MATHEMATICS", 15, SEPIA),
                       Line(LEFT * 1.0, RIGHT * 1.0, color=SEPIA, stroke_width=1),
                       serif(t1, 14, INK, italic=True), serif(t2, 14, INK, italic=True),
                       mono(pages, 12, FADED))
            g[1:].arrange(DOWN, buff=0.12).move_to(body)
            return g

        j1 = journal("Modular elliptic curves and", "Fermat's Last Theorem", "141 (1995) 443–551").move_to(P(-4.3, 0.8))
        j2 = journal("Ring-theoretic properties of", "certain Hecke algebras", "141 (1995) 553–572").move_to(P(-1.4, 0.8))
        j1a = note("A. Wiles", 14).next_to(j1, DOWN, buff=0.1)
        j2a = note("R. Taylor and A. Wiles", 14).next_to(j2, DOWN, buff=0.1)
        jnote = note("covers drawn, not the real ones", 13).next_to(VGroup(j1a, j2a), DOWN, buff=0.1)
        line("The proof appeared in 1995, in two papers that filled an issue of the Annals of Mathematics.",
             FadeIn(j1, shift=UP * 0.2), FadeIn(j2, shift=UP * 0.2), FadeIn(j1a), FadeIn(j2a), FadeIn(jnote),
             run_time=1.0)
        self.vo_wait()
        bank_l = VGroup(Rectangle(width=1.8, height=1.0, fill_color=RED_INK, fill_opacity=0.25, stroke_color=INK),
                        serif("elliptic curves", 17, RED_INK)).move_to(P(1.05, -1.5))
        bank_l[1].move_to(bank_l[0])
        bank_r = VGroup(Rectangle(width=1.8, height=1.0, fill_color=BLUE_INK, fill_opacity=0.25, stroke_color=INK),
                        serif("modular forms", 17, BLUE_INK)).move_to(P(5.35, -1.5))
        bank_r[1].move_to(bank_r[0])
        arch = ArcBetweenPoints(bank_l[0].get_corner(UR), bank_r[0].get_corner(UL), angle=-PI / 1.5, color=INK,
                                stroke_width=5)
        deck = Line(bank_l[0].get_corner(UR), bank_r[0].get_corner(UL), color=INK, stroke_width=3)
        hangers = VGroup(*[Line(deck.point_from_proportion(t), arch.point_from_proportion(t), color=SEPIA,
                                stroke_width=1.5) for t in np.linspace(0.15, 0.85, 6)])
        y01 = VGroup(mono("1995: semistable curves", 15, INK),
                     mono("2001: every elliptic curve", 15, INK),
                     note("Breuil, Conrad, Diamond, Taylor", 13)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        y01.move_to(P(3.2, 1.9))
        line("By 2001, others had carried the bridge across to every elliptic curve.", FadeIn(y01), run_time=0.9)
        self.play(FadeIn(bank_l), FadeIn(bank_r), Create(arch), Create(deck), run_time=1.2)
        self.play(LaggedStart(*[Create(h) for h in hangers], lag_ratio=0.15), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(j1, j2, j1a, j2a, jnote, bank_l, bank_r, arch, deck, hangers, y01)),
                  run_time=0.8)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 20, RED_INK).move_to(P(0, 3.05))
        src = ["def count(p):",
               "    return sum((y*y + y - x**3 + x*x) % p == 0",
               "               for x in range(p) for y in range(p))",
               "",
               "for p in [2, 3, 5, 7, 11, 13]:",
               "    print(p, p - count(p))"]
        cw = mono("M" * 10, 17).width / 10
        code = VGroup()
        for i, ln in enumerate(src):
            if not ln.strip():
                continue
            t = mono(ln.strip(), 17, INK)
            lead = len(ln) - len(ln.lstrip())
            t.move_to(P(0, -0.36 * i), aligned_edge=LEFT).shift(RIGHT * lead * cw)
            t.set_y(-0.36 * i)
            code.add(t)
        ccard = ink_card(code, pad=0.25).move_to(P(-2.4, 1.0))
        out = VGroup(*[mono(f"{p:>2} {p - len(solutions(p)):>3}", 18, RED_INK) for p in [2, 3, 5, 7, 11, 13]])
        out.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        ocard = ink_card(VGroup(note("its output", 13), out).arrange(DOWN, buff=0.1), pad=0.2).move_to(P(3.3, 1.0))
        line("Try it yourself. Write a short program that counts the pairs that work, modulo each prime.",
             FadeIn(tiy), FadeIn(ccard, shift=UP * 0.2), run_time=1.0)
        self.vo_wait()
        ser2 = MathTex(r"q-2q^2-q^3+2q^4+q^5+2q^6-2q^7-2q^9-2q^{10}+q^{11}-2q^{12}+4q^{13}+\cdots",
                       font_size=30, color=BLUE_INK).move_to(P(0, -1.45))
        ser_l = note("compare: the series from before", 14).next_to(ser2, UP, buff=0.12)
        more = note("then go on to 17, 19, 23 ... and check them yourself", 15, SEPIA).next_to(ser2, DOWN, buff=0.15)
        line("Subtract each count from its prime, compare with the series, then try bigger primes.", FadeIn(ocard, shift=LEFT * 0.2), run_time=0.9)
        self.play(FadeIn(ser_l), Write(ser2), run_time=1.6)
        self.play(FadeIn(more), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tiy, ccard, ocard, ser2, ser_l, more)), run_time=0.8)

        # ================= close =================
        eqc = MathTex("x^n+y^n=z^n", font_size=48, color=INK).move_to(P(0, 1.9))
        last = VGroup(serif("A problem a ten-year-old could understand,", 30, INK),
                      serif("and a promise kept three decades later.", 30, RED_INK)).arrange(DOWN, buff=0.22)
        last.move_to(P(0, -0.2))
        line("A problem a ten-year-old could understand, and a promise kept three decades later.",
             FadeIn(eqc), FadeIn(last, lag_ratio=0.2), run_time=1.2)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(last, eqc)), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after S. Singh, Fermat's Enigma (1997) · sources in the episode notes", 17),
                     note("facts checked against MacTutor, the IMU Abel Prize biography, Britannica, NOVA (2000), "
                          "Wikipedia and the LMFDB", 17),
                     note("silhouettes stylised, not likenesses · books and journals drawn schematically · point "
                          "counts and series computed in the episode · Manim · synthetic narration", 15)
                     ).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        for m in end:
            if m.width > 12.8:
                m.scale_to_fit_width(12.8)
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(2.0)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)

    @staticmethod
    def _roots():
        """x where 1 + 4(x^3 - x^2) = 0 (the curve's vertical tangents), found numerically."""
        r = np.roots([4, -4, 0, 1])
        return [float(x.real) for x in r if abs(x.imag) < 1e-9]
