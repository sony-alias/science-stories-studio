"""I021 Why Cracks Grow: Griffith's Glass, a Science Stories episode.

After J. E. Gordon, Structures: Or Why Things Don't Fall Down (1978). Script and sources: episodes/I021_script.md

Render:  manim -qh --frame_rate 30 episodes/I021_griffith_cracks.py GriffithCracks
Then:    scripts/finish_video.sh media/videos/I021_griffith_cracks/1080p30/GriffithCracks.mp4 out/I021_griffith_cracks.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

GLASS = "#7f9ea6"
GLASS_FILL = "#c9d8d6"


def note(text, size=17, color=FADED):
    return serif(text, size, color, italic=True)


def poly(pts, color=INK, width=2.5):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners([np.array([p[0], p[1], 0]) for p in pts])
    return m


# ---------- lines of force around an elliptical hole (potential-flow analogy, an illustration) ----------
def force_lines(A, B, cs, y_span=2.2, x_clip=2.4, n=90):
    """Lines of a uniform vertical 'flow' bent round an ellipse with semi-axes A (across) and B (along the load).

    Joukowski map z = zeta + k^2/zeta takes the circle |zeta| = R to the ellipse; in the zeta plane the lines are
    x (1 - R^2 / r^2) = c. Returns a list of point arrays (local coordinates, ellipse at the origin)."""
    R = (A + B) / 2
    k2 = R * (A - B) / 2
    out = []
    ys = np.concatenate([np.linspace(-y_span * 1.3, -R * 1.0001, n // 2), np.linspace(R * 1.0001, y_span * 1.3, n // 2)])
    ys = np.linspace(-y_span * 1.3, y_span * 1.3, n)
    for c in cs:
        s = np.sign(c)
        cc = abs(c)
        pts = []
        for y in ys:
            lo = np.sqrt(max(R * R - y * y, 0.0)) + 1e-9
            hi = cc + R + 6
            for _ in range(48):
                mid = 0.5 * (lo + hi)
                f = mid - R * R * mid / (mid * mid + y * y)
                if f < cc:
                    lo = mid
                else:
                    hi = mid
            x = s * 0.5 * (lo + hi)
            zeta = complex(x, y)
            z = zeta + k2 / zeta
            if abs(z.imag) <= y_span and abs(z.real) <= x_clip:
                pts.append([z.real, z.imag, 0.0])
        if len(pts) > 2:
            out.append(np.array(pts))
    return out


def glass_rod(w=4.0, h=0.42):
    body = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=GLASS, stroke_width=2.5,
                            fill_color=GLASS_FILL, fill_opacity=0.9)
    shine = Line(LEFT * (w / 2 - 0.3) + UP * h * 0.22, RIGHT * (w / 2 - 0.3) + UP * h * 0.22, color=WHITE,
                 stroke_width=2, stroke_opacity=0.7)
    return VGroup(body, shine)


def crack_mark(p, length=0.12, angle=0.0, color=INK, width=1.6):
    p = np.array([p[0], p[1], 0])
    d = np.array([np.cos(angle), np.sin(angle), 0]) * length / 2
    return Line(p - d, p + d, color=color, stroke_width=width)


class GriffithCracks(NarratedScene):
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
        title = serif("Why Cracks Grow", 56).next_to(orn1, DOWN, buff=0.35)
        sub = serif("A. A. Griffith and the strength of glass", 26, FADED, italic=True).next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("after J. E. Gordon, Structures: Or Why Things Don't Fall Down (1978)", 16).move_to([0, -2.6, 0])
        self.vo("Science Stories. Why cracks grow.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.3)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= Griffith and the glass =================
        cam = cameo("collar", 0.95).move_to([-4.3, 0.55, 0])
        cam_l = note("A. A. Griffith (1893–1963) · stylised silhouette", 15).next_to(cam, DOWN, buff=0.2)
        place = VGroup(spaced("Farnborough, England", 20, SEPIA),
                       serif("around 1920", 26, INK, italic=True)).arrange(DOWN, buff=0.15).move_to([1.6, 2.5, 0])
        rod = glass_rod(4.6, 0.46).move_to([1.6, 0.6, 0])
        line("Farnborough, England, around 1920. A young engineer named Alan Arnold Griffith is breaking glass on purpose.",
             FadeIn(cam, shift=RIGHT * 0.2), FadeIn(cam_l), FadeIn(place), run_time=1.0)
        self.play(FadeIn(rod), run_time=0.7)
        self.vo_wait()
        rae = ink_card(VGroup(serif("Royal Aircraft Establishment", 22, INK),
                              note("how strong is a material, exactly?", 17)).arrange(DOWN, buff=0.1)).move_to([1.6, -1.15, 0])
        line("He works at the Royal Aircraft Establishment, where engineers need to know exactly how strong their "
             "materials are.", FadeIn(rae, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()

        # pull and snap
        tug = ValueTracker(0.0)
        arrL = always_redraw(lambda: Arrow([-0.75 - tug.get_value(), 0.6, 0], [-1.85 - tug.get_value(), 0.6, 0],
                                           buff=0, color=RED_INK, stroke_width=5,
                                           max_tip_length_to_length_ratio=0.3))
        arrR = always_redraw(lambda: Arrow([3.95 + tug.get_value(), 0.6, 0], [5.05 + tug.get_value(), 0.6, 0],
                                           buff=0, color=RED_INK, stroke_width=5,
                                           max_tip_length_to_length_ratio=0.3))
        line("Glass is a perfect test. It does not bend out of shape, or flow, before it breaks. It simply snaps.",
             FadeOut(rae), FadeIn(arrL), FadeIn(arrR), run_time=0.8)
        self.play(tug.animate.set_value(0.25), run_time=1.6, rate_func=there_and_back_with_pause)
        left_half = VGroup(Polygon([-0.7, 0.83, 0], [1.75, 0.83, 0], [1.62, 0.6, 0], [1.72, 0.37, 0], [-0.7, 0.37, 0],
                                   stroke_color=GLASS, stroke_width=2.5, fill_color=GLASS_FILL, fill_opacity=0.9))
        right_half = VGroup(Polygon([1.75, 0.83, 0], [3.9, 0.83, 0], [3.9, 0.37, 0], [1.72, 0.37, 0], [1.62, 0.6, 0],
                                    stroke_color=GLASS, stroke_width=2.5, fill_color=GLASS_FILL, fill_opacity=0.9))
        self.remove(rod)
        self.add(left_half, right_half)
        snap = serif("snap", 30, RED_INK, italic=True).move_to([1.7, 1.45, 0])
        self.play(left_half.animate.shift(LEFT * 0.35).rotate(-4 * DEGREES),
                  right_half.animate.shift(RIGHT * 0.35).rotate(4 * DEGREES),
                  tug.animate.set_value(0.5), FadeIn(snap, scale=1.4), run_time=0.5)
        self.vo_wait()
        arrL.clear_updaters()
        arrR.clear_updaters()
        self.play(FadeOut(VGroup(left_half, right_half, arrL, arrR, snap, place)), run_time=0.6)

        # ================= the puzzle: theory vs reality =================
        base_y = -2.35
        ax_line = Line([-1.2, base_y, 0], [5.6, base_y, 0], color=INK, stroke_width=2)
        bar_h = 4.6
        th_bar = Rectangle(width=1.3, height=bar_h, stroke_color=INK, stroke_width=2, fill_color=SEPIA,
                           fill_opacity=0.55).move_to([0.6, base_y + bar_h / 2, 0])
        real_bar = Rectangle(width=1.3, height=bar_h / 100, stroke_color=RED_INK, stroke_width=3, fill_color=RED_INK,
                             fill_opacity=0.9).move_to([3.6, base_y + bar_h / 200, 0])
        th_l = VGroup(serif("theory", 22, INK), note("≈ 10,000 MPa", 18, INK)).arrange(DOWN, buff=0.06).next_to(
            th_bar, RIGHT, buff=0.2).align_to(th_bar, UP)
        atoms = VGroup(*[Dot([0.1 + 0.25 * i, 2.75, 0], radius=0.06, color=INK) for i in range(5)])
        atoms_l = note("pull the atoms apart", 15).next_to(atoms, LEFT, buff=0.15)
        real_l = VGroup(serif("real glass", 22, RED_INK), note("≈ 100 MPa", 18, RED_INK)).arrange(DOWN, buff=0.06).next_to(
            real_bar, UP, buff=0.25)
        fig_note = note("modern round figures, for scale", 14).move_to([4.2, -2.65, 0])
        line("And glass holds a puzzle. Work out the force needed to pull its atoms apart, and you expect a strength of "
             "roughly ten thousand megapascals.", cam.animate.scale(0.8).move_to([-4.6, 1.1, 0]),
             cam_l.animate.scale(0.9).move_to([-4.6, -0.55, 0]), Create(ax_line), run_time=1.0)
        self.play(FadeIn(atoms), FadeIn(atoms_l), GrowFromEdge(th_bar, DOWN), FadeIn(th_l), run_time=1.6)
        self.vo_wait()
        line("Pull on an ordinary piece of glass, and it breaks at around a hundred. A hundred times weaker than theory, "
             "or worse.", GrowFromEdge(real_bar, DOWN), FadeIn(real_l), FadeIn(fig_note), run_time=1.0)
        ratio = serif("× 1/100", 30, RED_INK).move_to([2.1, 0.7, 0])
        self.play(FadeIn(ratio, scale=1.2), run_time=0.6)
        self.vo_wait()
        q1 = VGroup(serif("Is the theory wrong?", 26, INK), serif("Or is the glass?", 26, RED_INK, italic=True)).arrange(
            DOWN, buff=0.18).move_to([-4.6, -1.6, 0])
        line("The obvious answer is that the theory is wrong. Griffith suspected the glass.", FadeIn(q1[0]), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(q1[1], shift=UP * 0.1), run_time=0.6)
        self.vo_wait()
        self.play(FadeOut(VGroup(ax_line, th_bar, real_bar, th_l, real_l, atoms, atoms_l, fig_note, ratio, q1)),
                  FadeOut(cam), FadeOut(cam_l), run_time=0.8)

        # ================= fibres =================
        fibres = VGroup()
        for i, t in enumerate([0.36, 0.22, 0.12, 0.06, 0.025]):
            fibres.add(RoundedRectangle(corner_radius=t / 2, width=4.2, height=t, stroke_width=0.8, stroke_color=GLASS,
                                        fill_color=GLASS, fill_opacity=0.85).move_to([-3.3, 1.6 - 0.75 * i, 0]))
        fib_l = note("drawn thinner and thinner", 16).next_to(fibres, UP, buff=0.25)
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1], x_length=4.6, y_length=3.8, tips=False,
                  axis_config={"color": INK, "stroke_width": 2, "include_ticks": False}).move_to([3.2, 0.25, 0])
        xl = note("fibre thickness →", 15).next_to(ax.x_axis, DOWN, buff=0.15)
        yl = note("breaking strength", 15).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.15)
        theory = DashedLine(ax.c2p(0, 4.5), ax.c2p(5, 4.5), color=SEPIA, stroke_width=2)
        theory_l = note("theoretical strength", 14, SEPIA).next_to(theory, UP, buff=0.06).align_to(theory, RIGHT)
        curve = ax.plot(lambda x: 0.55 + 3.6 / (1 + 1.6 * x ** 1.1), x_range=[0.05, 5], color=RED_INK, stroke_width=4)
        schem = note("schematic: the trend, not Griffith's numbers", 14).next_to(ax, DOWN, buff=0.45)
        line("He drew glass into fibres, thinner and thinner. The thinner the fibre, the stronger it was, creeping up "
             "towards the theoretical strength.", LaggedStart(*[FadeIn(f, shift=RIGHT * 0.3) for f in fibres],
                                                              lag_ratio=0.25), FadeIn(fib_l), run_time=1.6)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(theory), FadeIn(theory_l), run_time=1.0)
        self.play(Create(curve.reverse_points()), FadeIn(schem), run_time=2.2)
        self.vo_wait()

        # flaws: thick rod full of tiny cracks, thin fibre with few
        thick = RoundedRectangle(corner_radius=0.3, width=4.6, height=1.3, stroke_color=GLASS, stroke_width=2.5,
                                 fill_color=GLASS_FILL, fill_opacity=0.9).move_to([-3.0, 0.9, 0])
        rng = np.random.default_rng(21)
        flaws = VGroup(*[crack_mark([rng.uniform(-5.0, -1.0), rng.uniform(0.4, 1.4)], rng.uniform(0.06, 0.16),
                                    rng.uniform(0, PI), INK, 1.4) for _ in range(26)])
        bad = crack_mark([-2.2, 1.45], 0.34, PI / 2, RED_INK, 3).shift(DOWN * 0.04)
        bad_l = note("one bad crack is enough", 15, RED_INK).next_to(thick, UP, buff=0.15).shift(RIGHT * 0.8)
        thin = RoundedRectangle(corner_radius=0.04, width=4.6, height=0.08, stroke_width=0.6, stroke_color=GLASS,
                                fill_color=GLASS, fill_opacity=0.9).move_to([-3.0, -0.9, 0])
        thin_flaw = crack_mark([-3.6, -0.9], 0.05, PI / 2, INK, 1.2)
        thin_l = note("a thin fibre has room only for tiny ones", 15).next_to(thin, DOWN, buff=0.22)
        thick_l = note("ordinary glass (magnified sketch)", 15).next_to(thick, DOWN, buff=0.15)
        line("Why should size matter? Griffith's answer: real glass is full of tiny cracks. A thin fibre has less room "
             "for a bad one.", FadeOut(fibres), FadeOut(fib_l), FadeIn(thick), FadeIn(thick_l), run_time=0.9)
        self.play(LaggedStart(*[Create(f) for f in flaws], lag_ratio=0.05), run_time=1.6)
        self.play(Create(bad), FadeIn(bad_l), run_time=0.6)
        self.play(FadeIn(thin), FadeIn(thin_flaw), FadeIn(thin_l), run_time=0.8)
        self.vo_wait()
        self.play(FadeOut(VGroup(thick, flaws, bad, bad_l, thin, thin_flaw, thin_l, thick_l, ax, xl, yl, theory,
                                 theory_l, curve, schem)), run_time=0.7)

        # ================= Inglis: lines of force crowding round a hole =================
        PC = np.array([-2.9, 0.35, 0])
        plate = Rectangle(width=5.2, height=4.7, stroke_color=INK, stroke_width=2.2, fill_color=PAPER_DARK,
                          fill_opacity=0.55).move_to(PC)
        pull_up = VGroup(*[Arrow(PC + [x, 2.4, 0], PC + [x, 3.0, 0], buff=0, color=RED_INK, stroke_width=4,
                                 max_tip_length_to_length_ratio=0.35) for x in (-1.8, 0, 1.8)])
        pull_dn = VGroup(*[Arrow(PC + [x, -2.4, 0], PC + [x, -3.0, 0], buff=0, color=RED_INK, stroke_width=4,
                                 max_tip_length_to_length_ratio=0.35) for x in (-1.8, 0, 1.8)])
        A_SEMI = 0.9
        bsemi = ValueTracker(0.9)
        CS = [s * v for s in (-1, 1) for v in (0.07, 0.2, 0.38, 0.6, 0.88, 1.2, 1.6, 2.05)]

        def build_lines():
            b = bsemi.get_value()
            g = VGroup()
            for pts in force_lines(A_SEMI, b, CS, y_span=2.3, x_clip=2.55):
                m = VMobject(stroke_color=SEPIA, stroke_width=1.8, stroke_opacity=0.9)
                m.set_points_smoothly(pts + PC)
                g.add(m)
            return g

        def build_hole():
            b = bsemi.get_value()
            return Ellipse(width=2 * A_SEMI, height=2 * b, stroke_color=INK, stroke_width=2.2, fill_color=PAPER,
                           fill_opacity=1).move_to(PC)

        lines = always_redraw(build_lines)
        hole = always_redraw(build_hole)
        inglis = VGroup(serif("Charles Inglis", 24, INK), note("a few years earlier", 16)).arrange(DOWN, buff=0.08).move_to(
            [3.4, 2.6, 0])
        line("A few years earlier, the engineer Charles Inglis had worked out what a hole does to the stress in a plate.",
             FadeIn(plate), FadeIn(inglis), run_time=1.0)
        self.play(FadeIn(pull_up), FadeIn(pull_dn), run_time=0.6)
        self.vo_wait()
        illus = note("lines of force: an illustration", 14).next_to(plate, LEFT, buff=0.1).rotate(PI / 2).shift(RIGHT * 0.05)
        illus.move_to(PC + [-2.85, 0, 0])
        line("Picture the force passing through a stretched plate as lines. A hole makes them crowd around its edges.",
             Create(lines), FadeIn(illus), run_time=1.6)
        self.play(FadeIn(hole), run_time=0.8)
        tips = VGroup(*[Circle(radius=0.28, color=RED_INK, stroke_width=3).move_to(PC + [s * A_SEMI, 0, 0])
                        for s in (-1, 1)])
        self.play(Create(tips), run_time=0.7)
        self.vo_wait()
        # formula
        form = MathTex(r"\sigma_{\text{tip}} = \sigma\left(1 + \frac{2a}{b}\right)", font_size=48, color=INK).move_to(
            [3.4, 1.3, 0])
        a_brace = always_redraw(lambda: VGroup(
            Line(PC + [0, -0.02, 0], PC + [A_SEMI, -0.02, 0], color=RED_INK, stroke_width=2.5),
            MathTex("a", font_size=30, color=RED_INK).move_to(PC + [A_SEMI / 2, -0.26, 0])))
        b_brace = always_redraw(lambda: VGroup(
            Line(PC, PC + [0, bsemi.get_value(), 0], color=BLUE_INK, stroke_width=2.5),
            MathTex("b", font_size=30, color=BLUE_INK).move_to(PC + [-0.22, max(bsemi.get_value() / 2, 0.15), 0])))
        factor = always_redraw(lambda: VGroup(
            serif("stress at the tip:", 20, INK),
            serif(f"× {1 + 2 * A_SEMI / bsemi.get_value():.0f}", 40, RED_INK)).arrange(RIGHT, buff=0.2).move_to(
            [3.4, -0.1, 0]))
        line("For an elliptical hole, the stress at its tip is multiplied by one, plus twice its length over its width.",
             Write(form), FadeOut(tips), run_time=1.2)
        self.play(FadeIn(a_brace), FadeIn(b_brace), FadeIn(factor), run_time=0.8)
        self.vo_wait()
        circ_note = note("a round hole: × 3", 16).move_to([3.4, -0.85, 0])
        self.play(FadeIn(circ_note), run_time=0.5)
        line("Now make the hole a crack, long and razor thin, and that factor becomes enormous. At the tip, the stress can "
             "reach the theoretical strength, even under a modest load.", run_time=0.6)
        self.play(bsemi.animate.set_value(0.009), FadeOut(circ_note), run_time=3.2, rate_func=smooth)
        crack_note = note("a sharp crack: the factor climbs into the hundreds", 16, RED_INK).move_to([3.4, -0.85, 0])
        self.play(FadeIn(crack_note), run_time=0.6)
        self.vo_wait()
        q2 = ink_card(VGroup(serif("Then why doesn't every crack run?", 24, INK),
                             note("cracks sit in glass for years", 16)).arrange(DOWN, buff=0.1)).move_to([3.4, -1.95, 0])
        line("But that raises a new puzzle. By this rule, every sharp crack should run at almost any load. They don't. "
             "So what decides?", FadeIn(q2, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()
        for m in (lines, hole, a_brace, b_brace, factor):
            m.clear_updaters()
        self.play(FadeOut(VGroup(lines, hole, a_brace, b_brace, factor, form, crack_note, q2, inglis, illus, plate,
                                 pull_up, pull_dn)), run_time=0.8)

        # ================= energy =================
        big = VGroup(serif("force", 40, FADED), serif("→", 40, INK), serif("energy", 40, RED_INK)).arrange(RIGHT, buff=0.4)
        big.move_to([0, 0.6, 0])
        strike = Line(big[0].get_left() + LEFT * 0.1, big[0].get_right() + RIGHT * 0.1, color=RED_INK, stroke_width=3)
        line("Griffith's leap was to stop thinking about force, and start thinking about energy.", FadeIn(big[0]),
             run_time=0.8)
        self.play(Create(strike), FadeIn(big[1]), FadeIn(big[2], shift=LEFT * 0.2), run_time=1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(big, strike)), run_time=0.5)

        PC2 = np.array([-3.7, 0.4, 0])
        plate2 = Rectangle(width=4.4, height=4.4, stroke_color=INK, stroke_width=2.2, fill_color=PAPER_DARK,
                           fill_opacity=0.55).move_to(PC2)
        pulls = VGroup(*[Arrow(PC2 + [x, s * 2.25, 0], PC2 + [x, s * 2.8, 0], buff=0, color=RED_INK, stroke_width=4,
                               max_tip_length_to_length_ratio=0.35) for x in (-1.4, 0, 1.4) for s in (-1, 1)])
        clen = ValueTracker(0.0)   # half-length a of the crack, in graph units (0..2.4)
        SC = 0.62                  # screen units per graph unit for the drawn crack

        def build_relax():
            a = clen.get_value() * SC
            if a < 0.02:
                return VGroup()
            g = VGroup()
            for k, op in ((1.0, 0.18), (0.75, 0.25), (0.5, 0.32)):
                g.add(Ellipse(width=2 * a * (1 + 0.15 * k), height=2.6 * a * k, stroke_width=0, fill_color=PAPER,
                              fill_opacity=op).move_to(PC2))
            return g

        def build_crack():
            a = max(clen.get_value() * SC, 0.01)
            return Line(PC2 + LEFT * a, PC2 + RIGHT * a, color=INK, stroke_width=3.5)

        relax = always_redraw(build_relax)
        crk = always_redraw(build_crack)
        relax_l = note("material near the crack relaxes (sketch)", 15).move_to(PC2 + DOWN * 1.55)
        stores = note("stretched: stores energy", 16).next_to(plate2, UP, buff=0.62)

        gx = Axes(x_range=[0, 2.6, 1], y_range=[-3, 2.2, 1], x_length=5.6, y_length=4.6, tips=False,
                  axis_config={"color": INK, "stroke_width": 2, "include_ticks": False}).move_to([3.0, 0.45, 0])
        gxl = note("crack length →", 15).next_to(gx.x_axis.get_right(), DOWN, buff=0.12).shift(LEFT * 0.6)
        gyl = note("energy", 15).next_to(gx.y_axis.get_top(), RIGHT, buff=0.12)
        COST, REL = 1.6, 0.6

        rel_curve = gx.plot(lambda a: -REL * a * a, x_range=[0, 2.23], color=BLUE_INK, stroke_width=3.5)
        rel_l = note("energy released ∝ length²", 15, BLUE_INK).move_to(gx.c2p(1.15, -2.35))
        cost_curve = gx.plot(lambda a: COST * a, x_range=[0, 1.37], color=SEPIA, stroke_width=3.5)
        cost_l = note("cost of new surface ∝ length", 15, SEPIA).next_to(gx.c2p(1.37, 2.19), RIGHT, buff=0.1)
        tot = gx.plot(lambda a: COST * a - REL * a * a, x_range=[0, 2.6], color=RED_INK, stroke_width=4.5)
        tot_l = note("total", 16, RED_INK).move_to(gx.c2p(2.25, 1.2))
        a_star = COST / (2 * REL)

        line("A stretched plate stores energy, like a spring. A crack lets the material around it relax, and releases "
             "some of that energy.", FadeIn(plate2), FadeIn(pulls), FadeIn(stores), run_time=0.9)
        self.add(relax, crk)
        self.play(clen.animate.set_value(1.0), FadeIn(relax_l), run_time=2.0)
        self.vo_wait()
        line("The energy released grows with the square of the crack's length.", Create(gx), FadeIn(gxl), FadeIn(gyl),
             run_time=0.9)
        self.play(Create(rel_curve), FadeIn(rel_l), run_time=1.6)
        self.vo_wait()
        surf = VGroup(*[Line(PC2 + [-0.6, s * 0.05, 0], PC2 + [0.6, s * 0.05, 0], color=SEPIA, stroke_width=2)
                        for s in (-1, 1)])
        surf_l = note("two new surfaces", 15, SEPIA).move_to(PC2 + [0, 0.42, 0])
        line("But a crack has a cost. It makes two new surfaces, and breaking bonds takes energy. That cost grows only in "
             "step with the length.", FadeIn(surf), FadeIn(surf_l), run_time=0.8)
        self.play(Create(cost_curve), FadeIn(cost_l), run_time=1.4)
        self.play(FadeOut(surf), FadeOut(surf_l), run_time=0.5)
        self.vo_wait()
        dot = Dot(gx.c2p(0, 0), radius=0.09, color=INK)
        crit = DashedLine(gx.c2p(a_star, -3), gx.c2p(a_star, 2.1), color=FADED, stroke_width=2)
        crit_l = note("critical length", 15).next_to(crit, DOWN, buff=0.08)
        stays = note("short: the crack stays put", 15, INK).move_to(gx.c2p(0.62, -1.25))
        runs = note("long: it runs on its own", 15, RED_INK).move_to(gx.c2p(2.05, -0.7))
        self.play(clen.animate.set_value(0.0), run_time=0.4)
        line("Add them up. For a short crack the cost wins, and the crack stays put. Past a critical length, the release "
             "wins, and the crack runs on its own.", Create(tot), FadeIn(tot_l),
             rel_curve.animate.set_stroke(opacity=0.35), cost_curve.animate.set_stroke(opacity=0.35), run_time=1.4)
        self.add(dot)
        dot.add_updater(lambda m: m.move_to(gx.c2p(clen.get_value(), COST * clen.get_value() - REL * clen.get_value() ** 2)))
        self.play(clen.animate.set_value(0.9), FadeIn(stays), run_time=1.8)
        self.play(clen.animate.set_value(0.35), run_time=0.9)
        self.play(clen.animate.set_value(a_star), Create(crit), FadeIn(crit_l), run_time=1.6)
        dot.set_color(RED_INK)
        self.play(clen.animate.set_value(2.6), FadeIn(runs), run_time=1.2, rate_func=rush_into)
        self.vo_wait()
        dot.clear_updaters()
        relax.clear_updaters()
        crk.clear_updaters()
        self.play(FadeOut(VGroup(relax, crk, plate2, pulls, stores, relax_l, rel_curve, rel_l, cost_curve, cost_l, dot,
                                 crit, crit_l, stays, runs)), tot.animate.set_stroke(opacity=0.25),
                  tot_l.animate.set_opacity(0.25), run_time=0.8)
        self.play(FadeOut(VGroup(gx, gxl, gyl, tot, tot_l)), run_time=0.5)

        # ================= Griffith's rule =================
        rule = MathTex(r"\sigma_{\text{break}} = \sqrt{\frac{2E\gamma}{\pi a}}", font_size=64, color=INK).move_to(
            [-3.2, 1.0, 0])
        legend = VGroup(note("E : stiffness of the material", 16, INK),
                        note("γ : surface energy, the cost of new surface", 16, INK),
                        note("a : half the length of the crack", 16, INK),
                        note("modern form, for a crack in a wide plate", 14)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend.next_to(rule, DOWN, buff=0.45)
        rax = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1], x_length=4.6, y_length=3.6, tips=False,
                   axis_config={"color": INK, "stroke_width": 2, "include_ticks": False}).move_to([3.4, 0.4, 0])
        rxl = note("crack length →", 15).next_to(rax.x_axis, DOWN, buff=0.15)
        ryl = note("breaking stress", 15).rotate(PI / 2).next_to(rax.y_axis, LEFT, buff=0.15)
        rcurve = rax.plot(lambda x: 1.2 / np.sqrt(x), x_range=[0.1, 4], color=RED_INK, stroke_width=4)
        rlab = MathTex(r"\propto 1/\sqrt{a}", font_size=34, color=RED_INK).move_to(rax.c2p(2.6, 1.4))
        line("Out of this balance comes Griffith's rule: the breaking stress falls with the square root of the crack's "
             "length.", Write(rule), run_time=1.4)
        self.play(FadeIn(legend), Create(rax), FadeIn(rxl), FadeIn(ryl), run_time=0.9)
        self.play(Create(rcurve), FadeIn(rlab), run_time=1.4)
        self.vo_wait()

        # bulbs and tubes
        bulb = VGroup(Circle(radius=0.75, stroke_color=GLASS, stroke_width=3, fill_color=GLASS_FILL, fill_opacity=0.8),
                      Rectangle(width=0.26, height=0.7, stroke_color=GLASS, stroke_width=3, fill_color=GLASS_FILL,
                                fill_opacity=0.8).shift(UP * 1.05))
        bulb[1].set_z_index(-1)
        bulb_crack = crack_mark([0.1, -0.05], 0.55, 0.5, RED_INK, 3)
        tube = VGroup(RoundedRectangle(corner_radius=0.2, width=2.0, height=0.42, stroke_color=GLASS, stroke_width=3,
                                       fill_color=GLASS_FILL, fill_opacity=0.8))
        tube_crack = crack_mark([0.0, 0.0], 0.45, 0.0, RED_INK, 3)
        vessels = VGroup(VGroup(bulb, bulb_crack), VGroup(tube, tube_crack)).arrange(RIGHT, buff=0.7).move_to([-3.4, 0.6, 0])
        ves_l = note("cracks of known length, then pressure until they burst", 15).next_to(vessels, DOWN, buff=0.3)
        pts_a = [0.35, 0.6, 1.0, 1.6, 2.5, 3.5]
        jit = [0.05, -0.06, 0.04, -0.03, 0.05, -0.04]
        pdots = VGroup(*[Dot(rax.c2p(a, 1.2 / np.sqrt(a) * (1 + j)), radius=0.07, color=INK) for a, j in zip(pts_a, jit)])
        const = MathTex(r"\sigma\sqrt{a} \approx \text{constant}", font_size=40, color=INK).move_to([-3.4, -1.3, 0])
        ill = note("points: an illustration, not Griffith's measurements", 14).next_to(rax, DOWN, buff=0.5)
        line("He tested it. He made cracks of known length in glass bulbs and tubes, and broke them. Stress times the "
             "square root of crack length came out nearly constant.", FadeOut(rule), FadeOut(legend),
             FadeIn(vessels), FadeIn(ves_l), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in pdots], lag_ratio=0.25), FadeIn(ill), run_time=2.0)
        self.play(Write(const), run_time=1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(vessels, ves_l, pdots, const, ill, rax, rxl, ryl, rcurve, rlab)), run_time=0.7)

        # ================= legacy: timeline =================
        tl = Line([-5.6, 1.2, 0], [5.6, 1.2, 0], color=INK, stroke_width=2.5)

        def mark(x, top, bottom, color=INK):
            tick = Line([x, 1.05, 0], [x, 1.35, 0], color=color, stroke_width=3)
            t = serif(top, 26, color).next_to(tick, UP, buff=0.15)
            b = VGroup(*[note(s, 16, color if color != INK else FADED) for s in bottom]).arrange(DOWN, buff=0.06)
            b.next_to(tick, DOWN, buff=0.2)
            return VGroup(tick, t, b)

        m1 = mark(-4.0, "1921", ["Griffith's paper", "Phil. Trans. Royal Society A"])
        m2 = mark(0.0, "at first", ["seen as a rule for", "brittle solids like glass"])
        m3 = mark(4.0, "1950s", ["extended to metals", "fracture mechanics"], RED_INK)
        line("The paper appeared in 1921. At first it was seen as a rule for brittle things like glass. Decades later, "
             "others extended it to metals, and fracture mechanics was born.", Create(tl), FadeIn(m1), run_time=1.0)
        self.wait(1.6)
        self.play(FadeIn(m2), run_time=0.7)
        self.wait(1.6)
        self.play(FadeIn(m3), run_time=0.7)
        self.vo_wait()
        self.play(FadeOut(VGroup(tl, m1, m2, m3)), run_time=0.6)

        # aircraft crack growth
        wing = Polygon([-6.0, 1.6, 0], [-1.2, 2.2, 0], [-1.2, 1.3, 0], [-6.0, 0.6, 0], stroke_color=INK, stroke_width=2.2,
                       fill_color=PAPER_DARK, fill_opacity=0.7)
        rivets = VGroup(*[Dot([-5.6 + 0.5 * i, 1.05 + 0.07 * i, 0], radius=0.04, color=INK) for i in range(9)])
        wcrack = crack_mark([-3.35, 1.26], 0.3, 0.3, RED_INK, 3)
        wing_l = note("a small crack, assumed to be there", 15, RED_INK).next_to(wing, DOWN, buff=0.2)
        cax = Axes(x_range=[0, 10, 1], y_range=[0, 4, 1], x_length=5.4, y_length=3.6, tips=False,
                   axis_config={"color": INK, "stroke_width": 2, "include_ticks": False}).move_to([3.1, 0.4, 0])
        cxl = note("flights →", 15).next_to(cax.x_axis, DOWN, buff=0.15)
        cyl = note("crack length", 15).rotate(PI / 2).next_to(cax.y_axis, LEFT, buff=0.15)
        crit_c = DashedLine(cax.c2p(0, 3.3), cax.c2p(10, 3.3), color=RED_INK, stroke_width=2)
        crit_cl = note("critical length", 14, RED_INK).next_to(crit_c, UP, buff=0.05).align_to(crit_c, LEFT).shift(
            RIGHT * 0.2)
        grow = cax.plot(lambda x: 0.3 * np.exp(0.25 * x), x_range=[0, 9.6], color=INK, stroke_width=3.5)
        insp = VGroup(*[VGroup(DashedLine(cax.c2p(x, 0), cax.c2p(x, 0.3 * np.exp(0.25 * x)), color=BLUE_INK,
                                          stroke_width=2),
                               note("inspect", 13, BLUE_INK).move_to(cax.c2p(x, 0.3 * np.exp(0.25 * x) + 0.4)))
                         for x in (2.5, 5.0, 7.5)])
        sch2 = note("schematic", 14).next_to(cax, DOWN, buff=0.5)
        line("Today, aircraft are designed on the assumption that small cracks are already there. Engineers work out "
             "how long a crack can safely grow, and inspect before it gets there.", FadeIn(wing), FadeIn(rivets),
             Create(wcrack), FadeIn(wing_l), run_time=1.0)
        self.play(Create(cax), FadeIn(cxl), FadeIn(cyl), Create(crit_c), FadeIn(crit_cl), FadeIn(sch2), run_time=1.0)
        self.play(Create(grow), run_time=2.4)
        self.play(LaggedStart(*[FadeIn(i) for i in insp], lag_ratio=0.3), run_time=1.2)
        self.vo_wait()
        self.play(FadeOut(VGroup(wing, rivets, wcrack, wing_l, cax, cxl, cyl, crit_c, crit_cl, grow, insp, sch2)),
                  run_time=0.6)

        # Griffith later
        cam2 = cameo("collar", 0.8).move_to([-4.2, 0.6, 0])
        later = VGroup(serif("Later: jet engines", 26, INK),
                       note("Rolls-Royce, from 1939", 17)).arrange(DOWN, buff=0.1).move_to([-4.2, -1.55, 0])
        lesson = VGroup(serif("strength =", 34, INK),
                        serif("what it is made of", 30, FADED, italic=True),
                        serif("+ its flaws", 38, RED_INK)).arrange(DOWN, buff=0.25).move_to([2.2, 0.5, 0])
        line("Griffith himself went on to design jet engines at Rolls-Royce. But his glass taught a deeper lesson: "
             "strength depends not only on what a material is made of, but on its flaws.", FadeIn(cam2), FadeIn(later),
             run_time=1.0)
        self.wait(2.2)
        self.play(FadeIn(lesson[0]), FadeIn(lesson[1]), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(lesson[2], scale=1.2), run_time=0.7)
        self.vo_wait()
        self.play(FadeOut(VGroup(cam2, later, lesson)), run_time=0.6)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 22, RED_INK).move_to([0, 3.2, 0])
        s1 = Rectangle(width=4.2, height=0.9, stroke_color=INK, stroke_width=2, fill_color=WHITE,
                       fill_opacity=0.85).move_to([-3.2, 1.9, 0])
        hands1 = VGroup(Arrow([-5.3, 1.9, 0], [-6.2, 1.9, 0], buff=0, color=RED_INK, stroke_width=4,
                              max_tip_length_to_length_ratio=0.3),
                        Arrow([-1.1, 1.9, 0], [-0.2, 1.9, 0], buff=0, color=RED_INK, stroke_width=4,
                              max_tip_length_to_length_ratio=0.3))
        s1_l = note("plain strip: hard to pull apart", 16).next_to(s1, DOWN, buff=0.15)
        line("Try it yourself. Take a strip of paper and pull it from both ends. It is surprisingly hard to break.",
             FadeIn(tiy), FadeIn(s1), run_time=0.8)
        self.play(FadeIn(hands1), FadeIn(s1_l), run_time=0.6)
        self.vo_wait()

        y2 = -0.25
        s2a = Polygon([-5.3, y2 + 0.45, 0], [-3.27, y2 + 0.45, 0], [-3.2, y2 + 0.2, 0], [-3.13, y2 + 0.45, 0],
                      [-1.1, y2 + 0.45, 0], [-1.1, y2 - 0.45, 0], [-5.3, y2 - 0.45, 0], stroke_color=INK, stroke_width=2,
                      fill_color=WHITE, fill_opacity=0.85)
        hands2 = hands1.copy().shift(DOWN * (1.9 - y2))
        notch_l = note("snip a notch", 16, RED_INK).next_to(s2a, UP, buff=0.12)
        line("Now snip a small notch in one edge, and pull again. It tears easily, and the tear starts at the notch.",
             FadeIn(s2a), FadeIn(notch_l), FadeIn(hands2), run_time=0.8)
        left2 = Polygon([-5.3, y2 + 0.45, 0], [-3.27, y2 + 0.45, 0], [-3.2, y2 + 0.2, 0], [-3.24, y2 - 0.1, 0],
                        [-3.18, y2 - 0.45, 0], [-5.3, y2 - 0.45, 0], stroke_color=INK, stroke_width=2, fill_color=WHITE,
                        fill_opacity=0.85)
        right2 = Polygon([-3.13, y2 + 0.45, 0], [-1.1, y2 + 0.45, 0], [-1.1, y2 - 0.45, 0], [-3.18, y2 - 0.45, 0],
                         [-3.24, y2 - 0.1, 0], [-3.2, y2 + 0.2, 0], stroke_color=INK, stroke_width=2, fill_color=WHITE,
                         fill_opacity=0.85)
        self.wait(1.2)
        self.remove(s2a)
        self.add(left2, right2)
        tear_l = note("tears from the notch", 16, RED_INK).next_to(left2, DOWN, buff=0.15).shift(RIGHT * 1.0)
        self.play(left2.animate.shift(LEFT * 0.3), right2.animate.shift(RIGHT * 0.3),
                  hands2.animate.set_opacity(0.5), FadeIn(tear_l), run_time=0.7)
        self.vo_wait()

        # plastic lid, crack, stop hole
        LC = np.array([3.3, 0.8, 0])
        lid = Circle(radius=1.85, stroke_color=BLUE_INK, stroke_width=3, fill_color="#d5dde3", fill_opacity=0.9).move_to(LC)
        rim = Circle(radius=1.65, stroke_color=BLUE_INK, stroke_width=1.2).move_to(LC)
        lcrack = poly([LC + [-1.85, 0.1, 0], LC + [-1.4, 0.18, 0], LC + [-1.0, 0.05, 0], LC + [-0.55, 0.12, 0]],
                      RED_INK, 3)
        tip = LC + [-0.55, 0.12, 0]
        drill = VGroup(Rectangle(width=0.16, height=1.1, stroke_width=0, fill_color=FADED, fill_opacity=1),
                       Triangle(stroke_width=0, fill_color=FADED, fill_opacity=1).scale(0.09).rotate(PI).shift(DOWN * 0.6))
        drill.move_to(tip + UP * 1.35)
        hole2 = Circle(radius=0.09, stroke_color=INK, stroke_width=2.5, fill_color=PAPER, fill_opacity=1).move_to(tip)
        lid_l = note("old plastic lid with a crack", 16).next_to(lid, DOWN, buff=0.15)
        line("Next, find a crack in an old plastic lid. With an adult's help, drill a small hole right at the crack's "
             "tip.", FadeIn(lid), FadeIn(rim), Create(lcrack), FadeIn(lid_l), run_time=1.0)
        self.play(FadeIn(drill, shift=DOWN * 0.2), run_time=0.6)
        self.play(drill.animate.shift(DOWN * 0.55), run_time=0.8)
        self.play(FadeIn(hole2), drill.animate.shift(UP * 0.8).set_opacity(0), run_time=0.7)
        self.vo_wait()
        stop_l = VGroup(serif("stop hole", 22, RED_INK), note("a round tip spreads the stress", 13)).arrange(
            DOWN, buff=0.06).move_to(LC + [0.15, -0.55, 0])
        ring = Circle(radius=0.22, color=RED_INK, stroke_width=2.5).move_to(tip)
        safe = ink_card(note("safety glasses on · clamp the plastic · an adult runs the drill", 16, INK)).move_to(
            [0, -2.35, 0])
        line("The round hole blunts the sharp tip, so the stress no longer piles up there, and the crack stops growing. "
             "Engineers call it a stop hole.", Create(ring), run_time=0.8)
        self.play(FadeIn(stop_l), run_time=0.6)
        self.play(FadeIn(safe), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tiy, s1, hands1, s1_l, left2, right2, hands2, notch_l, tear_l, lid, rim,
                                          lcrack, hole2, drill, lid_l, stop_l, ring, safe)), run_time=0.8)

        # ================= close =================
        last = VGroup(serif("A crack is a lever on a material's atoms.", 36, INK),
                      serif("Count the energy. Respect the flaw.", 36, RED_INK)).arrange(DOWN, buff=0.25).move_to([0, 0.6, 0])
        line("A crack is a lever on a material's atoms. Griffith taught engineers to count the energy, and respect the "
             "flaw.", FadeIn(last, lag_ratio=0.2), run_time=1.2)
        self.vo_wait()
        self.play(clear(), FadeOut(last), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after J. E. Gordon, Structures: Or Why Things Don't Fall Down (1978) · sources in the "
                          "episode notes", 17),
                     note("facts checked against the Royal Society, Britannica, Grace's Guide and Wikipedia, "
                          "among others", 17),
                     note("silhouette is stylised, not a likeness · graphs and force lines are schematic · "
                          "animated with Manim · synthetic narration", 15)).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(1.6)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)
