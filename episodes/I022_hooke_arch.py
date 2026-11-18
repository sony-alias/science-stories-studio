"""I022 How a Stone Arch Stands: Hooke's Hanging Chain, a Science Stories episode.

After J. E. Gordon, Structures: Or Why Things Don't Fall Down (1978). Script and sources: episodes/I022_script.md

Render:  manim -qh --frame_rate 30 episodes/I022_hooke_arch.py HookeArch
Then:    scripts/finish_video.sh media/videos/I022_hooke_arch/1080p30/HookeArch.mp4 out/I022_hooke_arch.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

STONE = "#cdb98f"
STONE_EDGE = "#6b5536"
CHAIN = "#5a4a3a"
SUGAR = "#fbf8f0"


def note(text, size=17, color=FADED):
    return serif(text, size, color, italic=True)


def P(x, y):
    return np.array([x, y, 0.0])


# ---------- the catenary (exact) ----------
def catenary_pts(a, L, n=160):
    """Hanging chain y = a cosh(x/a) - a for -L <= x <= L (lowest point at y = 0)."""
    xs = np.linspace(-L, L, n)
    return xs, a * np.cosh(xs / a) - a


def curve(xs, ys, origin, sy=1.0, color=INK, width=3):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_smoothly([origin + P(x, sy * y) for x, y in zip(xs, ys)])
    return m


def chain_links(xs, ys, origin, sy=1.0, spacing=0.13, color=CHAIN):
    """Small oval links laid along a curve at equal arc length."""
    pts = np.array([origin + P(x, sy * y) for x, y in zip(xs, ys)])
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    links = VGroup()
    for k, sk in enumerate(np.arange(0, s[-1], spacing)):
        i = min(np.searchsorted(s, sk), len(pts) - 1)
        j = min(i + 1, len(pts) - 1)
        d = pts[j] - pts[max(i - 1, 0)]
        ang = np.arctan2(d[1], d[0])
        e = Ellipse(width=spacing * 1.25, height=spacing * (0.55 if k % 2 == 0 else 0.25),
                    stroke_color=color, stroke_width=2.2).rotate(ang).move_to(pts[i])
        links.add(e)
    return links


def stones_along(pts, t, n, gap=0.025, fill=STONE):
    """Voussoirs: n blocks of thickness t laid along a polyline pts (Nx3), joints normal to the curve."""
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    cuts = np.linspace(0, s[-1], n + 1)

    def at(sk):
        i = int(np.clip(np.searchsorted(s, sk), 1, len(pts) - 1))
        f = (sk - s[i - 1]) / max(s[i] - s[i - 1], 1e-9)
        p = pts[i - 1] + f * (pts[i] - pts[i - 1])
        d = pts[i] - pts[i - 1]
        nrm = np.array([-d[1], d[0], 0]) / np.linalg.norm(d)
        return p, nrm

    blocks = VGroup()
    for k in range(n):
        a0, a1 = cuts[k] + gap / 2, cuts[k + 1] - gap / 2
        ss = np.linspace(a0, a1, 6)
        outer, inner = [], []
        for sk in ss:
            p, nr = at(sk)
            outer.append(p + nr * t / 2)
            inner.append(p - nr * t / 2)
        blocks.add(Polygon(*(outer + inner[::-1]), stroke_color=STONE_EDGE, stroke_width=1.6,
                           fill_color=fill, fill_opacity=1))
    return blocks


# ---------- line of thrust in a semicircular arch under its own weight ----------
def thrust_polyline(R, t, H, y0, N=60):
    """Funicular polygon of the voussoir weights of a half arch (crown to springing), horizontal thrust H,
    passing the crown at height y0. Total half-arch weight is 1. Mirrored for the other half."""
    th = np.linspace(np.pi / 2, 0, N + 1)
    mid = (th[:-1] + th[1:]) / 2
    Ri, Ro = R - t / 2, R + t / 2
    h = (th[0] - th[1]) / 2
    rc = 2 / 3 * (Ro ** 3 - Ri ** 3) / (Ro ** 2 - Ri ** 2) * np.sin(h) / h
    xs = rc * np.cos(mid)
    pts = [(0.0, y0)]
    x, y, V = 0.0, y0, 0.0
    for xk in xs:
        y -= (xk - x) * V / H
        x = xk
        pts.append((x, y))
        V += 1.0 / N
    pts.append((x + y * H / V, 0.0))
    return np.array(pts)


def dense(p, k=12):
    out = [p[0]]
    for a, b in zip(p[:-1], p[1:]):
        for s in np.linspace(0, 1, k)[1:]:
            out.append(a + (b - a) * s)
    return np.array(out)


def best_thrust(R, t):
    best = (1e9, None, None)
    for H in np.linspace(0.25, 0.7, 46):
        for y0 in np.linspace(R - t / 2, R + t / 2, 21):
            d = dense(thrust_polyline(R, t, H, y0))
            m = np.max(np.abs(np.hypot(d[:, 0], d[:, 1]) - R))
            if m < best[0]:
                best = (m, H, y0)
    return best


def full_thrust(R, t, H, y0):
    half = dense(thrust_polyline(R, t, H, y0))
    left = half[::-1] * np.array([-1, 1])
    return np.vstack([left, half[1:]])


def semicircle_stones(c, R, t, n, gap=0.03):
    th = np.linspace(np.pi, 0, 200)
    pts = np.array([c + P(R * np.cos(a), R * np.sin(a)) for a in th])
    return stones_along(pts, t, n, gap)


def pier(x, y_top, w=0.5, h=0.7):
    return Rectangle(width=w, height=h, stroke_color=STONE_EDGE, stroke_width=1.6, fill_color=STONE_EDGE,
                     fill_opacity=0.35).move_to(P(x, y_top - h / 2))


class HookeArch(NarratedScene):
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
        title = serif("How a Stone Arch Stands", 56).next_to(orn1, DOWN, buff=0.35)
        sub = serif("Robert Hooke and the hanging chain", 26, FADED, italic=True).next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("after J. E. Gordon, Structures: Or Why Things Don't Fall Down (1978)", 16).move_to([0, -2.6, 0])
        self.vo("Science Stories. How a stone arch stands.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.3)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= Hooke in London =================
        cam = cameo("wig", 0.95).move_to([-4.4, 0.7, 0])
        cam_l = VGroup(serif("Robert Hooke (1635–1703)", 18, INK),
                       note("outline only: no confirmed portrait survives", 14)).arrange(DOWN, buff=0.06)
        cam_l.next_to(cam, DOWN, buff=0.2)
        place = VGroup(spaced("London", 20, SEPIA), serif("after the Great Fire of 1666", 26, INK, italic=True)
                       ).arrange(DOWN, buff=0.15).move_to([1.7, 2.6, 0])
        # a schematic street being rebuilt: burnt plots and new houses
        ground = Line(P(-1.6, 0.2), P(5.0, 0.2), color=INK, stroke_width=2)
        plots = VGroup()
        for i, x in enumerate(np.arange(-1.3, 4.8, 0.62)):
            h = 0.9 + 0.35 * ((i * 7) % 3)
            body = Rectangle(width=0.5, height=h, stroke_color=INK, stroke_width=1.5, fill_color=PAPER_DARK,
                             fill_opacity=1).move_to(P(x, 0.2 + h / 2))
            roof = Polygon(P(x - 0.27, 0.2 + h), P(x + 0.27, 0.2 + h), P(x, 0.2 + h + 0.3), stroke_color=INK,
                           stroke_width=1.5, fill_color=SEPIA, fill_opacity=0.6)
            win = Rectangle(width=0.14, height=0.18, stroke_color=INK, stroke_width=1).move_to(P(x, 0.2 + h * 0.6))
            plots.add(VGroup(body, roof, win))
        survey = VGroup(*[DashedLine(P(x - 0.31, 0.12), P(x - 0.31, -0.25), color=RED_INK, stroke_width=1.5)
                          for x in np.arange(-1.3, 5.2, 0.62)])
        survey_l = note("plots measured and pegged out: schematic", 14, RED_INK).move_to([1.7, -0.5, 0])
        line("London, in the years after the Great Fire of 1666. Robert Hooke is helping to rebuild the city as one of "
             "its surveyors.", FadeIn(cam, shift=RIGHT * 0.2), FadeIn(cam_l), FadeIn(place), Create(ground),
             run_time=1.0)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in plots], lag_ratio=0.15), Create(survey),
                  FadeIn(survey_l), run_time=2.4)
        self.vo_wait()
        curator = ink_card(VGroup(serif("Curator of Experiments", 24, INK),
                                  note("Royal Society, from 1662: something new for every meeting", 16)
                                  ).arrange(DOWN, buff=0.1)).move_to([1.7, -1.55, 0])
        line("He is also the Royal Society's curator of experiments, the man who has to show something new at every "
             "meeting.", FadeIn(curator, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()
        q = serif("?", 60, RED_INK).move_to(cam[2].get_center() + RIGHT * 0.05)
        line("No confirmed portrait of him survives, so we know his face only in outline.",
             Indicate(cam_l[1], color=RED_INK, scale_factor=1.08), run_time=1.0)
        self.play(FadeIn(q, scale=1.3), run_time=0.6)
        self.play(FadeOut(q), run_time=0.5)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(place, ground, plots, survey, survey_l, curator)),
                  cam.animate.scale(0.7).move_to([-5.3, 2.0, 0]), cam_l.animate.scale(0.75).move_to([-5.3, 0.65, 0]),
                  run_time=0.9)

        # ================= the puzzle =================
        AC = P(1.0, -1.3)
        Rp, tp = 2.0, 0.42
        arch0 = semicircle_stones(AC, Rp, tp, 11)
        piers0 = VGroup(pier(1.0 - Rp, -1.3 - 0.0, 0.62, 1.0), pier(1.0 + Rp, -1.3, 0.62, 1.0))
        piers0.shift(DOWN * 0.0)
        noglue = note("cut stones · no glue that can hold them in tension", 16).move_to([1.0, 1.55, 0])
        line("Builders around him face an old puzzle. An arch is just a pile of cut stones, with no glue that can hold "
             "them together.", FadeIn(piers0), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in arch0], lag_ratio=0.18), run_time=2.2)
        self.play(FadeIn(noglue), run_time=0.5)
        self.vo_wait()
        qs = VGroup(serif("Why does it stand?", 30, RED_INK), serif("Which shape is best?", 30, RED_INK)
                    ).arrange(DOWN, buff=0.2).move_to([1.0, 2.55, 0])
        compass = VGroup(Line(P(-3.3, 0.9), P(-2.9, -0.2), color=INK, stroke_width=3),
                         Line(P(-3.3, 0.9), P(-3.7, -0.2), color=INK, stroke_width=3),
                         Circle(radius=0.08, color=INK, fill_opacity=1).move_to(P(-3.3, 0.9)))
        thumb = note("circles and rules of thumb", 16).next_to(compass, DOWN, buff=0.15)
        line("So why does it stand? And which shape is best? For centuries, builders had relied on circles and on "
             "rules of thumb.", FadeOut(noglue), FadeIn(qs[0]), run_time=0.8)
        self.play(FadeIn(qs[1]), run_time=0.6)
        self.play(FadeIn(compass), FadeIn(thumb), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(arch0, piers0, qs, compass, thumb)), run_time=0.7)

        # ================= 1671 and the anagram =================
        c1671 = ink_card(VGroup(spaced("Royal Society · 1671", 18, SEPIA),
                                serif("Hooke: I have found the true shape of an arch.", 24, INK),
                                note("(our words) · but he does not say what it is", 15)).arrange(DOWN, buff=0.12)
                         ).move_to([0.6, 1.9, 0])
        line("In 1671, Hooke told the Royal Society that he had solved the true shape of an arch. But he did not say "
             "what it was.", FadeIn(c1671, shift=DOWN * 0.1), run_time=0.9)
        self.vo_wait()
        book = VGroup(spaced("A Description of Helioscopes", 16, SEPIA),
                      note("and some other Instruments · London, 1676", 15)).arrange(DOWN, buff=0.08)
        book.move_to([0.6, 0.55, 0])
        letters = "abcccddeeeeefggiiiiiiiillmmmmnnnnnooprrsssttttttuuuuuuuux"
        src = Text(letters, font_size=28, color=INK, disable_ligatures=True).move_to([0.3, -0.35, 0])
        assert len(src.submobjects) == len(letters)
        src_l = note("the letters as printed: an anagram", 15).move_to([0.6, -0.95, 0])
        line("Instead, at the end of a book on instruments printed in 1676, he hid the answer as a scramble of "
             "letters.", FadeOut(c1671), FadeIn(book), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in src], lag_ratio=0.03), FadeIn(src_l), run_time=2.0)
        self.vo_wait()
        claim = note("publish the letters now · reveal the meaning later · priority kept", 16, RED_INK).move_to(
            [0.6, -1.6, 0])
        key = note("key published after his death (he died in 1703)", 15).move_to([0.6, -2.1, 0])
        line("It was a way to claim an idea without giving it away. The key was published only after his death.",
             FadeIn(claim), run_time=0.8)
        self.play(FadeIn(key), run_time=0.6)
        self.vo_wait()

        # rearrange the letters into the Latin
        l1 = Text("ut pendet continuum flexile,", font_size=34, color=INK, disable_ligatures=True)
        l2 = Text("sic stabit contiguum rigidum inversum", font_size=34, color=INK, disable_ligatures=True)
        latin = VGroup(l1, l2).arrange(DOWN, buff=0.22).move_to([0.6, 0.7, 0])
        t_chars = list("ut pendet continuum flexile,") + list("sic stabit contiguum rigidum inversum")
        t_glyphs = list(l1.submobjects) + list(l2.submobjects)
        assert len(t_glyphs) == len(t_chars), (len(t_glyphs), len(t_chars))
        pool = {}
        for i, ch in enumerate(letters):
            pool.setdefault(ch, []).append(i)
        moves, extra = [], []
        for g, ch in zip(t_glyphs, t_chars):
            if ch == " ":
                continue
            k = "u" if ch == "v" else ch
            if k in pool and pool[k]:
                i = pool[k].pop(0)
                moves.append(Transform(src[i], g))
            else:
                extra.append(FadeIn(g))
        eng = VGroup(serif("“As hangs the flexible line, so, upside down,", 28, RED_INK, italic=True),
                     serif("will stand the rigid arch.”", 28, RED_INK, italic=True)).arrange(DOWN, buff=0.12)
        eng.move_to([0.6, -1.15, 0])
        line("Unscrambled, it is Latin. As hangs the flexible line, so, upside down, will stand the rigid arch.",
             FadeOut(VGroup(book, src_l, claim, key)), run_time=0.6)
        self.play(*moves, *extra, run_time=2.2)
        self.play(FadeIn(eng, shift=UP * 0.1), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(src, *[g for g in t_glyphs], eng)), FadeOut(cam), FadeOut(cam_l), run_time=0.8)

        # ================= the hanging chain =================
        a_c, L_c = 1.6, 2.6
        xs, ys = catenary_pts(a_c, L_c)
        sag = ys[-1]
        O = P(-1.2, 2.55 - sag)         # lowest point of the chain; pins at y = 2.55
        beam = Line(P(-4.4, 2.75), P(2.0, 2.75), color=INK, stroke_width=3)
        hatch = VGroup(*[Line(P(x, 2.75), P(x + 0.18, 2.95), color=INK, stroke_width=1.2)
                         for x in np.arange(-4.4, 2.0, 0.22)])
        pins = VGroup(*[Dot(O + P(sx * L_c, sag), radius=0.07, color=INK) for sx in (-1, 1)])
        rods = VGroup(*[Line(O + P(sx * L_c, sag), P(-1.2 + sx * L_c, 2.75), color=INK, stroke_width=2)
                        for sx in (-1, 1)])
        links = chain_links(xs, ys, O)
        line("Let's see why. Hang a chain between two pins.", FadeIn(beam), FadeIn(hatch), FadeIn(pins), FadeIn(rods),
             run_time=0.7)
        self.play(LaggedStart(*[FadeIn(k) for k in links], lag_ratio=0.02), run_time=1.6)
        self.vo_wait()

        # it can only pull: tension arrows along the curve
        def tangent_at(x):
            sl = np.sinh(x / a_c)
            v = np.array([1.0, sl, 0])
            return v / np.linalg.norm(v)

        def ypos(x):
            return a_c * np.cosh(x / a_c) - a_c

        pulls = VGroup()
        for x in (-2.0, -1.0, 0.6, 1.7):
            p = O + P(x, ypos(x))
            tv = tangent_at(x)
            pulls.add(Arrow(p - tv * 0.05, p + tv * 0.6, buff=0, color=RED_INK, stroke_width=4,
                            max_tip_length_to_length_ratio=0.3),
                      Arrow(p + tv * 0.05, p - tv * 0.6, buff=0, color=RED_INK, stroke_width=4,
                            max_tip_length_to_length_ratio=0.3))
        pull_l = VGroup(serif("tension only", 24, RED_INK), note("pulls along its own length", 16)).arrange(
            DOWN, buff=0.08).move_to([4.6, 1.3, 0])
        line("A chain cannot push, and it cannot resist bending. All it can do is pull, along its own length.",
             run_time=0.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in pulls], lag_ratio=0.1), FadeIn(pull_l), run_time=1.4)
        self.vo_wait()
        self.play(FadeOut(pulls), FadeOut(pull_l), run_time=0.5)

        # free body of a piece of chain: from x1 to x2
        x1, x2 = 0.35, 1.85
        seg_x = np.linspace(x1, x2, 40)
        piece = curve(seg_x, ypos(seg_x), O, color=RED_INK, width=7)
        g = O + P((x1 + x2) / 2, ypos((x1 + x2) / 2))
        wlen = 0.9 * (a_c * (np.sinh(x2 / a_c) - np.sinh(x1 / a_c)))  # weight ~ arc length
        T1 = -tangent_at(x1) * np.cosh(x1 / a_c)
        T2 = tangent_at(x2) * np.cosh(x2 / a_c)
        k = 0.9
        p1, p2 = O + P(x1, ypos(x1)), O + P(x2, ypos(x2))
        fW = Arrow(g, g + DOWN * wlen, buff=0, color=INK, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        fT1 = Arrow(p1, p1 + T1 * k, buff=0, color=BLUE_INK, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        fT2 = Arrow(p2, p2 + T2 * k, buff=0, color=BLUE_INK, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        fW_l = serif("weight", 20, INK).next_to(fW.get_end(), RIGHT, buff=0.12)
        fT_l = serif("pull", 20, BLUE_INK).next_to(fT2.get_end(), RIGHT, buff=0.1)
        fT1_l = serif("pull", 20, BLUE_INK).next_to(fT1.get_end(), DOWN, buff=0.1)
        # force triangle (closed): T1 + T2 + W = 0
        TO = P(3.9, 1.3)
        tri_T2 = Arrow(TO, TO + T2 * k, buff=0, color=BLUE_INK, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        tri_W = Arrow(TO + T2 * k, TO + T2 * k + DOWN * wlen, buff=0, color=INK, stroke_width=4,
                      max_tip_length_to_length_ratio=0.15)
        tri_T1 = Arrow(TO + T2 * k + DOWN * wlen, TO, buff=0, color=BLUE_INK, stroke_width=4,
                       max_tip_length_to_length_ratio=0.15)
        tri_l = VGroup(note("the three forces close", 15), note("a triangle: they balance", 15)).arrange(
            DOWN, buff=0.05).move_to([4.6, -0.95, 0])
        line("Cut out any piece of it. Its weight pulls down. The chain on either side pulls along the curve. Those "
             "three forces must balance.", Create(piece), run_time=0.8)
        self.play(GrowArrow(fW), FadeIn(fW_l), run_time=0.7)
        self.play(GrowArrow(fT1), GrowArrow(fT2), FadeIn(fT_l), FadeIn(fT1_l), run_time=0.8)
        self.play(TransformFromCopy(fT2, tri_T2), TransformFromCopy(fW, tri_W), TransformFromCopy(fT1, tri_T1),
                  run_time=1.2)
        self.play(FadeIn(tri_l), run_time=0.5)
        self.vo_wait()
        self.play(FadeOut(VGroup(piece, fW, fT1, fT2, fW_l, fT_l, fT1_l, tri_T2, tri_W, tri_T1, tri_l)), run_time=0.6)

        # H constant, V grows: decomposition at several points
        H_len = 0.55
        comps = VGroup()
        for x in (0.0, 0.7, 1.4, 2.1):
            p = O + P(x, ypos(x))
            V = H_len * np.sinh(x / a_c)
            hA = Arrow(p, p + RIGHT * H_len, buff=0, color=BLUE_INK, stroke_width=4, max_tip_length_to_length_ratio=0.3)
            grp = VGroup(hA)
            if V > 0.05:
                grp.add(Arrow(p, p + UP * V, buff=0, color=RED_INK, stroke_width=4,
                              max_tip_length_to_length_ratio=min(0.3, 0.12 / V)))
            comps.add(grp)
        key2 = VGroup(VGroup(Arrow(LEFT * 0.25, RIGHT * 0.25, buff=0, color=BLUE_INK, stroke_width=4),
                             note("sideways pull: the same everywhere", 16, BLUE_INK)).arrange(RIGHT, buff=0.15),
                      VGroup(Arrow(DOWN * 0.25, UP * 0.25, buff=0, color=RED_INK, stroke_width=4),
                             note("upward pull: carries the weight below", 16, RED_INK)).arrange(RIGHT, buff=0.15)
                      ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([4.4, 0.9, 0])
        line("The sideways part of the pull is the same all along the chain. Only the upward part grows, as more "
             "weight hangs below.", FadeIn(key2), run_time=0.8)
        self.play(LaggedStart(*[GrowFromPoint(c, c[0].get_start()) for c in comps], lag_ratio=0.35), run_time=2.2)
        self.vo_wait()
        flat = note("flat at the bottom", 16).move_to(O + P(0, -0.35))
        steep = note("steep near the pins", 16).move_to(O + P(-L_c - 1.15, sag * 0.7))
        line("That is why the chain is flat at the bottom and steep near the pins.", FadeIn(flat), FadeIn(steep),
             run_time=0.8)
        self.vo_wait()
        self.play(FadeOut(VGroup(comps, key2, flat, steep)), run_time=0.5)

        # ================= flip it =================
        # mirror about the line through the pins: a hanging chain becomes an arch standing on the same feet
        y_pins = 2.55
        base_y = -2.15
        Of = P(-1.2, base_y + sag)      # crown of the arch
        arch_curve = curve(xs, ys, Of, sy=-1.0, color=CHAIN, width=3)
        links_up = chain_links(xs, ys, Of, sy=-1.0)
        ground2 = Line(P(-4.6, base_y), P(2.2, base_y), color=INK, stroke_width=2.5)
        line("Now turn it upside down. Every pull becomes a push.", FadeOut(beam), FadeOut(hatch), FadeOut(rods),
             FadeOut(pins), run_time=0.6)
        self.play(Transform(links, links_up), Create(ground2), run_time=1.8)
        pushes = VGroup()
        for x in (-2.0, -1.0, 0.6, 1.7):
            p = Of + P(x, -ypos(x))
            tv = tangent_at(x) * np.array([1, -1, 0])
            pushes.add(Arrow(p + tv * 0.65, p + tv * 0.08, buff=0, color=RED_INK, stroke_width=4,
                             max_tip_length_to_length_ratio=0.3),
                       Arrow(p - tv * 0.65, p - tv * 0.08, buff=0, color=RED_INK, stroke_width=4,
                             max_tip_length_to_length_ratio=0.3))
        push_l = VGroup(serif("compression only", 24, RED_INK), note("every force pushes along the curve", 16)
                        ).arrange(DOWN, buff=0.08).move_to([4.6, 1.3, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in pushes], lag_ratio=0.1), FadeIn(push_l), run_time=1.2)
        self.vo_wait()
        pts_up = np.array([Of + P(x, -y) for x, y in zip(xs, ys)])
        stones = stones_along(pts_up, 0.42, 15)
        line("Build stones along that curve, and each one is only squeezed, straight along the arch. Nothing tries to "
             "pull the joints apart.", FadeOut(pushes), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in stones], lag_ratio=0.12), run_time=2.2)
        self.play(links.animate.set_opacity(0.0), run_time=0.5)
        self.remove(links)
        joint_arrows = VGroup()
        for x in np.linspace(-2.2, 2.2, 7):
            p = Of + P(x, -ypos(x))
            tv = tangent_at(x) * np.array([1, -1, 0])
            joint_arrows.add(VGroup(
                Arrow(p - tv * 0.34, p - tv * 0.04, buff=0, color=RED_INK, stroke_width=3,
                      max_tip_length_to_length_ratio=0.4),
                Arrow(p + tv * 0.34, p + tv * 0.04, buff=0, color=RED_INK, stroke_width=3,
                      max_tip_length_to_length_ratio=0.4)).set_z_index(3))
        self.play(LaggedStart(*[FadeIn(j) for j in joint_arrows], lag_ratio=0.1), run_time=1.0)
        self.vo_wait()
        strong = ink_card(VGroup(serif("stone: strong when squeezed", 22, INK),
                                 note("weak when pulled · and the joints cannot pull at all", 15)).arrange(DOWN, buff=0.08)
                          ).move_to([4.15, -0.6, 0])
        line("Stone is very strong when squeezed. That is the arch it wants to be.", FadeIn(strong, shift=UP * 0.1),
             run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(stones, joint_arrows, ground2, push_l, strong)), run_time=0.7)

        # ================= what curve? =================
        ax_o = P(-2.4, -2.35)
        cxs, cys = catenary_pts(0.9, 2.2)
        S = 4.4 / cys[-1]
        Lp, sagp = 2.2, cys[-1]
        axis = VGroup(Line(ax_o + P(-Lp * S - 0.3, 0), ax_o + P(Lp * S + 0.3, 0), color=FADED, stroke_width=1.5),
                      Line(ax_o, ax_o + P(0, sagp * S + 0.2), color=FADED, stroke_width=1.5))
        cat_m = curve(cxs * S, cys * S, ax_o, color=INK, width=4)
        par_y = sagp * (cxs / Lp) ** 2
        par_m = DashedVMobject(curve(cxs * S, par_y * S, ax_o, color=BLUE_INK, width=3), num_dashes=70)
        par_l = VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=BLUE_INK, stroke_width=3),
                       note("parabola: Galileo's 'roughly'", 16, BLUE_INK)).arrange(RIGHT, buff=0.15)
        cat_l = VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=INK, stroke_width=4),
                       note("hanging chain", 16, INK)).arrange(RIGHT, buff=0.15)
        legend = VGroup(cat_l, par_l).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([-2.4, 2.85, 0])
        same = note("same span, same sag", 14).move_to(ax_o + P(0, -0.35))
        line("What is this curve? Galileo had called a hanging chain roughly a parabola. It is close, but not the "
             "same.", FadeIn(axis), Create(cat_m), FadeIn(legend[0]), run_time=1.2)
        self.play(Create(par_m), FadeIn(legend[1]), FadeIn(same), run_time=1.4)
        self.vo_wait()
        names = VGroup(spaced("1691", 20, SEPIA), serif("Leibniz · Huygens · Johann Bernoulli", 24, INK)
                       ).arrange(DOWN, buff=0.12).move_to([3.3, 2.5, 0])
        eq = MathTex(r"y = a\cosh\!\left(\frac{x}{a}\right)", font_size=50, color=INK).move_to([3.3, 1.2, 0])
        eq_a = MathTex(r"a = \frac{\text{sideways pull}}{\text{weight per length}}", font_size=34, color=FADED
                       ).next_to(eq, DOWN, buff=0.3)
        catn = VGroup(serif("the catenary", 30, RED_INK), note("from catena, Latin for chain", 16)).arrange(
            DOWN, buff=0.08).next_to(eq_a, DOWN, buff=0.35)
        line("In 1691, Leibniz, Huygens and Johann Bernoulli found the exact answer. We now call it the catenary, from "
             "the Latin for chain.", FadeIn(names), run_time=0.8)
        self.play(Write(eq), run_time=1.2)
        self.play(FadeIn(eq_a), run_time=0.7)
        self.play(FadeIn(catn, shift=UP * 0.1), run_time=0.7)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(axis, cat_m, par_m, legend, same, names, eq, eq_a, catn)), run_time=0.7)

        # ================= circles and the line of thrust =================
        R_s = 1.85                       # scene radius of the arch centre line
        C1 = P(-3.25, -2.0)
        C2 = P(3.25, -2.0)
        t_thick, t_thin = 0.24, 0.05     # thickness / radius
        m1, H1, y1 = best_thrust(1.0, t_thick)
        m2, H2, y2 = best_thrust(1.0, t_thin)
        arch_a = semicircle_stones(C1, R_s, t_thick * R_s, 13)
        arch_b = semicircle_stones(C2, R_s, t_thin * R_s, 17, gap=0.02)
        base_a = Line(C1 + P(-2.6, 0), C1 + P(2.6, 0), color=INK, stroke_width=2.5)
        base_b = Line(C2 + P(-2.6, 0), C2 + P(2.6, 0), color=INK, stroke_width=2.5)
        q2 = serif("Real arches are often circles. How do they stand?", 26, INK).move_to([0, 2.95, 0])
        line("But real arches are often circles, and many have stood for centuries. How?", FadeIn(q2),
             FadeIn(base_a), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in arch_a], lag_ratio=0.1), run_time=1.6)
        self.vo_wait()
        greg = ink_card(VGroup(spaced("David Gregory · 1697", 16, SEPIA),
                               serif("An arch of another shape stands", 22, INK),
                               serif("if a hanging-chain line fits inside its thickness.", 22, INK),
                               note("(paraphrase)", 14)).arrange(DOWN, buff=0.08)).move_to([3.3, 0.6, 0])
        line("In 1697, David Gregory gave the answer. An arch of any other shape stands if a hanging-chain line can fit "
             "inside its thickness.", FadeOut(q2), FadeIn(greg, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()

        def thrust_mob(C, t, H, y0, color=RED_INK):
            pts = full_thrust(1.0, t, H, y0) * R_s
            m = VMobject(stroke_color=color, stroke_width=4).set_points_as_corners([C + P(p[0], p[1]) for p in pts])
            return m.set_z_index(4)

        th_a = thrust_mob(C1, t_thick, H1, y1)
        ok = stamp(r"\text{stands}", color=SEPIA, size=34).move_to(C1 + P(0, 2.75))
        th_l = note("line of thrust · computed for the stones' own weight", 15, RED_INK).move_to(C1 + P(0, -0.35))
        line("Engineers call that path the line of thrust. Here it is for a thick semicircle, from the stones' own "
             "weight. It stays inside. The arch stands.", FadeOut(greg), run_time=0.6)
        self.play(Create(th_a), FadeIn(th_l), run_time=2.2)
        self.play(FadeIn(ok, scale=1.2), run_time=0.6)
        self.vo_wait()

        # thin arch: the best line still escapes
        th_b = thrust_mob(C2, t_thin, H2, y2)
        pts_b = full_thrust(1.0, t_thin, H2, y2)
        rr = np.hypot(pts_b[:, 0], pts_b[:, 1])
        out_idx = np.where(np.abs(rr - 1.0) > t_thin / 2 * 1.02)[0]
        # pick the deepest escape in each run: those are the hinges
        hinges = []
        if len(out_idx):
            runs = np.split(out_idx, np.where(np.diff(out_idx) > 1)[0] + 1)
            for r_ in runs:
                j = r_[np.argmax(np.abs(rr[r_] - 1.0))]
                hinges.append(pts_b[j])
        hinge_dots = VGroup(*[Circle(radius=0.13, color=RED_INK, stroke_width=3).move_to(C2 + P(*(h * R_s)))
                              .set_z_index(5) for h in hinges])
        thin_l = note("thin arch: even the best line escapes", 15, RED_INK).move_to(C2 + P(0, -0.35))
        line("Make the same arch thin, and the line has to leave the stones. Where it escapes, the joints open like "
             "hinges.", FadeIn(base_b), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in arch_b], lag_ratio=0.06), run_time=1.4)
        self.play(Create(th_b), FadeIn(thin_l), run_time=1.8)
        self.play(LaggedStart(*[Create(h) for h in hinge_dots], lag_ratio=0.2), run_time=1.0)
        self.vo_wait()

        # schematic collapse: crown drops, haunches kick outwards
        n_b = len(arch_b)
        left_b = VGroup(*arch_b[: n_b // 3])
        midl = VGroup(*arch_b[n_b // 3: n_b // 2])
        midr = VGroup(*arch_b[n_b // 2: n_b - n_b // 3])
        right_b = VGroup(*arch_b[n_b - n_b // 3:])
        fall_l = note("collapse drawn schematically", 14).move_to(C2 + P(0, 2.75))
        line("With enough hinges, the arch folds, and falls.", th_b.animate.set_opacity(0),
             hinge_dots.animate.set_opacity(0), run_time=0.5)
        self.play(midl.animate.shift(DOWN * 0.9 + RIGHT * 0.15).rotate(-25 * DEGREES),
                  midr.animate.shift(DOWN * 0.9 + LEFT * 0.15).rotate(25 * DEGREES),
                  left_b.animate.rotate(-14 * DEGREES, about_point=C2 + P(-R_s - 0.05, 0)),
                  right_b.animate.rotate(14 * DEGREES, about_point=C2 + P(R_s + 0.05, 0)),
                  FadeIn(fall_l), run_time=1.0, rate_func=rush_into)
        self.play(midl.animate.shift(DOWN * 0.75).rotate(-20 * DEGREES), midr.animate.shift(DOWN * 0.75).rotate(20 * DEGREES),
                  left_b.animate.rotate(-20 * DEGREES, about_point=C2 + P(-R_s - 0.05, 0)),
                  right_b.animate.rotate(20 * DEGREES, about_point=C2 + P(R_s + 0.05, 0)),
                  run_time=0.6, rate_func=rush_into)
        self.vo_wait()
        self.remove(th_b, hinge_dots)
        self.play(clear(), FadeOut(VGroup(arch_a, base_a, th_a, ok, th_l, arch_b, base_b, thin_l, fall_l)),
                  run_time=0.7)

        # ================= legacy =================
        # Poleni: dome profile with a hanging chain drawn inside it (schematic)
        D = P(-4.3, -1.6)
        dome_o = Arc(radius=1.55, start_angle=0, angle=PI, arc_center=D, color=INK, stroke_width=3)
        dome_i = Arc(radius=1.18, start_angle=0, angle=PI, arc_center=D, color=INK, stroke_width=2)
        dome = VGroup(dome_o, dome_i, Line(D + P(-1.75, 0), D + P(1.75, 0), color=INK, stroke_width=2))
        lantern = Rectangle(width=0.3, height=0.45, stroke_color=INK, stroke_width=2).move_to(D + P(0, 1.77))
        dx, dy = catenary_pts(0.8663, 1.40, 80)
        dome_line = curve(dx, -dy, D + P(0, dy[-1]), color=RED_INK, width=3)
        pol = VGroup(spaced("1748 · Rome", 16, SEPIA), serif("Giovanni Poleni", 22, INK),
                     note("Saint Peter's dome: does a chain line fit? (schematic)", 14)).arrange(DOWN, buff=0.06)
        pol.move_to(D + P(0, -0.65))
        line("This idea never went away. In 1748, Giovanni Poleni used a hanging chain to check the cracked dome of "
             "Saint Peter's in Rome.", FadeIn(dome), FadeIn(lantern), FadeIn(pol), run_time=0.9)
        self.play(Create(dome_line), run_time=1.2)
        self.vo_wait()
        # Gaudí: hanging strings with weights, and the arches they become
        G = P(0.0, 2.2)
        g_bar = VGroup(Line(G + P(-1.7, 0), G + P(1.7, 0), color=INK, stroke_width=3),
                       *[Line(G + P(x_, 0), G + P(x_ + 0.15, 0.17), color=INK, stroke_width=1.2)
                         for x_ in np.arange(-1.7, 1.7, 0.2)])
        # a string loaded by small weights hangs as a polygon of straight pieces (a funicular)
        wx = np.array([-0.9, -0.3, 0.3, 0.9])
        Hs, wgt = 1.0, 0.55
        V = 2 * wgt                     # vertical pull at the left pin carries all four weights / 2 each side
        xs_ = [-1.5] + list(wx) + [1.5]
        y = 0.0
        knots = [G + P(-1.5, 0)]
        for i in range(1, len(xs_)):
            y -= (xs_[i] - xs_[i - 1]) * V / Hs
            knots.append(G + P(xs_[i], y))
            if i <= len(wx):
                V -= wgt
        strings = VGroup(VMobject(stroke_color=SEPIA, stroke_width=2.5).set_points_as_corners(knots))
        bags = VGroup()
        for k_ in knots[1:-1]:
            bags.add(Line(k_, k_ + DOWN * 0.3, color=SEPIA, stroke_width=1.5),
                     Circle(radius=0.08, stroke_color=INK, stroke_width=1.5, fill_color=SEPIA,
                            fill_opacity=1).move_to(k_ + DOWN * 0.38))
        flipped = VMobject(stroke_color=RED_INK, stroke_width=2.5).set_points_as_corners(
            [P(k_[0], -2.0 + (G[1] - k_[1])) for k_ in knots])
        g_lab = VGroup(spaced("Barcelona", 16, SEPIA), serif("Antoni Gaudí", 22, INK),
                       note("hanging models of strings and weights", 14)).arrange(DOWN, buff=0.06).move_to(
            P(0.0, -0.35))
        flip_note = note("turned over: an arch", 14, RED_INK).move_to(P(0.0, -2.3))
        line("Antoni Gaudí designed churches upside down, with models made from strings and little weights.",
             FadeIn(g_bar), FadeIn(g_lab), run_time=0.7)
        self.play(LaggedStart(*[Create(s_) for s_ in strings], lag_ratio=0.2), FadeIn(bags), run_time=1.3)
        self.play(Create(flipped), FadeIn(flip_note), run_time=0.8)
        self.vo_wait()
        # bridge check
        B = P(4.3, -1.7)
        br = semicircle_stones(B + P(0, 0), 1.25, 0.3, 11)
        deck = VGroup(Rectangle(width=3.4, height=0.3, stroke_color=STONE_EDGE, stroke_width=1.5, fill_color=STONE,
                                fill_opacity=1).move_to(B + P(0, 1.55)),
                      *[Rectangle(width=0.3, height=1.4, stroke_color=STONE_EDGE, stroke_width=1.5, fill_color=STONE,
                                  fill_opacity=1).move_to(B + P(sx_ * 1.55, 0.7)) for sx_ in (-1, 1)])
        br_line = VMobject(stroke_color=RED_INK, stroke_width=3).set_points_as_corners(
            [B + P(p[0], p[1]) for p in full_thrust(1.0, 0.24, H1, y1) * 1.25]).set_z_index(4)
        br_l = VGroup(spaced("today", 16, SEPIA), serif("checking old bridges", 22, INK),
                      note("does a line of thrust fit inside?", 14)).arrange(DOWN, buff=0.06).move_to(P(4.3, -2.35))
        line("And engineers still check old bridges by asking whether a line of thrust can fit inside the stone.",
             FadeIn(br), FadeIn(deck), FadeIn(br_l), run_time=0.8)
        self.play(Create(br_line), run_time=1.2)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(dome, lantern, dome_line, pol, g_bar, strings, bags, g_lab, flip_note, flipped, br,
                                          deck, br_line, br_l)), run_time=0.7)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 22, RED_INK).move_to([0, 3.2, 0])
        board = Rectangle(width=4.0, height=3.0, stroke_color=INK, stroke_width=2, fill_color=WHITE,
                          fill_opacity=0.75).move_to([-3.7, 0.9, 0])
        tx, ty = catenary_pts(0.95, 1.45, 100)
        TB = P(-3.7, 2.0 - ty[-1])
        tacks = VGroup(*[Dot(TB + P(s_ * 1.45, ty[-1]), radius=0.06, color=RED_INK) for s_ in (-1, 1)])
        t_chain = chain_links(tx, ty, TB, spacing=0.11)
        t_trace = DashedVMobject(curve(tx, ty, TB, color=BLUE_INK, width=2.5), num_dashes=40)
        s1_l = note("1 · hang a light chain on card, trace it", 16).next_to(board, DOWN, buff=0.15)
        line("Try it yourself. Hang a light chain against a sheet of card, and trace its curve.", FadeIn(tiy),
             FadeIn(board), FadeIn(tacks), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(k_) for k_ in t_chain], lag_ratio=0.02), FadeIn(s1_l), run_time=1.2)
        self.play(Create(t_trace), run_time=1.0)
        self.vo_wait()
        # step 2: cut and flip into a former
        FB = P(2.6, -1.25)
        fx, fy = tx, -ty + ty[-1]
        former_pts = [FB + P(x, y) for x, y in zip(fx, fy)] + [FB + P(1.45, 0), FB + P(-1.45, 0)]
        former = Polygon(*former_pts, stroke_color=BLUE_INK, stroke_width=2, fill_color="#d8cfb8", fill_opacity=1)
        table = Line(FB + P(-2.6, 0), FB + P(2.6, 0), color=INK, stroke_width=2.5)
        s2_l = note("2 · cut along the curve, flip it: a temporary support", 16).move_to(FB + P(0, -0.35))
        line("Cut the card along the curve and flip it over, to make a temporary support.",
             FadeOut(t_chain), FadeOut(tacks), run_time=0.6)
        self.play(Create(table), FadeIn(s2_l), run_time=0.6)
        self.play(FadeIn(former, shift=DOWN * 0.3), run_time=0.9)
        self.vo_wait()
        # step 3: sugar cubes
        cube_pts = np.array([FB + P(x, y) for x, y in zip(fx, fy)])
        nrm_shift = 0.17
        cubes = stones_along(cube_pts, 0.3, 13, gap=0.03, fill=SUGAR)
        # move the cubes out so they sit on top of the former (offset by half their thickness along the normal)
        for b_ in cubes:
            c_ = b_.get_center()
            d_ = c_ - (FB + P(0, fy.max() * 0.0))
            b_.shift(normalize(c_ - (FB + P(0, -0.2))) * nrm_shift)
        icing = note("3 · sugar cubes, a dab of icing in each joint", 16).move_to(FB + P(0, -0.35))
        line("Stack sugar cubes along it, with a dab of icing in each joint. When it has set, slide the card out.",
             FadeOut(s2_l), FadeIn(icing), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(b_, shift=DOWN * 0.15) for b_ in cubes], lag_ratio=0.12), run_time=2.0)
        self.wait(0.6)
        self.play(former.animate.shift(RIGHT * 3.4).set_opacity(0), run_time=1.2)
        self.remove(former)
        self.vo_wait()
        top = cubes[len(cubes) // 2].get_top()
        finger = Arrow(top + UP * 0.9, top + UP * 0.05, buff=0, color=RED_INK, stroke_width=5,
                       max_tip_length_to_length_ratio=0.25)
        stands = note("4 · it stands on its own · press gently on the top", 16).move_to(FB + P(0, -0.35))
        line("Your arch stands with no support. Press gently on the top, and feel it push back.", FadeOut(icing),
             FadeIn(stands), GrowArrow(finger), run_time=0.8)
        self.play(cubes.animate.shift(DOWN * 0.02), run_time=0.3)
        self.play(cubes.animate.shift(UP * 0.02), run_time=0.3)
        self.vo_wait()
        semi = DashedVMobject(Arc(radius=1.45, start_angle=0, angle=PI, color=BLUE_INK, stroke_width=2.5)
                              .move_to(board.get_center() + P(0, -0.55)), num_dashes=36)
        cmp_l = note("5 · now a semicircle, same width: press and compare", 16).move_to(s1_l)
        line("Then build a semicircle of the same width, press on it the same way, and compare.",
             FadeOut(t_trace), FadeOut(s1_l), FadeIn(semi), FadeIn(cmp_l), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tiy, board, semi, cmp_l, table, cubes, finger, stands)), run_time=0.8)

        # ================= close =================
        last = VGroup(serif("Hooke hid his answer in a scramble of letters.", 34, INK),
                      serif("You can find it again with a piece of string.", 34, RED_INK)).arrange(DOWN, buff=0.25)
        last.move_to([0, 0.9, 0])
        cx2, cy2 = catenary_pts(0.9, 1.6, 120)
        string = curve(cx2, cy2, P(0, -1.9 - 0.0), color=SEPIA, width=3)
        string_up = curve(cx2, -cy2 + cy2[-1], P(0, -2.25), color=INK, width=3)
        line("Hooke hid his answer in a scramble of letters. You can find it again with a piece of string.",
             FadeIn(last, lag_ratio=0.2), Create(string), run_time=1.2)
        self.play(Transform(string, string_up), run_time=1.4)
        self.vo_wait()
        self.play(clear(), FadeOut(last), FadeOut(string), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after J. E. Gordon, Structures: Or Why Things Don't Fall Down (1978) · sources in the "
                          "episode notes", 17),
                     note("facts checked against Hooke's Helioscopes (1676), Wikipedia, the BSHM, Hutton's Dictionary "
                          "and New World Encyclopedia, among others", 17),
                     note("silhouette is stylised, not a likeness · thrust lines computed for self-weight; collapse, "
                          "street and models schematic · Manim · synthetic narration", 15)
                     ).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        for m in end:
            if m.width > 12.8:
                m.scale_to_fit_width(12.8)
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(3.0)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)

