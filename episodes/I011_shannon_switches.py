"""I011 The Most Important Master's Thesis, a Science Stories episode.

After J. Soni and R. Goodman, A Mind at Play (Simon & Schuster, 2017). Script and sources: episodes/I011_script.md

Render:  manim -qh --frame_rate 30 episodes/I011_shannon_switches.py ShannonSwitches
Then:    scripts/finish_video.sh media/videos/I011_shannon_switches/1080p30/ShannonSwitches.mp4 out/I011_shannon_switches.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

GLOW = "#e8b14a"
OPEN_ANGLE = 32 * DEGREES


# ---------------- circuit parts ----------------
def wire(*pts, color=INK, width=2.5):
    pts = [np.array([p[0], p[1], 0]) for p in pts]
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners(pts)
    return m


class Switch(VGroup):
    """A knife switch between (x0, y) and (x1, y). Lever pivots at the left terminal."""

    def __init__(self, x0, x1, y, label=None, closed=False, size=26, color=INK, **kw):
        super().__init__(**kw)
        self.p0 = np.array([x0, y, 0])
        self.p1 = np.array([x1, y, 0])
        self.closed = closed
        self.t0 = Dot(self.p0, radius=0.06, color=color)
        self.t1 = Dot(self.p1, radius=0.06, color=color)
        self.lever = Line(self.p0, self.p1 - np.array([0.02, 0, 0]), color=color, stroke_width=4)
        if not closed:
            self.lever.rotate(OPEN_ANGLE, about_point=self.p0)
        self.add(self.t0, self.t1, self.lever)
        if label:
            self.label = serif(label, size, RED_INK, italic=True).move_to(
                (self.p0 + self.p1) / 2 + UP * max(0.62, (x1 - x0) * np.sin(OPEN_ANGLE) + 0.3))
            self.add(self.label)

    def set(self, closed):
        if closed == self.closed:
            return None
        ang = -OPEN_ANGLE if closed else OPEN_ANGLE
        self.closed = closed
        return Rotate(self.lever, angle=ang, about_point=self.t0.get_center())


class Lamp(VGroup):
    def __init__(self, center, r=0.3, **kw):
        super().__init__(**kw)
        c = np.array([center[0], center[1], 0])
        self.glow = Circle(radius=r * 1.9, stroke_width=0, fill_color=GLOW, fill_opacity=0).move_to(c)
        self.bulb = Circle(radius=r, stroke_color=INK, stroke_width=2.5, fill_color=PAPER, fill_opacity=1).move_to(c)
        d = r * 0.7071
        self.cross = VGroup(Line(c + [-d, -d, 0], c + [d, d, 0], color=INK, stroke_width=2),
                            Line(c + [-d, d, 0], c + [d, -d, 0], color=INK, stroke_width=2))
        self.rays = VGroup(*[Line(c + r * 1.25 * np.array([np.cos(a), np.sin(a), 0]),
                                  c + r * 1.75 * np.array([np.cos(a), np.sin(a), 0]),
                                  color=GLOW, stroke_width=3, stroke_opacity=0)
                             for a in np.linspace(0, TAU, 9)[:-1]])
        self.lit = False
        self.add(self.glow, self.rays, self.bulb, self.cross)

    def set(self, on):
        if on == self.lit:
            return None
        self.lit = on
        return AnimationGroup(self.glow.animate.set_fill(opacity=0.55 if on else 0),
                              self.bulb.animate.set_fill(GLOW if on else PAPER, opacity=1),
                              self.rays.animate.set_stroke(opacity=1 if on else 0))


def battery_v(x, y):
    """Vertical-wire battery symbol centred at (x, y)."""
    long = Line([x - 0.32, y + 0.08, 0], [x + 0.32, y + 0.08, 0], color=INK, stroke_width=3)
    short = Line([x - 0.17, y - 0.08, 0], [x + 0.17, y - 0.08, 0], color=INK, stroke_width=5)
    plus = serif("+", 18, FADED).move_to([x + 0.48, y + 0.22, 0])
    return VGroup(long, short, plus)


def series_circuit():
    L, R, T, B = -2.4, 2.4, 1.0, -1.0
    a = Switch(-1.45, -0.55, T, "A")
    b = Switch(0.55, 1.45, T, "B")
    lamp = Lamp([R, 0])
    wires = VGroup(wire((L, 0.08), (L, T), (-1.45, T)), wire((-0.55, T), (0.55, T)),
                   wire((1.45, T), (R, T), (R, 0.3)), wire((R, -0.3), (R, B), (L, B), (L, -0.08)))
    g = VGroup(wires, battery_v(L, 0), a, b, lamp)
    return g, a, b, lamp


def parallel_circuit():
    L, R, T, B = -2.4, 2.4, 1.0, -1.0
    y2 = 0.05
    a = Switch(-0.45, 0.45, T, "A")
    b = Switch(-0.45, 0.45, y2, "B")
    b.label.next_to(b, DOWN, buff=0.1)
    lamp = Lamp([R, -0.35])
    wires = VGroup(wire((L, -0.27), (L, T), (-0.45, T)), wire((0.45, T), (R, T), (R, -0.05)),
                   wire((-1.3, T), (-1.3, y2), (-0.45, y2)), wire((0.45, y2), (1.3, y2), (1.3, T)),
                   wire((R, -0.65), (R, B), (L, B), (L, -0.43)))
    dots = VGroup(*[Dot([x, T, 0], radius=0.07, color=INK) for x in (-1.3, 1.3)])
    g = VGroup(wires, dots, battery_v(L, -0.35), a, b, lamp)
    return g, a, b, lamp


def truth_table(headers, rows, col_w=0.9, row_h=0.46, size=24):
    n = len(headers)
    cells = VGroup()
    head = VGroup(*[serif(h, size, SEPIA, italic=True).move_to([i * col_w, 0, 0]) for i, h in enumerate(headers)])
    body = VGroup()
    for r, row in enumerate(rows):
        body.add(VGroup(*[serif(str(v), size, INK).move_to([i * col_w, -(r + 1) * row_h, 0])
                          for i, v in enumerate(row)]))
    rule = Line([-col_w / 2, -row_h / 2, 0], [(n - 0.5) * col_w, -row_h / 2, 0], color=INK, stroke_width=1.5)
    split = Line([(n - 1.5) * col_w, row_h / 2 - 0.1, 0], [(n - 1.5) * col_w, -(len(rows) + 0.5) * row_h, 0],
                 color=INK, stroke_width=1)
    cells.add(head, rule, split, body)
    cells.head, cells.body = head, body
    return cells


def row_box(table, i):
    row = table.body[i]
    return SurroundingRectangle(row, color=RED_INK, buff=0.08, stroke_width=2, corner_radius=0.05)


def gear(center, r=0.35, teeth=10, color=SEPIA):
    c = np.array([center[0], center[1], 0])
    body = Circle(radius=r, color=color, stroke_width=2.5, fill_color=PAPER_DARK, fill_opacity=1).move_to(c)
    hub = Dot(c, radius=0.05, color=color)
    tt = VGroup(*[Line(c + r * np.array([np.cos(a), np.sin(a), 0]),
                       c + (r + 0.1) * np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=4)
                  for a in np.linspace(0, TAU, teeth + 1)[:-1]])
    spoke = Line(c, c + r * 0.85 * RIGHT, color=color, stroke_width=2)
    return VGroup(body, tt, hub, spoke)


def integrator(x, y):
    """A disc-and-wheel integrator: a flat disc seen at an angle and a small wheel resting on it."""
    disc = Ellipse(width=1.5, height=0.42, color=INK, stroke_width=2, fill_color=PAPER_DARK, fill_opacity=1)
    disc.move_to([x, y, 0])
    rim = Ellipse(width=1.5, height=0.42, color=INK, stroke_width=1).move_to([x, y - 0.08, 0])
    post = Line([x, y - 0.1, 0], [x, y - 0.75, 0], color=INK, stroke_width=3)
    wheel = Ellipse(width=0.14, height=0.5, color=RED_INK, stroke_width=2.5, fill_color=PAPER,
                    fill_opacity=1).move_to([x + 0.35, y + 0.22, 0])
    axle = Line([x + 0.35, y + 0.22, 0], [x + 0.35, y + 1.05, 0], color=RED_INK, stroke_width=2)
    return VGroup(post, rim, disc, wheel, axle)


def relay(x, y, energised=False):
    """Coil on the left, pivoting armature above it, a contact pair on the right (normally open)."""
    core = Rectangle(width=0.5, height=1.1, color=INK, stroke_width=2, fill_color=PAPER_DARK,
                     fill_opacity=1).move_to([x, y, 0])
    turns = VGroup(*[Line([x - 0.3, y - 0.45 + 0.1 * i, 0], [x + 0.3, y - 0.4 + 0.1 * i, 0], color=SEPIA,
                          stroke_width=2) for i in range(10)])
    pivot = Dot([x - 0.5, y + 0.85, 0], radius=0.06, color=INK)
    arm = Line([x - 0.5, y + 0.85, 0], [x + 1.6, y + 0.85, 0], color=INK, stroke_width=4)
    up = Line([x + 1.6, y + 0.75, 0], [x + 1.6, y + 0.85, 0], color=INK, stroke_width=0)
    contact_top = Dot([x + 1.6, y + 0.85, 0], radius=0.07, color=INK)
    contact_bot = Dot([x + 1.6, y + 0.58, 0], radius=0.07, color=INK)
    lead = Line([x + 1.6, y + 0.58, 0], [x + 2.4, y + 0.58, 0], color=INK, stroke_width=2.5)
    lead2 = Line([x - 0.5, y + 0.85, 0], [x - 1.0, y + 0.85, 0], color=INK, stroke_width=2.5)
    coil_leads = VGroup(Line([x - 0.25, y - 0.55, 0], [x - 0.25, y - 1.0, 0], color=INK, stroke_width=2),
                        Line([x + 0.25, y - 0.55, 0], [x + 0.25, y - 1.0, 0], color=INK, stroke_width=2))
    arm_group = VGroup(arm, contact_top)
    arm_group.rotate(6 * DEGREES, about_point=pivot.get_center())
    g = VGroup(core, turns, coil_leads, lead2, pivot, contact_bot, lead, arm_group, up)
    g.core, g.arm, g.pivot = core, arm_group, pivot
    return g


def two_terminal(branches, x_in=-2.2, x_out=2.2):
    """A two-terminal network. branches: list of (y, [labels]) with switches in series on each branch,
    or a special 'A then (B || C)' layout when branches == 'factored'."""
    g = VGroup()
    sw = []
    if branches == "factored":
        g.add(wire((x_in, 0), (-1.6, 0)))
        a = Switch(-1.6, -0.8, 0, "A", closed=False, size=24)
        g.add(a, wire((-0.8, 0), (-0.2, 0), (-0.2, 0.45), (0.2, 0.45)), wire((-0.2, 0), (-0.2, -0.45), (0.2, -0.45)))
        b = Switch(0.2, 1.0, 0.45, "B", closed=False, size=24)
        c = Switch(0.2, 1.0, -0.45, "C", closed=False, size=24)
        c.label.next_to(c, DOWN, buff=0.08)
        g.add(b, c, wire((1.0, 0.45), (1.4, 0.45), (1.4, -0.45), (1.0, -0.45)), wire((1.4, 0), (x_out, 0)))
        g.add(Dot([-0.2, 0, 0], radius=0.06, color=INK), Dot([1.4, 0, 0], radius=0.06, color=INK))
        sw = [a, b, c]
    else:
        ys = [y for y, _ in branches]
        nl = x_in + 0.5
        nr = x_out - 0.5
        g.add(wire((x_in, 0), (nl, 0)), wire((nr, 0), (x_out, 0)))
        g.add(wire((nl, max(ys)), (nl, min(ys))), wire((nr, max(ys)), (nr, min(ys))))
        g.add(Dot([nl, 0, 0], radius=0.06, color=INK), Dot([nr, 0, 0], radius=0.06, color=INK))
        for y, labels in branches:
            n = len(labels)
            span = (nr - nl - 0.4) / n
            x = nl + 0.2
            g.add(wire((nl, y), (x, y)))
            for i, lab in enumerate(labels):
                s = Switch(x + 0.1, x + span - 0.1, y, lab, closed=False, size=24)
                if y < 0:
                    s.label.next_to(s, DOWN, buff=0.08)
                g.add(s, wire((x + span - 0.1, y), (x + span + (0.1 if i < n - 1 else 0.2), y)))
                sw.append(s)
                x += span
            g.add(wire((x + 0.1, y), (nr, y)))
    term = VGroup(Circle(radius=0.08, color=INK, stroke_width=2.5, fill_color=PAPER, fill_opacity=1).move_to([x_in, 0, 0]),
                  Circle(radius=0.08, color=INK, stroke_width=2.5, fill_color=PAPER, fill_opacity=1).move_to([x_out, 0, 0]))
    g.add(term)
    g.switches = sw
    return g


def led(x, y, color=INK):
    tri = Polygon([x - 0.18, y + 0.2, 0], [x - 0.18, y - 0.2, 0], [x + 0.16, y, 0], color=color, stroke_width=2.5,
                  fill_color=PAPER, fill_opacity=1)
    bar = Line([x + 0.17, y + 0.2, 0], [x + 0.17, y - 0.2, 0], color=color, stroke_width=3)
    arrows = VGroup(*[Arrow([x + 0.0 + dx, y + 0.25, 0], [x + 0.2 + dx, y + 0.5, 0], buff=0, stroke_width=2,
                            color=RED_INK, tip_length=0.1, max_tip_length_to_length_ratio=0.4) for dx in (-0.08, 0.1)])
    return VGroup(tri, bar, arrows)


def resistor(x0, x1, y):
    n = 6
    xs = np.linspace(x0, x1, 2 * n + 1)
    pts = [(xs[0], y)] + [(xs[i], y + (0.12 if i % 2 else -0.12)) for i in range(1, 2 * n)] + [(xs[-1], y)]
    return wire(*pts)


class ShannonSwitches(NarratedScene):
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

        def set_all(pairs, lamp, on, rt=0.5):
            anims = [s.set(v) for s, v in pairs]
            anims = [a for a in anims if a is not None]
            la = lamp.set(on) if lamp is not None else None
            if la is not None:
                anims.append(la)
            if anims:
                self.play(*anims, run_time=rt)

        # ================= title =================
        series = spaced("Science Stories", 22).move_to([0, 1.8, 0])
        orn1 = ornament(3.4).next_to(series, DOWN, buff=0.3)
        title = serif("The Most Important Master's Thesis", 54).next_to(orn1, DOWN, buff=0.35)
        sub = serif("Claude Shannon · M.I.T. · 1937", 26, FADED, italic=True).next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = serif("after Jimmy Soni and Rob Goodman, A Mind at Play (Simon & Schuster, 2017)", 16, FADED,
                       italic=True).move_to([0, -3.2, 0])
        self.vo("Science Stories. The most important master's thesis.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.wait(0.6)
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= M.I.T., 1937 =================
        place = serif("Cambridge, Massachusetts · 1937", 22, SEPIA, italic=True).move_to([0, 3.15, 0])
        shannon = cameo("modern", 0.75)
        shannon[2][1][0].set_fill(opacity=0)          # clean-shaven in the 1930s
        s_name = serif("Claude Shannon", 24, INK).next_to(shannon, DOWN, buff=0.15)
        s_dates = serif("1916 – 2001 · aged 21 in 1937", 16, FADED, italic=True).next_to(s_name, DOWN, buff=0.06)
        who = VGroup(shannon, s_name, s_dates).move_to([-4.6, 0.3, 0])
        line("1937. At M.I.T., a twenty-one-year-old graduate student named Claude Shannon",
             FadeIn(place), FadeIn(who, shift=UP * 0.15), run_time=1.2)
        self.vo_wait()

        # the differential analyzer (schematic)
        table = Rectangle(width=7.4, height=0.18, color=INK, stroke_width=2, fill_color=PAPER_DARK, fill_opacity=1)
        table.move_to([1.6, -1.35, 0])
        legs = VGroup(*[Line([x, -1.44, 0], [x, -2.4, 0], color=INK, stroke_width=3) for x in (-1.9, 5.1)])
        shaft = Line([-2.1, 1.75, 0], [5.3, 1.75, 0], color=INK, stroke_width=4)
        ints = VGroup(*[integrator(x, -0.45) for x in (-0.9, 1.6, 4.1)])
        gears = VGroup(*[gear((x, 1.75), r=0.3) for x in (-0.55, 1.95, 4.45)])
        rods = VGroup(*[Line([x + 0.35, 0.6, 0], [x + 0.35, 1.45, 0], color=RED_INK, stroke_width=2)
                        for x in (-0.9, 1.6, 4.1)])
        dan = VGroup(table, legs, ints, rods, shaft, gears)
        dlab = serif("differential analyzer (schematic)", 18, FADED, italic=True).move_to([1.6, 2.45, 0])
        line("spends his days looking after a machine the size of a room.",
             FadeIn(dan, lag_ratio=0.1), FadeIn(dlab), run_time=1.4)
        for g in gears:
            g.add_updater(lambda m, dt: m.rotate(-1.4 * dt))
        self.vo_wait()
        line("It is Vannevar Bush's differential analyzer: shafts, gears and spinning discs that solve equations by turning.",
             Indicate(shaft, color=RED_INK, scale_factor=1.0), run_time=1.0)
        self.play(*[Indicate(it[2], color=RED_INK, scale_factor=1.08) for it in ints], run_time=1.2)
        self.vo_wait()

        # relays
        line("To run it, there was a complicated control circuit full of relays.",
             FadeOut(VGroup(ints, rods, table, legs, dlab)), run_time=0.8)
        for g in gears:
            g.clear_updaters()
        self.play(FadeOut(VGroup(shaft, gears)), run_time=0.5)
        rel = relay(1.0, 0.0).scale(1.4, about_point=[1.8, 0.4, 0])
        rlabs = VGroup(serif("coil", 20, FADED, italic=True).next_to(rel.core, LEFT, buff=0.55),
                       serif("contact", 20, FADED, italic=True).move_to([3.1, 2.0, 0]),
                       serif("a relay", 26, SEPIA, italic=True).move_to([1.8, 2.45, 0]))
        self.play(FadeIn(rel), FadeIn(rlabs), run_time=1.0)
        self.vo_wait()
        line("A relay is just a switch, flipped by an electromagnet.", run_time=0.6)
        self.play(rel.core.animate.set_fill(RED_INK, opacity=0.55),
                  Rotate(rel.arm, angle=-13 * DEGREES, about_point=rel.pivot.get_center()), run_time=0.8)
        state = serif("current flows", 22, RED_INK, italic=True).move_to([4.2, 0.0, 0])
        self.play(FadeIn(state), run_time=0.5)
        line("Current flows, or it does not.", run_time=0.5)
        self.play(rel.core.animate.set_fill(PAPER_DARK, opacity=1),
                  Rotate(rel.arm, angle=13 * DEGREES, about_point=rel.pivot.get_center()),
                  Transform(state, serif("no current", 22, FADED, italic=True).move_to([4.2, 0.0, 0])), run_time=0.8)
        self.vo_wait()

        # the tangle
        self.play(FadeOut(VGroup(rel, rlabs, state)), run_time=0.5)
        rng = np.random.default_rng(1937)
        few = VGroup(*[Switch(-0.5 + 1.5 * i, 0.2 + 1.5 * i, 0.6, closed=bool(i % 2)) for i in range(3)])
        few_w = VGroup(*[wire((0.2 + 1.5 * i, 0.6), (1.0 + 1.5 * i, 0.6)) for i in range(2)])
        line("Wire a few relays together and it is easy to say what happens.",
             FadeIn(VGroup(few, few_w).scale(1.5).move_to([1.6, 0.6, 0])), run_time=0.9)
        self.vo_wait()
        many = VGroup()
        for i in range(8):
            for j in range(6):
                x, y = -1.6 + 0.85 * i, 2.3 - 0.75 * j
                many.add(Switch(x, x + 0.45, y, closed=bool(rng.integers(0, 2)), color=INK).scale(0.8))
        tangle = VGroup()
        pts = [m.get_center() for m in many]
        for k in range(70):
            a, b = rng.choice(len(pts), 2, replace=False)
            pa, pb = pts[a], pts[b]
            tangle.add(ArcBetweenPoints(pa, pb, angle=rng.uniform(-1.6, 1.6), color=SEPIA,
                                        stroke_width=1.3, stroke_opacity=0.6))
        line("Wire a hundred, and the tangle becomes very hard to reason about.",
             FadeOut(VGroup(few, few_w)), FadeIn(many, lag_ratio=0.02), run_time=1.2)
        self.play(Create(tangle, lag_ratio=0.03), run_time=2.0)
        self.vo_wait()
        q = serif("Could you calculate with switches?", 34, RED_INK, italic=True)
        qc = ink_card(q).move_to([1.6, 0.4, 0])
        line("Shannon wanted something better: a way to calculate with switches, the way we calculate with numbers.",
             many.animate.set_opacity(0.25), tangle.animate.set_stroke(opacity=0.15), run_time=0.9)
        self.play(FadeIn(qc, scale=0.9), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(many, tangle, qc, who, place)), run_time=0.8)

        # ================= Michigan and Boole =================
        place2 = serif("University of Michigan · Philosophy 33: Introduction to Logic", 22, SEPIA,
                       italic=True).move_to([0, 3.15, 0])
        line("The answer came from an unlikely place.", run_time=0.6)
        self.vo_wait()
        line("Back at the University of Michigan, he had taken a philosophy class in logic.",
             FadeIn(place2), run_time=0.8)
        self.vo_wait()
        boole = cameo("beard", 0.75)
        b_name = serif("George Boole", 24, INK).next_to(boole, DOWN, buff=0.15)
        b_dates = serif("1815 – 1864 · logic as algebra, 1847 and 1854", 16, FADED, italic=True).next_to(
            b_name, DOWN, buff=0.06)
        bw = VGroup(boole, b_name, b_dates).move_to([-4.3, 0.3, 0])
        line("There he met the algebra of George Boole, from the eighteen-forties and fifties.",
             FadeIn(bw, shift=UP * 0.15), run_time=1.0)
        self.vo_wait()
        st = VGroup(serif("“It is raining.”", 30, INK, italic=True),
                    serif("true  or  false", 26, SEPIA, italic=True)).arrange(DOWN, buff=0.25).move_to([1.6, 1.4, 0])
        line("An algebra not of numbers, but of statements that are either true or false,",
             FadeIn(st, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()
        words = VGroup(*[serif(w, 44, RED_INK, bold=True) for w in ("AND", "OR", "NOT")]).arrange(RIGHT, buff=1.1)
        words.move_to([1.6, -0.6, 0])
        line("combined with three words: and, or, not.", run_time=0.6)
        self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.15) for w in words], lag_ratio=0.5), run_time=1.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(st, bw, place2)), words.animate.scale(0.6).move_to([0, 3.15, 0]),
                  run_time=0.8)

        # ================= a switch is a statement =================
        big = Switch(-1.0, 1.0, 0.4, closed=False)
        big.scale(1.4)
        lab_open = serif("open  =  false  =  0", 30, INK).move_to([0, -1.1, 0])
        lab_closed = serif("closed  =  true  =  1", 30, RED_INK).move_to([0, -1.1, 0])
        line("Shannon's insight was that a switch is a statement.", FadeIn(big), run_time=0.8)
        self.vo_wait()
        line("Closed means true.", big.set(True), FadeIn(lab_closed), run_time=0.7)
        self.vo_wait()
        line("Open means false.", big.set(False), FadeOut(lab_closed), FadeIn(lab_open), run_time=0.7)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(big, lab_open)), run_time=0.6)

        # ================= series = AND =================
        sc, sa, sb, slamp = series_circuit()
        sc.scale(0.95).move_to([-2.6, 0.5, 0])
        ttab = truth_table(["A", "B", "lamp"], [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1)]).move_to([3.6, 0.6, 0])
        stitle = serif("in a row (series)", 24, SEPIA, italic=True).move_to([-2.6, 2.25, 0])
        line("Put two switches in a row.", FadeIn(sc), FadeIn(stitle), run_time=0.9)
        self.vo_wait()
        line("The lamp lights only if A is closed and B is closed.", FadeIn(ttab.head), FadeIn(ttab[1]),
             FadeIn(ttab[2]), run_time=0.7)
        box = None
        for i, (va, vb) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            set_all([(sa, bool(va)), (sb, bool(vb))], slamp, bool(va and vb), rt=0.45)
            nb = row_box(ttab, i)
            self.play(FadeIn(ttab.body[i]), (Transform(box, nb) if box else Create(nb)), run_time=0.45)
            if box is None:
                box = nb
            self.wait(0.25)
        self.vo_wait()
        eq_and = MathTex(r"\text{lamp} = A \;\text{and}\; B", font_size=40, color=RED_INK).move_to([3.6, -1.55, 0])
        line("That is and.", FadeIn(eq_and), run_time=0.6)
        self.vo_wait()
        self.wait(0.3)
        self.play(clear(), FadeOut(VGroup(sc, ttab, box, eq_and, stitle)), run_time=0.7)

        # ================= parallel = OR =================
        pc, pa, pb, plamp = parallel_circuit()
        pc.scale(0.95).move_to([-2.6, 0.45, 0])
        otab = truth_table(["A", "B", "lamp"], [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 1)]).move_to([3.6, 0.6, 0])
        ptitle = serif("side by side (parallel)", 24, SEPIA, italic=True).move_to([-2.6, 2.25, 0])
        line("Put them side by side.", FadeIn(pc), FadeIn(ptitle), run_time=0.9)
        self.vo_wait()
        line("The lamp lights if A is closed or B is closed.", FadeIn(otab.head), FadeIn(otab[1]),
             FadeIn(otab[2]), run_time=0.7)
        box = None
        for i, (va, vb) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            set_all([(pa, bool(va)), (pb, bool(vb))], plamp, bool(va or vb), rt=0.45)
            nb = row_box(otab, i)
            self.play(FadeIn(otab.body[i]), (Transform(box, nb) if box else Create(nb)), run_time=0.45)
            if box is None:
                box = nb
            self.wait(0.25)
        self.vo_wait()
        eq_or = MathTex(r"\text{lamp} = A \;\text{or}\; B", font_size=40, color=RED_INK).move_to([3.6, -1.55, 0])
        line("That is or.", FadeIn(eq_or), run_time=0.6)
        self.vo_wait()
        self.wait(0.3)
        self.play(clear(), FadeOut(VGroup(pc, otab, box, eq_or, ptitle)), run_time=0.7)

        # ================= NOT =================
        L, R, T, B = -2.4, 2.4, 0.6, -1.2
        ns = Switch(-0.45, 0.45, T, closed=True)
        nl = Lamp([R, -0.3])
        nwires = VGroup(wire((L, -0.22), (L, T), (-0.45, T)), wire((0.45, T), (R, T), (R, 0.0)),
                        wire((R, -0.6), (R, B), (L, B), (L, -0.38)))
        coil = Rectangle(width=0.9, height=0.45, color=INK, stroke_width=2, fill_color=PAPER_DARK,
                         fill_opacity=1).move_to([0, 1.75, 0])
        coil_lab = serif("coil A", 20, RED_INK, italic=True).next_to(coil, LEFT, buff=0.2)
        link = DashedLine([0, 1.52, 0], [0, 0.95, 0], color=FADED, stroke_width=1.5)
        nc_lab = serif("contact springs open when the coil pulls", 16, FADED, italic=True).move_to([0, B - 0.35, 0])
        ng = VGroup(nwires, battery_v(L, -0.3), ns, nl, coil, coil_lab, link, nc_lab).move_to([-2.4, 0.5, 0])
        nl.set(True)
        nl.glow.set_fill(opacity=0.55)
        nl.bulb.set_fill(GLOW, opacity=1)
        nl.rays.set_stroke(opacity=1)
        ntab = truth_table(["A", "lamp"], [(0, 1), (1, 0)]).move_to([3.6, 0.9, 0])
        line("And a relay whose contact springs open when its coil is energised gives you not.",
             FadeIn(ng), FadeIn(ntab.head), FadeIn(ntab[1]), FadeIn(ntab[2]), run_time=1.0)
        self.play(FadeIn(ntab.body[0]), run_time=0.4)
        self.play(coil.animate.set_fill(RED_INK, opacity=0.55), ns.set(False), nl.set(False), run_time=0.6)
        self.play(FadeIn(ntab.body[1]), run_time=0.4)
        eq_not = MathTex(r"\text{lamp} = \text{not}\; A", font_size=40, color=RED_INK).move_to([3.6, -0.7, 0])
        self.play(FadeIn(eq_not), run_time=0.5)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(ng, ntab, eq_not)), run_time=0.7)

        # ================= Shannon's own convention =================
        then = VGroup(serif("Shannon, 1937: “hindrance”", 26, SEPIA, italic=True),
                      MathTex(r"\text{closed} = 0,\quad \text{open} = 1", font_size=36, color=INK),
                      MathTex(r"\text{series} \to +,\quad \text{parallel} \to \times", font_size=36, color=INK)
                      ).arrange(DOWN, buff=0.3)
        now = VGroup(serif("in this video, as today", 26, SEPIA, italic=True),
                     MathTex(r"\text{closed} = 1,\quad \text{open} = 0", font_size=36, color=RED_INK),
                     MathTex(r"\text{series} \to \text{and},\quad \text{parallel} \to \text{or}", font_size=36,
                             color=RED_INK)).arrange(DOWN, buff=0.3)
        then_c = ink_card(then, pad=0.3).move_to([-3.3, 0.6, 0])
        now_c = ink_card(now, pad=0.3).move_to([3.3, 0.6, 0])
        mirror = serif("same algebra, mirrored", 24, FADED, italic=True).move_to([0, -1.6, 0])
        line("One small detail. In his thesis Shannon actually counted the other way round, with zero for a closed circuit.",
             FadeIn(then_c, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()
        line("It is the same algebra, mirrored. Today we use the version you see here.",
             FadeIn(now_c, shift=UP * 0.1), FadeIn(mirror), run_time=0.9)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(then_c, now_c, mirror, words)), run_time=0.7)

        # ================= simplification =================
        big_net = two_terminal([(0.55, ["A", "B"]), (-0.55, ["A", "C"])]).scale(1.05).move_to([-3.4, 0.8, 0])
        small_net = two_terminal("factored").scale(1.05).move_to([3.4, 0.8, 0])
        eq1 = MathTex(r"(A \text{ and } B)\ \text{or}\ (A \text{ and } C)", font_size=34, color=INK)
        eq1.next_to(big_net, DOWN, buff=0.45)
        eq2 = MathTex(r"A \text{ and } (B \text{ or } C)", font_size=34, color=RED_INK).next_to(small_net, DOWN, buff=0.45)
        eq2.set_y(eq1.get_y())
        eqs = MathTex("=", font_size=48, color=INK).move_to([0, eq1.get_y(), 0])
        n4 = serif("4 contacts", 22, FADED, italic=True).next_to(eq1, DOWN, buff=0.25)
        n3 = serif("3 contacts", 22, RED_INK, italic=True).next_to(eq2, DOWN, buff=0.25)
        head = serif("A circuit is an equation", 30, SEPIA, italic=True).move_to([0, 3.0, 0])
        line("Now the payoff. A circuit becomes an equation, and equations can be simplified.",
             FadeIn(head), FadeIn(big_net), run_time=0.9)
        self.vo_wait()
        line("This circuit uses four contacts: A and B, or A and C.", run_time=0.6)
        self.play(Write(eq1), FadeIn(n4), run_time=1.2)
        self.vo_wait()
        line("But algebra says that is the same as A, and B or C.", run_time=0.6)
        self.play(Write(eqs), TransformFromCopy(eq1, eq2), run_time=1.2)
        self.play(FadeIn(small_net), run_time=0.8)
        self.vo_wait()
        line("Same behaviour, one fewer switch.", FadeIn(n3), Indicate(small_net.switches[0], color=RED_INK),
             run_time=0.8)
        self.vo_wait()
        line("Shannon's thesis did this on far bigger circuits, sometimes cutting the number of parts dramatically.",
             run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(big_net, small_net, eq1, eq2, eqs, n4, n3, head)), run_time=0.7)

        # ================= design by algebra: lock and adder =================
        want = serif("the logic you want", 28, INK, italic=True)
        arrow = MathTex(r"\longrightarrow", font_size=56, color=RED_INK)
        algebra = serif("algebra", 28, RED_INK, italic=True)
        arrow2 = MathTex(r"\longrightarrow", font_size=56, color=RED_INK)
        circ = serif("the circuit", 28, INK, italic=True)
        flow = VGroup(want, arrow, algebra, arrow2, circ).arrange(RIGHT, buff=0.35).move_to([0, 2.2, 0])
        line("And it works the other way too.", FadeIn(want), run_time=0.6)
        self.vo_wait()
        line("Write down the logic you want, and the algebra hands you the circuit.",
             LaggedStart(FadeIn(arrow), FadeIn(algebra), FadeIn(arrow2), FadeIn(circ), lag_ratio=0.4),
             run_time=1.6)
        self.vo_wait()
        ex = VGroup(serif("from the thesis's examples", 20, FADED, italic=True),
                    serif("An Electric Combination Lock", 28, INK),
                    serif("An Adder to the Base Two", 28, INK)).arrange(DOWN, buff=0.22)
        ex_c = ink_card(ex, pad=0.3).move_to([0, 0.2, 0])
        line("His thesis designed an electric combination lock, and a circuit that adds numbers in binary.",
             FadeIn(ex_c, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()
        self.play(FadeOut(VGroup(ex_c, flow)), clear(), run_time=0.6)

        atab = truth_table(["A", "B", "carry", "sum"], [(0, 0, 0, 0), (0, 1, 0, 1), (1, 0, 0, 1), (1, 1, 1, 0)],
                           col_w=1.1).move_to([-3.4, 0.7, 0])
        sum_eq = MathTex(r"\text{sum} = (A \text{ or } B) \text{ and not } (A \text{ and } B)", font_size=32,
                         color=INK).move_to([2.6, 1.3, 0])
        car_eq = MathTex(r"\text{carry} = A \text{ and } B", font_size=32, color=RED_INK).move_to([2.6, 0.2, 0])
        add_ex = MathTex(r"1 + 1 = 10_{\,\text{two}}", font_size=40, color=SEPIA).move_to([2.6, -1.0, 0])
        mod = serif("a modern half-adder, written in logic", 18, FADED, italic=True).move_to([0, 2.9, 0])
        line("Adding two binary digits needs only logic.", FadeIn(atab.head), FadeIn(atab[1]), FadeIn(atab[2]),
             FadeIn(mod), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(r) for r in atab.body], lag_ratio=0.4), FadeIn(add_ex), run_time=1.6)
        self.vo_wait()
        hl_sum = VGroup(*[SurroundingRectangle(atab.body[i][3], color=INK, buff=0.07, stroke_width=1.6)
                          for i in (1, 2)])
        line("The sum digit is one when exactly one input is one.", Create(hl_sum), Write(sum_eq), run_time=1.3)
        self.vo_wait()
        hl_car = SurroundingRectangle(atab.body[3][2], color=RED_INK, buff=0.07, stroke_width=2)
        line("The carry is simply A and B.", Create(hl_car), Write(car_eq), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(atab, sum_eq, car_eq, add_ex, mod, hl_sum, hl_car)), run_time=0.7)

        # ================= Shannon's remark =================
        quote = VGroup(serif("“It just happened that no one else was familiar", 30, INK, italic=True),
                       serif("with both those fields at the same time.”", 30, INK, italic=True),
                       serif("Shannon, interviewed by John Horgan, IEEE Spectrum, 1992", 18, FADED, italic=True)
                       ).arrange(DOWN, buff=0.2)
        quote[2].shift(DOWN * 0.15)
        qcard = ink_card(quote, pad=0.4).move_to([1.3, 0.5, 0])
        sh2 = cameo("modern", 0.6)
        sh2[2][1][0].set_fill(opacity=0)
        sh2.move_to([-5.0, 0.5, 0])
        line("Years later, Shannon said it just happened that no one else was familiar with both those fields at the same time.",
             FadeIn(sh2), FadeIn(qcard, shift=UP * 0.1), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(qcard, sh2)), run_time=0.7)

        # ================= now =================
        chip = Square(3.2, color=INK, stroke_width=3, fill_color=PAPER_DARK, fill_opacity=1).move_to([-2.6, 0.6, 0])
        pins = VGroup()
        for k in range(8):
            off = -1.4 + 0.4 * k
            for d in (UP, DOWN, LEFT, RIGHT):
                if np.allclose(d, UP) or np.allclose(d, DOWN):
                    p = chip.get_center() + d * 1.6 + RIGHT * off
                    pins.add(Line(p, p + d * 0.25, color=INK, stroke_width=3))
                else:
                    p = chip.get_center() + d * 1.6 + UP * off
                    pins.add(Line(p, p + d * 0.25, color=INK, stroke_width=3))
        grid = VGroup(*[Square(0.11, stroke_width=0, fill_color=SEPIA, fill_opacity=0.5).move_to(
            chip.get_center() + np.array([-1.35 + 0.15 * i, -1.35 + 0.15 * j, 0])) for i in range(19) for j in range(19)])
        zoom = Circle(radius=0.25, color=RED_INK, stroke_width=3).move_to(chip.get_center() + [0.6, 0.45, 0])
        tiny = Switch(2.6, 4.6, 0.6, closed=False)
        tiny.move_to([3.6, 0.6, 0])
        zl = DashedLine(zoom.get_right(), tiny.get_left() + LEFT * 0.2, color=RED_INK, stroke_width=1.5)
        tl = serif("each one a switch", 24, RED_INK, italic=True).next_to(tiny, DOWN, buff=0.5)
        bl = serif("a phone chip: billions of transistors", 20, FADED, italic=True).next_to(chip, DOWN, buff=0.45)
        line("Every chip in your phone holds billions of tiny switches,",
             FadeIn(VGroup(chip, pins)), FadeIn(grid, lag_ratio=0.002), FadeIn(bl), run_time=1.2)
        self.play(Create(zoom), Create(zl), FadeIn(tiny), FadeIn(tl), run_time=1.0)
        self.vo_wait()
        eqs3 = VGroup(MathTex(r"A \text{ and } B", font_size=34, color=INK),
                      MathTex(r"A \text{ or } B", font_size=34, color=INK),
                      MathTex(r"\text{not } A", font_size=34, color=INK)).arrange(RIGHT, buff=0.6).move_to([3.6, 2.4, 0])
        line("and they are still designed with the algebra Shannon joined to circuits in 1937.",
             FadeIn(eqs3, lag_ratio=0.3), run_time=1.2)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(chip, pins, grid, zoom, zl, tiny, tl, bl, eqs3)), run_time=0.7)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 24, RED_INK).move_to([0, 3.05, 0])

        def kit_circuit(kind, cx):
            Lx, Rx, T, B = cx - 2.4, cx + 2.4, 1.6, -0.6
            g = VGroup()
            pack = Rectangle(width=0.55, height=1.0, color=INK, stroke_width=2.5, fill_color=PAPER_DARK,
                             fill_opacity=1).move_to([Lx, (T + B) / 2, 0])
            pk = VGroup(serif("3 V", 16, INK).move_to(pack),
                        serif("+", 18, INK).next_to(pack, LEFT, buff=0.08).align_to(pack, UP))
            g.add(wire((Lx, pack.get_top()[1]), (Lx, T), (cx - 1.5, T)))
            g.add(wire((Lx, pack.get_bottom()[1]), (Lx, B), (cx + 0.6, B)))
            g.add(resistor(cx + 0.6, cx + 1.5, B), wire((cx + 1.5, B), (Rx, B), (Rx, 0.15)))
            d = led(Rx, 0.35).rotate(-PI / 2, about_point=[Rx, 0.35, 0])
            g.add(d, wire((Rx, 0.55), (Rx, T), (cx + 1.5, T)))
            if kind == "and":
                s1 = Switch(cx - 1.5, cx - 0.65, T, "A", size=22)
                s2 = Switch(cx + 0.65, cx + 1.5, T, "B", size=22)
                g.add(s1, s2, wire((cx - 0.65, T), (cx + 0.65, T)))
            else:
                s1 = Switch(cx - 0.45, cx + 0.45, T, "A", size=22)
                s2 = Switch(cx - 0.45, cx + 0.45, T - 0.85, "B", size=22)
                s2.label.next_to(s2, DOWN, buff=0.05)
                g.add(s1, s2, wire((cx - 1.5, T), (cx - 0.45, T)), wire((cx + 0.45, T), (cx + 1.5, T)),
                      wire((cx - 1.0, T), (cx - 1.0, T - 0.85), (cx - 0.45, T - 0.85)),
                      wire((cx + 0.45, T - 0.85), (cx + 1.0, T - 0.85), (cx + 1.0, T)))
            g.add(pack, pk)
            rl = serif("resistor", 15, FADED, italic=True).next_to(resistor(cx + 0.6, cx + 1.5, B), DOWN, buff=0.12)
            ll = serif("LED", 15, FADED, italic=True).next_to(d, RIGHT, buff=0.12)
            g.add(rl, ll)
            return g, s1, s2, d

        ga, a1, a2, d1 = kit_circuit("and", -3.3)
        go, o1, o2, d2 = kit_circuit("or", 3.3)
        cap_a = serif("in a row: AND", 24, SEPIA, italic=True).move_to([-3.3, -1.25, 0])
        cap_o = serif("side by side: OR", 24, SEPIA, italic=True).move_to([3.3, -1.25, 0])
        line("Try it yourself. Take a battery pack, an L.E.D. with a resistor, and two switches.",
             FadeIn(tiy), FadeIn(ga), run_time=1.0)
        self.vo_wait()

        def led_on(d, on):
            return AnimationGroup(d[0].animate.set_fill(GLOW if on else PAPER, opacity=1),
                                  d[2].animate.set_opacity(1 if on else 0.15))

        self.add(d1, d2)
        d1[2].set_opacity(0.15)
        d2[2].set_opacity(0.15)
        line("Wire them in a row and you have an and gate.", FadeIn(cap_a), run_time=0.6)
        self.play(a1.set(True), run_time=0.4)
        self.play(a2.set(True), led_on(d1, True), run_time=0.5)
        self.vo_wait()
        line("Wire them side by side and you have or.", FadeIn(go), FadeIn(cap_o), run_time=0.8)
        self.play(o2.set(True), led_on(d2, True), run_time=0.5)
        self.vo_wait()
        lock = VGroup(serif("a lock: lamp = A and (not B) and C", 24, INK),
                      serif("two-way switches let a path need a switch to be off", 18, FADED, italic=True),
                      ).arrange(DOWN, buff=0.12)
        lock_c = ink_card(lock, pad=0.2).move_to([0, -2.15, 0])
        line("Then, with two-way switches, build a lock that lights only for your secret combination.",
             FadeIn(lock_c, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()
        safe = serif("a small battery pack and always a resistor with the LED", 18, FADED, italic=True)
        safe.next_to(tiy, DOWN, buff=0.15)
        line("Write its equation first, then test it.", FadeIn(safe), run_time=0.6)
        self.vo_wait()
        self.wait(0.8)
        self.play(clear(), FadeOut(VGroup(ga, go, cap_a, cap_o, lock_c, tiy, safe)), run_time=0.8)

        # ================= end card =================
        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     serif("Claude Shannon, A Symbolic Analysis of Relay and Switching Circuits (M.I.T. thesis, 1937)",
                           17, FADED, italic=True),
                     serif("story after J. Soni and R. Goodman, A Mind at Play (2017) · sources in the episode notes",
                           17, FADED, italic=True),
                     serif("silhouettes are stylised, not likenesses · animated with Manim · synthetic narration",
                           15, FADED, italic=True)).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(2.5)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)
