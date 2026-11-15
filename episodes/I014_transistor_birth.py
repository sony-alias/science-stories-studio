"""I014 The Transistor's Messy Birth, a Science Stories episode.

After J. Gertner, The Idea Factory (Penguin Press, 2012). Script and sources: episodes/I014_script.md

Render:  manim -qh --frame_rate 30 episodes/I014_transistor_birth.py TransistorBirth
Then:    scripts/finish_video.sh media/videos/I014_transistor_birth/1080p30/TransistorBirth.mp4 out/I014_transistor_birth.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

GOLD = "#c9962e"
GLOW = "#e8b14a"
N_COL = "#c9d6e3"     # n-type wash
P_COL = "#ecc9b8"     # p-type wash


# ---------------- small drawing helpers ----------------
def wire(*pts, color=INK, width=2.5):
    pts = [np.array([p[0], p[1], 0]) for p in pts]
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners(pts)
    return m


def zigzag(p0, p1, n=7, amp=0.16, color=INK, width=2.5):
    p0, p1 = np.array(p0, dtype=float), np.array(p1, dtype=float)
    d = p1 - p0
    nrm = np.array([-d[1], d[0], 0]) / np.linalg.norm(d)
    pts = [p0]
    for i in range(1, 2 * n):
        pts.append(p0 + d * i / (2 * n) + nrm * (amp if i % 2 else -amp))
    pts.append(p1)
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners(pts)
    return m


def wave(x0, x1, y, amp, cycles=3, color=RED_INK, width=3):
    return FunctionGraph(lambda x: y + amp * np.sin(TAU * cycles * (x - x0) / (x1 - x0)), x_range=[x0, x1, 0.02],
                         color=color, stroke_width=width)


def note(text, size=17):
    return serif(text, size, FADED, italic=True)


def battery_h(x, y, label="9 V"):
    """Horizontal battery symbol (plus on the left) centred at (x, y)."""
    long = Line([x - 0.08, y - 0.32, 0], [x - 0.08, y + 0.32, 0], color=INK, stroke_width=3)
    short = Line([x + 0.08, y - 0.17, 0], [x + 0.08, y + 0.17, 0], color=INK, stroke_width=5)
    plus = serif("+", 18, FADED).move_to([x - 0.3, y + 0.32, 0])
    lab = serif(label, 16, FADED, italic=True).move_to([x, y - 0.55, 0])
    return VGroup(long, short, plus, lab)


def led_sym(x, y, color=INK):
    """LED pointing down (current flows downward), centred at (x, y)."""
    tri = Polygon([x - 0.22, y + 0.18, 0], [x + 0.22, y + 0.18, 0], [x, y - 0.18, 0], color=color, stroke_width=2.5,
                  fill_color=PAPER, fill_opacity=1)
    bar = Line([x - 0.22, y - 0.19, 0], [x + 0.22, y - 0.19, 0], color=color, stroke_width=3)
    rays = VGroup(*[Arrow([x + 0.25, y + dy, 0], [x + 0.55, y + dy + 0.2, 0], buff=0, stroke_width=2, color=RED_INK,
                          tip_length=0.1, max_tip_length_to_length_ratio=0.4) for dy in (-0.05, 0.13)])
    return VGroup(tri, bar, rays)


def resistor_v(x, y0, y1):
    n = 5
    ys = np.linspace(y0, y1, 2 * n + 1)
    pts = [(x, ys[0])] + [(x + (0.12 if i % 2 else -0.12), ys[i]) for i in range(1, 2 * n)] + [(x, ys[-1])]
    return wire(*pts)


def resistor_h(x0, x1, y):
    n = 5
    xs = np.linspace(x0, x1, 2 * n + 1)
    pts = [(xs[0], y)] + [(xs[i], y + (0.12 if i % 2 else -0.12)) for i in range(1, 2 * n)] + [(xs[-1], y)]
    return wire(*pts)


def npn_sym(cx, cy, r=0.55):
    """Bipolar NPN symbol: base on the left, collector up-right, emitter down-right (arrow out)."""
    c = np.array([cx, cy, 0])
    circ = Circle(radius=r, color=INK, stroke_width=2).move_to(c)
    bar = Line(c + [-0.18, 0.3, 0], c + [-0.18, -0.3, 0], color=INK, stroke_width=4)
    base = Line(c + [-r - 0.35, 0, 0], c + [-0.18, 0, 0], color=INK, stroke_width=2.5)
    col = Line(c + [-0.18, 0.12, 0], c + [0.22, 0.45, 0], color=INK, stroke_width=2.5)
    col2 = Line(c + [0.22, 0.45, 0], c + [0.22, r + 0.35, 0], color=INK, stroke_width=2.5)
    em = Arrow(c + [-0.18, -0.12, 0], c + [0.22, -0.45, 0], buff=0, color=INK, stroke_width=2.5, tip_length=0.14,
               max_tip_length_to_length_ratio=0.5)
    em2 = Line(c + [0.22, -0.45, 0], c + [0.22, -r - 0.35, 0], color=INK, stroke_width=2.5)
    g = VGroup(circ, bar, base, col, col2, em, em2)
    g.b = c + [-r - 0.35, 0, 0]
    g.c = c + [0.22, r + 0.35, 0]
    g.e = c + [0.22, -r - 0.35, 0]
    return g


class Carriers(VGroup):
    """A recycled pool of dots that flow left to right through an npn bar. Some vanish in the base."""

    def __init__(self, x0, xb0, xb1, x1, y0, y1, n=60, color=BLUE_INK, **kw):
        super().__init__(**kw)
        self.x0, self.xb0, self.xb1, self.x1, self.y0, self.y1 = x0, xb0, xb1, x1, y0, y1
        self.rng = np.random.default_rng(1948)
        self.rate = 0.0          # 0 = off; 1 = full flow
        self.speed = 1.4
        self.dots = []
        for _ in range(n):
            d = Dot(radius=0.055, color=color).set_opacity(0)
            d.alive = False
            d.doomed = False
            self.dots.append(d)
            self.add(d)
        self.add_updater(lambda m, dt: m.step(dt))

    def step(self, dt):
        dt = min(dt, 1 / 15)
        for d in self.dots:
            if d.alive:
                p = d.get_center()
                vy = self.rng.normal(0, 0.6)
                p = p + np.array([self.speed * dt, vy * dt, 0])
                p[1] = np.clip(p[1], self.y0 + 0.08, self.y1 - 0.08)
                d.move_to(p)
                if d.doomed and p[0] > (self.xb0 + self.xb1) / 2:
                    d.alive = False
                    d.set_opacity(0)
                elif p[0] > self.x1 - 0.06:
                    d.alive = False
                    d.set_opacity(0)
            elif self.rate > 0 and self.rng.random() < self.rate * dt * 0.7:
                d.alive = True
                d.doomed = self.rng.random() < 0.12
                d.move_to([self.x0 + 0.08, self.rng.uniform(self.y0 + 0.1, self.y1 - 0.1), 0])
                d.set_opacity(1)

    def stop_all(self):
        self.rate = 0.0
        for d in self.dots:
            d.alive = False
            d.set_opacity(0)


class TransistorBirth(NarratedScene):
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
                anim = AnimationGroup(FadeOut(caption[0], shift=UP * 0.1), FadeIn(new, shift=UP * 0.1))
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
        title = serif("The Transistor's Messy Birth", 56).next_to(orn1, DOWN, buff=0.35)
        sub = serif("Bardeen · Brattain · Shockley · Bell Labs · 1947–48", 26, FADED, italic=True).next_to(
            title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("after Jon Gertner, The Idea Factory: Bell Labs and the Great Age of American Innovation "
                      "(Penguin Press, 2012)", 16).move_to([0, -3.2, 0])
        self.vo("Science Stories. The transistor's messy birth.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= Brattain and the gold wedge =================
        place = serif("Bell Labs · December 1947", 22, SEPIA, italic=True).move_to([0, 3.15, 0])
        brattain = cameo("modern", 0.7)
        b_name = serif("Walter Brattain", 24, INK).next_to(brattain, DOWN, buff=0.15)
        b_role = note("experimental physicist", 16).next_to(b_name, DOWN, buff=0.06)
        bw = VGroup(brattain, b_name, b_role).move_to([-4.9, 0.4, 0])

        cx = 1.4
        slab = Rectangle(width=4.2, height=0.75, color=INK, stroke_width=2.5, fill_color="#b9b2a4",
                         fill_opacity=1).move_to([cx, -1.55, 0])
        plate = Rectangle(width=4.6, height=0.18, color=INK, stroke_width=2, fill_color=INK,
                          fill_opacity=0.8).next_to(slab, DOWN, buff=0)
        slab_l = note("germanium", 18).next_to(slab, DOWN, buff=0.32)
        apex = np.array([cx, slab.get_top()[1] + 0.02, 0])
        wl, wr = np.array([cx - 0.95, 1.0, 0]), np.array([cx + 0.95, 1.0, 0])
        wedge = Polygon(wl, wr, apex, color=INK, stroke_width=2, fill_color="#d8d0c0", fill_opacity=1)
        wedge_l = note("plastic wedge", 16).move_to([cx, 0.62, 0])
        foil_full = VGroup(Line(wl + (apex - wl) * 0.25, apex, color=GOLD, stroke_width=7),
                           Line(apex, wr + (apex - wr) * 0.25, color=GOLD, stroke_width=7))
        gap = 0.07
        foil_cut = VGroup(Line(wl + (apex - wl) * 0.25, apex + LEFT * gap, color=GOLD, stroke_width=7),
                          Line(apex + RIGHT * gap, wr + (apex - wr) * 0.25, color=GOLD, stroke_width=7))
        foil_l = serif("gold foil", 18, GOLD, italic=True).move_to([cx + 1.75, 0.15, 0])
        razor = VGroup(Rectangle(width=0.12, height=1.3, color=INK, stroke_width=1.5, fill_color="#9aa3ab",
                                 fill_opacity=1)).move_to(apex + UP * 1.9)
        spring = zigzag([cx, 1.0, 0], [cx, 2.3, 0], n=6, amp=0.18)
        bracket = Line([cx - 0.7, 2.3, 0], [cx + 0.7, 2.3, 0], color=INK, stroke_width=5)
        spring_l = note("spring", 16).next_to(spring, LEFT, buff=0.25)
        pc_label = note("point-contact amplifier (schematic)", 16).move_to([cx, 2.75, 0])

        line("December 1947, at Bell Labs. Walter Brattain takes a razor blade to a strip of gold foil.",
             FadeIn(place), FadeIn(bw, shift=UP * 0.15), run_time=1.0)
        self.play(FadeIn(VGroup(wedge, foil_full)), FadeIn(foil_l), run_time=0.9)
        self.vo_wait()
        line("The foil is glued around the tip of a plastic wedge.", FadeIn(wedge_l), run_time=0.6)
        self.vo_wait()
        line("One careful cut splits it into two gold contacts, about the width of a sheet of paper apart.",
             FadeIn(razor), run_time=0.6)
        self.play(razor.animate.move_to(apex + UP * 0.45), run_time=0.8)
        self.play(ReplacementTransform(foil_full, foil_cut), razor.animate.move_to(apex + UP * 2.0).set_opacity(0),
                  run_time=0.8)
        self.remove(razor)
        mag = Circle(radius=0.45, color=RED_INK, stroke_width=2.5).move_to(apex + UP * 0.12)
        mag_l = serif("≈ a sheet of paper", 18, RED_INK, italic=True).next_to(mag, LEFT, buff=0.25)
        self.play(Create(mag), FadeIn(mag_l), run_time=0.7)
        self.vo_wait()
        line("A spring presses them onto a slab of germanium.", FadeOut(VGroup(mag, mag_l)),
             FadeIn(VGroup(slab, plate)), FadeIn(slab_l), run_time=0.8)
        self.play(Create(spring), FadeIn(bracket), FadeIn(spring_l), FadeIn(pc_label), run_time=0.9)
        self.vo_wait()

        # signal in, bigger signal out
        ty = -0.35
        lead_in = VGroup(wire((cx - 0.62, ty), (cx - 2.3, ty)),
                         Circle(radius=0.07, color=INK, stroke_width=2.5, fill_color=PAPER, fill_opacity=1).move_to(
                             [cx - 2.37, ty, 0]))
        lead_out = VGroup(wire((cx + 0.62, ty), (cx + 2.3, ty)),
                          Circle(radius=0.07, color=INK, stroke_width=2.5, fill_color=PAPER, fill_opacity=1).move_to(
                              [cx + 2.37, ty, 0]))
        w_in = wave(cx - 3.5, cx - 2.6, ty, 0.08, cycles=2)
        w_out = wave(cx + 2.6, cx + 3.6, ty, 0.42, cycles=2)
        in_l = note("signal in", 16).next_to(w_in, UP, buff=0.5)
        out_l = note("signal out", 16).next_to(w_out, UP, buff=0.12).set_y(in_l.get_y())
        gain = serif("roughly 100×", 30, RED_INK).move_to([cx + 3.1, -1.25, 0])
        line("And on December the sixteenth, this crude contraption amplifies a signal, roughly a hundred times.",
             FadeOut(foil_l), FadeOut(wedge_l), Create(lead_in), Create(lead_out), run_time=0.9)
        self.play(Create(w_in), FadeIn(in_l), run_time=0.7)
        self.play(TransformFromCopy(w_in, w_out), FadeIn(out_l), run_time=1.0)
        self.play(FadeIn(gain, scale=0.9), run_time=0.6)
        self.vo_wait()
        device = VGroup(slab, plate, slab_l, wedge, foil_cut, spring, bracket, spring_l, pc_label, lead_in, lead_out,
                        w_in, w_out, in_l, out_l, gain)
        self.play(clear(), FadeOut(device), FadeOut(bw), FadeOut(place), run_time=0.8)

        # ================= why: vacuum tubes =================
        def tube(x, y, s=1.0):
            glass = RoundedRectangle(corner_radius=0.45, width=1.1, height=1.9, color=INK, stroke_width=2.5,
                                     fill_color=PAPER, fill_opacity=0.6).move_to([x, y, 0])
            top = Arc(radius=0.55, start_angle=0, angle=PI, color=INK, stroke_width=2.5).move_to([x, y + 0.95, 0])
            base = Rectangle(width=1.0, height=0.35, color=INK, stroke_width=2, fill_color=INK,
                             fill_opacity=0.85).move_to([x, y - 1.1, 0])
            pins = VGroup(*[Line([x + dx, y - 1.28, 0], [x + dx, y - 1.55, 0], color=INK, stroke_width=2.5)
                            for dx in (-0.3, -0.1, 0.1, 0.3)])
            fil = zigzag([x, y - 0.6, 0], [x, y + 0.4, 0], n=4, amp=0.12, color=GLOW, width=3)
            halo = Ellipse(width=1.0, height=1.5, stroke_width=0, fill_color=GLOW, fill_opacity=0.25).move_to([x, y - 0.1, 0])
            return VGroup(halo, glass, fil, base, pins).scale(s)

        tubes = VGroup(*[tube(x, 0.6) for x in (-4.6, -2.9, -1.2)])
        pros = VGroup(note("hot", 24), note("power-hungry", 24), note("unreliable", 24)).arrange(DOWN, buff=0.3,
                                                                                                 aligned_edge=LEFT)
        pros.move_to([2.6, 1.0, 0])
        tube_l = note("vacuum tubes (schematic)", 18).move_to([-2.9, -1.6, 0])
        line("The telephone network ran on vacuum tubes: hot, power-hungry and unreliable.",
             FadeIn(tubes, lag_ratio=0.2), FadeIn(tube_l), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in pros], lag_ratio=0.5), run_time=1.5)
        self.play(tubes[2][0].animate.set_fill(opacity=0), tubes[2][2].animate.set_stroke(FADED, opacity=0.4),
                  run_time=0.5)
        self.vo_wait()
        goal = ink_card(VGroup(serif("Wanted:", 24, SEPIA, italic=True),
                               serif("an amplifier made of solid crystal", 30, RED_INK)).arrange(DOWN, buff=0.15))
        goal.move_to([2.6, -1.2, 0])
        line("Bell Labs wanted an amplifier made from a solid crystal.", FadeIn(goal, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tubes, pros, tube_l, goal)), run_time=0.7)

        # ================= Shockley's 1945 field-effect idea =================
        shock = cameo("modern", 0.65)
        shock[2][1][0].set_fill(opacity=0)     # clean-shaven (stylised)
        s_name = serif("William Shockley", 22, INK).next_to(shock, DOWN, buff=0.12)
        s_role = note("group leader", 16).next_to(s_name, DOWN, buff=0.05)
        sw = VGroup(shock, s_name, s_role).move_to([-5.0, 0.6, 0])
        place2 = serif("1945 · the obvious design", 22, SEPIA, italic=True).move_to([0, 3.15, 0])
        fx = 1.3
        semi = Rectangle(width=5.2, height=0.6, color=INK, stroke_width=2.5, fill_color="#b9b2a4",
                         fill_opacity=1).move_to([fx, -0.6, 0])
        semi_l = note("thin layer of semiconductor", 16).next_to(semi, DOWN, buff=0.15)
        cplate = Rectangle(width=4.0, height=0.2, color=INK, stroke_width=2, fill_color=INK,
                           fill_opacity=0.8).move_to([fx, 0.65, 0])
        plus = VGroup(*[serif("+", 26, RED_INK).move_to([fx - 1.6 + 0.4 * i, 1.0, 0]) for i in range(9)])
        cplate_l = note("charged plate", 16).next_to(cplate, RIGHT, buff=0.25)
        field = VGroup(*[Arrow([fx - 1.6 + 0.8 * i, 0.5, 0], [fx - 1.6 + 0.8 * i, -0.25, 0], buff=0,
                               color=SEPIA, stroke_width=2, tip_length=0.12) for i in range(5)])
        cur_in = Arrow([fx - 3.6, -0.6, 0], [fx - 2.65, -0.6, 0], buff=0, color=BLUE_INK, stroke_width=3,
                       tip_length=0.15)
        cur_out = Arrow([fx + 2.65, -0.6, 0], [fx + 3.6, -0.6, 0], buff=0, color=BLUE_INK, stroke_width=3,
                        tip_length=0.15)
        cur_l = serif("current", 18, BLUE_INK, italic=True).next_to(cur_out, UP, buff=0.1)
        sch = note("schematic", 15).move_to([fx + 2.7, 1.55, 0])
        line("The obvious design came from their boss, William Shockley, in 1945.",
             FadeIn(sw, shift=UP * 0.15), FadeIn(place2), run_time=1.0)
        self.play(FadeIn(semi), FadeIn(semi_l), GrowArrow(cur_in), GrowArrow(cur_out), FadeIn(cur_l), FadeIn(sch),
                  run_time=0.9)
        self.vo_wait()
        line("Hold a charged plate near a thin layer of semiconductor, and its electric field should pull in extra electrons, and let more current flow.",
             FadeIn(cplate), FadeIn(plus), FadeIn(cplate_l), run_time=0.8)
        rng = np.random.default_rng(45)
        hope = VGroup(*[Dot([fx + rng.uniform(-2.4, 2.4), -0.6 + rng.uniform(-0.2, 0.2), 0], radius=0.05,
                            color=BLUE_INK) for _ in range(26)])
        big_out = Arrow([fx + 2.65, -0.6, 0], [fx + 3.9, -0.6, 0], buff=0, color=BLUE_INK, stroke_width=8,
                        tip_length=0.25)
        expect = serif("expected: more current", 20, BLUE_INK, italic=True).move_to([fx + 2.5, -1.6, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=0.15), run_time=1.0)
        self.play(FadeIn(hope, lag_ratio=0.05), Transform(cur_out, big_out), FadeIn(expect), run_time=1.2)
        self.vo_wait()
        small_out = Arrow([fx + 2.65, -0.6, 0], [fx + 3.6, -0.6, 0], buff=0, color=BLUE_INK, stroke_width=3,
                          tip_length=0.15)
        fail = stamp(r"\text{did not work as planned}", size=30).move_to([fx, 2.05, 0])
        line("It did not work as planned.", FadeOut(hope), Transform(cur_out, small_out), FadeOut(expect),
             run_time=0.8)
        self.play(FadeIn(fail, scale=1.2), run_time=0.5)
        self.vo_wait()

        # Bardeen and surface states
        bardeen = cameo("modern", 0.65)
        bardeen[2][1][0].set_fill(opacity=0)
        bd_name = serif("John Bardeen", 22, INK).next_to(bardeen, DOWN, buff=0.12)
        bd_role = note("theorist", 16).next_to(bd_name, DOWN, buff=0.05)
        bdw = VGroup(bardeen, bd_name, bd_role).move_to([-5.0, 0.6, 0])
        trapped = VGroup(*[Dot([fx - 2.45 + 0.21 * i, semi.get_top()[1] - 0.07, 0], radius=0.05, color=RED_INK)
                           for i in range(24)])
        short_field = VGroup(*[Arrow([fx - 1.6 + 0.8 * i, 0.5, 0], [fx - 1.6 + 0.8 * i, -0.18, 0], buff=0,
                                     color=SEPIA, stroke_width=2, tip_length=0.12) for i in range(5)])
        ss_l = serif("electrons trapped at the surface", 20, RED_INK, italic=True).move_to([fx, -1.6, 0])
        line("The theorist John Bardeen worked out why: electrons trapped at the crystal's surface were blocking the field, like a crowd jammed in a doorway.",
             FadeOut(sw), FadeIn(bdw, shift=UP * 0.15), FadeOut(fail), run_time=0.9)
        self.play(FadeIn(trapped, lag_ratio=0.05), Transform(field, short_field), FadeOut(semi_l), FadeIn(ss_l),
             run_time=1.4)
        self.play(Indicate(trapped, color=RED_INK, scale_factor=1.15), run_time=1.0)
        self.vo_wait()
        line("The gold wedge was Bardeen and Brattain's way around it.",
             run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(semi, cplate, plus, cplate_l, field, cur_in, cur_out, cur_l, sch, trapped,
                                          ss_l, bdw, place2)), run_time=0.8)

        # ================= December 23 demonstration =================
        place3 = serif("December 23, 1947 · a demonstration for Bell Labs executives", 22, SEPIA,
                       italic=True).move_to([0, 3.15, 0])
        mic = VGroup(Circle(radius=0.32, color=INK, stroke_width=2.5, fill_color=PAPER_DARK, fill_opacity=1),
                     Line([0, -0.32, 0], [0, -1.0, 0], color=INK, stroke_width=3),
                     Line([-0.35, -1.0, 0], [0.35, -1.0, 0], color=INK, stroke_width=3)).move_to([-4.6, 0.6, 0])
        box = RoundedRectangle(corner_radius=0.1, width=2.0, height=1.2, color=INK, stroke_width=2.5,
                               fill_color=PAPER_DARK, fill_opacity=1).move_to([0, 0.6, 0])
        mini_wedge = Polygon([-0.35, 0.95, 0], [0.35, 0.95, 0], [0, 0.35, 0], color=INK, stroke_width=1.5,
                             fill_color="#d8d0c0", fill_opacity=1)
        mini_slab = Rectangle(width=1.2, height=0.22, color=INK, stroke_width=1.5, fill_color="#b9b2a4",
                              fill_opacity=1).move_to([0, 0.24, 0])
        amp_g = VGroup(box, mini_wedge, mini_slab)
        amp_l = note("the point-contact amplifier", 16).next_to(box, DOWN, buff=0.2)
        cone = Polygon([3.9, 0.85, 0], [4.6, 1.3, 0], [4.6, -0.1, 0], [3.9, 0.35, 0], color=INK, stroke_width=2.5,
                       fill_color=PAPER_DARK, fill_opacity=1)
        mag2 = Rectangle(width=0.35, height=0.5, color=INK, stroke_width=2.5, fill_color=INK,
                         fill_opacity=0.8).move_to([3.72, 0.6, 0])
        spk = VGroup(cone, mag2)
        l1 = wire((-4.28, 0.6), (-1.0, 0.6))
        l2 = wire((1.0, 0.6), (3.55, 0.6))
        sw_in = wave(-3.8, -1.6, 1.3, 0.08, cycles=4)
        sw_out = wave(1.4, 3.3, 1.3, 0.38, cycles=4)
        arcs = VGroup(*[Arc(radius=0.4 + 0.3 * k, start_angle=-0.6, angle=1.2, color=RED_INK, stroke_width=2.5)
                        .move_arc_center_to([4.6, 0.6, 0]) for k in range(3)])
        line("A week later, someone spoke through it for the lab's executives, and was heard, amplified.",
             FadeIn(place3), FadeIn(VGroup(mic, amp_g, spk, l1, l2)), FadeIn(amp_l), run_time=1.0)
        self.play(Create(sw_in), run_time=0.9)
        self.play(TransformFromCopy(sw_in, sw_out), run_time=0.9)
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.3), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(mic, amp_g, amp_l, spk, l1, l2, sw_in, sw_out, arcs)), run_time=0.7)

        # ================= Shockley's reaction =================
        sh = cameo("modern", 0.7)
        sh[2][1][0].set_fill(opacity=0)
        shn = serif("William Shockley", 22, INK).next_to(sh, DOWN, buff=0.12)
        shw = VGroup(sh, shn).move_to([-4.9, 0.4, 0])
        gift = serif("“a magnificent Christmas present”", 34, RED_INK, italic=True).move_to([1.4, 1.5, 0])
        line("Shockley called it a magnificent Christmas present.", FadeIn(shw, shift=UP * 0.15), FadeIn(gift),
             run_time=0.9)
        self.vo_wait()
        q = VGroup(serif("“My elation with the group's success was balanced", 26, INK, italic=True),
                   serif("by the frustration of not being one of the inventors.”", 26, INK, italic=True),
                   note("Shockley, as quoted in Electronic News, 1972", 16)).arrange(DOWN, buff=0.14)
        q[2].shift(DOWN * 0.1)
        qc = ink_card(q, pad=0.3).move_to([1.4, -0.5, 0])
        line("But he later admitted that his elation was balanced by the frustration of not being one of the inventors.",
             FadeIn(qc, shift=UP * 0.1), gift.animate.set_opacity(0.35), run_time=1.0)
        self.vo_wait()
        self.play(FadeOut(qc), FadeOut(gift), FadeOut(place3), run_time=0.6)

        # Chicago, New Year's Eve
        place4 = serif("Chicago · New Year's Eve, 1947", 22, SEPIA, italic=True).move_to([0, 3.15, 0])
        pages = VGroup()
        for k in range(30):
            pg = Rectangle(width=1.3, height=1.7, color=INK, stroke_width=1.2, fill_color=PAPER, fill_opacity=1)
            lines_ = VGroup(*[Line([-0.45, 0.6 - 0.2 * j, 0], [0.45 - 0.25 * ((j + k) % 3) * 0.5, 0.6 - 0.2 * j, 0],
                                   color=FADED, stroke_width=1) for j in range(7)])
            pg = VGroup(pg, lines_).rotate((k % 5 - 2) * 3 * DEGREES)
            pg.move_to([0.0 + (k % 10) * 0.45, 1.3 - (k // 10) * 1.0 - 0.02 * k, 0])
            pages.add(pg)
        cnt = serif("about 30 pages of notes", 22, RED_INK, italic=True).move_to([2.0, -2.3, 0])
        line("He spent New Year's Eve alone in a Chicago hotel, filling about thirty pages of notes.",
             FadeIn(place4), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.1) for p in pages], lag_ratio=0.12), run_time=2.4)
        self.play(FadeIn(cnt), run_time=0.5)
        self.vo_wait()

        # January 23, 1948: the sandwich
        place5 = serif("January 23, 1948", 22, SEPIA, italic=True).move_to([0, 3.15, 0])
        sx = 1.6
        n1 = Rectangle(width=2.0, height=1.4, stroke_width=2.5, color=INK, fill_color=N_COL, fill_opacity=1)
        p1 = Rectangle(width=0.6, height=1.4, stroke_width=2.5, color=INK, fill_color=P_COL, fill_opacity=1)
        n2 = Rectangle(width=2.0, height=1.4, stroke_width=2.5, color=INK, fill_color=N_COL, fill_opacity=1)
        sand = VGroup(n1, p1, n2).arrange(RIGHT, buff=0).move_to([sx, 0.4, 0])
        sand_l = VGroup(*[serif(t, 34, INK).move_to(r) for t, r in zip("NPN", sand)])
        nopts = note("no delicate points", 18).next_to(sand, DOWN, buff=0.3)
        line("Then, on January the twenty-third, 1948, he found a different design: a sandwich of crystal, with no delicate points.",
             FadeOut(pages), FadeOut(cnt), ReplacementTransform(place4, place5), run_time=0.8)
        self.play(FadeIn(sand, lag_ratio=0.3), run_time=1.0)
        self.play(FadeIn(sand_l), FadeIn(nopts), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(shw, place5, nopts)), VGroup(sand, sand_l).animate.scale(0.5).move_to(
            [5.0, 2.6, 0]), run_time=0.8)

        # ================= doping =================
        lat_c = np.array([-1.0, 0.3, 0])
        cols, rows, sp = 7, 4, 0.85
        atoms, bonds = VGroup(), VGroup()
        pos = {}
        for i in range(cols):
            for j in range(rows):
                p = lat_c + np.array([(i - (cols - 1) / 2) * sp, (j - (rows - 1) / 2) * sp, 0])
                pos[(i, j)] = p
        for (i, j), p in pos.items():
            if i + 1 < cols:
                bonds.add(Line(p, pos[(i + 1, j)], color=SEPIA, stroke_width=2))
            if j + 1 < rows:
                bonds.add(Line(p, pos[(i, j + 1)], color=SEPIA, stroke_width=2))
        bound = VGroup()
        for b in bonds:
            m = b.get_center()
            d = b.get_unit_vector()
            nrm = np.array([-d[1], d[0], 0])
            bound.add(Dot(m + nrm * 0.07, radius=0.035, color=BLUE_INK), Dot(m - nrm * 0.07, radius=0.035,
                                                                               color=BLUE_INK))
        for (i, j), p in pos.items():
            atoms.add(Circle(radius=0.2, color=INK, stroke_width=2, fill_color=PAPER_DARK, fill_opacity=1).move_to(p))
        lat_l = note("a pure crystal (germanium or silicon), schematic", 17).move_to([lat_c[0], -1.75, 0])
        bond_l = note("electrons locked in bonds", 17).move_to([4.2, 0.3, 0])
        line("To see how it works, start with a pure crystal of germanium or silicon. Its electrons are locked into bonds, so it barely conducts.",
             FadeIn(bonds), FadeIn(atoms), FadeIn(lat_l), run_time=1.0)
        self.play(FadeIn(bound, lag_ratio=0.01), FadeIn(bond_l), run_time=1.0)
        self.vo_wait()
        # phosphorus
        pa = atoms[2 * rows + 2]
        pP = pa.get_center()
        p_atom = VGroup(Circle(radius=0.22, color=RED_INK, stroke_width=2.5, fill_color=PAPER, fill_opacity=1),
                        serif("P", 20, RED_INK, bold=True)).move_to(pP)
        free_e = Dot(pP + np.array([0.35, 0.3, 0]), radius=0.06, color=BLUE_INK)
        n_l = serif("N-type: spare electrons", 26, BLUE_INK).move_to([4.2, 1.3, 0])
        line("Add a trace of phosphorus, and each phosphorus atom brings one spare electron, free to roam. That is N-type.",
             FadeOut(bond_l), FadeIn(p_atom), run_time=0.8)
        self.play(FadeIn(free_e, scale=2), run_time=0.4)
        path = VMobject().set_points_smoothly([free_e.get_center(), pP + [1.2, 0.8, 0], pP + [2.1, -0.2, 0],
                                               pP + [2.9, 0.75, 0], pP + [3.3, -0.5, 0]])
        self.play(MoveAlongPath(free_e, path), FadeIn(n_l), run_time=2.0, rate_func=linear)
        self.vo_wait()
        # boron
        ba = atoms[4 * rows + 1]
        bP = ba.get_center()
        b_atom = VGroup(Circle(radius=0.22, color=SEPIA, stroke_width=2.5, fill_color=PAPER, fill_opacity=1),
                        serif("B", 20, SEPIA, bold=True)).move_to(bP)
        # find the bond electron next to boron on its right-hand bond and remove it -> a hole
        hole_pos = (bP + pos[(5, 1)]) / 2 + np.array([0, 0.07, 0])
        victim = min(bound, key=lambda d: np.linalg.norm(d.get_center() - hole_pos))
        hole = Circle(radius=0.09, color=RED_INK, stroke_width=2.5).move_to(victim.get_center())
        p_l = serif("P-type: holes", 26, RED_INK).move_to([4.2, -0.9, 0])
        line("Add boron instead, and each boron atom leaves a gap where an electron is missing.",
             FadeIn(b_atom), run_time=0.8)
        self.play(victim.animate.set_opacity(0), FadeIn(hole), run_time=0.6)
        self.vo_wait()
        # hole hops: a neighbouring electron fills it, so the gap moves the other way
        line("The gap moves like a positive charge. We call it a hole. That is P-type.", run_time=0.6)
        hop_targets = [(4, 1, 4, 2), (3, 2, 4, 2), (3, 2, 3, 3)]
        current = victim
        for (i0, j0, i1, j1) in hop_targets:
            mid = (pos[(i0, j0)] + pos[(i1, j1)]) / 2
            nb = min([d for d in bound if d is not victim], key=lambda d: np.linalg.norm(d.get_center() - mid))
            src = nb.get_center()
            self.play(nb.animate.move_to(hole.get_center()), hole.animate.move_to(src), run_time=0.6)
        self.play(FadeIn(p_l), run_time=0.5)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(atoms, bonds, bound, p_atom, free_e, b_atom, hole, lat_l)),
                  FadeOut(VGroup(n_l, p_l)), run_time=0.8)

        # ================= the sandwich at work =================
        X0, XB0, XB1, X1 = -3.6, -0.35, 0.35, 3.6
        Y0, Y1 = -0.4, 1.0
        e_reg = Rectangle(width=XB0 - X0, height=Y1 - Y0, stroke_width=2.5, color=INK, fill_color=N_COL,
                          fill_opacity=1).move_to([(X0 + XB0) / 2, (Y0 + Y1) / 2, 0])
        b_reg = Rectangle(width=XB1 - XB0, height=Y1 - Y0, stroke_width=2.5, color=INK, fill_color=P_COL,
                          fill_opacity=1).move_to([0, (Y0 + Y1) / 2, 0])
        c_reg = Rectangle(width=X1 - XB1, height=Y1 - Y0, stroke_width=2.5, color=INK, fill_color=N_COL,
                          fill_opacity=1).move_to([(XB1 + X1) / 2, (Y0 + Y1) / 2, 0])
        bar = VGroup(e_reg, b_reg, c_reg)
        e_t = serif("N", 30, INK).move_to([(X0 + XB0) / 2, Y1 + 0.35, 0])
        b_t = serif("P", 30, INK).move_to([0, Y1 + 0.35, 0])
        c_t = serif("N", 30, INK).move_to([(XB1 + X1) / 2, Y1 + 0.35, 0])
        e_n = note("emitter", 17).next_to(e_t, RIGHT, buff=0.25)
        c_n = note("collector", 17).next_to(c_t, RIGHT, buff=0.25)
        tags = VGroup(e_t, b_t, c_t, e_n, c_n)
        line("Shockley's sandwich is N-type, then a very thin slice of P-type, then N-type again.",
             FadeOut(VGroup(sand, sand_l)), FadeIn(bar, lag_ratio=0.3), FadeIn(tags), run_time=1.2)
        self.vo_wait()
        # main circuit: battery under the bar, from collector (+) back to emitter (-)
        yb = -1.55
        main_l = wire((X0, (Y0 + Y1) / 2), (X0 - 0.4, (Y0 + Y1) / 2), (X0 - 0.4, yb), (-0.08, yb))
        main_r = wire((X1, (Y0 + Y1) / 2), (X1 + 0.4, (Y0 + Y1) / 2), (X1 + 0.4, yb), (0.08, yb))
        batt = battery_h(0, yb, "battery")
        # plus on the right side for the collector: mirror the symbol
        batt = VGroup(Line([0.08, yb - 0.32, 0], [0.08, yb + 0.32, 0], color=INK, stroke_width=3),
                      Line([-0.08, yb - 0.17, 0], [-0.08, yb + 0.17, 0], color=INK, stroke_width=5),
                      serif("+", 18, FADED).move_to([0.3, yb + 0.32, 0]))
        meter = VGroup(Circle(radius=0.32, color=INK, stroke_width=2, fill_color=PAPER, fill_opacity=1),
                       serif("A", 20, INK)).move_to([X1 + 0.4, -0.65, 0])
        big_i = ValueTracker(0.0)
        needle = always_redraw(lambda: Line(meter[0].get_center(), meter[0].get_center() + 0.26 * np.array(
            [np.sin(-1.0 + 2.0 * big_i.get_value()), np.cos(-1.0 + 2.0 * big_i.get_value()), 0]),
            color=RED_INK, stroke_width=2.5))
        nothing = serif("almost nothing flows", 22, RED_INK, italic=True).move_to([0, -2.3, 0])
        block = Line([XB0 + 0.04, Y0 + 0.05, 0], [XB0 + 0.04, Y1 - 0.05, 0], color=RED_INK, stroke_width=6)
        line("Put a battery across it, and almost nothing flows.", Create(main_l), Create(main_r), FadeIn(batt),
             FadeIn(meter), FadeIn(needle), run_time=1.0)
        self.vo_wait()
        line("The middle layer blocks the electrons.", FadeIn(nothing), Create(block), run_time=0.8)
        self.vo_wait()
        # base current
        base_w = wire((0, Y1), (0, 2.1), (-1.2, 2.1))
        base_l = serif("base", 22, INK, italic=True).move_to([0.55, 1.75, 0])
        small_i = Arrow([-1.2, 2.1, 0], [-0.3, 2.1, 0], buff=0, color=RED_INK, stroke_width=3, tip_length=0.14)
        small_l = serif("tiny current", 18, RED_INK, italic=True).next_to(small_i, UP, buff=0.08)
        line("Now feed a tiny current into that middle layer, the base.", FadeOut(nothing), Create(base_w),
             FadeIn(base_l), run_time=0.8)
        self.play(GrowArrow(small_i), FadeIn(small_l), FadeOut(block), run_time=0.7)
        self.vo_wait()
        carriers = Carriers(X0, XB0, XB1, X1, Y0, Y1)
        self.add(carriers)
        holes = VGroup(*[Circle(radius=0.05, color=RED_INK, stroke_width=2).move_to([0, Y0 + 0.2 + 0.25 * k, 0])
                         for k in range(5)])
        line("Electrons pour in from the left.", FadeIn(holes), run_time=0.6)
        carriers.rate = 1.0
        self.play(big_i.animate.set_value(0.85), run_time=2.0)
        self.vo_wait()
        line("The base is so thin that most of them never meet a hole, and are swept into the far side.", run_time=0.6)
        self.vo_wait()
        big_arrow = Arrow([X1 - 1.9, -0.75, 0], [X1 - 0.4, -0.75, 0], buff=0, color=BLUE_INK, stroke_width=9,
                          tip_length=0.3)
        big_l = serif("large current", 20, BLUE_INK, italic=True).next_to(big_arrow, DOWN, buff=0.08)
        ratio = MathTex(r"I_{\text{collector}} \approx 100 \times I_{\text{base}}", font_size=34,
                        color=RED_INK).move_to([-4.3, 2.6, 0])
        ratio_n = note("typical; varies from transistor to transistor", 15).next_to(ratio, DOWN, buff=0.1)
        amp_w = serif("amplification", 30, RED_INK, bold=True).move_to([0, -2.35, 0])
        line("So a small current in the base controls a current many times larger, often around a hundred times. That is amplification.",
             GrowArrow(big_arrow), FadeIn(big_l), run_time=1.0)
        self.play(Write(ratio), FadeIn(ratio_n), run_time=1.0)
        self.play(FadeIn(amp_w, scale=0.9), run_time=0.6)
        self.vo_wait()
        sw_w = serif("a switch", 30, RED_INK, bold=True).move_to([0, -2.35, 0])
        line("Stop the small current, and the big one stops too. That is a switch.", FadeOut(small_i), FadeOut(small_l),
             run_time=0.6)
        carriers.rate = 0.0
        self.play(big_i.animate.set_value(0.0), FadeOut(big_arrow), FadeOut(big_l), run_time=1.6)
        self.play(ReplacementTransform(amp_w, sw_w), run_time=0.6)
        self.vo_wait()
        carriers.stop_all()
        carriers.clear_updaters()
        self.play(clear(), FadeOut(VGroup(bar, tags, main_l, main_r, batt, meter, needle, base_w, base_l, holes,
                                          ratio, ratio_n, sw_w)), run_time=0.8)
        self.remove(carriers)

        # ================= what happened next =================
        tl = Line([-5.6, 0.2, 0], [5.6, 0.2, 0], color=INK, stroke_width=2)
        events = [(1947, "point contact"), (1948, "sandwich idea"), (1951, "junction transistors\nannounced"),
                  (1952, "beat point-contact"), (1956, "Nobel Prize"), (1960, "MOS field-effect\ntransistor")]

        def tx(y):
            return -5.2 + (y - 1947) * 10.4 / 13

        ticks, labs = VGroup(), VGroup()
        for k, (yr, txt) in enumerate(events):
            x = tx(yr)
            ticks.add(Line([x, 0.05, 0], [x, 0.35, 0], color=INK, stroke_width=2.5))
            yr_t = serif(str(yr), 20, SEPIA).move_to([x, 0.62 if k % 2 == 0 else -0.25, 0])
            lab_t = VGroup(*[note(s, 15) for s in txt.split("\n")]).arrange(DOWN, buff=0.04)
            lab_t.next_to(yr_t, UP if k % 2 == 0 else DOWN, buff=0.1)
            labs.add(VGroup(yr_t, lab_t))
        line("Bell Labs announced working junction transistors in 1951, and within a year they beat the best point-contact devices.",
             Create(tl), FadeIn(ticks[:2]), FadeIn(labs[:2]), run_time=0.9)
        self.play(FadeIn(ticks[2]), FadeIn(labs[2]), run_time=0.8)
        self.play(FadeIn(ticks[3]), FadeIn(labs[3]), run_time=0.7)
        self.vo_wait()
        nob = ink_card(VGroup(serif("Nobel Prize in Physics, 1956", 26, INK),
                              note("Shockley, Bardeen and Brattain, “for their researches on semiconductors", 16),
                              note("and their discovery of the transistor effect”", 16)).arrange(DOWN, buff=0.1))
        nob.move_to([0, -2.0, 0])
        line("In 1956 all three shared the Nobel Prize in Physics, though by then they were no longer working together.",
             FadeIn(ticks[4]), FadeIn(labs[4]), FadeIn(nob, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()
        self.play(clear(), FadeOut(nob), run_time=0.6)

        # ================= the twist: MOS =================
        line("And here is the twist.", FadeIn(ticks[5]), FadeIn(labs[5]), run_time=0.7)
        self.wait(0.3)
        self.play(FadeOut(VGroup(tl, ticks, labs)), run_time=0.6)
        place6 = serif("Bell Labs · 1959–60", 22, SEPIA, italic=True).move_to([0, 3.15, 0])
        mx = 0.0
        semi2 = Rectangle(width=5.6, height=0.7, color=INK, stroke_width=2.5, fill_color="#b9b2a4",
                          fill_opacity=1).move_to([mx, -0.7, 0])
        oxide = Rectangle(width=3.6, height=0.2, color=INK, stroke_width=1.5, fill_color="#e9f0f2",
                          fill_opacity=1).next_to(semi2, UP, buff=0)
        gate = Rectangle(width=3.6, height=0.25, color=INK, stroke_width=2, fill_color=INK,
                         fill_opacity=0.8).next_to(oxide, UP, buff=0)
        ox_l = serif("thin oxide layer", 20, RED_INK, italic=True).next_to(oxide, LEFT, buff=0.35)
        gate_l = note("gate (the charged plate)", 16).next_to(gate, UP, buff=0.15)
        names = note("Mohamed Atalla and Dawon Kahng", 18).move_to([0, 2.55, 0])
        chan = VGroup(*[Dot([mx - 1.6 + 0.16 * i, semi2.get_top()[1] - 0.1, 0], radius=0.045, color=BLUE_INK)
                        for i in range(21)])
        flow = Arrow([mx - 3.6, -0.55, 0], [mx + 3.9, -0.55, 0], buff=0, color=BLUE_INK, stroke_width=6,
                     tip_length=0.25).set_opacity(0)
        mos_sch = note("MOS field-effect transistor (schematic)", 16).next_to(semi2, DOWN, buff=0.2)
        self.vo_wait()
        line("By 1960, Mohamed Atalla and Dawon Kahng at Bell Labs had tamed the surface with a thin layer of oxide.",
             FadeIn(place6), FadeIn(names), FadeIn(semi2), FadeIn(mos_sch), run_time=1.0)
        self.play(FadeIn(oxide, shift=DOWN * 0.1), FadeIn(ox_l), run_time=0.8)
        self.play(FadeIn(gate), FadeIn(gate_l), run_time=0.6)
        self.vo_wait()
        line("Shockley's failed field-effect idea came back to life.", FadeIn(chan, lag_ratio=0.05), run_time=1.0)
        self.play(flow.animate.set_opacity(1), run_time=0.6)
        self.vo_wait()
        pct = serif("over 99% of microchips use MOS transistors", 24, RED_INK, italic=True).move_to([0, -2.25, 0])
        line("Today, over ninety-nine percent of microchips are built from these field-effect transistors.",
             FadeOut(mos_sch), FadeIn(pct), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(place6, semi2, oxide, gate, ox_l, gate_l, names, chan, flow, pct)),
                  run_time=0.8)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 24, RED_INK).move_to([0, 3.05, 0])
        parts = VGroup(note("1 NPN transistor (e.g. 2N3904 or BC547)", 18), note("9 V battery", 18),
                       note("1 LED", 18), note("2 resistors, about 1 kΩ", 18), note("2 bare wires", 18)
                       ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        parts_c = ink_card(parts, pad=0.25).move_to([-3.95, 0.35, 0])
        # circuit on the right
        T = npn_sym(2.2, -0.1)
        bx = 4.6          # battery + rail x
        top_y, bot_y = 2.3, -1.9
        rail_p = wire((bx, 0.2), (bx, top_y), (T.c[0], top_y))
        led_d = led_sym(T.c[0], 1.75)
        r1 = resistor_v(T.c[0], 1.3, 0.85)
        col_w = VGroup(wire((T.c[0], top_y), (T.c[0], 1.93)), wire((T.c[0], 1.57), (T.c[0], 1.3)),
                       wire((T.c[0], 0.85), T.c))
        rail_n = wire(T.e, (T.e[0], bot_y), (bx, bot_y), (bx, -0.2))
        batt2 = VGroup(Line([bx - 0.32, 0.08, 0], [bx + 0.32, 0.08, 0], color=INK, stroke_width=3),
                       Line([bx - 0.17, -0.08, 0], [bx + 0.17, -0.08, 0], color=INK, stroke_width=5),
                       serif("+", 18, FADED).move_to([bx + 0.45, 0.25, 0]),
                       note("9 V", 16).move_to([bx + 0.6, -0.25, 0]))
        r2 = resistor_h(T.b[0] - 1.1, T.b[0] - 0.4, T.b[1])
        base_w2 = VGroup(wire((T.b[0] - 0.4, T.b[1]), T.b), wire((T.b[0] - 1.1, T.b[1]), (T.b[0] - 1.6, T.b[1]),
                                                                 (T.b[0] - 1.6, 1.0)))
        pad1 = Dot([T.b[0] - 1.6, 1.0, 0], radius=0.09, color=SEPIA)
        pos_w = wire((bx, top_y), (bx, top_y), (T.b[0] - 1.2, top_y), (T.b[0] - 1.2, 1.25))
        pad2 = Dot([T.b[0] - 1.2, 1.25, 0], radius=0.09, color=SEPIA)
        pads_l = note("touch here", 16).move_to([T.b[0] - 0.5, 1.3, 0])
        lab_c = note("collector", 15).next_to(T.c, RIGHT, buff=0.15).shift(DOWN * 0.2)
        lab_e = note("emitter", 15).next_to(T.e, RIGHT, buff=0.15).shift(UP * 0.2)
        lab_b = note("base", 15).next_to(T.b, UP, buff=0.1).shift(LEFT * 0.15)
        lab_r1 = note("1 kΩ", 15).next_to(r1, LEFT, buff=0.15)
        lab_r2 = note("1 kΩ", 15).next_to(r2, DOWN, buff=0.12)
        lab_led = note("LED", 15).next_to(led_d[0], LEFT, buff=0.15)
        circuit = VGroup(rail_p, col_w, led_d, r1, T, rail_n, batt2)
        line("Try it yourself. You need an N P N transistor, a nine-volt battery, an L.E.D., and two one-thousand-ohm resistors.",
             FadeIn(tiy), FadeIn(parts_c, shift=UP * 0.1), run_time=1.0)
        self.vo_wait()
        led_d[2].set_opacity(0.15)
        line("Wire plus through the L.E.D. and a resistor to the collector, and the emitter to minus.",
             Create(rail_p), FadeIn(T), FadeIn(batt2), run_time=1.0)
        self.play(FadeIn(led_d), Create(col_w), Create(r1), FadeIn(VGroup(lab_c, lab_led, lab_r1)), run_time=1.0)
        self.play(Create(rail_n), FadeIn(lab_e), run_time=0.8)
        self.vo_wait()
        line("Run the base through the other resistor to a bare wire, and put a second bare wire on plus.",
             Create(r2), Create(base_w2), FadeIn(pad1), FadeIn(lab_b), FadeIn(lab_r2), run_time=1.0)
        self.play(Create(pos_w), FadeIn(pad2), FadeIn(pads_l), run_time=0.8)
        self.vo_wait()
        finger = Ellipse(width=0.55, height=0.9, color=INK, stroke_width=2, fill_color="#e5c6a8",
                         fill_opacity=1).rotate(30 * DEGREES).move_to([T.b[0] - 1.4, 1.65, 0])
        skin = DashedLine(pad1.get_center(), pad2.get_center(), color=RED_INK, stroke_width=2.5)
        line("Touch both wires with one finger.", FadeIn(finger, shift=DOWN * 0.3), run_time=0.8)
        self.play(finger.animate.move_to([T.b[0] - 1.4, 1.12, 0]), Create(skin), run_time=0.6)
        self.vo_wait()
        line("The tiny current through your skin switches on a much larger one, and the L.E.D. lights.",
             run_time=0.6)
        halo = Circle(radius=0.45, stroke_width=0, fill_color=GLOW, fill_opacity=0).move_to(led_d[0])
        self.add(halo)
        self.bring_to_front(led_d)
        self.play(led_d[0].animate.set_fill(GLOW, opacity=1), led_d[2].animate.set_opacity(1),
                  halo.animate.set_fill(opacity=0.5), run_time=0.8)
        self.vo_wait()
        safe = note("9 V battery only, never mains · keep the resistors in", 17).next_to(tiy, DOWN, buff=0.15)
        line("If the glow is faint, dampen your fingertip.", FadeIn(safe), run_time=0.8)
        self.vo_wait()
        self.wait(0.4)
        self.play(clear(), FadeOut(VGroup(tiy, parts_c, circuit, r2, base_w2, pad1, pad2, pos_w, pads_l, lab_c,
                                          lab_e, lab_b, lab_r1, lab_r2, lab_led, finger, skin, halo, safe)),
                  run_time=0.8)

        # ================= end card =================
        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after Jon Gertner, The Idea Factory (Penguin Press, 2012) · sources in the episode notes",
                          17),
                     note("facts checked against the Computer History Museum, PBS Transistorized! and nobelprize.org", 17),
                     note("silhouettes are stylised, not likenesses · device drawings are schematic · "
                          "animated with Manim · synthetic narration", 15)).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(1.6)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)
