"""I032 Archimedes Traps Pi, a Science Stories episode.

After W. Dunham, Journey Through Genius (1990). Script and sources: episodes/I032_script.md

Render:  manim -qh --frame_rate 30 episodes/I032_archimedes_pi.py ArchimedesTrapsPi
Then:    scripts/finish_video.sh media/videos/I032_archimedes_pi/1080p30/ArchimedesTrapsPi.mp4 out/I032_archimedes_pi.mp4
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

MONO = "DejaVu Sans Mono"


def note(text, size=17, color=FADED):
    return serif(text, size, color, italic=True)


def P(x, y):
    return np.array([x, y, 0.0])


def mono(text, size=20, color=INK):
    return Text(text, font=MONO, font_size=size, color=color)


# ---------- the mathematics, computed exactly (checked at render time) ----------
def inside(n):          # perimeter of the inscribed n-gon, in diameters
    return n * math.sin(math.pi / n)


def outside(n):         # perimeter of the circumscribed n-gon, in diameters
    return n * math.tan(math.pi / n)


def doubling_table(steps):
    """Archimedes' doubling done the spreadsheet way: harmonic mean, then geometric mean."""
    a, b, n = 2 * math.sqrt(3), 3.0, 6
    rows = [(n, b, a)]
    for _ in range(steps):
        a = 2 * a * b / (a + b)
        b = math.sqrt(a * b)
        n *= 2
        rows.append((n, b, a))
    return rows


SIDES = [6, 12, 24, 48, 96]
for _n, _b, _a in doubling_table(4):
    assert abs(_b - inside(_n)) < 1e-12 and abs(_a - outside(_n)) < 1e-12
assert 223 / 71 < inside(96) < math.pi < outside(96) < 22 / 7
assert 265 / 153 < math.sqrt(3) < 1351 / 780
assert 6336 / 2017.25 > 223 / 71 and 14688 / 4673.5 < 22 / 7
_long = doubling_table(20)[-1]
assert abs(_long[1] - math.pi) < 5e-11 and abs(_long[2] - math.pi) < 5e-11


def polygon(n, R, center, outer=False, color=BLUE_INK, width=3):
    rr = R / math.cos(math.pi / n) if outer else R
    off = math.pi / n if outer else 0.0      # outer polygon: edges touch the circle at angle 0
    pts = [center + rr * np.array([math.cos(off + 2 * math.pi * k / n + math.pi / 2),
                                    math.sin(off + 2 * math.pi * k / n + math.pi / 2), 0])
           for k in range(n)]
    return Polygon(*pts, color=color, stroke_width=width)


def polys(n, R, center):
    w = 3 if n <= 12 else 2.2
    return (polygon(n, R, center, outer=False, color=BLUE_INK, width=w),
            polygon(n, R, center, outer=True, color=RED_INK, width=w))


class ArchimedesTrapsPi(NarratedScene):
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
        title = serif("Archimedes Traps Pi", 54).next_to(orn1, DOWN, buff=0.35)
        sub = serif("How to pin down a number you can never measure", 26, FADED, italic=True).next_to(
            title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("after W. Dunham, Journey Through Genius (1990)", 16).move_to([0, -2.6, 0])
        self.vo("Science Stories. Archimedes traps pi.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.wait(0.6)
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= the person and the puzzle =================
        arch = cameo("beard", 0.85).move_to(P(-4.4, 0.7))
        arch_l = VGroup(serif("Archimedes", 22, INK), note("c. 287 – 212 BCE", 15)).arrange(DOWN, buff=0.05)
        arch_l.next_to(arch, DOWN, buff=0.15)
        place = spaced("Syracuse · Sicily · 3rd century BCE", 17, SEPIA).move_to(P(1.6, 3.0))
        sil_n = note("silhouette stylised, not a likeness", 13).next_to(arch_l, DOWN, buff=0.1)
        C0 = P(1.6, 0.5)
        R0 = 1.6
        circ = Circle(radius=R0, color=INK, stroke_width=4).move_to(C0)
        centre = Dot(C0, radius=0.05, color=SEPIA)
        arm = Line(C0, C0 + RIGHT * R0, color=SEPIA, stroke_width=2)
        line("Syracuse, Sicily, in the third century BCE. Archimedes puzzles over a question that sounds almost "
             "childish.", FadeIn(arch), FadeIn(arch_l), FadeIn(place), FadeIn(sil_n), run_time=1.0)
        self.play(FadeIn(centre), Create(arm), run_time=0.6)
        self.play(Create(circ), Rotate(arm, 2 * PI, about_point=C0), run_time=2.6)
        self.play(FadeOut(arm), run_time=0.4)
        self.vo_wait()
        q = serif("How far is it around a circle?", 32, INK).move_to(P(1.6, -1.75))
        travel = Dot(C0 + RIGHT * R0, radius=0.08, color=RED_INK)
        line("How far is it around a circle?", FadeIn(q, shift=UP * 0.1), FadeIn(travel), run_time=0.6)
        self.play(MoveAlongPath(travel, circ), run_time=1.6)
        self.play(FadeOut(travel), run_time=0.3)
        self.vo_wait()

        diam = Line(C0 + LEFT * R0, C0 + RIGHT * R0, color=SEPIA, stroke_width=3)
        diam_l = note("width (diameter)", 16, SEPIA).next_to(diam, UP, buff=0.08)
        ratio = MathTex(r"\frac{\text{distance around}}{\text{width}} \approx 3.14\ldots", font_size=34,
                        color=INK).move_to(P(1.6, -1.75))
        line("Every circle goes around a little more than three times its width. That ratio is the number we now "
             "call pi.", Create(diam), FadeIn(diam_l), FadeOut(q), run_time=1.0)
        small = VGroup(Circle(radius=0.45, color=FADED, stroke_width=2),
                       Line(LEFT * 0.45, RIGHT * 0.45, color=SEPIA, stroke_width=1.5)).move_to(P(4.6, 2.1))
        self.play(FadeIn(small), run_time=0.6)
        self.play(FadeIn(ratio, shift=UP * 0.1), run_time=0.9)
        pi_now = note("the Greek letter π for it came much later", 14).next_to(ratio, DOWN, buff=0.1)
        self.play(FadeIn(pi_now), run_time=0.6)
        self.vo_wait()

        ruler = VGroup(Rectangle(width=3.6, height=0.32, fill_color="#d9c296", fill_opacity=1, stroke_color=INK,
                                 stroke_width=1.5))
        for i in range(19):
            h = 0.16 if i % 2 == 0 else 0.09
            x = -1.7 + i * 0.19
            ruler.add(Line(P(x, 0.16), P(x, 0.16 - h), color=INK, stroke_width=1))
        ruler.move_to(C0 + UP * (R0 + 0.16))
        touch = Dot(C0 + UP * R0, radius=0.06, color=RED_INK)
        line("But the edge of a circle is curved, and a ruler is straight. You cannot lay a straight ruler along a "
             "curve.", FadeOut(VGroup(ratio, pi_now, small, centre)), FadeIn(ruler, shift=DOWN * 0.3), run_time=1.0)
        self.play(FadeIn(touch, scale=2), run_time=0.5)
        self.play(Rotate(ruler, 18 * DEGREES, about_point=touch.get_center()), run_time=0.8)
        self.play(Rotate(ruler, -36 * DEGREES, about_point=touch.get_center()), run_time=1.0)
        self.play(Rotate(ruler, 18 * DEGREES, about_point=touch.get_center()), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(ruler, touch, arch, arch_l, sil_n, place)), run_time=0.7)

        # ================= the obvious answer: measure it =================
        Rw = 0.7
        wheel_c = P(-2.6, 1.3)
        wheel = Circle(radius=Rw, color=INK, stroke_width=4).move_to(wheel_c)
        string = Circle(radius=Rw, color=RED_INK, stroke_width=5).move_to(wheel_c)
        self.play(FadeOut(VGroup(circ, diam, diam_l)), FadeIn(wheel), run_time=0.6)
        base_y = 0.2
        start = P(-5.2 - 0.0, base_y)
        straight = Line(P(-3.3, base_y), P(-3.3 + 2 * math.pi * Rw, base_y), color=RED_INK, stroke_width=5)
        line("The obvious answer is to measure. Wrap a string around a wheel, then stretch it out.",
             Create(string), run_time=1.2)
        self.play(Transform(string, straight), run_time=1.6)
        dticks = VGroup()
        for k in range(4):
            x = -3.3 + k * 2 * Rw
            dticks.add(Line(P(x, base_y - 0.25), P(x, base_y - 0.45), color=SEPIA, stroke_width=2))
        dlabs = VGroup(*[note(f"{k} d", 15, SEPIA).move_to(P(-3.3 + k * 2 * Rw, base_y - 0.65)) for k in range(1, 4)])
        self.vo_wait()
        bit = Brace(Line(P(-3.3 + 6 * Rw, base_y), P(-3.3 + 2 * math.pi * Rw, base_y)), UP, color=RED_INK,
                    buff=0.12)
        bit_l = note("a bit", 16, RED_INK).next_to(bit, UP, buff=0.05)
        wobble = note("string stretches, eyes misjudge: a measurement, not a proof", 17, FADED).move_to(P(-1.2, -1.2))
        line("You get about three and a bit. But a measurement is only as good as your string.",
             FadeIn(dticks), FadeIn(dlabs), run_time=0.9)
        self.play(GrowFromCenter(bit), FadeIn(bit_l), run_time=0.7)
        self.play(FadeIn(wobble), string.animate.set_stroke(width=8, opacity=0.6), run_time=0.8)
        self.vo_wait()
        proof = serif("a proof", 52, RED_INK, italic=True).move_to(P(4.0, 1.3))
        line("Archimedes wanted something no string could give him. A proof.", run_time=0.6)
        self.wait(1.5)
        self.play(Write(proof), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(wheel, string, dticks, dlabs, bit, bit_l, wobble, proof)), run_time=0.7)

        # ================= the idea: trap it =================
        C = P(-3.4, 0.45)
        R = 2.0
        circle = Circle(radius=R, color=INK, stroke_width=3).move_to(C).set_z_index(3)
        idea = VGroup(serif("If you cannot measure the curve,", 28, INK),
                      serif("trap it.", 34, RED_INK, italic=True)).arrange(DOWN, buff=0.18).move_to(P(2.9, 0.9))
        line("His idea was this. If you cannot measure the curve, trap it, between shapes made only of straight "
             "lines.", Create(circle), FadeIn(idea[0]), run_time=1.0)
        self.wait(1.0)
        self.play(FadeIn(idea[1], scale=1.2), run_time=0.7)
        self.vo_wait()

        hin, hout = polys(6, R, C)
        spokes = VGroup(*[Line(C, v, color=FADED, stroke_width=1.5) for v in hin.get_vertices()])
        r_lab = MathTex("r", font_size=30, color=SEPIA)
        v0, v1 = hin.get_vertices()[0], hin.get_vertices()[1]
        r_lab.move_to((v0 + v1) / 2 - normalize((v0 + v1) / 2 - C) * 0.32)
        r_lab2 = MathTex("r", font_size=30, color=SEPIA).move_to((C + v0) / 2 + RIGHT * 0.22)
        line("Draw a hexagon inside the circle. Each of its six sides is exactly as long as the radius.",
             FadeOut(idea), Create(hin), run_time=1.4)
        self.play(Create(spokes), run_time=0.8)
        self.play(FadeIn(r_lab), FadeIn(r_lab2), run_time=0.6)
        eq_n = note("six equilateral triangles: every side equals r", 18, BLUE_INK).move_to(P(2.7, 2.5))
        self.play(FadeIn(eq_n), run_time=0.5)
        self.vo_wait()

        # number line: where pi sits
        nl = NumberLine(x_range=[2.9, 3.5, 0.1], length=6.0, color=INK, include_numbers=True,
                        decimal_number_config={"num_decimal_places": 1, "color": INK}, font_size=22).move_to(P(2.7, 0.2))
        nl_t = note("distance around ÷ width", 16).next_to(nl, UP, buff=0.8)
        pmark = VGroup(Line(nl.n2p(math.pi) + UP * 0.12, nl.n2p(math.pi) + DOWN * 0.12, color=FADED, stroke_width=2),
                       MathTex(r"\pi\,?", font_size=26, color=FADED).next_to(nl.n2p(math.pi), UP, buff=0.42))

        def marker(val, color, lab, up=True):
            p = nl.n2p(val)
            tri = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(0.11)
            tri.rotate(PI).move_to(p + UP * 0.24)
            t = Text(lab, font=MONO, font_size=16, color=color)
            t.next_to(tri, UP, buff=0.06)
            return VGroup(tri, t)

        per_in = MathTex(r"6r = 3d", font_size=32, color=BLUE_INK).move_to(P(2.7, 2.5))
        lo = marker(3.0, BLUE_INK, "3", up=False)
        line("So its perimeter is six radii, which is three diameters. The circle bulges outside it, so pi must be "
             "more than three.", FadeOut(eq_n), FadeIn(per_in), run_time=0.8)
        self.play(Create(nl), FadeIn(nl_t), FadeIn(pmark), run_time=1.2)
        self.play(FadeIn(lo, shift=UP * 0.2), circle.animate.set_stroke(color=INK, width=4), run_time=0.8)
        self.vo_wait()

        per_out = MathTex(r"4\sqrt{3}\,r = 2\sqrt{3}\,d \approx 3.46\,d", font_size=32, color=RED_INK).move_to(
            P(2.7, 1.85))
        hi = marker(outside(6), RED_INK, "3.46", up=False)
        line("Now draw a hexagon outside the circle. Its perimeter works out to about three point four six "
             "diameters. So pi must be less than that.", FadeOut(VGroup(spokes, r_lab, r_lab2)), Create(hout),
             run_time=1.4)
        self.play(FadeIn(per_out), run_time=0.7)
        self.wait(1.5)
        self.play(FadeIn(hi, shift=UP * 0.2), run_time=0.8)
        self.vo_wait()

        def cage(lo_v, hi_v, numline):
            a, b = numline.n2p(lo_v), numline.n2p(hi_v)
            return Rectangle(width=max(b[0] - a[0], 0.02), height=0.34, stroke_width=0, fill_color=RED_INK,
                             fill_opacity=0.16).move_to((a + b) / 2)

        box = cage(3.0, outside(6), nl)
        line("Pi is caught between three and three point four six. A loose cage.", FadeIn(box), run_time=0.8)
        self.vo_wait()

        # ================= doubling =================
        self.play(FadeOut(VGroup(per_in, per_out)), run_time=0.5)
        hdr = VGroup(*[Text(s, font=MONO, font_size=17, color=SEPIA) for s in ("sides", "inside", "outside")])
        col_x = [0.5, 2.3, 4.3]
        for t, x in zip(hdr, col_x):
            t.move_to(P(x, 3.0))
        rule = Line(P(-0.2, 2.78), P(5.2, 2.78), color=FADED, stroke_width=1)

        def trow(n, y):
            return VGroup(Text(str(n), font=MONO, font_size=17, color=INK).move_to(P(col_x[0], y)),
                          Text(f"{inside(n):.4f}", font=MONO, font_size=17, color=BLUE_INK).move_to(P(col_x[1], y)),
                          Text(f"{outside(n):.4f}", font=MONO, font_size=17, color=RED_INK).move_to(P(col_x[2], y)))
        ys = [2.55, 2.25, 1.95, 1.65, 1.35]
        rows = [trow(n, y) for n, y in zip(SIDES, ys)]
        tab_n = note("modern decimals, computed exactly", 13).move_to(P(2.5, 1.02))
        self.play(FadeIn(hdr), Create(rule), FadeIn(rows[0]), FadeIn(tab_n),
                  VGroup(nl, nl_t, pmark, lo, hi, box).animate.shift(DOWN * 0.9), run_time=0.8)

        cur_in, cur_out = hin, hout
        cur_lo, cur_hi, cur_box = lo, hi, box

        def step(n, numline, rt=1.0):
            nonlocal cur_in, cur_out, cur_lo, cur_hi, cur_box
            ni, no = polys(n, R, C)
            l2 = marker(inside(n), BLUE_INK, "", up=False)
            h2 = marker(outside(n), RED_INK, "", up=False)
            b2 = cage(inside(n), outside(n), numline)
            self.play(Transform(cur_in, ni), Transform(cur_out, no), Transform(cur_lo, l2), Transform(cur_hi, h2),
                      Transform(cur_box, b2), FadeIn(rows[SIDES.index(n)]), run_time=rt)

        line("So Archimedes doubled the sides. Twelve sides. Now pi is trapped between about three point one one "
             "and three point two two.", run_time=0.6)
        self.wait(1.2)
        step(12, nl, 1.4)
        self.vo_wait()

        # zoomed number line for the finer cages
        nl2 = NumberLine(x_range=[3.13, 3.17, 0.01], length=6.0, color=INK, include_numbers=True,
                         decimal_number_config={"num_decimal_places": 2, "color": INK}, font_size=22).move_to(
            P(2.7, -1.65))
        nl2_t = note("zoomed in ×15", 15, SEPIA).next_to(nl2, DOWN, buff=0.5)
        pm2 = VGroup(Line(nl2.n2p(math.pi) + UP * 0.12, nl2.n2p(math.pi) + DOWN * 0.12, color=FADED, stroke_width=2),
                     MathTex(r"\pi", font_size=24, color=FADED).next_to(nl2.n2p(math.pi), UP, buff=0.42))
        line("Twenty-four sides. Forty-eight. Ninety-six.", run_time=0.5)
        step(24, nl, 0.9)
        zoom_lo = marker(inside(24), BLUE_INK, "", up=False)
        self.play(Create(nl2), FadeIn(nl2_t), FadeIn(pm2), run_time=0.7)
        cur_lo2 = marker(inside(24), BLUE_INK, "", up=False)
        cur_lo2 = VGroup(cur_lo2[0].copy().move_to(nl2.n2p(inside(24)) + UP * 0.24))
        cur_hi2 = VGroup(Triangle(color=RED_INK, fill_color=RED_INK, fill_opacity=1, stroke_width=0).scale(0.11)
                         .rotate(PI).move_to(nl2.n2p(min(outside(24), 3.17)) + UP * 0.24))
        cur_box2 = cage(inside(24), min(outside(24), 3.17), nl2)
        self.play(FadeIn(cur_lo2), FadeIn(cur_hi2), FadeIn(cur_box2), run_time=0.4)
        del zoom_lo
        for n in (48, 96):
            ni, no = polys(n, R, C)
            l1 = marker(inside(n), BLUE_INK, "", up=False)
            h1 = marker(outside(n), RED_INK, "", up=False)
            b1 = cage(inside(n), outside(n), nl)
            l2 = VGroup(cur_lo2[0].copy().move_to(nl2.n2p(inside(n)) + UP * 0.24))
            h2 = VGroup(cur_hi2[0].copy().move_to(nl2.n2p(outside(n)) + UP * 0.24))
            b2 = cage(inside(n), outside(n), nl2)
            self.play(Transform(cur_in, ni), Transform(cur_out, no), Transform(cur_lo, l1), Transform(cur_hi, h1),
                      Transform(cur_box, b1), Transform(cur_lo2, l2), Transform(cur_hi2, h2),
                      Transform(cur_box2, b2), FadeIn(rows[SIDES.index(n)]), run_time=0.8)
        self.vo_wait()
        quarter = VGroup(*[Text(f"gap {outside(n) - inside(n):.4f}", font=MONO, font_size=14, color=FADED)
                           .move_to(P(6.05, y)) for n, y in zip(SIDES, ys)])
        for q_ in quarter:
            if q_.get_right()[0] > 6.55:
                q_.shift(LEFT * (q_.get_right()[0] - 6.55))
        hug = VGroup(note("at 96 sides, both polygons lie", 15, SEPIA),
                     note("within a line's width of the circle", 15, SEPIA)).arrange(DOWN, buff=0.04)
        hug.move_to(C + DOWN * (R + 0.42))
        line("With each doubling, the polygons hug the circle more closely, and the gap between them shrinks to "
             "about a quarter.", LaggedStart(*[FadeIn(q_) for q_ in quarter], lag_ratio=0.3), run_time=2.0)
        self.play(FadeIn(hug), run_time=0.6)
        self.vo_wait()
        thumb_group = VGroup(circle, cur_in, cur_out, hug)
        self.play(clear(), FadeOut(VGroup(hdr, rule, *rows, tab_n, quarter, nl, nl_t, pmark, cur_lo, cur_hi, cur_box,
                                          nl2, nl2_t, pm2, cur_lo2, cur_hi2, cur_box2)), run_time=0.7)

        # ================= by hand, in fractions =================
        nodec = VGroup(serif("No decimals.", 30, INK), note("whole numbers and fractions, by hand", 18)).arrange(
            DOWN, buff=0.12).move_to(P(2.9, 2.3))
        line("And Archimedes had no decimals. Every step was done in whole numbers and fractions, by hand.",
             FadeIn(nodec), run_time=0.9)
        self.vo_wait()
        sq = MathTex(r"\frac{265}{153}", r"<", r"\sqrt{3}", r"<", r"\frac{1351}{780}", font_size=42, color=INK)
        sq.move_to(P(2.9, 0.75))
        sq_n = note("1.73202…  <  1.73205…  <  1.73205…", 15).next_to(sq, DOWN, buff=0.15)
        line("Even the square root of three had to be pinned between two fractions. He never said how he found them.",
             FadeIn(sq[2]), run_time=0.7)
        self.play(FadeIn(sq[0], shift=RIGHT * 0.2), FadeIn(sq[1]), FadeIn(sq[3]), FadeIn(sq[4], shift=LEFT * 0.2),
                  run_time=0.9)
        self.play(FadeIn(sq_n), run_time=0.5)
        self.vo_wait()

        res = MathTex(r"3\tfrac{10}{71}", r"<", r"\pi", r"<", r"3\tfrac{1}{7}", font_size=52, color=INK)
        res[0].set_color(BLUE_INK)
        res[4].set_color(RED_INK)
        res.move_to(P(2.9, 0.3))
        ratios = MathTex(r"\frac{6336}{2017\frac14}", r"<\ \frac{\text{around}}{\text{width}}\ <",
                         r"\frac{14688}{4673\frac12}", font_size=30, color=INK).move_to(P(2.9, 1.95))
        ratios[0].set_color(BLUE_INK)
        ratios[2].set_color(RED_INK)
        rat_n = note("his 96-gon ratios, in modern notation", 14).next_to(ratios, DOWN, buff=0.1)
        line("At ninety-six sides he stopped. His result: pi is less than three and one seventh, and more than three "
             "and ten seventy-firsts.", FadeOut(VGroup(nodec, sq, sq_n)), FadeIn(ratios), FadeIn(rat_n),
             run_time=1.0)
        self.wait(1.2)
        self.play(FadeIn(res[1:4]), run_time=0.5)
        self.play(FadeIn(res[4], shift=LEFT * 0.2), run_time=0.6)
        self.wait(0.8)
        self.play(FadeIn(res[0], shift=RIGHT * 0.2), run_time=0.6)
        src = note("Measurement of a Circle, Proposition 3", 15, SEPIA).next_to(res, DOWN, buff=0.25)
        self.play(FadeIn(src), run_time=0.5)
        self.vo_wait()

        dec = VGroup(Text("3.1408", font=MONO, font_size=30, color=BLUE_INK),
                     MathTex(r"< \pi <", font_size=36, color=INK),
                     Text("3.1429", font=MONO, font_size=30, color=RED_INK)).arrange(RIGHT, buff=0.25)
        dec.move_to(P(2.9, -1.0))
        both = SurroundingRectangle(VGroup(dec[0][:4], dec[2][:4]), color=SEPIA, stroke_width=0)
        u1 = Underline(dec[0][:4], color=SEPIA, stroke_width=3)
        u2 = Underline(dec[2][:4], color=SEPIA, stroke_width=3)
        sure = note("3.14 for certain", 18, SEPIA).next_to(dec, DOWN, buff=0.25)
        line("In decimals, between three point one four oh eight and three point one four two nine. Right to two "
             "decimal places, and proven.", FadeIn(dec), run_time=0.9)
        self.wait(2.2)
        self.play(Create(u1), Create(u2), FadeIn(sure), run_time=0.8)
        stamp_m = stamp(r"\text{PROVEN}", size=30).move_to(P(5.3, -1.95))
        self.play(FadeIn(stamp_m, scale=1.4), run_time=0.5)
        self.vo_wait()
        del both
        self.play(clear(), FadeOut(VGroup(ratios, rat_n, res, src, dec, u1, u2, sure, stamp_m)),
                  FadeOut(thumb_group), run_time=0.8)

        # ================= the method =================
        ax = Axes(x_range=[0, 4.4, 1], y_range=[2.9, 3.5, 0.1], x_length=7.0, y_length=4.0,
                  axis_config={"color": INK, "include_ticks": True, "stroke_width": 2},
                  y_axis_config={"numbers_to_include": [3.0, 3.1, 3.2, 3.3, 3.4, 3.5],
                                 "decimal_number_config": {"num_decimal_places": 1, "color": INK}, "font_size": 20},
                  tips=False).move_to(P(-0.6, 0.35))
        xl = VGroup(*[Text(str(n), font=MONO, font_size=16, color=INK).next_to(ax.c2p(i, 2.9), DOWN, buff=0.15)
                      for i, n in enumerate(SIDES)])
        xt = note("sides", 15).next_to(xl, DOWN, buff=0.1)
        pil = DashedLine(ax.c2p(0, math.pi), ax.c2p(4.4, math.pi), color=FADED, stroke_width=2)
        pil_l = MathTex(r"\pi", font_size=28, color=FADED).next_to(ax.c2p(4.4, math.pi), RIGHT, buff=0.1)
        ups = VGroup(*[Dot(ax.c2p(i, outside(n)), radius=0.07, color=RED_INK) for i, n in enumerate(SIDES)])
        lows = VGroup(*[Dot(ax.c2p(i, inside(n)), radius=0.07, color=BLUE_INK) for i, n in enumerate(SIDES)])
        upl = VMobject(color=RED_INK, stroke_width=2).set_points_as_corners([d.get_center() for d in ups])
        lowl = VMobject(color=BLUE_INK, stroke_width=2).set_points_as_corners([d.get_center() for d in lows])
        ub = serif("upper bound", 20, RED_INK).move_to(ax.c2p(1.3, 3.33))
        lb = serif("lower bound", 20, BLUE_INK).move_to(ax.c2p(1.3, 2.99))
        gift = VGroup(serif("the real gift:", 22, FADED, italic=True),
                      serif("the method", 34, INK)).arrange(DOWN, buff=0.08).move_to(P(4.7, 2.0))
        line("But the real gift was the method. Archimedes showed how to get as close as you like, and to know "
             "exactly how close you are.", FadeIn(gift), Create(ax), FadeIn(xl), FadeIn(xt), run_time=1.0)
        self.play(Create(pil), FadeIn(pil_l), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d) for d in ups], lag_ratio=0.25), Create(upl),
                  LaggedStart(*[FadeIn(d) for d in lows], lag_ratio=0.25), Create(lowl), run_time=2.2)
        self.vo_wait()
        arrows = VGroup(Arrow(ax.c2p(3.8, 3.45), ax.c2p(3.8, math.pi + 0.02), color=RED_INK, buff=0, stroke_width=4),
                        Arrow(ax.c2p(3.8, 2.98), ax.c2p(3.8, math.pi - 0.02), color=BLUE_INK, buff=0,
                              stroke_width=4))
        still = VGroup(note("an answer trapped between", 17, SEPIA), note("two you can compute", 17, SEPIA)).arrange(
            DOWN, buff=0.06).move_to(P(4.8, 0.85))
        line("An upper bound and a lower bound, squeezing in on the truth. That idea is still used across mathematics "
             "and computing.", FadeIn(ub), FadeIn(lb), run_time=0.8)
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=1.0)
        self.play(FadeIn(still), run_time=0.7)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(ax, xl, xt, pil, pil_l, ups, lows, upl, lowl, ub, lb, gift, arrows,
                                          still)), run_time=0.7)

        # ================= the end of Archimedes =================
        head = spaced("Syracuse · 212 BCE", 20, SEPIA).move_to(P(0, 3.0))
        arch2 = cameo("beard", 0.7).move_to(P(-4.9, 0.9))
        city = VGroup()
        for i, (w, h) in enumerate([(0.8, 1.2), (0.6, 0.8), (1.0, 1.5), (0.7, 1.0), (0.9, 1.3)]):
            bx = -1.6 + i * 1.0
            body = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=1.5, fill_color=PAPER_DARK,
                             fill_opacity=1).move_to(P(bx, 0.3 + h / 2))
            roof = Polygon(P(bx - w / 2 - 0.06, 0.3 + h), P(bx + w / 2 + 0.06, 0.3 + h), P(bx, 0.3 + h + 0.28),
                           stroke_color=INK, stroke_width=1.5, fill_color=PAPER_DARK, fill_opacity=1)
            cols = VGroup(*[Line(P(bx + dx, 0.32), P(bx + dx, 0.3 + h - 0.06), color=SEPIA, stroke_width=1.2)
                            for dx in np.linspace(-w / 2 + 0.12, w / 2 - 0.12, 3)])
            city.add(VGroup(body, cols, roof))
        wall = Line(P(-2.3, 0.3), P(3.0, 0.3), color=INK, stroke_width=3)
        city_n = note("drawn schematically", 13).next_to(wall, DOWN, buff=0.1)
        line("In 212 BCE, Roman forces captured Syracuse, and Archimedes was killed by a Roman soldier.",
             FadeIn(head), FadeIn(arch2), FadeIn(city, lag_ratio=0.2), Create(wall), FadeIn(city_n), run_time=1.2)
        self.vo_wait()
        cards = VGroup()
        texts = [("1", "absorbed in a problem on a diagram,", "he would not leave it"),
                 ("2", "he asked a soldier for", "a moment to finish"),
                 ("3", "his instruments were", "mistaken for gold")]
        for num, a, b in texts:
            body = VGroup(serif(num, 24, RED_INK), serif(a, 17, INK), serif(b, 17, INK)).arrange(DOWN, buff=0.08)
            cards.add(ink_card(body, pad=0.18))
        cards.arrange(RIGHT, buff=0.3).move_to(P(0.6, -1.15))
        plut = note("three versions, in Plutarch's Life of Marcellus", 15, SEPIA).next_to(cards, UP, buff=0.15)
        line("Plutarch gives three versions. In one, Archimedes was so absorbed in a problem on a diagram that he "
             "would not leave it.", FadeOut(VGroup(city, wall, city_n)), FadeIn(plut),
             LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.3), run_time=1.6)
        self.play(cards[0].animate.scale(1.08), cards[1].animate.set_opacity(0.45),
                  cards[2].animate.set_opacity(0.45), run_time=0.7)
        self.vo_wait()
        quote = serif("“Do not disturb my circles.”", 34, INK, italic=True).move_to(P(0.6, 1.5))
        legend = stamp(r"\text{LATER RETELLING}", size=24, rot=-5 * DEGREES).next_to(quote, DOWN, buff=0.15)
        legend.shift(RIGHT * 1.6)
        line("The famous words, do not disturb my circles, come from later retellings. No one knows what he said.",
             FadeIn(quote), run_time=1.0)
        self.wait(0.8)
        self.play(FadeIn(legend, scale=1.4), run_time=0.5)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(head, arch2, cards, plut, quote, legend)), run_time=0.7)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 22, RED_INK).move_to(P(0, 3.15))
        colw = [0.8, 1.6, 2.6, 2.6]
        X0 = -6.5
        rowh = 0.47

        def cell(txt, c, r, color=INK, fill="#f6eedb", size=18):
            x = X0 + sum(colw[:c]) + colw[c] / 2
            y = 2.45 - r * rowh
            box = Rectangle(width=colw[c], height=rowh, stroke_color=FADED, stroke_width=1, fill_color=fill,
                            fill_opacity=1).move_to(P(x, y))
            t = Text(txt, font=MONO, font_size=size, color=color)
            if t.width > colw[c] - 0.12:
                t.scale_to_fit_width(colw[c] - 0.12)
            return VGroup(box, t.move_to(box))

        sheet = VGroup(cell("", 0, 0, fill=PAPER_DARK), cell("A", 1, 0, SEPIA, PAPER_DARK),
                       cell("B", 2, 0, SEPIA, PAPER_DARK), cell("C", 3, 0, SEPIA, PAPER_DARK),
                       cell("1", 0, 1, SEPIA, PAPER_DARK), cell("sides", 1, 1, SEPIA),
                       cell("inside", 2, 1, BLUE_INK), cell("outside", 3, 1, RED_INK))
        tab = doubling_table(20)
        data = []
        for i, r_ in enumerate([0, 1, 2, 3, 4, 10, 20]):
            n, b, a = tab[r_]
            rr = i + 2
            label = str(r_ + 2)
            row = VGroup(cell(label, 0, rr, SEPIA, PAPER_DARK), cell(f"{n:,}", 1, rr),
                         cell(f"{b:.10f}", 2, rr, BLUE_INK), cell(f"{a:.10f}", 3, rr, RED_INK))
            data.append(row)
        dots = VGroup(*[Text("⋮", font_size=18, color=FADED).move_to(data[k][2].get_bottom() + DOWN * 0.0)
                        for k in (4, 5)])
        # spread rows so the elided ones show a gap
        for k in range(5, 7):
            data[k].shift(DOWN * 0.18 * (k - 4))
        for k, d_ in zip((4, 5), dots):
            mid_y = (data[k].get_bottom()[1] + data[k + 1].get_top()[1]) / 2
            d_.move_to(P(X0 + sum(colw[:2]) + colw[2] / 2, mid_y)).scale(0.8)
        f2 = VGroup(mono("C3: =2*B2*C2/(B2+C2)", 18, RED_INK))
        f3 = VGroup(mono("B3: =SQRT(C3*B2)", 18, BLUE_INK))
        f1 = VGroup(mono("A2: 6", 18, FADED), mono("B2: 3", 18, BLUE_INK), mono("C2: =2*SQRT(3)", 18, RED_INK)).arrange(
            DOWN, buff=0.08, aligned_edge=LEFT)
        f4 = VGroup(mono("A3: =2*A2", 18, FADED), note("then fill row 3 down", 19, SEPIA)).arrange(
            DOWN, buff=0.08, aligned_edge=LEFT)
        forms = VGroup(f1, f2, f3, f4).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(P(3.9, 0.6))
        forms.align_to(P(1.75, 0), LEFT)
        line("Try it yourself. In a spreadsheet, start with the hexagon. Inside, three. Outside, two root three.",
             FadeIn(tiy), FadeIn(sheet), run_time=1.0)
        self.play(FadeIn(data[0]), FadeIn(f1), run_time=0.8)
        self.vo_wait()
        line("To double the sides: new outside is two times inside times outside, over inside plus outside.",
             FadeIn(f2), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(VGroup(data[1][0], data[1][1], data[1][3])), run_time=0.7)
        self.vo_wait()
        line("New inside is the square root of new outside times old inside.", FadeIn(f3), run_time=0.8)
        self.play(FadeIn(data[1][2]), run_time=0.6)
        self.vo_wait()
        hl = SurroundingRectangle(data[4], color=RED_INK, stroke_width=3, buff=0.03)
        line("Four rows give Archimedes' ninety-six sides. Twenty rows trap pi to ten decimal places.",
             FadeIn(f4), LaggedStart(*[FadeIn(data[k]) for k in (2, 3, 4)], lag_ratio=0.4), run_time=1.6)
        self.play(Create(hl), run_time=0.5)
        self.play(FadeIn(dots), FadeIn(data[5]), run_time=0.6)
        self.play(FadeIn(data[6]), hl.animate.become(SurroundingRectangle(data[6], color=RED_INK, stroke_width=3,
                                                                          buff=0.03)), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tiy, sheet, *data, dots, forms, hl)), run_time=0.8)

        # ================= close =================
        Cc = P(0, 1.35)
        cc = Circle(radius=1.1, color=INK, stroke_width=3).move_to(Cc).set_z_index(3)
        ci, co = polys(12, 1.1, Cc)
        c6i, c6o = polys(6, 1.1, Cc)
        last = VGroup(serif("A curve no ruler could measure, two cages of straight lines,", 28, INK),
                      serif("and a number trapped over two thousand years ago.", 28, RED_INK)).arrange(
            DOWN, buff=0.2).move_to(P(0, -1.05))
        line("A curve no ruler could measure, two cages of straight lines, and a number trapped over two thousand "
             "years ago.", Create(cc), Create(c6i), Create(c6o), run_time=1.2)
        self.play(Transform(c6i, ci), Transform(c6o, co), FadeIn(last, lag_ratio=0.2), run_time=1.6)
        self.vo_wait()
        self.wait(0.5)
        self.play(clear(), FadeOut(VGroup(last, cc, c6i, c6o)), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after W. Dunham, Journey Through Genius (1990) · sources in the episode notes", 17),
                     note("facts checked against MacTutor, B. Rosenberg (Archimedes and Pi), J. Feldman (UBC), "
                          "PBS NOVA and Plutarch's Life of Marcellus", 17),
                     note("silhouettes and city stylised · polygon values computed exactly · Manim · synthetic "
                          "narration", 15)
                     ).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        for m in end:
            if m.width > 12.8:
                m.scale_to_fit_width(12.8)
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(3.0)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)
