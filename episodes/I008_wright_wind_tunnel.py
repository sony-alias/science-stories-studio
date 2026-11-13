"""I008 The Wind Tunnel in a Bicycle Shop, a Science Stories episode.

After D. McCullough, The Wright Brothers (Simon & Schuster, 2015). Script and sources: episodes/I008_script.md

Render:  manim -qh --frame_rate 30 episodes/I008_wright_wind_tunnel.py WrightWindTunnel
Then:    scripts/finish_video.sh media/videos/I008_wright_wind_tunnel/1080p30/WrightWindTunnel.mp4 out/I008_wright_wind_tunnel.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

SAND = "#d9c49a"


# ---------------- drawings ----------------
def glider_side(span=2.4, gap=0.55, color=INK):
    """Schematic side view of a Wright glider: two cambered wings, struts, forward elevator."""
    def wing(y, w):
        return ArcBetweenPoints([-w / 2, y, 0], [w / 2, y, 0], angle=-0.35, color=color, stroke_width=4)
    top, bot = wing(gap / 2, span * 0.42), wing(-gap / 2, span * 0.42)
    struts = VGroup(*[Line([x, -gap / 2 + 0.03, 0], [x, gap / 2 + 0.03, 0], color=color, stroke_width=1.5)
                      for x in (-0.35, 0.0, 0.35)])
    elev = ArcBetweenPoints([-span * 0.62, 0.02, 0], [-span * 0.44, 0.02, 0], angle=-0.4, color=color,
                            stroke_width=3)
    booms = VGroup(Line([-span * 0.53, 0.02, 0], [-span * 0.21, gap / 2, 0], color=color, stroke_width=1),
                   Line([-span * 0.53, 0.02, 0], [-span * 0.21, -gap / 2, 0], color=color, stroke_width=1))
    return VGroup(top, bot, struts, elev, booms)


def dunes():
    pts = [[-6.75, -2.25, 0], [-4.5, -1.55, 0], [-2.0, -2.2, 0], [1.0, -1.7, 0], [4.0, -2.35, 0], [6.75, -1.92, 0]]
    curve = VMobject(stroke_color=SEPIA, stroke_width=2).set_points_smoothly([np.array(p) for p in pts])
    fill = Polygon(*[curve.point_from_proportion(t) for t in np.linspace(0, 1, 80)],
                   [6.75, -3.65, 0], [-6.75, -3.65, 0], stroke_width=0, fill_color=SAND, fill_opacity=0.55)
    return VGroup(fill, curve)


def wind_arrows(x0=-6.2, ys=(1.6, 0.6, -0.4), length=1.2, color=BLUE_INK):
    return VGroup(*[Arrow([x0, y, 0], [x0 + length, y, 0], buff=0, color=color, stroke_width=3,
                          tip_length=0.16, max_tip_length_to_length_ratio=0.2) for y in ys])


def person(kind, name, place):
    c = cameo("modern", 0.6)
    if kind == "wilbur":            # Wilbur was clean-shaven; Orville kept a moustache
        c[2][1][0].set_fill(opacity=0)
    lab = serif(name, 22, INK).next_to(c, DOWN, buff=0.15)
    sub = serif(place, 16, FADED, italic=True).next_to(lab, DOWN, buff=0.06)
    return VGroup(c, lab, sub)


def airfoil(chord=1.0, camber=0.08, thick=0.05, color=INK, fill=PAPER_DARK):
    xs = np.linspace(0, 1, 40)
    yc = 4 * camber * xs * (1 - xs)
    yt = thick * 2.4 * np.sqrt(np.clip(xs, 0, 1)) * (1 - xs)
    upper = [np.array([chord * (x - 0.5), chord * (c + t), 0]) for x, c, t in zip(xs, yc, yt)]
    lower = [np.array([chord * (x - 0.5), chord * (c - t * 0.3), 0]) for x, c, t in zip(xs[::-1], yc[::-1], yt[::-1])]
    m = VMobject(stroke_color=color, stroke_width=1.6, fill_color=fill, fill_opacity=1)
    m.set_points_as_corners(upper + lower + [upper[0]])
    return m


def planform(ar, area=1.6, color=INK, fill=PAPER_DARK):
    span = np.sqrt(ar * area)
    chord = area / span
    r = Rectangle(width=span, height=chord, stroke_color=color, stroke_width=2, fill_color=fill, fill_opacity=1)
    return r


def cl_curve(alpha_deg, ar, a0_deg=3.0):
    """Lift coefficient from thin-airfoil theory with the lifting-line aspect-ratio correction (schematic)."""
    a = np.radians(alpha_deg + a0_deg)
    return 2 * PI * a / (1 + 2 / ar)


class WrightWindTunnel(NarratedScene):
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
        title = serif("The Wind Tunnel in a Bicycle Shop", 54).next_to(orn1, DOWN, buff=0.35)
        sub = serif("Wilbur and Orville Wright · Dayton, Ohio · 1901", 26, FADED, italic=True)
        sub.next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = serif("after David McCullough, The Wright Brothers (Simon & Schuster, 2015)", 16, FADED,
                       italic=True).move_to([0, -3.2, 0])
        self.vo("Science Stories. The wind tunnel in a bicycle shop.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.wait(0.6)
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= the dunes, 1901 =================
        land = dunes()
        place = serif("Kill Devil Hills, North Carolina · summer 1901", 22, SEPIA, italic=True).move_to([0, 3.15, 0])
        glider = glider_side().scale(1.5).move_to([-1.0, 0.9, 0])
        wind = wind_arrows(x0=-6.4, ys=(2.2, 1.2, 0.2), length=1.0)
        self.play(FadeIn(land, shift=UP * 0.2), FadeIn(place), run_time=1.0)
        line("Summer, 1901. On the windy dunes of Kill Devil Hills, in North Carolina,",
             FadeIn(glider), LaggedStart(*[GrowArrow(a) for a in wind], lag_ratio=0.2), run_time=1.2)
        self.play(glider.animate.shift(LEFT * 1.2 + UP * 0.25).rotate(3 * DEGREES), run_time=3.5,
                  rate_func=there_and_back_with_pause)
        self.play(clear(), run_time=0.3)
        w = person("wilbur", "Wilbur Wright", "1867 – 1912").move_to([2.6, 0.7, 0])
        o = person("orville", "Orville Wright", "1871 – 1948").move_to([5.0, 0.7, 0])
        line("two bicycle makers from Dayton, Ohio, are flying their new glider. Wilbur and Orville Wright.",
             FadeIn(w, shift=UP * 0.1), FadeIn(o, shift=UP * 0.1),
             glider.animate.shift(LEFT * 0.4 + UP * 0.2), run_time=1.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(w, o, wind)), glider.animate.move_to([-4.2, 1.0, 0]), run_time=0.8)

        # predicted vs measured lift
        base = -1.2
        bar_p = Rectangle(width=1.1, height=3.0, fill_color=SEPIA, fill_opacity=0.35, stroke_color=INK,
                          stroke_width=2).move_to([0.6, base + 1.5, 0])
        bar_m = Rectangle(width=1.1, height=1.0, fill_color=RED_INK, fill_opacity=0.55, stroke_color=INK,
                          stroke_width=2).move_to([2.6, base + 0.5, 0])
        axis = Line([-0.4, base, 0], [3.6, base, 0], color=INK, stroke_width=2)
        lab_p = serif("lift the tables promised", 18, INK).next_to(bar_p, UP, buff=0.12)
        lab_m = serif("lift measured", 18, RED_INK).next_to(bar_m, UP, buff=0.12)
        third = serif("about one third", 24, RED_INK, italic=True).next_to(bar_m, RIGHT, buff=0.25)
        line("They had designed it with the best numbers anyone had published.",
             Create(axis), GrowFromEdge(bar_p, DOWN), FadeIn(lab_p), run_time=1.2)
        self.play(clear(), run_time=0.3)
        line("But it lifts only about a third of what those numbers promised.",
             GrowFromEdge(bar_m, DOWN), FadeIn(lab_m), run_time=1.2)
        self.play(FadeIn(third, shift=DOWN * 0.1), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(bar_p, bar_m, axis, lab_p, lab_m, third, glider, land, place)),
                  run_time=0.8)

        # recollection
        rec = VGroup(
            serif("Men would not fly in a thousand years.", 36, INK, italic=True),
            serif("Wilbur in 1901, as Orville remembered it years later", 20, FADED, italic=True),
            serif("(other tellings: not within our lifetime; fifty years)", 16, FADED, italic=True),
        ).arrange(DOWN, buff=0.25)
        rec_card = ink_card(rec, pad=0.45).move_to([0, 0.4, 0])
        line("Years later, Orville remembered Wilbur saying that men would not fly in a thousand years.",
             FadeIn(rec_card, shift=UP * 0.1), run_time=1.0)
        self.vo_wait()
        self.wait(0.6)
        self.play(clear(), FadeOut(rec_card), run_time=0.8)

        # ================= the lift equation =================
        eq = MathTex("L", "=", "k", r"\;\;S\;\;", "V^2", r"\;\;C_L", font_size=84, color=INK).move_to([0, 1.5, 0])
        labels = VGroup(
            serif("lift", 20, FADED, italic=True).next_to(eq[0], DOWN, buff=0.35),
            serif("constant", 20, FADED, italic=True).next_to(eq[2], DOWN, buff=0.35),
            serif("area", 20, FADED, italic=True).next_to(eq[3], DOWN, buff=0.75),
            serif("speed²", 20, FADED, italic=True).next_to(eq[4], DOWN, buff=0.35),
            serif("lift coefficient", 20, FADED, italic=True).next_to(eq[5], DOWN, buff=0.75),
        )
        line("So where was the mistake? Every designer of the time worked from one equation for lift.",
             Write(eq), run_time=1.6)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("Lift equals a constant, times the wing's area, times the speed squared,",
             LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in labels[:4]], lag_ratio=0.5), run_time=2.4)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("times a lift coefficient that depends on the wing's shape and its angle to the wind.",
             FadeIn(labels[4], shift=UP * 0.1), run_time=1.0)
        self.vo_wait()
        self.play(clear(), run_time=0.3)

        k_box = SurroundingRectangle(eq[2], color=RED_INK, buff=0.12)
        k_val = MathTex(r"k = 0.005", font_size=44, color=RED_INK).move_to([-3.2, -1.2, 0])
        k_note = serif("a value dating from the 1700s (John Smeaton)", 18, FADED, italic=True).next_to(k_val, DOWN, buff=0.15)
        cl_box = SurroundingRectangle(eq[5], color=BLUE_INK, buff=0.12)
        table = VGroup(*[VGroup(*[Line([0, 0, 0], [0.55, 0, 0], color=INK, stroke_width=2).shift(RIGHT * 0.75 * j)
                                  for j in range(4)]).shift(DOWN * 0.22 * i) for i in range(5)])
        table_frame = SurroundingRectangle(table, color=INK, stroke_width=1.2, buff=0.18)
        tbl = VGroup(table_frame, table).move_to([3.2, -1.3, 0])
        tbl_note = serif("Otto Lilienthal's published tables", 18, FADED, italic=True).next_to(tbl, DOWN, buff=0.15)
        line("The constant was more than a century old: point zero zero five.",
             Create(k_box), FadeIn(k_val, shift=UP * 0.1), FadeIn(k_note), run_time=1.0)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("The lift coefficients came from tables published by the German glider pioneer Otto Lilienthal.",
             Create(cl_box), FadeIn(tbl, shift=UP * 0.1), FadeIn(tbl_note), run_time=1.0)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("Either the glider was wrong, or the numbers were.", run_time=0.6)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("So the brothers set out to test the numbers themselves.", run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(eq, labels, k_box, k_val, k_note, cl_box, tbl, tbl_note)), run_time=0.8)

        # ================= the bicycle test =================
        hub = np.array([0, 0.25, 0])
        rim = Circle(radius=1.5, color=INK, stroke_width=4).move_to(hub)
        spokes = VGroup(*[Line(hub, hub + 1.5 * np.array([np.cos(a), np.sin(a), 0]), color=INK, stroke_width=1)
                          for a in np.linspace(0, TAU, 16, endpoint=False)])
        plate = Rectangle(width=0.12, height=0.7, fill_color=SEPIA, fill_opacity=1, stroke_width=0).move_to(
            hub + LEFT * 1.5)
        wingm = airfoil(1.0, 0.16, 0.07).rotate(PI / 2).move_to(hub + RIGHT * 1.55)
        wheel = VGroup(rim, spokes, plate, wingm)
        pl_lab = serif("flat plate", 20, SEPIA).move_to(hub + LEFT * 2.9)
        wi_lab = serif("curved wing", 20, INK).move_to(hub + RIGHT * 3.0)
        bike_dir = Arrow([0, -2.2, 0], [0, -1.45, 0], buff=0, color=INK, stroke_width=3, tip_length=0.16)
        bike_lab = serif("bicycle rides this way", 16, FADED, italic=True).next_to(bike_dir, RIGHT, buff=0.15)
        air = VGroup(*[Arrow([x, 3.0, 0], [x, 2.3, 0], buff=0, color=BLUE_INK, stroke_width=3, tip_length=0.14)
                       for x in (-2.2, -1.1, 0, 1.1, 2.2)])
        air_lab = serif("air", 18, BLUE_INK, italic=True).next_to(air, RIGHT, buff=0.2)
        schem = serif("schematic, seen from above · Dayton, autumn 1901", 16, FADED, italic=True).move_to([-3.9, -2.6, 0])
        bike_dir.move_to([0, 3.1, 0]).rotate(PI)
        bike_dir.put_start_and_end_on([-4.6, 2.3, 0], [-4.6, 3.1, 0])
        bike_lab = serif("riding direction", 16, FADED, italic=True).next_to(bike_dir, RIGHT, buff=0.15)
        line("That autumn, back in Dayton, they fixed a spare wheel flat on the handlebars of a bicycle,",
             Create(rim), Create(spokes), FadeIn(schem), run_time=1.6)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("with a small curved wing on one side and a flat plate on the other.",
             FadeIn(plate), FadeIn(wingm), FadeIn(pl_lab), FadeIn(wi_lab), run_time=1.0)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        should = serif("if the table is right: balanced", 22, INK, italic=True).move_to([0, -2.05, 0])
        line("Riding into the air, the two should have balanced, if Lilienthal's table was right.",
             LaggedStart(*[GrowArrow(a) for a in air], lag_ratio=0.15), FadeIn(air_lab), GrowArrow(bike_dir),
             FadeIn(bike_lab), FadeIn(should), run_time=1.2)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        swung = serif("measured: the wheel swings round", 22, RED_INK, italic=True).move_to([0, -2.05, 0])
        line("Instead the wheel swung round. The wing was giving far less lift than the table said.",
             FadeOut(pl_lab), FadeOut(wi_lab), Transform(should, swung), run_time=0.6)
        self.play(Rotate(wheel, angle=38 * DEGREES, about_point=hub), run_time=2.2, rate_func=smooth)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("The street was too rough a laboratory.", run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(wheel, air, air_lab, bike_dir, bike_lab, should, schem)), run_time=0.8)

        # ================= the tunnel =================
        box = Rectangle(width=8.4, height=2.0, stroke_color=INK, stroke_width=3, fill_color=PAPER_DARK,
                        fill_opacity=0.35).move_to([0.3, 0.7, 0])
        planks = VGroup(*[Line(box.get_corner(UL) + RIGHT * x, box.get_corner(UL) + RIGHT * x + DOWN * 0.08,
                               color=SEPIA, stroke_width=1) for x in np.arange(0.5, 8.4, 0.5)])
        fan_c = box.get_left() + LEFT * 1.05
        fan = VGroup(*[Ellipse(width=0.25, height=0.85, color=INK, fill_color=SEPIA, fill_opacity=0.6,
                               stroke_width=1.2).shift(UP * 0.42).rotate(a, about_point=ORIGIN)
                       for a in (0, PI / 2, PI, 3 * PI / 2)]).move_to(fan_c)
        fan_ring = Circle(radius=1.0, color=INK, stroke_width=2).move_to(fan_c)
        fan.add_updater(lambda m, dt: m.rotate(dt * 9.0))
        engine = VGroup(Rectangle(width=1.0, height=0.8, color=INK, stroke_width=2, fill_color=PAPER_DARK,
                                  fill_opacity=1),
                        Circle(radius=0.22, color=INK, stroke_width=2).shift(UP * 0.1)).move_to([-5.6, -1.25, 0])
        belt = VGroup(Line(engine[1].get_top(), fan_c + LEFT * 0.05, color=INK, stroke_width=1.4),
                      Line(engine[1].get_right(), fan_c + RIGHT * 0.05 + DOWN * 0.05, color=INK, stroke_width=1.4))
        eng_lab = serif("shop engine, via belt and shaft", 16, FADED, italic=True).next_to(engine, RIGHT, buff=0.2)
        len_brace = BraceBetweenPoints(box.get_corner(DL), box.get_corner(DR), DOWN, color=SEPIA)
        len_lab = serif("about 6 ft", 20, SEPIA).next_to(len_brace, DOWN, buff=0.1)
        h_brace = BraceBetweenPoints(box.get_corner(DR), box.get_corner(UR), RIGHT, color=SEPIA)
        h_lab = serif("16 in square", 20, SEPIA).next_to(h_brace, RIGHT, buff=0.1)
        if h_lab.get_right()[0] > 6.6:
            h_lab.next_to(box.get_corner(UR), UP, buff=0.12).shift(LEFT * 0.6)

        line("So in the bicycle shop they built a wooden box, about six feet long and sixteen inches square,",
             Create(box), FadeIn(planks), GrowFromCenter(len_brace), FadeIn(len_lab), GrowFromCenter(h_brace),
             FadeIn(h_lab), run_time=2.0)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        self.add(fan)
        line("with a fan at one end driven by the shop's engine.",
             FadeIn(fan), Create(fan_ring), FadeIn(engine), Create(belt), FadeIn(eng_lab), run_time=1.0)
        self.vo_wait()
        self.play(clear(), run_time=0.3)

        # moving air: streaks that run through the box and wrap round
        x_in, x_out = box.get_left()[0] + 0.1, box.get_right()[0] - 0.1
        streaks = VGroup(*[Line(ORIGIN, RIGHT * 0.35, color=BLUE_INK, stroke_width=2, stroke_opacity=0.7)
                           .move_to([RNG.uniform(x_in, x_out), RNG.uniform(0.1, 1.7), 0]) for _ in range(40)])

        def flow(m, dt):
            for s in m:
                s.shift(RIGHT * 3.2 * dt)
                if s.get_center()[0] > x_out:
                    s.move_to([x_in, RNG.uniform(0.1, 1.7), 0])
        streaks.add_updater(flow)
        speed = serif("about 25 to 30 mph", 22, BLUE_INK, italic=True).next_to(box, UP, buff=0.18)
        line("Air ran through it at roughly twenty-five to thirty miles an hour.",
             FadeIn(streaks), FadeIn(speed), run_time=1.0)
        self.vo_wait()
        self.play(clear(), run_time=0.3)

        # the balance inside, with a dial above the box
        bc = box.get_center() + RIGHT * 1.6
        test_wing = airfoil(0.9, 0.1, 0.04).move_to(bc + UP * 0.25)
        plates = VGroup(*[Rectangle(width=0.08, height=0.32, fill_color=SEPIA, fill_opacity=1, stroke_width=0)
                          .move_to(bc + DOWN * 0.45 + RIGHT * dx) for dx in (-0.3, 0, 0.3)])
        axle = Line(bc + DOWN * 0.8, bc + UP * 1.7, color=INK, stroke_width=1.5)
        dial_c = box.get_top() + RIGHT * 1.6 + UP * 0.75
        dial = VGroup(Arc(radius=0.7, start_angle=20 * DEGREES, angle=140 * DEGREES, color=INK,
                          stroke_width=2).move_arc_center_to(dial_c),
                      *[Line(dial_c + 0.62 * np.array([np.cos(a), np.sin(a), 0]),
                             dial_c + 0.7 * np.array([np.cos(a), np.sin(a), 0]), color=INK, stroke_width=1.5)
                        for a in np.radians(np.arange(20, 161, 10))])
        theta = ValueTracker(90.0)
        piv = Dot(dial_c, radius=0.04, color=RED_INK)
        arc_w0 = dial[0].width

        def _pointer():
            c, sc = piv.get_center(), dial[0].width / arc_w0
            a = np.radians(theta.get_value())
            return Line(c, c + 0.68 * sc * np.array([np.cos(a), np.sin(a), 0]), color=RED_INK, stroke_width=3)
        pointer = always_redraw(_pointer)
        bal_lab = serif("balance: spoke wire and old hacksaw blades", 18, INK).move_to([-1.6, 2.35, 0])
        self.play(FadeOut(speed), run_time=0.4)
        line("Inside sat a balance made from bicycle spoke wire and old hacksaw blades.",
             FadeIn(test_wing), FadeIn(plates), Create(axle), FadeIn(dial), FadeIn(piv), FadeIn(pointer), FadeIn(bal_lab),
             run_time=1.2)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        wing_lab = serif("test wing", 16, INK, italic=True).next_to(test_wing, RIGHT, buff=0.15)
        pl_lab2 = serif("flat plates", 16, SEPIA, italic=True).next_to(plates, RIGHT, buff=0.15)
        line("The clever part: the balance set the lift of a test wing against the drag of flat plates.",
             FadeIn(wing_lab), FadeIn(pl_lab2), theta.animate.set_value(62), run_time=2.4)
        self.vo_wait()
        self.play(clear(), run_time=0.3)

        streaks.clear_updaters()
        self.play(FadeOut(streaks), run_time=0.4)
        streaks.set_opacity(0)
        self.remove(streaks)
        tunnel = VGroup(box, planks, fan, fan_ring, engine, belt, eng_lab, len_brace, len_lab, h_brace, h_lab,
                        test_wing, plates, axle, dial, piv, bal_lab, wing_lab, pl_lab2)
        self.play(tunnel.animate.scale(0.55).move_to([0, 1.95, 0]), run_time=1.0)
        lhs = MathTex(r"{L \over D_{\text{plates}}} =", font_size=50, color=INK)
        num = MathTex("k", r"\,S\,", "V^2", r"\,C_L", font_size=50, color=INK)
        den = MathTex("k", r"\,S_p\,", "V^2", r"\,C_D", font_size=50, color=INK)
        bar = Line(LEFT, RIGHT, color=INK, stroke_width=2.5).set_width(max(num.width, den.width) + 0.1)
        frac = VGroup(num, bar, den).arrange(DOWN, buff=0.12)
        ratio = VGroup(lhs, frac).arrange(RIGHT, buff=0.25).move_to([0, -1.25, 0])
        strikes = VGroup(*[Line(m.get_corner(DL) + LEFT * 0.05, m.get_corner(UR) + RIGHT * 0.05, color=RED_INK,
                                stroke_width=4) for m in (num[0], den[0], num[2], den[2])])
        line("The old constant appeared on both sides, and cancelled.", Write(ratio), run_time=1.6)
        self.play(LaggedStart(*[Create(s) for s in strikes], lag_ratio=0.25), run_time=1.2)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        res = MathTex(r"\text{angle on the dial} \;\longrightarrow\; C_L", font_size=40, color=RED_INK).move_to(
            [0, -1.25, 0])
        line("A pointer simply gave an angle, and the angle gave the lift coefficient.",
             FadeOut(VGroup(ratio, strikes)), FadeIn(res, shift=UP * 0.1), theta.animate.set_value(48), run_time=1.6)
        self.vo_wait()
        self.play(clear(), FadeOut(res), run_time=0.6)
        fan.clear_updaters()
        self.play(FadeOut(tunnel), FadeOut(pointer), run_time=0.8)

        # ================= around two hundred shapes =================
        grid = VGroup()
        for i in range(48):
            cam = 0.03 + 0.11 * ((i * 7) % 11) / 10
            th = 0.02 + 0.06 * ((i * 5) % 7) / 6
            grid.add(airfoil(1.05, cam, th + 0.02).set_stroke(width=2.4))
        grid.arrange_in_grid(rows=6, cols=8, buff=(0.45, 0.42)).move_to([0, 0.55, 0])
        count = serif("around two hundred shapes tested · a few dozen in depth", 22, SEPIA,
                      italic=True).move_to([0, 2.95, 0])
        line("Through the late autumn they tested around two hundred small metal wing shapes,",
             LaggedStart(*[FadeIn(g, scale=0.7) for g in grid], lag_ratio=0.06), FadeIn(count), run_time=3.2)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("and studied a few dozen of them in depth, angle after angle.",
             *[g.animate.set_opacity(0.2) for j, g in enumerate(grid) if j % 5], run_time=1.2)
        self.vo_wait()
        self.play(clear(), FadeOut(grid), FadeOut(count), run_time=0.8)

        # ================= lift curves =================
        ax = Axes(x_range=[0, 14, 2], y_range=[0, 1.6, 0.4], x_length=6.6, y_length=4.2, tips=False,
                  axis_config={"color": INK, "stroke_width": 2, "include_ticks": True},
                  ).move_to([-2.1, 0.35, 0])
        xl = serif("angle to the wind (degrees)", 18, FADED, italic=True).next_to(ax.x_axis, DOWN, buff=0.15)
        yl = serif("lift coefficient", 18, FADED, italic=True).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.2)
        xnums = VGroup(*[serif(str(v), 18, FADED).next_to(ax.c2p(v, 0), DOWN, buff=0.1) for v in range(0, 15, 4)])
        xl.next_to(xnums, DOWN, buff=0.08)
        c_long = ax.plot(lambda a: cl_curve(a, 6.5), x_range=[0, 14], color=RED_INK, stroke_width=4)
        c_short = ax.plot(lambda a: cl_curve(a, 3.3), x_range=[0, 14], color=SEPIA, stroke_width=4)
        p_long = planform(6.5).set_fill(RED_INK, opacity=0.25).set_stroke(RED_INK).move_to([4.3, 1.8, 0])
        p_short = planform(3.3).set_fill(SEPIA, opacity=0.25).set_stroke(SEPIA).move_to([4.3, -0.4, 0])
        l_long = serif("long and narrow", 20, RED_INK).next_to(p_long, DOWN, buff=0.15)
        l_short = serif("short and wide", 20, SEPIA).next_to(p_short, DOWN, buff=0.15)
        same = serif("same area", 16, FADED, italic=True).move_to([4.3, -1.75, 0])
        note = serif("schematic: modern thin-wing theory, not the Wrights' own measurements", 15, FADED,
                     italic=True).move_to([0, -2.65, 0])
        line("Curve by curve, a picture emerged.",
             Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xnums), FadeIn(note), run_time=1.2)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("A long, narrow wing lifted more than a short, wide one of the same area.",
             FadeIn(p_short), FadeIn(l_short), Create(c_short), run_time=1.6)
        self.play(FadeIn(p_long), FadeIn(l_long), FadeIn(same), Create(c_long), run_time=1.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(ax, xl, yl, xnums, c_long, c_short, note, same)), run_time=0.8)

        # ================= the constant =================
        old = MathTex(r"k = 0.005", font_size=60, color=INK).move_to([-3.0, 1.6, 0])
        cross = Line(old.get_corner(DL), old.get_corner(UR), color=RED_INK, stroke_width=5)
        new = MathTex(r"k \approx 0.0033", font_size=60, color=RED_INK).move_to([-3.0, 0.2, 0])
        factor = MathTex(r"\frac{0.005}{0.0033} \approx 1.5", font_size=48, color=INK).move_to([-3.0, -1.4, 0])
        self.play(p_long.animate.move_to([3.4, 1.7, 0]), l_long.animate.move_to([3.4, 1.15, 0]),
                  p_short.animate.move_to([3.4, -0.3, 0]), l_short.animate.move_to([3.4, -1.05, 0]), run_time=0.8)
        line("And the old constant was wrong. The true value was nearer point zero zero three three.",
             Write(old), run_time=1.0)
        self.play(Create(cross), FadeIn(new, shift=DOWN * 0.1), run_time=1.2)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("That alone made every prediction about one and a half times too high.",
             Write(factor), run_time=1.4)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        lil = serif("Lilienthal's test wing · about 6.5 : 1", 20, RED_INK).move_to(l_long)
        wri = serif("Wrights' 1901 glider · about 3.3 : 1", 20, SEPIA).move_to(l_short)
        line("Lilienthal's tables, it turned out, were largely sound for his own wing.",
             Transform(l_long, lil), FadeOut(VGroup(old, cross, new, factor)), run_time=1.0)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("But the Wrights' wing was far shorter and wider for its area, and nobody had known how much that mattered.",
             Transform(l_short, wri), Indicate(p_short, color=SEPIA, scale_factor=1.08), run_time=1.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(p_long, p_short, l_long, l_short)), run_time=0.8)

        # ================= 1902 and 1903 =================
        land = dunes()
        g02 = glider_side(span=3.4, gap=0.5).flip(UP).move_to([-4.6, 1.8, 0])
        path = DashedVMobject(Line([-4.6, 1.8, 0], [4.4, -0.9, 0], color=SEPIA, stroke_width=2), num_dashes=40)
        y02 = serif("Kill Devil Hills · autumn 1902", 22, SEPIA, italic=True).move_to([0, 3.15, 0])
        stats = VGroup(serif("700 to 1,000 glides", 26, INK),
                       serif("longest: 622½ ft", 22, FADED, italic=True)).arrange(DOWN, buff=0.12).move_to([3.4, 1.9, 0])
        line("In 1902 they went back to the dunes with a glider whose wings were about twice as long for their depth.",
             FadeIn(land, shift=UP * 0.2), FadeIn(y02), FadeIn(g02), run_time=1.2)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("That autumn they made somewhere between seven hundred and a thousand glides, the longest more than six hundred feet.",
             Create(path), g02.animate.move_to([4.4, -0.9, 0]).rotate(-3 * DEGREES), FadeIn(stats), run_time=5.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(g02, path, stats, y02)), run_time=0.6)
        d03 = serif("17 December 1903", 46, INK).move_to([0, 1.3, 0])
        d03b = serif("the first powered flights · Kill Devil Hills", 24, FADED, italic=True).next_to(d03, DOWN, buff=0.25)
        line("And on the seventeenth of December, 1903, they flew under power.",
             FadeIn(d03, shift=UP * 0.1), FadeIn(d03b), run_time=1.0)
        self.vo_wait()
        self.wait(0.4)
        self.play(clear(), FadeOut(VGroup(d03, d03b, land)), run_time=0.8)

        # ================= why it matters =================
        habit = VGroup(serif("When the numbers disagree with the world,", 36, INK),
                       serif("go and measure.", 44, RED_INK, italic=True)).arrange(DOWN, buff=0.3).move_to([0, 0.9, 0])
        mt = Rectangle(width=7.0, height=2.2, stroke_color=INK, stroke_width=2.5, fill_color=PAPER_DARK,
                       fill_opacity=0.3).move_to([0, 0.6, 0])
        mw = airfoil(2.4, 0.06, 0.12).rotate(-5 * DEGREES).move_to(mt.get_center())
        mlines = VGroup(*[VMobject(stroke_color=BLUE_INK, stroke_width=1.6).set_points_smoothly([
            np.array([x, mt.get_center()[1] + y0 + 0.28 * np.exp(-((x - 0.2) ** 2) / 1.2) * np.sign(y0) * (1.4 - abs(y0)), 0])
            for x in np.linspace(-3.4, 3.4, 30)]) for y0 in (-0.85, -0.55, 0.55, 0.85)])
        mlab = serif("still part of how new wings are tested", 20, FADED, italic=True).next_to(mt, DOWN, buff=0.2)
        line("Wind tunnels have shaped aircraft ever since.",
             Create(mt), FadeIn(mw), Create(mlines), FadeIn(mlab), run_time=1.6)
        self.vo_wait()
        self.play(FadeOut(VGroup(mt, mw, mlines, mlab)), run_time=0.6)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("The brothers' real invention was a habit: when the numbers disagree with the world, go and measure.",
             FadeIn(habit[0], shift=UP * 0.1), run_time=1.0)
        self.wait(2.2)
        self.play(FadeIn(habit[1], shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(habit), run_time=0.8)

        # ================= try it yourself =================
        tb = Rectangle(width=5.4, height=1.5, stroke_color=SEPIA, stroke_width=3, fill_color=PAPER_DARK,
                       fill_opacity=0.5).move_to([0.6, 0.6, 0])
        bfan = VGroup(Square(1.9, color=INK, stroke_width=2),
                      Circle(radius=0.8, color=INK, stroke_width=1.5),
                      *[Line(ORIGIN, 0.8 * np.array([np.cos(a), np.sin(a), 0]), color=INK, stroke_width=1)
                        for a in np.linspace(0, TAU, 8, endpoint=False)]).move_to(tb.get_left() + LEFT * 1.1)
        ruler = Rectangle(width=2.6, height=0.12, fill_color=SEPIA, fill_opacity=1, stroke_width=0).move_to(
            tb.get_top() + UP * 0.55 + RIGHT * 0.6)
        pivot = Triangle(color=INK, fill_color=INK, fill_opacity=1).scale(0.14).next_to(ruler, DOWN, buff=0)
        pivot.move_to(ruler.get_center() + DOWN * 0.14)
        thread = Line(ruler.get_left() + RIGHT * 0.3, ruler.get_left() + RIGHT * 0.3 + DOWN * 1.3, color=INK,
                      stroke_width=1)
        cw = airfoil(0.8, 0.1, 0.03).move_to(thread.get_end() + DOWN * 0.05)
        coins = VGroup(*[Circle(radius=0.11, color=INK, fill_color=PAPER_DARK, fill_opacity=1, stroke_width=1.5)
                         .move_to(ruler.get_right() + LEFT * 0.25 + UP * (0.17 + 0.05 * i)) for i in range(3)])
        labs = VGroup(serif("box fan", 18, INK).next_to(bfan, UP, buff=0.12),
                      serif("cardboard box, open at both ends", 18, SEPIA).next_to(tb, DOWN, buff=0.12),
                      serif("ruler balance with coins", 18, INK).next_to(ruler, UP, buff=0.35),
                      serif("card wing", 18, INK, italic=True).next_to(cw, DOWN, buff=0.15))
        rig = VGroup(tb, bfan, ruler, pivot, thread, cw, coins, labs)
        tryt = serif("Try it yourself", 34, INK).move_to([0, 3.0, 0])
        safe = serif("Keep fingers clear of the fan, and use one with a guard.", 18, RED_INK, italic=True).move_to(
            [0, -1.95, 0])
        line("Try it yourself. Tape a long cardboard box open at both ends in front of a box fan.",
             FadeIn(tryt), FadeIn(VGroup(tb, bfan, labs[0], labs[1])), run_time=1.2)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("Hang a card wing on a ruler balance, and watch the reading change as you tilt the wing,",
             FadeIn(VGroup(ruler, pivot, thread, cw, coins, labs[2], labs[3])), run_time=1.2)
        self.play(Rotate(cw, angle=10 * DEGREES), run_time=1.2)
        self.vo_wait()
        self.play(clear(), run_time=0.3)
        line("or swap in a longer, narrower wing of the same area. Keep your fingers clear of the fan.",
             FadeIn(safe), run_time=0.8)
        self.vo_wait()
        self.wait(0.6)
        self.play(clear(), FadeOut(VGroup(rig, tryt, safe)), run_time=0.8)

        # ================= end card =================
        end = VGroup(serif("The Wind Tunnel in a Bicycle Shop", 40, INK),
                     ornament(3.0),
                     serif("story after David McCullough, The Wright Brothers (Simon & Schuster, 2015)", 18, FADED,
                           italic=True),
                     serif("sources listed with the video · silhouettes are stylised, not likenesses", 16, FADED,
                           italic=True),
                     serif("animated with Manim · narration by a synthetic voice", 16, FADED, italic=True),
                     ).arrange(DOWN, buff=0.25).move_to([0, 0.3, 0])
        self.play(FadeIn(end, shift=UP * 0.1), run_time=1.0)
        self.wait(3.0)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)
        self.wait(0.3)
