"""I045 Planck's Act of Desperation, a Science Stories episode.

After M. Kumar, Quantum: Einstein, Bohr and the Great Debate about the Nature of Reality (2008).
Script and sources: episodes/I045_script.md

Render:  manim -qh --frame_rate 30 episodes/I045_planck_desperation.py PlancksDesperation
Then:    scripts/finish_video.sh media/videos/I045_planck_desperation/1080p30/PlancksDesperation.mp4 out/I045_planck_desperation.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

# ---------- physics, exact (SI, 2019 values) ----------
H = 6.62607015e-34      # J s, exact since 20 May 2019
C = 2.99792458e8        # m/s
KB = 1.380649e-23       # J/K
WIEN_B = 2.897771955e-3  # m K


def planck(lam_um, T):
    lam = lam_um * 1e-6
    return 2 * H * C ** 2 / lam ** 5 / np.expm1(H * C / (lam * KB * T))


def wien(lam_um, T):
    lam = lam_um * 1e-6
    return 2 * H * C ** 2 / lam ** 5 * np.exp(-H * C / (lam * KB * T))


def rayleigh(lam_um, T):
    lam = lam_um * 1e-6
    return 2 * C * KB * T / lam ** 4


def x_of(lam_um, T):
    return H * C / (lam_um * 1e-6 * KB * T)


T_REF = 1500.0
NORM = planck(WIEN_B / T_REF * 1e6, T_REF)          # peak of the 1500 K curve = 1
assert abs(WIEN_B / 1000 * 1e6 - 2.9) < 0.01          # 1000 K peak ~2.9 um
assert abs(WIEN_B / 973.15 * 1e6 - 2.98) < 0.01       # ~700 C coil peaks near 3 um
assert 0.68 < wien(8, T_REF) / planck(8, T_REF) < 0.72 # Wien too low in the far infrared (ratio 1 - e^-x)
assert abs(wien(0.8, T_REF) / planck(0.8, T_REF) - 1) < 1e-5  # ...and right at short waves
assert rayleigh(100, T_REF) / planck(100, T_REF) < 1.06       # classical law right at long enough waves
P_ONE_SHORT = np.exp(-x_of(0.5, T_REF))               # chance of one packet at 0.5 um, 1500 K
assert 1 / 2.5e8 < P_ONE_SHORT < 1 / 1.8e8            # "about 1 in 200 million"
assert 1.1 < x_of(8, T_REF) < 1.3                     # long wave: one packet ~ one heat share
H_1900, H_NOW_CGS = 6.55e-27, H * 1e7                 # erg s
assert abs(H_NOW_CGS - 6.626e-27) < 1e-30
assert abs(525 + 273.15 - 798) < 1                    # Draper point, 525 C = 798 K

LAM_MAX = 8.0
VIS = (0.38, 0.75)
GLOW = "#c8641e"


def note(text, size=17, color=FADED):
    return serif(text, size, color, italic=True)


def P(x, y):
    return np.array([x, y, 0.0])


def glow_colour(t):
    """0 = cold iron, 1 = white hot (a pictorial ramp, not a colorimetric one)."""
    stops = [(0.0, "#2b2420"), (0.3, "#5a1a10"), (0.5, "#9b2d20"), (0.7, "#d0601e"), (0.85, "#eda640"),
             (1.0, "#fbeed0")]
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if t <= b:
            return interpolate_color(ManimColor(ca), ManimColor(cb), (t - a) / (b - a))
    return ManimColor(stops[-1][1])


def spectrum_axes(x0=-0.4, y0=0.25, w=9.0, h=4.4, ymax=1.25):
    ax = Axes(x_range=[0, LAM_MAX, 1], y_range=[0, ymax, 0.5], x_length=w, y_length=h, tips=False,
              axis_config={"color": INK, "stroke_width": 2, "tick_size": 0.05})
    ax.move_to(P(x0, y0))
    ticks = VGroup(*[serif(str(v), 13, FADED).next_to(ax.c2p(v, 0), DOWN, buff=0.08) for v in (1, 2, 4, 6, 8)])
    xl = note("wavelength (micrometres)", 15, INK).next_to(ax.x_axis, DOWN, buff=0.36)
    yl = note("brightness", 15, INK).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.12)
    vis = Rectangle(width=ax.c2p(VIS[1], 0)[0] - ax.c2p(VIS[0], 0)[0], height=h, stroke_width=0,
                    fill_opacity=0.22).move_to(ax.c2p(sum(VIS) / 2, ymax / 2))
    vis.set_fill(color=[BLUE_INK, "#5f8a4a", "#d0a030", RED_INK])
    vis.set_sheen_direction(RIGHT)
    vis_l = note("visible", 13, INK).next_to(vis, UP, buff=0.05)
    ir_l = note("infrared  →", 13, RED_INK).move_to(ax.c2p(7.2, 0.3))
    return ax, VGroup(ax, ticks, xl, yl, vis, vis_l, ir_l)


def curve(ax, fn, T, color, x_min=0.25, ymax=1.25, width=4, dashed=False):
    ls = np.arange(x_min, LAM_MAX, 0.005)
    inside = ls[fn(ls, T) / NORM <= ymax]
    x0 = inside[0] if len(inside) else x_min
    g = ax.plot(lambda l: fn(l, T) / NORM, x_range=[x0, LAM_MAX, 0.02], color=color,
                stroke_width=width, use_smoothing=False)
    return DashedVMobject(g, num_dashes=60) if dashed else g


def coil(scale=1.0, color=INK):
    pts = []
    for t in np.linspace(0, 3 * TAU, 300):
        r = 0.25 + 0.12 * t
        pts.append(P(r * np.cos(t), 0.42 * r * np.sin(t)))
    sp = VMobject(stroke_color=color, stroke_width=7).set_points_smoothly(pts)
    leads = VGroup(Line(pts[-1], pts[-1] + P(0.5, -0.5), color=INK, stroke_width=6),
                   Line(pts[0], P(0.25, -0.9), color=INK, stroke_width=6))
    return VGroup(sp, leads).scale(scale)


class PlancksDesperation(NarratedScene):
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
        title = serif("Planck's Act of Desperation", 56).next_to(orn1, DOWN, buff=0.35)
        sub = serif("how a cautious man let energy come in packets", 26, FADED, italic=True) \
            .next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("story after M. Kumar, Quantum: Einstein, Bohr and the Great Debate about the Nature of "
                      "Reality (2008)", 16).move_to([0, -2.6, 0])
        if credit.width > 12.4:
            credit.scale_to_fit_width(12.4)
        self.vo("Science Stories. Planck's act of desperation.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.wait(0.4)
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= Planck in Berlin =================
        place = spaced("Berlin · 1900", 18, SEPIA).move_to(P(0, 3.05))
        pl = cameo("plain", 0.85).move_to(P(-3.2, 0.5))
        pl_l = VGroup(serif("Max Planck", 24, INK), note("physicist, 1858–1947", 15),
                      note("professor at the University of Berlin", 15)).arrange(DOWN, buff=0.05) \
            .next_to(pl, DOWN, buff=0.25)
        sil_n = note("silhouette stylised, not a likeness", 12).next_to(pl_l, DOWN, buff=0.1)
        age = ink_card(VGroup(serif("aged 42", 24, INK), note("cautious, conservative,", 15),
                              note("no wish for a revolution", 15)).arrange(DOWN, buff=0.06), pad=0.2) \
            .move_to(P(2.4, 0.6))
        line("Berlin, 1900. Max Planck is forty-two, a professor of physics, and a cautious man. He does not want "
             "a revolution.", FadeIn(place), FadeIn(pl), FadeIn(pl_l), FadeIn(sil_n), run_time=1.2)
        self.play(FadeIn(age, shift=LEFT * 0.1), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(place, pl, pl_l, sil_n, age)), run_time=0.7)

        # ================= the glow of hot things =================
        bar = RoundedRectangle(corner_radius=0.12, width=5.0, height=0.7, stroke_color=INK, stroke_width=2.5,
                               fill_color=glow_colour(0), fill_opacity=1).move_to(P(0, 0.9))
        tongs = VGroup(Line(P(-2.5, 0.9), P(-4.6, 1.3), color=INK, stroke_width=6),
                       Line(P(-2.5, 0.9), P(-4.6, 0.5), color=INK, stroke_width=6))
        heat = ValueTracker(0.0)
        bar.add_updater(lambda m: m.set_fill(glow_colour(heat.get_value())))
        stage = VGroup(note("dull red", 18, INK), note("orange", 18, INK), note("nearly white", 18, INK)) \
            .arrange(RIGHT, buff=1.6).move_to(P(0, -0.3))
        line("His puzzle is the glow of hot things. Heat a bar of iron and it turns dull red, then orange, then "
             "nearly white.", FadeIn(bar), FadeIn(tongs), run_time=0.8)
        self.play(heat.animate.set_value(0.5), FadeIn(stage[0]), run_time=1.5)
        self.play(heat.animate.set_value(0.75), FadeIn(stage[1]), run_time=1.3)
        self.play(heat.animate.set_value(1.0), FadeIn(stage[2]), run_time=1.3)
        self.vo_wait()
        bb = ink_card(VGroup(serif("a black body", 22, INK), note("absorbs all light that falls on it;", 15),
                             note("its glow depends only on its temperature", 15)).arrange(DOWN, buff=0.06),
                      pad=0.18).move_to(P(0, -1.6))
        line("For a perfect absorber, which physicists call a black body, the colours of the glow depend only on "
             "its temperature.", FadeIn(bb, shift=UP * 0.1), run_time=1.0)
        self.vo_wait()
        goal = serif("one formula: brightness at every wavelength, for every temperature", 24, RED_INK) \
            .move_to(P(0, 2.6))
        line("So there should be one formula for that glow, at every wavelength and every temperature. Planck "
             "wanted it.", FadeIn(goal), run_time=1.0)
        self.vo_wait()
        bar.clear_updaters()
        self.play(clear(), FadeOut(VGroup(bar, tongs, stage, bb, goal)), run_time=0.7)

        # ================= the hump =================
        ax, axg = spectrum_axes()
        Tt = ValueTracker(1000.0)
        hump = always_redraw(lambda: curve(ax, planck, Tt.get_value(), INK))
        pk = always_redraw(lambda: Dot(ax.c2p(WIEN_B / Tt.get_value() * 1e6,
                                              planck(WIEN_B / Tt.get_value() * 1e6, Tt.get_value()) / NORM),
                                       radius=0.07, color=RED_INK))
        pk_l = always_redraw(lambda: note(f"{Tt.get_value():.0f} K · peak at {WIEN_B / Tt.get_value() * 1e6:.1f} µm",
                                          15, RED_INK).next_to(pk, UR, buff=0.08))
        line("Plot brightness against wavelength, and the measurements make a hump: rising from the short waves, "
             "peaking, then fading into the infrared.", FadeIn(axg), run_time=1.0)
        self.play(Create(hump), run_time=1.6)
        self.play(FadeIn(pk), FadeIn(pk_l), run_time=0.6)
        self.vo_wait()
        exact = note("curves computed from Planck's law", 12).next_to(axg, DOWN, buff=0.02).shift(RIGHT * 3.2)
        line("Heat the body more, and the hump grows taller, and its peak slides toward shorter waves. That is "
             "why red hot becomes white hot.", FadeIn(exact), run_time=0.6)
        ghosts = VGroup()
        for T in (1000, 1250):
            ghosts.add(curve(ax, planck, T, FADED, width=2))
        self.add(ghosts)
        self.play(Tt.animate.set_value(1500.0), run_time=3.0)
        self.vo_wait()
        hump.clear_updaters()
        pk.clear_updaters()
        pk_l.clear_updaters()
        self.play(FadeOut(pk), FadeOut(pk_l), FadeOut(ghosts), run_time=0.5)

        # ================= Wien's formula and the infrared =================
        wc = curve(ax, wien, T_REF, SEPIA, width=5, dashed=True)
        wl = VGroup(serif("Wilhelm Wien's formula", 18, SEPIA), note("1500 K", 13, SEPIA)) \
            .arrange(DOWN, buff=0.03).move_to(ax.c2p(5.3, 0.62))
        line("Wilhelm Wien had a formula that matched the short-wavelength side very well.", Create(wc),
             FadeIn(wl), run_time=1.6)
        self.vo_wait()
        # magnified inset of the infrared tail, 4 to 8 micrometres
        zx = ax.c2p(5, 0)[0]
        zone = Rectangle(width=ax.c2p(8, 0)[0] - zx, height=ax.c2p(0, 0.22)[1] - ax.c2p(0, 0)[1],
                         stroke_color=RED_INK, stroke_width=1.5).move_to(ax.c2p(6.5, 0.11))
        ins = Axes(x_range=[5, 8, 1], y_range=[0, 0.22, 0.1], x_length=4.0, y_length=2.1, tips=False,
                   axis_config={"color": INK, "stroke_width": 1.5, "tick_size": 0.04}).move_to(ax.c2p(6.0, 0.86))
        ins_bg = BackgroundRectangle(ins, color=PAPER, fill_opacity=1, buff=0.12).set_stroke(RED_INK, 1.5, 1)
        ins_p = ins.plot(lambda l: planck(l, T_REF) / NORM, x_range=[5, 8], color=INK, stroke_width=4)
        ins_w = DashedVMobject(ins.plot(lambda l: wien(l, T_REF) / NORM, x_range=[5, 8], color=SEPIA,
                                        stroke_width=4), num_dashes=30)
        ins_t = note("infrared, magnified", 13, RED_INK).next_to(ins_bg, UP, buff=0.05)
        dots = VGroup(*[Dot(ins.c2p(l, planck(l, T_REF) / NORM), radius=0.06, color=INK)
                        for l in (5.5, 6.25, 7.0, 7.75)])
        rk = VGroup(note("Heinrich Rubens and Ferdinand Kurlbaum, 1900", 13),
                    note("dots mark the true curve, not their actual data", 11)).arrange(DOWN, buff=0.02) \
            .next_to(ins_bg, DOWN, buff=0.08)
        low = Arrow(ins.c2p(6.0, planck(6.0, T_REF) / NORM + 0.002), ins.c2p(6.0, wien(6.0, T_REF) / NORM - 0.002),
                    color=RED_INK, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.45)
        low_l = note("Wien: too low", 14, RED_INK).next_to(ins.c2p(6.0, 0.04), DOWN, buff=0.05).shift(LEFT * 0.6)
        line("But by October 1900, Heinrich Rubens and Ferdinand Kurlbaum, measuring deep in the infrared, found "
             "that Wien's formula came out too low.", Create(zone), FadeOut(wl), run_time=1.0)
        self.play(FadeIn(ins_bg), FadeIn(ins), FadeIn(ins_t), run_time=0.6)
        self.play(Create(ins_p), Create(ins_w), run_time=1.0)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.25), FadeIn(rk), run_time=1.0)
        self.play(GrowArrow(low), FadeIn(low_l), run_time=0.8)
        self.vo_wait()
        inset = VGroup(zone, ins_bg, ins, ins_t, ins_p, ins_w, dots, rk, low, low_l)
        self.play(FadeOut(inset), hump.animate.set_stroke(opacity=0.25),
                  wc.animate.set_stroke(opacity=0.4), run_time=0.5)

        # ================= the classical answer =================
        rj = curve(ax, rayleigh, T_REF, RED_INK, x_min=0.6, width=5)
        rj_l = VGroup(serif("classical physics", 18, RED_INK), note("heat shared evenly among the waves", 13)) \
            .arrange(DOWN, buff=0.03).move_to(ax.c2p(6.75, 1.02))
        line("The obvious answer came from classical physics. Treat the light as waves, and share the heat out "
             "evenly among them.", FadeIn(rj_l), run_time=1.0)
        self.vo_wait()
        x_top = ax.p2c(rj.get_start())[0]
        inf = VGroup(Arrow(ax.c2p(x_top, 1.22), ax.c2p(x_top, 1.5), color=RED_INK, buff=0, stroke_width=4),
                     serif("to infinity", 18, RED_INK, italic=True).next_to(ax.c2p(x_top, 1.42), LEFT, buff=0.15))
        far = VGroup(note("agrees with experiment only far off", 12, RED_INK),
                     note("this chart, at much longer waves", 12, RED_INK)).arrange(DOWN, buff=0.02) \
            .next_to(rj_l, DOWN, buff=0.08)
        line("It agrees with experiment only at the longest waves, far off this chart. But shorter waves keep "
             "fitting in, without end. Give each its share, and the glow shoots to infinity.", Create(rj),
             FadeIn(far), run_time=2.4)
        self.play(FadeIn(inf), run_time=0.6)
        self.vo_wait()
        uvc = ink_card(VGroup(serif("“the ultraviolet catastrophe”", 20, RED_INK),
                              note("a name given later; Planck's own trigger", 13),
                              note("was the infrared data", 13)).arrange(DOWN, buff=0.04), pad=0.14) \
            .move_to(ax.c2p(6.45, 0.98))
        line("Every warm object would blaze in ultraviolet. This was later called the ultraviolet catastrophe, "
             "though it was not what drove Planck.", FadeOut(rj_l), FadeOut(far), FadeIn(uvc, shift=UP * 0.1),
             run_time=1.0)
        self.vo_wait()

        # ================= Planck's formula =================
        self.play(FadeOut(uvc), rj.animate.set_stroke(opacity=0.3), run_time=0.5)
        pc = curve(ax, planck, T_REF, INK, width=6)
        f_tex = MathTex(r"B = \frac{c_1}{\lambda^5}\,\frac{1}{e^{\,c_2/\lambda T}-1}", color=INK) \
            .scale(0.7)
        f_card = ink_card(VGroup(note("Planck, 19 October 1900", 14), f_tex,
                                 note("c₁, c₂: two constants fitted to the data", 12)).arrange(DOWN, buff=0.1),
                          pad=0.16) \
            .move_to(ax.c2p(6.5, 1.0))
        line("Planck found a formula that bends between the two: classical at long wavelengths, Wien's at short "
             "ones.", Create(pc), run_time=2.0)
        self.vo_wait()
        line("He showed it to the German Physical Society on the nineteenth of October, 1900. It fit the data. "
             "But it was a guess, and he needed a reason.", FadeIn(f_card, shift=UP * 0.1), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(axg, hump, wc, rj, inf, pc, exact)),
                  FadeOut(f_card), run_time=0.9)

        # ================= Boltzmann, packets =================
        bz = cameo("beard", 0.6).move_to(P(-4.6, 1.2))
        bz_l = VGroup(serif("Ludwig Boltzmann", 18, INK), note("counting the ways energy can be shared", 13)) \
            .arrange(DOWN, buff=0.04).next_to(bz, DOWN, buff=0.15)
        line("For that, he turned to a counting method from Ludwig Boltzmann, an approach he had long hoped to "
             "avoid.", FadeIn(bz), FadeIn(bz_l), run_time=1.0)
        self.vo_wait()
        # an energy ladder for one vibrating source
        BASE = -1.9

        def ladder(x, step, n, color, label, sub_label, numbers=True):
            rail = Line(P(x - 0.7, BASE), P(x - 0.7, BASE + 4.1), color=INK, stroke_width=2)
            rungs = VGroup(*[Line(P(x - 0.7, BASE + i * step), P(x + 0.7, BASE + i * step), color=color,
                                  stroke_width=4 if i else 2) for i in range(n)])
            nums = VGroup(*[serif(str(i), 13, FADED).next_to(rungs[i], RIGHT, buff=0.1)
                            for i in range(1, n if numbers else 0)])
            lab = VGroup(serif(label, 18, color), note(sub_label, 13)).arrange(DOWN, buff=0.03) \
                .next_to(rail, UP, buff=0.15).set_x(x)
            return VGroup(rail, rungs, nums, lab)

        lad0 = ladder(-0.6, 1.0, 5, SEPIA, "energy allowed", "whole packets only")
        half = DashedLine(P(-1.3, BASE + 2.5), P(0.1, BASE + 2.5), color=RED_INK, stroke_width=2)
        half_l = note("2½: not allowed", 13, RED_INK).next_to(half, LEFT, buff=0.1)
        line("And he made a strange assumption. The tiny vibrating sources of light could not hold just any amount "
             "of energy. Only whole packets: one, two, three, never two and a half.", FadeIn(lad0[0]), FadeIn(lad0[3]),
             run_time=0.8)
        self.play(LaggedStart(*[Create(r) for r in lad0[1]], lag_ratio=0.3), FadeIn(lad0[2]), run_time=1.6)
        self.play(Create(half), FadeIn(half_l), run_time=0.8)
        self.vo_wait()
        ehv = MathTex(r"E = h\nu", color=RED_INK).scale(1.3).move_to(P(3.2, 0.9))
        ehv_l = VGroup(note("one packet of energy", 14), note("h: a new constant · ν: the frequency", 14)) \
            .arrange(DOWN, buff=0.04).next_to(ehv, DOWN, buff=0.2)
        line("The size of a packet grows with frequency. E equals h times nu.", Write(ehv), FadeIn(ehv_l),
             run_time=1.2)
        self.vo_wait()
        self.play(FadeOut(VGroup(lad0, half, half_l, bz, bz_l)), VGroup(ehv, ehv_l).animate.move_to(P(-4.4, 1.2)),
                  run_time=0.8)

        # two ladders, long wave and short wave, with the heat budget kT
        KT = 0.62    # drawing scale: 1 heat share = 0.62 units of height
        LAM_LONG = 24.0
        lad_l = ladder(-0.4, KT * x_of(LAM_LONG, T_REF), 15, SEPIA, f"long wave, {LAM_LONG:.0f} µm",
                       "small packets", numbers=False)
        lad_s = ladder(3.6, 4.0, 2, BLUE_INK, "short wave, 0.5 µm", "one packet = 19 heat shares")
        cut = note("first rung drawn low: really 19 heat shares up", 12).move_to(P(5.05, -0.6))
        budget = DashedLine(P(-1.4, BASE + KT), P(4.6, BASE + KT), color=RED_INK, stroke_width=2.5)
        budget_l = VGroup(note("typical heat share", 13, RED_INK), note("kT, at 1500 K", 13, RED_INK)) \
            .arrange(DOWN, buff=0.02).next_to(budget, DOWN, buff=0.08).set_x(1.45)
        n_cheap = int(KT / (KT * x_of(LAM_LONG, T_REF)) * 1.0 + 1e-9)
        cheap = VGroup(*[lad_l[1][i].copy().set_stroke(GLOW, 7) for i in range(1, n_cheap + 1)])
        cheap_l = note("easily afforded", 13, GLOW).next_to(cheap, LEFT, buff=0.3)
        line("Now the trick. For long waves the packets are small, and the heat buys plenty of them.",
             FadeIn(lad_l), Create(budget), FadeIn(budget_l), run_time=1.2)
        self.play(LaggedStart(*[Create(c) for c in cheap], lag_ratio=0.3), FadeIn(cheap_l), run_time=1.0)
        self.vo_wait()
        odds = ink_card(VGroup(note("chance of holding even one packet", 13),
                               serif(f"about 1 in {round(1 / P_ONE_SHORT / 1e6, -2):.0f} million", 19, BLUE_INK),
                               MathTex(r"e^{-h\nu/kT}", color=INK).scale(0.6)).arrange(DOWN, buff=0.05),
                        pad=0.12).move_to(P(4.6, 0.4))
        line("For short waves one packet costs more than the heat can usually pay. Those waves are rarely "
             "excited, and stay nearly dark.", FadeIn(lad_s), FadeIn(cut), run_time=1.0)
        self.play(FadeIn(odds, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(lad_l, lad_s, cut, budget, budget_l, cheap, cheap_l, odds, ehv, ehv_l)),
                  run_time=0.7)

        # ================= the curve turns down =================
        ax2, axg2 = spectrum_axes(-0.2, 0.15, 9.0, 4.2)
        rj2 = curve(ax2, rayleigh, T_REF, RED_INK, x_min=0.6, width=3).set_stroke(opacity=0.35)
        pc2 = curve(ax2, planck, T_REF, INK, width=6)
        dec = ink_card(VGroup(note("German Physical Society, Berlin", 13),
                              serif("14 December 1900", 20, INK),
                              note("the derivation, with energy elements", 13),
                              MathTex(r"c_1 = 2hc^2 \qquad c_2 = hc/k", color=INK).scale(0.55)
                              ).arrange(DOWN, buff=0.06),
                       pad=0.14).move_to(ax2.c2p(5.6, 0.85))
        line("So the curve turns down instead of running away. Planck gave this derivation on the fourteenth of "
             "December, 1900.", FadeIn(axg2), FadeIn(rj2), run_time=0.8)
        self.play(Create(pc2), run_time=1.8)
        self.play(FadeIn(dec, shift=UP * 0.1), run_time=0.6)
        self.vo_wait()
        hc = ink_card(VGroup(serif("h", 30, RED_INK, italic=True),
                             serif("Planck, 1900:  6.55 × 10⁻²⁷ erg·s", 18, INK),
                             serif("today:  6.626 × 10⁻²⁷ erg·s", 18, INK),
                             note("(6.62607015 × 10⁻³⁴ J·s, exact since 2019)", 12)).arrange(DOWN, buff=0.06),
                      pad=0.16).move_to(ax2.c2p(5.6, 0.62))
        line("Out of it came a new constant of nature, h. His value was within about one percent of today's.",
             FadeOut(dec), FadeIn(hc), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(axg2, rj2, pc2, hc)), run_time=0.7)

        # ================= despair =================
        pl2 = cameo("plain", 0.75).move_to(P(-4.3, 0.6))
        quote = ink_card(VGroup(note("Planck, letter to R. W. Wood, 1931 (in English translation)", 13),
                                serif("“an act of despair ...", 26, INK),
                                serif("a theoretical interpretation", 26, INK),
                                serif("had to be found at any price”", 26, RED_INK)).arrange(DOWN, buff=0.08),
                         pad=0.22).move_to(P(1.6, 0.6))
        line("Planck did not think he had found a truth about light. Years later he called it an act of despair: "
             "an explanation had to be found at any price.", FadeIn(pl2), FadeIn(quote, shift=LEFT * 0.1),
             run_time=1.2)
        self.vo_wait()
        q2 = note("“My futile attempts to put the elementary quantum of action into the classical theory "
                  "continued for a number of years”", 15, INK).move_to(P(0.6, -1.85))
        if q2.width > 11.2:
            q2.scale_to_fit_width(11.2)
        line("For years he tried to fit the quantum back into classical physics. It would not go.", FadeIn(q2),
             run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(pl2, quote, q2)), run_time=0.7)

        # ================= what followed =================
        tl = Line(P(-6.0, 0.0), P(6.0, 0.0), color=INK, stroke_width=2)
        yrs = note("events in order, not to scale", 12).move_to(P(0, -2.3))
        xs = {1900: -4.5, 1905: -1.5, 1918: 1.5, 2019: 4.5}

        def ev(year, top, bottom, up=True, color=INK):
            d = Dot(P(xs[year], 0), radius=0.09, color=color)
            txt = VGroup(serif(top, 24, color), *[note(b, 15) for b in bottom]).arrange(DOWN, buff=0.04)
            txt.next_to(d, UP if up else DOWN, buff=0.35)
            return VGroup(d, txt)

        e1900 = ev(1900, "1900", ["Planck's energy packets"], True, RED_INK)
        e1905 = ev(1905, "1905", ["Einstein: light itself", "comes in quanta"], False)
        e1918 = ev(1918, "1918", ["Nobel Prize, “for the", "discovery of energy quanta”"], True)
        e2019 = ev(2019, "2019", ["h fixed exactly;", "it defines the kilogram"], False, RED_INK)
        line("Others took it further. In 1905, Einstein argued that light itself comes in quanta. In 1918, Planck "
             "won the Nobel Prize for the discovery of energy quanta.", Create(tl), FadeIn(yrs), FadeIn(e1900),
             run_time=1.0)
        self.play(FadeIn(e1905), run_time=0.8)
        self.play(FadeIn(e1918), run_time=0.8)
        self.vo_wait()
        line("Today his constant is so trusted that, since 2019, it defines the kilogram.", FadeIn(e2019),
             run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tl, yrs, e1900, e1905, e1918, e2019)), run_time=0.7)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 20, RED_INK).move_to(P(0, 3.05))
        cl = coil(1.0).move_to(P(-4.0, 1.2))
        cl_glow = ValueTracker(0.0)
        cl[0].add_updater(lambda m: m.set_stroke(color=glow_colour(cl_glow.get_value())))
        safe = note("from a safe distance · never touch it", 14, RED_INK).next_to(cl, DOWN, buff=0.25)
        line("Try it yourself. Watch the coil of an electric stove as it heats up, from a safe distance. Never "
             "touch it.", FadeIn(tiy), FadeIn(cl), FadeIn(safe), run_time=1.0)
        self.vo_wait()
        ax3 = Axes(x_range=[0, 6, 1], y_range=[0, 1.1, 0.5], x_length=6.2, y_length=3.0, tips=False,
                   axis_config={"color": INK, "stroke_width": 2, "tick_size": 0.05}).move_to(P(2.6, 0.5))
        n3 = planck(WIEN_B / 973.15 * 1e6, 973.15)
        t3 = ValueTracker(600.0)
        c3 = always_redraw(lambda: ax3.plot(lambda l: planck(l, t3.get_value()) / n3, x_range=[0.3, 6, 0.02],
                                            color=INK, stroke_width=4, use_smoothing=False))
        vis3 = Rectangle(width=ax3.c2p(VIS[1], 0)[0] - ax3.c2p(VIS[0], 0)[0], height=3.0, stroke_width=0,
                         fill_opacity=0.25).move_to(ax3.c2p(sum(VIS) / 2, 0.55))
        vis3.set_fill(color=[BLUE_INK, "#5f8a4a", "#d0a030", RED_INK]).set_sheen_direction(RIGHT)
        tk3 = VGroup(*[serif(str(v), 12, FADED).next_to(ax3.c2p(v, 0), DOWN, buff=0.06) for v in (1, 3, 5)])
        x3 = note("wavelength (µm)", 13, INK).next_to(ax3.x_axis, DOWN, buff=0.3)
        v3 = note("visible", 12, INK).next_to(vis3, UP, buff=0.04)
        temp = always_redraw(lambda: serif(f"{t3.get_value() - 273.15:.0f} °C", 22, RED_INK)
                             .move_to(ax3.c2p(5.2, 1.08)))
        line("At first you can feel its heat but see nothing. That is infrared, the long-wave side of the hump.",
             FadeIn(ax3), FadeIn(vis3), FadeIn(tk3), FadeIn(x3), FadeIn(v3), FadeIn(c3), FadeIn(temp), run_time=1.0)
        self.vo_wait()
        dp = note("glow begins near 525 °C: the Draper point (J. W. Draper, 1847)", 13, INK) \
            .next_to(x3, DOWN, buff=0.12)
        line("Near five hundred and twenty-five degrees Celsius, a dull red glow appears. Hotter still, it "
             "brightens toward orange.", t3.animate.set_value(798.0), cl_glow.animate.set_value(0.42),
             FadeIn(dp), run_time=2.0)
        self.play(t3.animate.set_value(973.15), cl_glow.animate.set_value(0.68), run_time=2.0)
        self.vo_wait()
        pk3 = Dot(ax3.c2p(WIEN_B / 973.15 * 1e6, 1.0), radius=0.07, color=RED_INK)
        pk3_l = note("peak near 3 µm, at about 700 °C", 13, RED_INK).next_to(pk3, UP, buff=0.1)
        tail = ax3.get_area(ax3.plot(lambda l: planck(l, 973.15) / n3, x_range=[0.3, 0.9]), x_range=[0.6, 0.9],
                            color=RED_INK, opacity=0.6)
        tail_l = VGroup(note("what you see:", 13, RED_INK), note("the tiny tail", 13, RED_INK),
                        note("in the visible", 13, RED_INK)).arrange(DOWN, buff=0.02).next_to(ax3, LEFT, buff=0.15) \
            .shift(DOWN * 0.6)
        line("Even then, the hump peaks in the infrared, near three micrometres. You only see its short-wave "
             "tail.",
             FadeIn(pk3), FadeIn(pk3_l), run_time=0.8)
        self.play(FadeIn(tail), FadeIn(tail_l), run_time=0.8)
        self.vo_wait()
        c3.clear_updaters()
        temp.clear_updaters()
        cl[0].clear_updaters()
        self.play(clear(), FadeOut(VGroup(tiy, cl, safe, ax3, c3, vis3, tk3, x3, v3, temp, dp, pk3, pk3_l, tail,
                                          tail_l)), run_time=0.7)

        # ================= close =================
        ehv2 = MathTex(r"E = h\nu", color=RED_INK).scale(1.6).move_to(P(0, 1.3))
        last = serif("A cautious man, a desperate guess, and a packet of energy that began quantum physics.", 28,
                     INK).move_to(P(0, -0.3))
        if last.width > 12.4:
            last.scale_to_fit_width(12.4)
        line("A cautious man, a desperate guess, and a packet of energy that began quantum physics.", Write(ehv2),
             FadeIn(last), run_time=1.2)
        self.vo_wait()
        self.wait(0.8)
        self.play(clear(), FadeOut(VGroup(ehv2, last)), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after M. Kumar, Quantum (2008) · sources in the episode notes", 17),
                     note("facts checked against Britannica, MacTutor (St Andrews), APS News, the Max Planck Society, "
                          "NobelPrize.org and NIST", 17),
                     note("silhouettes stylised · curves computed from Planck's, Wien's and the classical laws · "
                          "ladder heights not to scale · Manim · synthetic narration", 15)
                     ).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        for m in end:
            if m.width > 12.8:
                m.scale_to_fit_width(12.8)
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(2.6)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)


class Thumbnail(Scene):
    """Still for the thumbnail: manim -qh -s episodes/I045_planck_desperation.py Thumbnail"""

    def construct(self):
        self.camera.background_color = PAPER
        paper, frame = paper_background()
        self.add(paper, frame)
        ax = Axes(x_range=[0, LAM_MAX, 1], y_range=[0, 1.25, 0.5], x_length=5.6, y_length=4.6, tips=False,
                  axis_config={"color": INK, "stroke_width": 3, "include_ticks": False}).move_to(P(-3.7, -0.2))
        pc = curve(ax, planck, T_REF, INK, width=8)
        rj = curve(ax, rayleigh, T_REF, RED_INK, x_min=0.6, width=6)
        inf = serif("→ ∞ ?", 50, RED_INK, bold=True).next_to(ax.c2p(4.3, 1.25), RIGHT, buff=0.15)
        t1 = serif("Planck's", 80, INK, bold=True)
        t2 = serif("Act of", 80, INK, bold=True)
        t3 = serif("Desperation", 80, RED_INK, bold=True)
        t4 = MathTex(r"E = h\nu", color=INK).scale(1.5)
        t5 = serif("Berlin, 1900", 28, INK, italic=True)
        txt = VGroup(t1, t2, t3, VGroup(t4, t5).arrange(RIGHT, buff=0.5)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.22).move_to(P(3.2, 0.0))
        if txt.width > 6.3:
            txt.scale_to_fit_width(6.3)
        txt.move_to(P(3.35, -0.1))
        self.add(ax, rj, pc, inf, txt)
