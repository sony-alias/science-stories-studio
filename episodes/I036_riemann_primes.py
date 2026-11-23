"""I036 Eight Pages from Riemann, a Science Stories episode.

After J. Derbyshire, Prime Obsession (2003). Script and sources: episodes/I036_script.md

Render:  manim -qh --frame_rate 30 episodes/I036_riemann_primes.py EightPagesFromRiemann
Then:    scripts/finish_video.sh media/videos/I036_riemann_primes/1080p30/EightPagesFromRiemann.mp4 out/I036_riemann_primes.mp4
"""
import math
import os
import sys

import mpmath as mp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

MONO = "DejaVu Sans Mono"
_HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(_HERE, "..", "media", "I036_waves.npz")


def note(text, size=17, color=FADED):
    return serif(text, size, color, italic=True)


def P(x, y):
    return np.array([x, y, 0.0])


def mono(text, size=20, color=INK):
    return Text(text, font=MONO, font_size=size, color=color)


# ---------- the mathematics, computed exactly (checked at render time) ----------
X_MAX = 60.0
XS = np.linspace(2.0, X_MAX, 1161)       # step 0.05
N_ZEROS = 100


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


PRIMES = [p for p in range(2, 200) if is_prime(p)]


def prime_pi(x):
    return sum(1 for p in PRIMES if p <= x)


def mobius(n):
    r, k = 1, 2
    while k * k <= n:
        if n % k == 0:
            n //= k
            if n % k == 0:
                return 0
            r = -r
        k += 1
    return -r if n > 1 else r


MU = [0] + [mobius(n) for n in range(1, 40)]


def wave(x, gamma):
    """Contribution of the zero pair 1/2 +- i*gamma to Riemann's formula: -2 Re R(x^rho)."""
    L = mp.log(x)
    rho = mp.mpc(0.5, gamma)
    s = 0
    for n in range(1, 40):
        if MU[n]:
            s += MU[n] / mp.mpf(n) * mp.ei(rho * L / n)     # li(x^(rho/n)) = Ei(rho ln x / n)
    return -2.0 * float(s.real)


def extra(x):
    """Small terms of the explicit formula from the trivial zeros (modern form)."""
    L = np.log(x)
    return -1.0 / L + np.arctan(np.pi / L) / np.pi


def load_data():
    if os.path.exists(CACHE):
        d = np.load(CACHE)
        return d["gammas"], d["R"], d["W"], d["li"]
    mp.mp.dps = 15
    gammas = np.array([float(mp.zetazero(k).imag) for k in range(1, N_ZEROS + 1)])
    R = np.array([float(mp.riemannr(x)) for x in XS])
    li = np.array([float(mp.li(x)) for x in XS])
    W = np.array([[wave(x, g) for g in gammas] for x in XS])
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    np.savez(CACHE, gammas=gammas, R=R, W=W, li=li)
    return gammas, R, W, li


GAMMAS, RX, WAVES, LI = load_data()


def riemann_curve(n):
    return RX + WAVES[:, :n].sum(axis=1) + extra(XS)


# checks: the zeros, the counts and how well the formula rebuilds the staircase
assert abs(GAMMAS[0] - 14.134725) < 1e-5 and abs(GAMMAS[1] - 21.022040) < 1e-5 and abs(GAMMAS[2] - 25.010858) < 1e-5
assert prime_pi(10) == 4 and prime_pi(100) == 25 and prime_pi(60) == 17
# (below x = 6 the sum over zeros converges slowly, so 100 zeros still wobble there; checked from 6 up)
_mid = [i for i, x in enumerate(XS) if abs((x % 1) - 0.5) < 1e-6 and x > 6]
_err100 = max(abs(riemann_curve(100)[i] - prime_pi(XS[i])) for i in _mid)
_err0 = max(abs(riemann_curve(0)[i] - prime_pi(XS[i])) for i in _mid)
assert _err100 < 0.4 and _err0 > 0.8, (_err0, _err100)
print(f"I036 check: max |formula - pi(x)| at half-integers from 6 to 60, 0 zeros {_err0:.2f}, 100 zeros {_err100:.2f}")
# try-it values: pi(x) / (x / ln x)
TRY = [(10, 4), (100, 25), (1000, 168), (1_000_000, 78498)]
for _x, _c in TRY:
    assert sum(1 for p in range(2, min(_x, 2000) + 1) if is_prime(p)) == _c or _x > 2000


def curve_from(ax, ys, color, width=3, x_from=2.0):
    pts = [ax.c2p(x, y) for x, y in zip(XS, ys) if x >= x_from - 1e-9]
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)


def staircase(ax, color=INK, width=3.5):
    pts = [ax.c2p(2, 0)]
    count = 0
    for p in PRIMES:
        if p > X_MAX:
            break
        pts.append(ax.c2p(p, count))
        count += 1
        pts.append(ax.c2p(p, count))
    pts.append(ax.c2p(X_MAX, count))
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)


class EightPagesFromRiemann(NarratedScene):
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
        title = serif("Eight Pages from Riemann", 54).next_to(orn1, DOWN, buff=0.35)
        sub = serif("The hidden music of the prime numbers", 26, FADED, italic=True).next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("after J. Derbyshire, Prime Obsession (2003)", 16).move_to([0, -2.6, 0])
        self.vo("Science Stories. Eight pages from Riemann.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.wait(0.5)
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= the person =================
        riem = cameo("beard", 0.85).move_to(P(-4.3, 0.8))
        riem_l = VGroup(serif("Bernhard Riemann", 22, INK), note("1826 – 1866", 15)).arrange(DOWN, buff=0.05)
        riem_l.next_to(riem, DOWN, buff=0.15)
        sil_n = note("silhouette stylised, not a likeness", 13).next_to(riem_l, DOWN, buff=0.1)
        when = spaced("Göttingen · August 1859", 18, SEPIA).move_to(P(1.7, 2.75))
        academy = VGroup(serif("Berlin Academy of Sciences", 30, INK),
                         note("elected a corresponding member", 20, SEPIA)).arrange(DOWN, buff=0.12).move_to(P(1.7, 1.6))
        line("In August 1859, Bernhard Riemann, a mathematician at Göttingen, was made a corresponding member of the "
             "Berlin Academy.", FadeIn(riem), FadeIn(riem_l), FadeIn(sil_n), FadeIn(when), run_time=1.0)
        self.play(FadeIn(academy, shift=UP * 0.1), run_time=1.0)
        self.vo_wait()

        page = VGroup(Rectangle(width=2.8, height=3.3, fill_color="#f6eedb", fill_opacity=1, stroke_color=SEPIA,
                                stroke_width=2))
        ptitle = VGroup(serif("Ueber die Anzahl der Primzahlen", 15, INK),
                        serif("unter einer gegebenen Grösse.", 15, INK)).arrange(DOWN, buff=0.04)
        ptitle.move_to(page[0].get_top() + DOWN * 0.42)
        page.add(ptitle)
        for k in range(11):
            w = 2.2 if k % 5 != 4 else 1.5
            page.add(Line(LEFT * w / 2, RIGHT * w / 2, color=FADED, stroke_width=1.2).move_to(
                page[0].get_top() + DOWN * (0.95 + 0.2 * k) + LEFT * (2.2 - w) / 2))
        page.move_to(P(-0.6, -0.15))
        stack = VGroup(*[page[0].copy().set_fill("#efe3c6").shift(RIGHT * 0.07 * k + DOWN * 0.07 * k).set_z_index(-k)
                         for k in range(1, 8)])
        trans = VGroup(note("“On the Number of Primes", 17, SEPIA), note("Less Than a Given Magnitude”", 17, SEPIA),
                       note("Monatsberichte, Berlin, November 1859", 15),
                       note("about eight printed pages (some count nine)", 14)).arrange(DOWN, buff=0.06)
        trans.move_to(P(3.7, -0.3))
        line("The custom was to thank the Academy with an original paper. Riemann sent one about prime numbers, the "
             "only paper on number theory he ever published.", FadeOut(academy), FadeIn(stack), FadeIn(page),
             run_time=1.0)
        self.play(FadeIn(trans, shift=LEFT * 0.1), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(riem, riem_l, sil_n, when, page, stack, trans)), run_time=0.7)

        # ================= the puzzle: primes =================
        cells = VGroup()
        for n in range(1, 61):
            r, c = divmod(n - 1, 12)
            sq = Square(0.62, stroke_color=SEPIA, stroke_width=1.2)
            num = serif(str(n), 20, INK)
            cells.add(VGroup(sq, num).move_to(P(-3.6 + c * 0.66, 2.0 - r * 0.66)))
        line("Primes are the numbers with no divisors except one and themselves. Two, three, five, seven, eleven, "
             "thirteen.", FadeIn(cells, lag_ratio=0.01), run_time=1.2)
        marks = []
        for p in [2, 3, 5, 7, 11, 13]:
            c = cells[p - 1]
            self.play(c[0].animate.set_fill(RED_INK, 0.85), c[1].animate.set_color(PAPER), run_time=0.35)
            marks.append(c)
        self.vo_wait()
        rest = [cells[p - 1] for p in PRIMES if 13 < p <= 60]
        q = serif("How many primes are there below a given number?", 30, INK).move_to(P(0, -1.75))
        line("They never run out, but they seem to appear at random. So the question is: how many primes are there "
             "below a given number?", LaggedStart(*[AnimationGroup(c[0].animate.set_fill(RED_INK, 0.85),
                                                                    c[1].animate.set_color(PAPER)) for c in rest],
                                                   lag_ratio=0.15), run_time=2.0)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.7)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(cells, q)), run_time=0.7)

        # ================= the staircase =================
        ax = Axes(x_range=[0, 60, 10], y_range=[0, 21, 3], x_length=10.6, y_length=5.3, tips=False,
                  axis_config=dict(color=INK, stroke_width=2, include_numbers=True, font_size=22,
                                   decimal_number_config=dict(color=INK, num_decimal_places=0)))
        ax.move_to(P(0.25, 0.15))
        ax_lab_x = note("x", 20, SEPIA).next_to(ax.x_axis.get_end(), RIGHT, buff=0.2)
        ax_lab_y = note("number of primes up to x", 18, SEPIA).next_to(ax.y_axis.get_end(), RIGHT, buff=0.15)
        stairs = staircase(ax)
        line("Count them, and you get a staircase. It climbs one step at every prime, at uneven intervals.",
             Create(ax), FadeIn(ax_lab_x), FadeIn(ax_lab_y), run_time=1.0)
        self.play(Create(stairs), run_time=3.0, rate_func=linear)
        tag = note("17 primes up to 60", 18, INK).next_to(ax.c2p(60, 17), UP, buff=0.15).shift(LEFT * 0.6)
        self.play(FadeIn(tag), run_time=0.5)
        self.vo_wait()

        # ================= the obvious answer: Gauss =================
        gauss = cameo("plain", 0.5).move_to(P(-3.55, 1.95))
        gauss_l = VGroup(serif("Carl Friedrich Gauss", 17, INK), note("Riemann's doctoral supervisor", 13)
                         ).arrange(DOWN, buff=0.03).next_to(gauss, DOWN, buff=0.08)
        line("The obvious answer had come from Gauss, Riemann's own doctoral supervisor. As a boy of about fifteen, "
             "Gauss had counted primes in blocks of a thousand.", FadeIn(gauss), FadeIn(gauss_l), FadeOut(tag),
             run_time=1.0)
        blocks = VGroup(*[VGroup(Rectangle(width=0.5, height=h * 0.012, fill_color=SEPIA, fill_opacity=0.7,
                                           stroke_width=0)) for h in (168, 135, 127, 120, 119)])
        blocks.scale([1, 0.6, 1])
        blocks.arrange(RIGHT, buff=0.08, aligned_edge=DOWN).move_to(P(-0.9, 2.15))
        blocks_l = note("primes in each block of 1000: 168, 135, 127, 120, 119", 14, SEPIA).next_to(blocks, DOWN,
                                                                                                     buff=0.08)
        blocks_l.align_to(blocks, LEFT)
        self.play(FadeIn(blocks, lag_ratio=0.3), FadeIn(blocks_l), run_time=1.2)
        self.vo_wait()
        dens = MathTex(r"\text{density near } x \approx \frac{1}{\ln x}", font_size=32, color=INK)
        dens.move_to(P(-1.1, 2.0))
        gcurve = curve_from(ax, LI, BLUE_INK, 3)
        g_lab = MathTex(r"\mathrm{li}(x)=\int_0^x \frac{dt}{\ln t}", font_size=28, color=BLUE_INK)
        g_lab.next_to(ax.c2p(50, LI[-200]), UP, buff=0.35).shift(LEFT * 0.4)
        line("He noticed that, on average, the primes thin out like one over the logarithm. That gives a smooth curve.",
             FadeOut(blocks), FadeOut(blocks_l), FadeIn(dens), run_time=0.9)
        self.play(Create(gcurve), run_time=2.0)
        self.play(FadeIn(g_lab), run_time=0.6)
        self.vo_wait()
        zoom_box = SurroundingRectangle(VGroup(Dot(ax.c2p(28, 8)), Dot(ax.c2p(40, 13))), color=RED_INK, buff=0.05,
                                        stroke_width=2.5)
        line("The curve follows the staircase well. But a smooth curve can never make sharp steps. It always misses "
             "the details.", Create(zoom_box), run_time=1.0)
        self.vo_wait()
        line("Riemann wanted an exact formula. Not an estimate, but the staircase itself.",
             FadeOut(zoom_box), FadeOut(dens), FadeOut(gauss), FadeOut(gauss_l), run_time=0.8)
        self.vo_wait()
        graph_group = VGroup(ax, ax_lab_x, ax_lab_y, stairs, gcurve, g_lab)
        self.play(clear(), FadeOut(graph_group), run_time=0.7)

        # ================= the zeta function =================
        zeta = MathTex(r"\zeta(s)", r"=", r"1+\frac{1}{2^s}+\frac{1}{3^s}+\frac{1}{4^s}+\cdots", font_size=46,
                       color=INK).move_to(P(0, 1.4))
        line("His key was a function now called the zeta function. Add one, plus one over two to the power s, plus "
             "one over three to the power s, and so on forever.", Write(zeta[0:2]), run_time=1.0)
        self.play(Write(zeta[2]), run_time=2.0)
        self.vo_wait()
        prod = MathTex(r"=", r"\frac{1}{1-2^{-s}}\cdot\frac{1}{1-3^{-s}}\cdot\frac{1}{1-5^{-s}}\cdot"
                             r"\frac{1}{1-7^{-s}}\cdots", font_size=42, color=RED_INK)
        prod.next_to(zeta, DOWN, buff=0.5).align_to(zeta[1], LEFT)
        prod_l = note("Euler: a sum over all whole numbers equals a product over all the primes", 18, SEPIA)
        prod_l.next_to(prod, DOWN, buff=0.35)
        line("Euler had shown that this sum over all whole numbers equals a product over all the primes. So the zeta "
             "function secretly knows where the primes are.", Write(prod), run_time=1.6)
        self.play(FadeIn(prod_l), run_time=0.6)
        self.vo_wait()
        self.play(FadeOut(VGroup(prod, prod_l)), zeta.animate.scale(0.75).move_to(P(-3.6, 2.6)), run_time=0.8)

        # ================= complex plane and zeros =================
        cp = Axes(x_range=[-1, 2, 1], y_range=[0, 40, 10], x_length=3.6, y_length=4.6, tips=False,
                  axis_config=dict(color=INK, stroke_width=2, include_numbers=True, font_size=20,
                                   decimal_number_config=dict(color=INK, num_decimal_places=0)))
        cp.move_to(P(2.6, 0.45))
        strip = Polygon(cp.c2p(0, 0), cp.c2p(1, 0), cp.c2p(1, 40), cp.c2p(0, 40), stroke_width=0,
                        fill_color=PAPER_DARK, fill_opacity=0.8).set_z_index(-1)
        re_l = note("real part of s", 15, SEPIA).next_to(cp.x_axis.get_end(), RIGHT, buff=0.2)
        im_l = note("imaginary part", 15, SEPIA).rotate(PI / 2).next_to(cp.y_axis, LEFT, buff=0.45)
        expl = VGroup(note("s = a + b·i, a complex number", 20, INK),
                      note("where is ζ(s) = 0 ?", 22, RED_INK)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        expl.move_to(P(-3.6, 1.0))
        line("Riemann's bold step was to let s be a complex number, and to ask where zeta equals zero.",
             Create(cp), FadeIn(strip), FadeIn(re_l), FadeIn(im_l), run_time=1.2)
        self.play(FadeIn(expl, lag_ratio=0.3), run_time=0.8)
        self.vo_wait()
        zdots = VGroup()
        zlabs = VGroup()
        for g in GAMMAS[:6]:
            d = Dot(cp.c2p(0.5, g), radius=0.075, color=RED_INK)
            zdots.add(d)
            zlabs.add(MathTex(r"\tfrac12 + %.2f\,i" % g, font_size=22, color=RED_INK).next_to(d, RIGHT, buff=0.15))
        zlabs[3].shift(DOWN * 0.08)     # 30.42 and 32.94 sit close together; nudge the labels apart
        zlabs[4].shift(UP * 0.08)
        zl_note = note("zeros in the critical strip (shaded), lowest six", 15).move_to(P(-3.6, -0.2))
        line("Those zeros sit at heights fourteen point one, twenty-one point oh, twenty-five point oh, and on, "
             "without end.", LaggedStart(*[FadeIn(d, scale=2) for d in zdots[:3]], lag_ratio=0.5),
             LaggedStart(*[FadeIn(l) for l in zlabs[:3]], lag_ratio=0.5), run_time=2.4)
        self.play(FadeIn(zdots[3:], lag_ratio=0.3), FadeIn(zlabs[3:], lag_ratio=0.3), FadeIn(zl_note), run_time=1.2)
        self.vo_wait()
        plane = VGroup(cp, strip, re_l, im_l, zdots, zlabs)
        self.play(clear(), FadeOut(VGroup(expl, zl_note, zeta)), plane.animate.set_opacity(0), run_time=0.7)
        self.remove(plane)

        # ================= the waves =================
        ax2 = Axes(x_range=[0, 60, 10], y_range=[0, 21, 3], x_length=10.6, y_length=5.3, tips=False,
                   axis_config=dict(color=INK, stroke_width=2, include_numbers=True, font_size=22,
                                    decimal_number_config=dict(color=INK, num_decimal_places=0)))
        ax2.move_to(P(0.25, 0.15))
        stairs2 = staircase(ax2, color=INK, width=3)
        lab_x2 = note("x", 20, SEPIA).next_to(ax2.x_axis.get_end(), RIGHT, buff=0.2)
        smooth = curve_from(ax2, riemann_curve(0), BLUE_INK, 3.5, x_from=3.0)
        smooth_l = note("Riemann's smooth part, a sharper version of Gauss's curve", 16, BLUE_INK)
        smooth_l.move_to(ax2.c2p(40, 2.2))
        self.play(FadeIn(ax2), FadeIn(lab_x2), FadeIn(stairs2), run_time=0.8)
        self.play(Create(smooth), FadeIn(smooth_l), run_time=1.2)

        # inset: one wave on its own
        ins = Axes(x_range=[0, 60, 20], y_range=[-1.5, 1.5, 1], x_length=4.2, y_length=1.6, tips=False,
                   axis_config=dict(color=FADED, stroke_width=1.5))
        ins.move_to(ax2.c2p(15.5, 17.0))
        ins_box = SurroundingRectangle(ins, color=SEPIA, buff=0.15, stroke_width=1.5).set_fill(PAPER, 1)
        w1 = curve_from(ins, WAVES[:, 0], RED_INK, 2.5)
        ins_l = note("the wave from the zero at height 14.13", 14, RED_INK).next_to(ins_box, DOWN, buff=0.08)
        line("And here is the magic. Each zero adds a wave to the smooth curve.", FadeIn(ins_box), FadeIn(ins),
             run_time=0.8)
        self.play(Create(w1), FadeIn(ins_l), run_time=2.0)
        self.vo_wait()

        counter = VGroup(note("zeros used:", 20, SEPIA), serif("0", 26, RED_INK)).arrange(RIGHT, buff=0.15)
        counter.move_to(ax2.c2p(44, 4.4))

        def set_count(n):
            new = serif(str(n), 26, RED_INK).move_to(counter[1]).align_to(counter[1], LEFT)
            return Transform(counter[1], new)

        line("With one wave, the curve starts to wobble towards the steps. With ten, the steps begin to show. With a "
             "hundred, the curve hugs the staircase.", FadeOut(smooth_l), FadeIn(counter),
             smooth.animate.set_color(RED_INK), run_time=0.8)
        self.play(Transform(smooth, curve_from(ax2, riemann_curve(1), RED_INK, 3.5, x_from=3.0)), set_count(1), run_time=1.6)
        self.wait(0.8)
        for n, t in ((3, 0.9), (10, 1.3), (30, 1.3), (100, 1.6)):
            self.play(Transform(smooth, curve_from(ax2, riemann_curve(n), RED_INK, 3.5, x_from=3.0)), set_count(n), run_time=t)
            self.wait(0.5 if n < 100 else 0.2)
        self.vo_wait()
        modern = note("Riemann's formula in a modern form (with Möbius sums); waves computed exactly for the first 100 "
                      "zeros, drawn from x = 3", 14).move_to(ax2.c2p(38, 2.0))
        if modern.width > 7.2:
            modern.scale_to_fit_width(7.2)
        music = serif("The primes are a sum of waves.", 30, INK).move_to(ax2.c2p(19, 18.0))
        line("The primes, which look random, are a sum of waves, and the zeros of zeta set their pitch.",
             FadeOut(VGroup(ins_box, ins, w1, ins_l)), FadeIn(modern), run_time=0.8)
        self.play(FadeIn(music, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(ax2, stairs2, lab_x2, smooth, counter, modern, music)), run_time=0.7)

        # ================= the hypothesis =================
        plane.set_opacity(1)
        strip.set_fill(PAPER_DARK, 0.8).set_stroke(width=0)
        plane.move_to(P(3.6, 0.3))
        crit = DashedLine(cp.c2p(0.5, 0), cp.c2p(0.5, 40), color=RED_INK, stroke_width=3, dash_length=0.12)
        crit_l = MathTex(r"\text{real part} = \tfrac12", font_size=24, color=RED_INK).next_to(cp.c2p(0.5, 40), UP,
                                                                                             buff=0.12)
        self.add(plane)
        self.play(FadeIn(plane), run_time=0.01)
        line("The zeros all seem to sit on one straight line, where the real part is exactly one half.",
             Create(crit), FadeIn(crit_l), run_time=1.4)
        self.vo_wait()
        quote = VGroup(note("“it is very probable that all roots are real.", 22, INK),
                       note("Certainly one would wish for a stricter proof here;", 22, INK),
                       note("I have meanwhile temporarily put aside the search", 22, INK),
                       note("for this after some fleeting futile attempts …”", 22, INK)).arrange(
            DOWN, buff=0.1, aligned_edge=LEFT)
        qsrc = note("Riemann, 1859 · translated by D. R. Wilkins", 15, SEPIA)
        qnote = note("(“roots” of his ξ function = zeros on the line)", 14)
        qcard = VGroup(quote, qsrc, qnote).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        qcard = ink_card(qcard)
        qcard.move_to(P(-2.6, 0.6))
        line("Riemann wrote that it is very probable that all of them do, and that he had set the proof aside after "
             "some fleeting, futile attempts.", FadeIn(qcard, shift=RIGHT * 0.1), run_time=1.0)
        self.vo_wait()
        rh = serif("The Riemann Hypothesis", 34, RED_INK).move_to(P(-2.6, -1.8))
        unp = note("unproven, 1859 – today", 18, SEPIA).next_to(rh, DOWN, buff=0.1)
        line("That sentence is the Riemann hypothesis. It is still unproven.", Write(rh), run_time=1.2)
        self.play(FadeIn(unp), run_time=0.5)
        self.vo_wait()
        self.play(FadeOut(qcard), VGroup(rh, unp).animate.move_to(P(-2.6, 2.4)), run_time=0.8)

        koch = VGroup(note("if true, the error in counting the primes", 19, INK),
                      note("stays as small as it possibly can:", 19, INK),
                      MathTex(r"|\pi(x)-\mathrm{li}(x)| \lesssim \sqrt{x}\,\ln x", font_size=34, color=INK),
                      note("von Koch, 1901", 15, SEPIA)).arrange(DOWN, buff=0.15).move_to(P(-2.6, 0.5))
        line("If it is true, the waves are as small as they can be, and the primes are as regular as they can "
             "possibly be.", FadeIn(koch, lag_ratio=0.2), run_time=1.2)
        self.vo_wait()
        checked = VGroup(serif("10,000,000,000,000", 30, INK), note("zeros checked by computer, all on the line", 17,
                                                                     SEPIA)).arrange(DOWN, buff=0.08)
        prize = VGroup(serif("$1,000,000", 30, RED_INK), note("Clay Mathematics Institute prize for a proof", 17,
                                                              SEPIA)).arrange(DOWN, buff=0.08)
        VGroup(checked, prize).arrange(DOWN, buff=0.4).move_to(P(-2.6, -0.9))
        line("Computers have checked the first ten trillion zeros. All of them lie on the line.",
             FadeOut(koch), FadeIn(checked, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()
        line("But checking is not proving. The Clay Mathematics Institute offers a million dollars for a proof.",
             FadeIn(prize, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(plane, crit, crit_l, rh, unp, checked, prize)), run_time=0.8)

        # ================= Riemann's end, and the notes =================
        riem2 = cameo("beard", 0.75).move_to(P(-4.4, 0.9))
        r2l = VGroup(serif("Bernhard Riemann", 20, INK), note("died at Selasca, Italy, 20 July 1866, aged 39", 14)
                     ).arrange(DOWN, buff=0.05).next_to(riem2, DOWN, buff=0.12)
        line("Riemann did not live to see any of this. He fell ill with tuberculosis, and died in Italy in 1866, aged "
             "thirty-nine.", FadeIn(riem2), FadeIn(r2l), run_time=1.0)
        self.vo_wait()
        notes = VGroup()
        for k in range(3):
            sh = Rectangle(width=2.4, height=3.0, fill_color="#f3e8cf", fill_opacity=1, stroke_color=SEPIA,
                           stroke_width=1.5)
            scrib = VGroup(*[Line(LEFT * 0.9, RIGHT * (0.9 - 0.3 * ((j * 7 + k) % 3)), color=FADED, stroke_width=1)
                             .move_to(sh.get_top() + DOWN * (0.35 + 0.22 * j)) for j in range(11)])
            notes.add(VGroup(sh, scrib).rotate((k - 1) * 7 * DEGREES).move_to(P(-0.9 + k * 0.5, 0.5 - k * 0.12)))
        siegel = VGroup(serif("Carl Ludwig Siegel, 1932", 22, INK),
                        note("finds in Riemann's rough notes a formula", 17, SEPIA),
                        note("he used to calculate zeros himself", 17, SEPIA),
                        note("now called the Riemann–Siegel formula", 15)).arrange(DOWN, buff=0.08)
        siegel.move_to(P(3.9, 0.9))
        z_hand = MathTex(r"\tfrac12 + 14.13\,i", font_size=30, color=RED_INK).move_to(P(0.15, -0.05)).rotate(-7 * DEGREES).set_z_index(5)
        z_hand = VGroup(BackgroundRectangle(z_hand, color="#f3e8cf", fill_opacity=1, buff=0.06).set_z_index(4), z_hand)
        line("Decades later, Carl Ludwig Siegel studied Riemann's rough notes, and found that he had calculated zeros "
             "himself, with a formula he never published.", FadeIn(notes, lag_ratio=0.3), run_time=1.2)
        self.play(FadeIn(siegel, shift=LEFT * 0.1), run_time=0.8)
        self.play(Write(z_hand), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(riem2, r2l, notes, siegel, z_hand)), run_time=0.7)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 24, RED_INK).move_to(P(0, 2.85))
        code = VGroup(
            mono("from math import log", 18, FADED),
            mono("N = 1_000_000", 18, INK),
            mono("sieve = [True] * (N + 1)", 18, INK),
            mono("for i in range(2, int(N**0.5) + 1):", 18, INK),
            mono("    if sieve[i]:", 18, INK),
            mono("        sieve[i*i::i] = [False] * len(sieve[i*i::i])", 18, INK),
            mono("for x in [10, 100, 1000, N]:", 18, INK),
            mono("    count = sum(sieve[2:x + 1])", 18, BLUE_INK),
            mono("    print(x, count, count / (x / log(x)))", 18, RED_INK),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        for m, n_ind in zip(code, [0, 0, 0, 0, 1, 2, 0, 1, 1]):
            m.shift(RIGHT * 0.45 * n_ind)       # Text drops leading spaces, so indent by hand
        code.scale_to_fit_width(6.3).move_to(P(-2.9, 0.4))
        code_card = SurroundingRectangle(code, color=SEPIA, buff=0.2, stroke_width=1.5)
        rows = [("x", "primes", "x / ln x", "ratio")]
        for x, c in TRY:
            g = x / math.log(x)
            rows.append((f"{x:,}", f"{c:,}", f"{g:,.1f}", f"{c / g:.3f}"))
        table = VGroup()
        for i, r in enumerate(rows):
            col = SEPIA if i == 0 else INK
            row = VGroup(*[serif(t, 20, RED_INK if (j == 3 and i > 0) else col) for j, t in enumerate(r)])
            for j, m in enumerate(row):
                m.move_to(P(1.6 + [0, 1.45, 2.85, 4.05][j], 1.6 - i * 0.5))
            table.add(row)
        rule = Line(P(1.0, 1.36), P(6.4, 1.36), color=SEPIA, stroke_width=1.5)
        line("Try it yourself. Write a short program that counts the primes below ten, a hundred, a thousand, a "
             "million.", FadeIn(tiy), FadeIn(code_card), FadeIn(code, lag_ratio=0.1), run_time=1.4)
        self.play(FadeIn(table[0]), Create(rule), FadeIn(VGroup(*[r[:2] for r in table[1:]]), lag_ratio=0.3),
                  run_time=1.2)
        self.vo_wait()
        settle = VGroup(note("the ratio settles towards 1, very slowly:", 16, SEPIA),
                        note("the prime number theorem, proved in 1896", 16, SEPIA)).arrange(DOWN, buff=0.06)
        settle.move_to(P(3.7, -1.1))
        line("Divide each count by x over the natural log of x. Watch the ratio settle towards one, very slowly.",
             FadeIn(VGroup(*[r[2:] for r in table[1:]]), lag_ratio=0.3), run_time=1.4)
        self.play(FadeIn(settle), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tiy, code_card, code, table, rule, settle)), run_time=0.8)

        # ================= close =================
        ax3 = Axes(x_range=[0, 60, 10], y_range=[0, 21, 3], x_length=7.0, y_length=3.2, tips=False,
                   axis_config=dict(color=FADED, stroke_width=1.5))
        ax3.move_to(P(0, 1.2))
        st3 = staircase(ax3, INK, 2.5)
        cv3 = curve_from(ax3, riemann_curve(100), RED_INK, 2.5, x_from=3.0)
        last = VGroup(serif("Eight pages, one guess,", 30, INK),
                      serif("and a question still open after more than 160 years.", 28, RED_INK)).arrange(
            DOWN, buff=0.18).move_to(P(0, -1.55))
        line("Eight pages, one guess, and a question still open after more than a hundred and sixty years.",
             FadeIn(ax3), Create(st3), run_time=1.4)
        self.play(Create(cv3), FadeIn(last, lag_ratio=0.2), run_time=1.6)
        self.vo_wait()
        self.wait(0.5)
        self.play(clear(), FadeOut(VGroup(ax3, st3, cv3, last)), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after J. Derbyshire, Prime Obsession (2003) · sources in the episode notes", 17),
                     note("facts checked against MacTutor, Riemann's paper (tr. D. R. Wilkins), C. L. Siegel (1932, "
                          "tr. Barkan and Sklar), the Clay Mathematics Institute and Wikipedia", 17),
                     note("silhouettes stylised · zeros and waves computed with mpmath · Manim · synthetic narration",
                          15)
                     ).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        for m in end:
            if m.width > 12.8:
                m.scale_to_fit_width(12.8)
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(3.0)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)
