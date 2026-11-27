"""I043 Nature Cannot Be Fooled (Ice Water and the Challenger O-Ring), a Science Stories episode.

After J. Gleick, Genius: The Life and Science of Richard Feynman (1992). Script and sources: episodes/I043_script.md

Render:  manim -qh --frame_rate 30 episodes/I043_ice_water_oring.py NatureCannotBeFooled
Then:    scripts/finish_video.sh media/videos/I043_ice_water_oring/1080p30/NatureCannotBeFooled.mp4 out/I043_ice_water_oring.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

ICE = "#9fb8c8"
STEEL = "#8a8f94"


def note(text, size=17, color=FADED):
    return serif(text, size, color, italic=True)


def P(x, y):
    return np.array([x, y, 0.0])


# ---------- the numbers, computed and checked at render time ----------
def f_to_c(f):
    return (f - 32) * 5 / 9


assert round(f_to_c(53)) == 12          # coldest earlier launch, 53 F
assert round(f_to_c(36)) == 2           # air at launch, 36 F
assert round(f_to_c(28)) == -2          # joint, about 28 F
ORING_IN = 0.280                        # O-ring cross-section, inches (Mulloy, 11 Feb 1986 hearing)
assert round(ORING_IN * 25.4, 1) == 7.1  # "about seven millimetres thick"
GAP_IN = (0.017, 0.029)                 # joint opening at the two O-rings, inches (Commission, via CBS)
assert GAP_IN[1] * 25.4 < 1.0           # "less than a millimetre"
GAP_PEAK_S = 0.6                        # gap at its widest about 600 ms after ignition
DAYS_300Y = 300 * 365
assert 100_000 < DAYS_300Y < 110_000    # "a launch every day for 300 years" ~ 1 in 100,000


# ---------- illustrative seal model (qualitative, labelled on screen) ----------
def gap_curve(t):
    """Joint gap, fraction of its maximum, rising to a peak at about 0.6 s."""
    return np.clip(np.sin(np.clip(t / GAP_PEAK_S, 0, 1) * PI / 2), 0, 1)


def ring_follow(tau, T=1.0, n=400):
    """First-order lag: the ring's edge chases the moving steel with time constant tau (s)."""
    ts = np.linspace(0, T, n)
    r = np.zeros(n)
    for i in range(1, n):
        dt = ts[i] - ts[i - 1]
        r[i] = r[i - 1] + (gap_curve(ts[i]) - r[i - 1]) * (1 - np.exp(-dt / tau))
    return ts, r


TAU_WARM, TAU_COLD = 0.02, 0.6
_ts, _rw = ring_follow(TAU_WARM)
_, _rc = ring_follow(TAU_COLD)
assert np.max(gap_curve(_ts) - _rw) < 0.08       # warm ring keeps up
assert np.max(gap_curve(_ts) - _rc) > 0.4        # cold ring falls well behind


# ---------- small drawings ----------
def cup(scale=1.0):
    body = Polygon(P(-0.55, 0.7), P(0.55, 0.7), P(0.42, -0.7), P(-0.42, -0.7), fill_color=ICE, fill_opacity=0.25,
                   stroke_color=INK, stroke_width=2.5)
    water = Polygon(P(-0.51, 0.4), P(0.51, 0.4), P(0.42, -0.68), P(-0.42, -0.68), fill_color=ICE, fill_opacity=0.55,
                    stroke_width=0)
    cubes = VGroup(*[Square(0.26, fill_color=PAPER, fill_opacity=0.85, stroke_color=BLUE_INK, stroke_width=1.2)
                     .rotate(a).move_to(P(x, y)) for x, y, a in [(-0.18, 0.32, 0.3), (0.16, 0.38, -0.2),
                                                                  (0.0, 0.1, 0.6)]])
    return VGroup(water, cubes, body).scale(scale)


def shuttle(scale=1.0):
    tank = RoundedRectangle(corner_radius=0.25, width=0.55, height=3.0, fill_color=SEPIA, fill_opacity=0.55,
                            stroke_color=INK, stroke_width=2)
    nose = Triangle(fill_color=SEPIA, fill_opacity=0.55, stroke_color=INK, stroke_width=2).scale(0.3) \
        .stretch_to_fit_width(0.55).next_to(tank, UP, buff=-0.02)
    srbs = VGroup()
    for dx in (-0.42, 0.42):
        b = Rectangle(width=0.26, height=2.8, fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK,
                      stroke_width=2).move_to(P(dx, -0.1))
        tip = Triangle(fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=2).scale(0.15) \
            .stretch_to_fit_width(0.26).next_to(b, UP, buff=-0.01)
        srbs.add(VGroup(b, tip))
    orb = Polygon(P(0.28, 1.0), P(0.62, 0.9), P(0.75, -0.6), P(1.3, -1.2), P(1.3, -1.45), P(0.28, -1.45),
                  fill_color=PAPER, fill_opacity=1, stroke_color=INK, stroke_width=2).shift(RIGHT * 0.32)
    return VGroup(tank, nose, srbs, orb).scale(scale)


def booster(n=4, scale=1.0, joint_color=RED_INK):
    segs = VGroup(*[Rectangle(width=0.9, height=1.0, fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK,
                              stroke_width=2).move_to(P(0, -1.5 + i * 1.0)) for i in range(n)])
    tip = Triangle(fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=2).scale(0.5) \
        .stretch_to_fit_width(0.9).next_to(segs, UP, buff=-0.01)
    joints = VGroup(*[Line(P(-0.5, -1.0 + i * 1.0), P(0.5, -1.0 + i * 1.0), color=joint_color, stroke_width=5)
                      for i in range(n - 1)])
    return VGroup(segs, tip, joints).scale(scale)


def resilience_axes(x0, y0, w=7.0, h=3.4, label=True):
    ax = Axes(x_range=[0, 1.0, 0.2], y_range=[0, 1.1, 0.5], x_length=w, y_length=h, tips=False,
              axis_config={"color": INK, "stroke_width": 2, "include_ticks": True, "tick_size": 0.05})
    ax.move_to(P(x0, y0))
    xl = note("seconds after ignition", 16, INK).next_to(ax.x_axis, DOWN, buff=0.38)
    ticks = VGroup(*[serif(f"{v:.1f}", 13, FADED).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v in (0.2, 0.6, 1.0)])
    yl = note("opening", 15, INK).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.12)
    g = VGroup(ax, xl, ticks, yl)
    return ax, g


class NatureCannotBeFooled(NarratedScene):
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
        title = serif("Nature Cannot Be Fooled", 56).next_to(orn1, DOWN, buff=0.35)
        sub = serif("Feynman, a cup of ice water, and the Challenger seal", 26, FADED, italic=True) \
            .next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("story after J. Gleick, Genius: The Life and Science of Richard Feynman (1992)", 16) \
            .move_to([0, -2.6, 0])
        self.vo("Science Stories. Nature cannot be fooled.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.wait(0.4)
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= the hearing =================
        place = spaced("Washington · 11 February 1986", 18, SEPIA).move_to(P(0, 3.05))
        table = Line(P(-4.5, -1.0), P(4.5, -1.0), color=INK, stroke_width=4)
        table2 = Line(P(-4.3, -1.12), P(4.3, -1.12), color=INK, stroke_width=1.2)
        glass = cup(1.0).move_to(P(1.6, -0.28))
        glass_l = note("a cup of ice water", 15, INK).next_to(glass, RIGHT, buff=0.25)
        fey = cameo("plain", 0.7).move_to(P(-2.6, 0.75))
        fey_l = VGroup(serif("Richard Feynman", 20, INK), note("physicist, 1918–1988", 14)
                       ).arrange(DOWN, buff=0.04).next_to(fey, LEFT, buff=0.3)
        sil_n = note("silhouette stylised, not a likeness", 12).next_to(fey_l, DOWN, buff=0.1)
        line("Washington, the eleventh of February, 1986. At a public hearing sits a physicist, with a cup of "
             "ice water in front of him.", FadeIn(place), Create(table), Create(table2), run_time=1.0)
        self.play(FadeIn(glass, shift=DOWN * 0.15), FadeIn(glass_l), run_time=1.0)
        self.play(FadeIn(fey), FadeIn(fey_l), FadeIn(sil_n), run_time=1.0)
        self.vo_wait()
        comm = ink_card(VGroup(serif("Presidential Commission", 20, INK),
                               note("on the Space Shuttle Challenger Accident", 15)).arrange(DOWN, buff=0.06),
                        pad=0.18).move_to(P(3.6, 2.0))
        line("His name is Richard Feynman. He is one of the commissioners asked to find out why the space shuttle "
             "Challenger was lost.", FadeIn(comm, shift=DOWN * 0.1), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(place, table, table2, glass, glass_l, fey, fey_l, sil_n, comm)),
                  run_time=0.7)

        # ================= the loss, told quietly =================
        sh = shuttle(0.95).move_to(P(-3.2, 0.3))
        memo = VGroup(spaced("28 January 1986", 18, SEPIA),
                      serif("Challenger, flight 51-L", 26, INK),
                      serif("lost 73 seconds after launch", 24, INK),
                      serif("seven crew", 24, RED_INK)).arrange(DOWN, buff=0.18).move_to(P(2.4, 0.4))
        line("Two weeks earlier, on the twenty-eighth of January, Challenger broke apart seventy-three seconds "
             "after launch.", FadeIn(sh), FadeIn(memo[:3], lag_ratio=0.3), run_time=1.4)
        self.vo_wait()
        line("All seven of its crew were killed.", FadeIn(memo[3]), sh.animate.set_opacity(0.35), run_time=1.2)
        self.vo_wait()
        self.wait(0.8)
        self.play(clear(), FadeOut(memo), run_time=0.6)

        # ================= the booster and its joints =================
        srb_hi = SurroundingRectangle(sh[2][1], color=RED_INK, buff=0.06, stroke_width=3)
        line("Feynman's puzzle begins with something small: a ring of rubber, about seven millimetres thick.",
             sh.animate.set_opacity(1), run_time=0.8)
        ring = Annulus(inner_radius=0.95, outer_radius=1.15, fill_color=INK, fill_opacity=1, stroke_width=0) \
            .move_to(P(2.6, 0.5))
        ring_l = VGroup(serif("O-ring", 24, INK), note("cross-section about 7 mm (0.28 in)", 15)
                        ).arrange(DOWN, buff=0.06).next_to(ring, DOWN, buff=0.3)
        self.play(FadeIn(ring, scale=0.8), FadeIn(ring_l), run_time=1.0)
        self.vo_wait()
        bst = booster(4, 1.0).move_to(P(0.6, 0.2))
        bst_l = note("solid rocket booster (stylised)", 15, INK).next_to(bst, DOWN, buff=0.2)
        line("Each of the shuttle's two solid rocket boosters was built from steel segments, joined end to end.",
             Create(srb_hi), FadeOut(ring), FadeOut(ring_l), run_time=0.8)
        self.play(TransformFromCopy(sh[2][1], bst), FadeIn(bst_l), run_time=1.4)
        jl = note("field joints", 15, RED_INK).next_to(bst[2][1], RIGHT, buff=0.3)
        self.play(Indicate(bst[2], color=RED_INK, scale_factor=1.1), FadeIn(jl), run_time=1.0)
        self.vo_wait()

        # cross-section of a joint (wall drawn horizontally: inside at the bottom, outside at the top)
        Y0 = 0.4
        clevis = VGroup(
            Rectangle(width=4.6, height=0.36, fill_color=STEEL, fill_opacity=0.9, stroke_color=INK, stroke_width=2)
            .move_to(P(2.5, Y0 + 0.62)),
            Rectangle(width=4.6, height=0.36, fill_color=STEEL, fill_opacity=0.9, stroke_color=INK, stroke_width=2)
            .move_to(P(2.5, Y0 - 0.62)),
            Rectangle(width=1.0, height=1.6, fill_color=STEEL, fill_opacity=0.9, stroke_color=INK, stroke_width=2)
            .move_to(P(5.3, Y0)),
        )
        tang = Rectangle(width=5.4, height=0.62, fill_color="#b4b8bb", fill_opacity=1, stroke_color=INK,
                         stroke_width=2).move_to(P(1.7, Y0))
        gap_top = Y0 + 0.375
        o1 = Circle(radius=0.11, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(P(2.4, gap_top + 0.0))
        o2 = Circle(radius=0.11, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(P(3.4, gap_top + 0.0))
        lab_t = note("tang", 15, INK).move_to(P(0.2, Y0))
        lab_c = note("clevis", 15, INK).next_to(clevis[0], UP, buff=0.1).shift(LEFT * 1.4)
        lab_o = VGroup(note("primary", 14, RED_INK).next_to(o1, UP, buff=0.42),
                       note("secondary", 14, RED_INK).next_to(o2, UP, buff=0.42))
        inside = note("inside: burning propellant", 14, RED_INK).move_to(P(2.5, Y0 - 1.45))
        sec_n = note("joint cross-section, stylised and not to scale", 12).move_to(P(2.6, -1.4))
        joint = VGroup(clevis, tang, o1, o2)
        self.play(clear(), FadeOut(VGroup(sh, srb_hi, jl, bst_l)), bst.animate.scale(0.75).move_to(P(-5.2, 0.3)),
                  run_time=0.8)
        pointer = DashedLine(bst[2][1].get_right(), P(-0.2, Y0), color=RED_INK, stroke_width=2)
        line("At every joint, a tongue of steel slots into a groove, and two rubber O-rings seal the gap between "
             "them.", Create(pointer), FadeIn(clevis), FadeIn(tang), FadeIn(lab_t), FadeIn(lab_c),
             FadeIn(sec_n), run_time=1.4)
        self.play(GrowFromCenter(o1), GrowFromCenter(o2), FadeIn(lab_o), run_time=1.0)
        self.vo_wait()
        line("Their job is to keep the burning gas inside, at the moment the rocket fires.", FadeIn(inside),
             run_time=0.8)
        gas = VGroup(*[Arrow(P(x, Y0 - 1.25), P(x, Y0 - 0.86), color=RED_INK, stroke_width=4, buff=0,
                             max_tip_length_to_length_ratio=0.3) for x in np.linspace(0.6, 4.4, 6)])
        self.play(LaggedStart(*[GrowArrow(a) for a in gas], lag_ratio=0.12), run_time=1.2)
        self.vo_wait()

        # ================= the obvious answer =================
        obv = ink_card(VGroup(note("the obvious thought", 15),
                              serif("Cold rubber is still rubber.", 22, INK)).arrange(DOWN, buff=0.08),
                       pad=0.18).move_to(P(-2.6, 2.55))
        line("The obvious thought is that the cold should hardly matter. Chilled rubber does not shatter. It is "
             "still a ring, still in its groove.", FadeIn(obv, shift=DOWN * 0.1), run_time=1.0)
        self.vo_wait()

        # ================= the gap opens =================
        line("But the joint does not stay still. When the motor lights, pressure swells the steel, and the gap "
             "at the joint opens.", obv.animate.set_opacity(0.35), run_time=0.8)
        top_arm = clevis[0]
        GAP_DRAW = 0.32
        self.play(top_arm.animate.shift(UP * GAP_DRAW), lab_c.animate.shift(UP * GAP_DRAW),
                  lab_o.animate.shift(UP * GAP_DRAW), o1.animate.shift(UP * GAP_DRAW / 2).scale(1.45),
                  o2.animate.shift(UP * GAP_DRAW / 2).scale(1.45), run_time=1.6)
        self.vo_wait()
        gap_card = ink_card(VGroup(serif("less than 1 mm", 22, RED_INK),
                                   note("0.017 to 0.029 in at the two rings", 14),
                                   note("widest about 0.6 s after ignition", 14),
                                   note("gap exaggerated in the drawing", 12)).arrange(DOWN, buff=0.06),
                            pad=0.16).move_to(P(-2.5, -1.3))
        line("Not by much, less than a millimetre. But it opens in a fraction of a second.",
             FadeIn(gap_card, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        line("The seal only works if the rubber springs out and follows the moving steel.",
             Indicate(o1, color=RED_INK), Indicate(o2, color=RED_INK), run_time=1.2)
        self.vo_wait()
        self.play(top_arm.animate.shift(DOWN * GAP_DRAW), lab_c.animate.shift(DOWN * GAP_DRAW),
                  lab_o.animate.shift(DOWN * GAP_DRAW), o1.animate.shift(DOWN * GAP_DRAW / 2).scale(1 / 1.45),
                  o2.animate.shift(DOWN * GAP_DRAW / 2).scale(1 / 1.45), run_time=0.8)
        self.play(clear(), FadeOut(VGroup(obv, gap_card, joint, lab_t, lab_c, lab_o, inside, sec_n, gas, pointer,
                                          bst)), run_time=0.7)

        # ================= resilience: warm versus cold =================
        head = serif("Not whether it survives the cold, but how fast it springs back", 26, INK).move_to(P(0, 3.0))
        line("So the question is not whether the rubber survives the cold. It is how fast it springs back. "
             "Engineers call this resilience.", FadeIn(head), run_time=1.0)
        ax, axg = resilience_axes(-0.6, 0.35)
        self.play(FadeIn(axg), run_time=0.8)
        steel_c = ax.plot(lambda t: gap_curve(t) * 1.0, x_range=[0, 1.0], color=INK, stroke_width=4)
        steel_l = note("gap, as the steel moves", 15, INK).next_to(ax.c2p(1.0, 1.0), RIGHT, buff=0.15)
        self.play(Create(steel_c), FadeIn(steel_l), run_time=1.4)
        self.vo_wait()
        warm = ax.plot_line_graph(_ts, _rw, add_vertex_dots=False, line_color=SEPIA, stroke_width=5)
        warm_l = note("warm rubber", 15, SEPIA).next_to(ax.c2p(0.3, 0.75), LEFT, buff=0.2)
        line("Warm rubber is quick. It chases the gap and seals it.", Create(warm), FadeIn(warm_l), run_time=1.8)
        self.vo_wait()
        cold = ax.plot_line_graph(_ts, _rc, add_vertex_dots=False, line_color=BLUE_INK, stroke_width=5)
        cold_l = note("cold rubber", 15, BLUE_INK).next_to(ax.c2p(0.75, float(_rc[300])), DOWN, buff=0.15)
        xs = _ts
        poly_pts = [ax.c2p(x, gap_curve(x)) for x in xs] + [ax.c2p(x, r) for x, r in zip(xs[::-1], _rc[::-1])]
        lag = Polygon(*poly_pts, fill_color=RED_INK, fill_opacity=0.25, stroke_width=0)
        lag_l = note("gap left open", 15, RED_INK).move_to(ax.c2p(0.42, 0.62))
        line("Cold rubber is sluggish. For a moment the gap stays open, and hot gas can push past.",
             Create(cold), FadeIn(cold_l), run_time=1.8)
        self.play(FadeIn(lag), FadeIn(lag_l), run_time=0.8)
        qual = note("illustrative curves, not measured data", 13).next_to(axg, DOWN, buff=0.15)
        self.play(FadeIn(qual), run_time=0.4)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(head, axg, steel_c, steel_l, warm, warm_l, cold, cold_l, lag, lag_l, qual)),
                  run_time=0.7)

        # ================= the night before =================
        # thermometer
        TX, TB, TT = -3.6, -1.75, 2.55
        F_LO, F_HI = 20, 80

        def fy(f):
            return TB + (f - F_LO) / (F_HI - F_LO) * (TT - TB)

        tube = RoundedRectangle(corner_radius=0.18, width=0.36, height=TT - TB + 0.3, stroke_color=INK,
                                stroke_width=2.5, fill_color=PAPER, fill_opacity=1).move_to(P(TX, (TT + TB) / 2))
        bulb = Circle(radius=0.3, fill_color=RED_INK, fill_opacity=1, stroke_color=INK, stroke_width=2.5) \
            .move_to(P(TX, TB - 0.3))
        ticks = VGroup()
        for f in range(20, 81, 10):
            ticks.add(Line(P(TX - 0.18, fy(f)), P(TX - 0.34, fy(f)), color=INK, stroke_width=1.5))
            ticks.add(serif(f"{f}°F", 13, FADED).next_to(P(TX - 0.36, fy(f)), LEFT, buff=0.06))
        frz = DashedLine(P(TX - 0.2, fy(32)), P(TX + 3.0, fy(32)), color=BLUE_INK, stroke_width=1.5)
        frz_l = note("freezing", 13, BLUE_INK).next_to(frz, RIGHT, buff=0.1)
        merc = Rectangle(width=0.16, height=0.01, fill_color=RED_INK, fill_opacity=1, stroke_width=0) \
            .move_to(P(TX, TB), aligned_edge=DOWN)

        def mark(f, text, sub_text, color):
            ln = Line(P(TX + 0.2, fy(f)), P(TX + 0.8, fy(f)), color=color, stroke_width=3)
            lab = VGroup(serif(text, 19, color), note(sub_text, 13)).arrange(RIGHT, buff=0.15) \
                .next_to(ln, RIGHT, buff=0.12)
            return VGroup(ln, lab)

        m53 = mark(53, "53°F (12°C)", "coldest launch before", INK)
        m36 = mark(36, "36°F (2°C)", "air at launch", RED_INK)
        m28 = mark(28, "about 28°F (−2°C)", "near the joint that failed", RED_INK)
        thermo = VGroup(tube, bulb, ticks, merc)
        tk_box = ink_card(VGroup(serif("Morton Thiokol", 20, INK), note("maker of the boosters", 14))
                          .arrange(DOWN, buff=0.06), pad=0.18).move_to(P(4.3, 2.4))
        line("On the eve of the launch, engineers at the booster's maker, Morton Thiokol, were worried about "
             "exactly this.", FadeIn(thermo), FadeIn(tk_box, shift=DOWN * 0.1), run_time=1.0)
        self.play(merc.animate.stretch_to_fit_height(fy(53) - TB, about_edge=DOWN), run_time=1.0)
        self.vo_wait()
        line("The coldest launch so far had been at fifty-three degrees Fahrenheit, about twelve Celsius.",
             FadeIn(m53), run_time=0.8)
        self.vo_wait()
        boi = cameo("plain", 0.5).move_to(P(1.6, -0.9))
        quote = ink_card(VGroup(note("Roger Boisjoly, Thiokol engineer", 14),
                                serif("“we should not fly outside", 20, INK),
                                serif("of our data base”", 20, INK),
                                note("Commission report, chapter 5", 12)).arrange(DOWN, buff=0.05),
                         pad=0.16).next_to(boi, RIGHT, buff=0.25)
        line("One of the engineers, Roger Boisjoly, summed up their view: we should not fly outside of our data "
             "base.", FadeIn(boi), FadeIn(quote, shift=LEFT * 0.1), run_time=1.0)
        self.vo_wait()
        line("The launch went ahead. That morning the air at the pad was thirty-six degrees Fahrenheit, about "
             "two Celsius.", FadeIn(frz), FadeIn(frz_l), FadeOut(boi), FadeOut(quote), run_time=0.8)
        self.play(merc.animate.stretch_to_fit_height(fy(36) - TB, about_edge=DOWN), FadeIn(m36), run_time=1.2)
        self.vo_wait()
        line("Infrared readings near the joint that failed suggested about twenty-eight, below freezing.",
             merc.animate.stretch_to_fit_height(fy(28) - TB, about_edge=DOWN), FadeIn(m28), run_time=1.2)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(thermo, frz, frz_l, m53, m36, m28, tk_box)), run_time=0.7)

        # ================= the ice water =================
        place2 = spaced("the hearing · 11 February 1986", 18, SEPIA).move_to(P(0, 3.05))
        glass = cup(1.6).move_to(P(-3.6, 0.4))

        def piece(x, y):
            smp = Circle(radius=0.5, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(P(x, y))
            jt = Rectangle(width=1.5, height=0.18, fill_color=STEEL, fill_opacity=1, stroke_color=INK,
                           stroke_width=1.5).next_to(smp, UP, buff=0)
            jb = jt.copy().next_to(smp, DOWN, buff=0)
            return smp, jt, jb

        sample, jaw_t, jaw_b = piece(-0.6, 1.6)
        s_l = note("piece of seal rubber, squeezed", 15, INK).next_to(jaw_t, UP, buff=0.15)
        line("Back at the hearing, Feynman had chilled a squeezed piece of the seal's rubber in his ice water. "
             "Then he let it go.", FadeIn(place2), FadeIn(glass), FadeIn(sample), FadeIn(jaw_t), FadeIn(jaw_b),
             FadeIn(s_l), run_time=1.0)
        self.play(sample.animate.stretch_to_fit_height(0.4), jaw_t.animate.shift(DOWN * 0.3),
                  jaw_b.animate.shift(UP * 0.3), run_time=0.9)
        grp = VGroup(sample, jaw_t, jaw_b)
        self.play(FadeOut(s_l), grp.animate.move_to(glass.get_center() + DOWN * 0.2).scale(0.55), run_time=1.2)
        self.wait(0.5)
        self.play(grp.animate.move_to(P(1.2, 0.9)).scale(1 / 0.55), run_time=1.0)
        # a warm piece, squeezed the same way, for comparison (illustration)
        w_s, w_t, w_b = piece(4.2, 0.9)
        w_s.stretch_to_fit_height(0.4)
        w_t.next_to(w_s, UP, buff=0)
        w_b.next_to(w_s, DOWN, buff=0)
        self.play(FadeIn(VGroup(w_s, w_t, w_b)), run_time=0.5)
        for m in (jaw_t, w_t):
            m.generate_target()
            m.target.shift(UP * 0.7).set_opacity(0)
        for m in (jaw_b, w_b):
            m.generate_target()
            m.target.shift(DOWN * 0.7).set_opacity(0)
        self.play(*[MoveToTarget(m) for m in (jaw_t, jaw_b, w_t, w_b)], run_time=0.6)
        self.remove(jaw_t, jaw_b, w_t, w_b)
        self.play(w_s.animate.stretch_to_fit_height(1.0), run_time=0.5, rate_func=rate_functions.ease_out_back)
        self.play(sample.animate.stretch_to_fit_height(0.46), run_time=1.6, rate_func=rate_functions.ease_out_sine)
        still = VGroup(serif("from the ice water", 18, BLUE_INK), note("stays flattened", 15, BLUE_INK)) \
            .arrange(DOWN, buff=0.04).next_to(P(1.2, 0.9), DOWN, buff=0.75)
        warm_t = VGroup(serif("at room temperature", 18, SEPIA), note("springs back at once", 15, SEPIA)) \
            .arrange(DOWN, buff=0.04).next_to(P(4.2, 0.9), DOWN, buff=0.75)
        ill = note("comparison piece added as an illustration", 12).next_to(warm_t, DOWN, buff=0.1)
        self.play(FadeIn(still), FadeIn(warm_t), FadeIn(ill), run_time=0.5)
        self.vo_wait()
        fq = ink_card(VGroup(note("Feynman, hearing transcript, 11 February 1986", 13),
                             serif("“the stuff looked as if it was less resilient", 20, INK),
                             serif("at lower temperatures, in ice”", 20, INK)).arrange(DOWN, buff=0.06),
                      pad=0.18).move_to(P(0.2, -2.25))
        line("In his words, the stuff looked as if it was less resilient at lower temperatures.",
             FadeIn(fq, shift=UP * 0.1), run_time=1.0)
        self.vo_wait()
        line("He admitted it was not the way to do such experiments. But anyone watching could see the point.",
             run_time=0.6)
        self.play(sample.animate.stretch_to_fit_height(0.56), run_time=2.5, rate_func=linear)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(place2, glass, sample, w_s, still, warm_t, ill, fq)), run_time=0.7)

        # ================= payoff =================
        sh2 = shuttle(0.95).move_to(P(-3.0, 0.3))
        right = SurroundingRectangle(sh2[2][1], color=RED_INK, buff=0.06, stroke_width=3)
        find = VGroup(serif("The Commission's finding:", 22, INK),
                      serif("the seal failed in a joint", 24, RED_INK),
                      serif("of the right-hand booster", 24, RED_INK),
                      note("hot gas escaped; cold had made the seal worse", 15)).arrange(DOWN, buff=0.12) \
            .move_to(P(2.6, 0.5))
        line("The commission found that the seal had failed in a joint of the right-hand booster. Hot gas "
             "escaped, and the shuttle broke apart.", FadeIn(sh2), Create(right), FadeIn(find, lag_ratio=0.2),
             run_time=1.4)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(sh2, right, find)), run_time=0.7)

        # ================= why it matters: the odds =================
        head2 = serif("How likely is a shuttle to be lost?", 28, INK).move_to(P(0, 3.0))
        g100 = VGroup(*[Dot(radius=0.075, color=INK) for _ in range(100)]).arrange_in_grid(10, 10, buff=0.12) \
            .move_to(P(-3.3, 0.5))
        g100[0].set_color(RED_INK).scale(1.4)
        l100 = VGroup(serif("about 1 in 100", 24, RED_INK), note("working engineers", 15)) \
            .arrange(DOWN, buff=0.06).next_to(g100, DOWN, buff=0.25)
        l1e5 = VGroup(serif("1 in 100,000", 24, BLUE_INK), note("management", 15)).arrange(DOWN, buff=0.06)
        days = note("= a launch every day for 300 years, losing only one", 15, INK)
        right_side = VGroup(l1e5, days).arrange(DOWN, buff=0.2).move_to(P(3.0, 0.5))
        src = note("Feynman, Appendix F of the Commission report", 13).move_to(P(0, -2.45))
        line("In his own part of the report, Feynman asked how likely a shuttle was to fail. Working engineers "
             "said roughly one flight in a hundred.", FadeIn(head2), FadeIn(g100, lag_ratio=0.01), FadeIn(l100),
             FadeIn(src), run_time=1.6)
        self.vo_wait()
        line("Management said one in a hundred thousand: a launch every day for three hundred years, losing "
             "only one.", FadeIn(right_side, shift=LEFT * 0.1), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(head2, g100, l100, right_side, src)), run_time=0.7)

        fin = VGroup(serif("“For a successful technology,", 32, INK),
                     serif("reality must take precedence over public relations,", 32, INK),
                     serif("for nature cannot be fooled.”", 32, RED_INK),
                     note("Richard Feynman, Appendix F, 1986", 16)).arrange(DOWN, buff=0.22).move_to(P(0, 0.4))
        for m in fin:
            if m.width > 12.4:
                m.scale_to_fit_width(12.4)
        line("He ended with a sentence engineers still quote. For a successful technology, reality must take "
             "precedence over public relations, for nature cannot be fooled.", FadeIn(fin[0]), run_time=1.0)
        self.play(FadeIn(fin[1]), run_time=1.0)
        self.wait(2.2)
        self.play(FadeIn(fin[2]), FadeIn(fin[3]), run_time=1.0)
        self.vo_wait()
        self.wait(0.6)
        self.play(clear(), FadeOut(fin), run_time=0.7)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 20, RED_INK).move_to(P(0, 3.05))
        steps = VGroup(
            serif("1. Get two small rubber O-rings or tap washers.", 19, INK),
            serif("2. Squeeze each flat in a binder clip.", 19, INK),
            serif("3. One in ice water, one at room temperature,", 19, INK),
            serif("for ten minutes.", 19, INK),
            serif("4. Release both; measure thickness at once,", 19, INK),
            serif("then every few seconds.", 19, INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(P(-3.2, 0.9))
        steps[3].shift(RIGHT * 0.3)
        steps[5].shift(RIGHT * 0.3)
        line("Try it yourself. Get two small rubber O-rings or tap washers from a hardware shop.", FadeIn(tiy),
             FadeIn(steps[0]), run_time=0.8)
        self.vo_wait()
        c_ring = Ellipse(width=0.9, height=0.3, fill_color=INK, fill_opacity=1, stroke_width=0)
        c_top = Rectangle(width=1.4, height=0.14, fill_color=INK, fill_opacity=1, stroke_width=0).next_to(c_ring, UP, buff=0)
        c_bot = c_top.copy().next_to(c_ring, DOWN, buff=0)
        c_l = note("ring squeezed in a binder clip", 14, INK).next_to(c_bot, DOWN, buff=0.12)
        clip = VGroup(c_ring, c_top, c_bot, c_l)
        clip.move_to(P(3.6, 2.0))
        line("Squeeze each one flat in a binder clip. Put one in ice water and keep the other at room "
             "temperature, for ten minutes.", FadeIn(steps[1]), FadeIn(clip), run_time=0.8)
        self.play(FadeIn(steps[2:4]), run_time=0.8)
        self.vo_wait()
        ax2 = Axes(x_range=[0, 30, 10], y_range=[0, 1.1, 0.5], x_length=4.6, y_length=2.2, tips=False,
                   axis_config={"color": INK, "stroke_width": 2, "tick_size": 0.05}).move_to(P(3.6, -0.6))
        ax2_x = note("seconds after release", 14, INK).next_to(ax2.x_axis, DOWN, buff=0.32)
        ax2_y = note("thickness", 14, INK).rotate(PI / 2).next_to(ax2.y_axis, LEFT, buff=0.1)
        tk2 = VGroup(*[serif(str(v), 12, FADED).next_to(ax2.c2p(v, 0), DOWN, buff=0.06) for v in (10, 20, 30)])
        wr = ax2.plot(lambda t: 1 - 0.55 * np.exp(-t / 1.5), x_range=[0, 30], color=SEPIA, stroke_width=4)
        cr = ax2.plot(lambda t: 1 - 0.55 * np.exp(-t / 14), x_range=[0, 30], color=BLUE_INK, stroke_width=4)
        wr_l = note("room temperature", 13, SEPIA).next_to(ax2.c2p(20, 1.0), UP, buff=0.05)
        cr_l = note("ice water", 13, BLUE_INK).next_to(ax2.c2p(16, 0.7), DOWN, buff=0.08)
        ex_n = note("the shape you may see; your numbers will differ", 12).next_to(ax2_x, DOWN, buff=0.08)
        line("Release both, and measure their thickness with a ruler or caliper, at once and then every few "
             "seconds.", FadeIn(steps[4:]), FadeIn(ax2), FadeIn(ax2_x), FadeIn(ax2_y), FadeIn(tk2), run_time=0.8)
        self.vo_wait()
        line("Plot thickness against time. The warm ring should recover faster. Try other rubbers too: some cope "
             "with cold far better than others.", Create(wr), FadeIn(wr_l), run_time=1.6)
        self.play(Create(cr), FadeIn(cr_l), FadeIn(ex_n), run_time=1.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tiy, steps, clip, ax2, ax2_x, ax2_y, tk2, wr, cr, wr_l, cr_l, ex_n)),
                  run_time=0.7)

        # ================= close =================
        g3 = cup(1.1).move_to(P(0, 1.2))
        last = serif("A ring of rubber, a cup of ice water, and an honest question.", 30, INK).move_to(P(0, -0.4))
        if last.width > 12.4:
            last.scale_to_fit_width(12.4)
        mem = note("In memory of the crew of Challenger, flight 51-L", 18, SEPIA).next_to(last, DOWN, buff=0.5)
        line("A ring of rubber, a cup of ice water, and an honest question.", FadeIn(g3), FadeIn(last),
             run_time=1.0)
        self.vo_wait()
        self.play(FadeIn(mem), run_time=1.0)
        self.wait(2.0)
        self.play(clear(), FadeOut(VGroup(g3, last, mem)), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after J. Gleick, Genius (1992) · sources in the episode notes", 17),
                     note("facts checked against the Report of the Presidential Commission (vols. 1, 2 and 4), "
                          "APS News, CBS News and History.com", 17),
                     note("silhouettes, shuttle and joint stylised · seal curves illustrative · numbers from the "
                          "record · Manim · synthetic narration", 15)
                     ).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        for m in end:
            if m.width > 12.8:
                m.scale_to_fit_width(12.8)
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(3.0)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)


class Thumbnail(Scene):
    """Still for the thumbnail: manim -qh -s episodes/I043_ice_water_oring.py Thumbnail"""

    def construct(self):
        self.camera.background_color = PAPER
        paper, frame = paper_background()
        self.add(paper, frame)
        g = cup(2.6).move_to(P(-3.6, 0.0))
        ring = Annulus(inner_radius=0.55, outer_radius=0.75, fill_color=INK, fill_opacity=1, stroke_width=0) \
            .stretch(0.55, 1).move_to(P(-3.6, -0.6))
        t1 = serif("Nature", 84, INK, bold=True)
        t2 = serif("Cannot Be", 84, INK, bold=True)
        t3 = serif("Fooled", 84, RED_INK, bold=True)
        t4 = serif("Feynman, ice water and the Challenger seal", 28, INK, italic=True)
        txt = VGroup(t1, t2, t3, t4).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(P(2.6, 0.0))
        th = VGroup(serif("36°F", 40, RED_INK, bold=True), note("at launch", 18)).arrange(DOWN, buff=0.05) \
            .move_to(P(-5.2, 2.7))
        self.add(g, ring, txt, th)
