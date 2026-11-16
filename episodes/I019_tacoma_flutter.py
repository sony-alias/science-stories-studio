"""I019 The Bridge That Twisted Itself Apart, a Science Stories episode.

After H. Petroski, To Engineer Is Human (1985). Script and sources: episodes/I019_script.md

Render:  manim -qh --frame_rate 30 episodes/I019_tacoma_flutter.py TacomaFlutter
Then:    scripts/finish_video.sh media/videos/I019_tacoma_flutter/1080p30/TacomaFlutter.mp4 out/I019_tacoma_flutter.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

STEEL = "#6f7a80"
WATER = "#5d7a8c"


def note(text, size=17, color=FADED):
    return serif(text, size, color, italic=True)


def poly(pts, color=INK, width=2.5):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_as_corners([np.array([p[0], p[1], 0]) for p in pts])
    return m


def smooth(pts, color=INK, width=2.5):
    m = VMobject(stroke_color=color, stroke_width=width)
    m.set_points_smoothly([np.array([p[0], p[1], 0]) for p in pts])
    return m


def water(y=-2.35, x0=-6.4, x1=6.4, rows=3):
    g = VGroup()
    for r in range(rows):
        yy = y - 0.18 * r
        for k in range(9):
            xa = x0 + 0.4 + k * (x1 - x0) / 9 + (0.35 if r % 2 else 0)
            if xa + 0.6 > x1:
                continue
            g.add(ArcBetweenPoints([xa, yy, 0], [xa + 0.6, yy, 0], angle=-0.7, color=WATER, stroke_width=1.6,
                                   stroke_opacity=0.7 - 0.15 * r))
    return g


def h_section(w=3.2, gh=0.62, color=INK):
    """Cross-section of the 1940 deck: a thin roadway between two solid plate girders (schematic)."""
    deck = Rectangle(width=w, height=0.09, stroke_width=0, fill_color=color, fill_opacity=1)
    gl = Rectangle(width=0.12, height=gh, stroke_width=0, fill_color=color, fill_opacity=1).move_to(
        [-w / 2, -gh * 0.25, 0])
    gr = gl.copy().move_to([w / 2, -gh * 0.25, 0])
    return VGroup(deck, gl, gr)


def truss_section(w=3.2, h=2.2, color=INK):
    """Cross-section of the 1950 deck: deep open trusses and a roadway with open grates (schematic)."""
    g = VGroup()
    for sx in (-1, 1):
        x = sx * w / 2
        g.add(Line([x, h / 2, 0], [x, -h / 2, 0], color=color, stroke_width=3))
    g.add(Line([-w / 2, h / 2, 0], [w / 2, h / 2, 0], color=color, stroke_width=2))
    g.add(Line([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], color=color, stroke_width=2))
    for k in range(4):
        x0 = -w / 2 + k * w / 4
        g.add(Line([x0, -h / 2, 0], [x0 + w / 4, h / 2, 0], color=color, stroke_width=1.4))
    # roadway with gaps (grates)
    segs = [(-1.5, -0.95), (-0.75, -0.1), (0.1, 0.75), (0.95, 1.5)]
    for a, b in segs:
        g.add(Rectangle(width=(b - a) * w / 3.2, height=0.07, stroke_width=0, fill_color=color,
                        fill_opacity=1).move_to([(a + b) / 2 * w / 3.2, h / 2 - 0.05, 0]))
    return g


def fan_icon(c, r=0.5):
    c = np.array([c[0], c[1], 0])
    ring = Circle(radius=r, color=INK, stroke_width=2.5).move_to(c)
    blades = VGroup(*[Ellipse(width=r * 0.9, height=r * 0.38, stroke_width=0, fill_color=SEPIA, fill_opacity=0.8)
                      .move_to(c + r * 0.45 * np.array([np.cos(a), np.sin(a), 0])).rotate(a, about_point=c + r * 0.45 *
                                                                                         np.array([np.cos(a), np.sin(a), 0]))
                      for a in (0, TAU / 3, 2 * TAU / 3)])
    hub = Dot(c, radius=0.07, color=INK)
    stand = Line(c + DOWN * r, c + DOWN * (r + 0.5), color=INK, stroke_width=3)
    base = Line(c + DOWN * (r + 0.5) + LEFT * 0.35, c + DOWN * (r + 0.5) + RIGHT * 0.35, color=INK, stroke_width=3)
    return VGroup(ring, blades, hub, stand, base)


class TacomaFlutter(NarratedScene):
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

        clock = ValueTracker(0.0)
        clock.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(clock)

        # ================= title =================
        series = spaced("Science Stories", 22).move_to([0, 1.8, 0])
        orn1 = ornament(3.4).next_to(series, DOWN, buff=0.3)
        title = serif("The Bridge That Twisted Itself Apart", 52).next_to(orn1, DOWN, buff=0.35)
        sub = serif("Tacoma Narrows · 7 November 1940", 26, FADED, italic=True).next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("after Henry Petroski, To Engineer Is Human: The Role of Failure in Successful Design (1985)",
                      16).move_to([0, -3.2, 0])
        self.vo("Science Stories. The bridge that twisted itself apart.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= the bridge in elevation, bouncing =================
        TX, TOP, DY = 2.8, 1.25, -1.0           # tower x, tower top, deck height
        bounce = ValueTracker(0.0)

        def main_cable_y(x):
            return DY + 0.3 + (TOP - DY - 0.3) * (x / TX) ** 2

        def deck_v(x):
            if abs(x) >= TX:
                return 0.0
            return bounce.get_value() * np.sin(3 * PI * (x + TX) / (2 * TX)) * np.sin(TAU * clock.get_value() / 1.6)

        def build_elev():
            xs = np.linspace(-6.3, 6.3, 127)
            deck = smooth([(x, DY + deck_v(x)) for x in xs], INK, 4)
            hx = np.arange(-TX + 0.35, TX - 0.2, 0.35)
            hang = VGroup(*[Line([x, main_cable_y(x), 0], [x, DY + deck_v(x), 0], color=INK, stroke_width=1)
                            for x in hx])
            return VGroup(deck, hang)

        towers = VGroup(*[VGroup(Rectangle(width=0.22, height=TOP - DY + 1.35, stroke_color=INK, stroke_width=2,
                                           fill_color=STEEL, fill_opacity=1).move_to([sx * TX, (TOP + DY - 1.35) / 2, 0]))
                          for sx in (-1, 1)])
        cable_main = FunctionGraph(main_cable_y, x_range=[-TX, TX, 0.05], color=INK, stroke_width=2.5)
        cable_side = VGroup(*[ArcBetweenPoints([sx * TX, TOP, 0], [sx * 6.3, DY + 0.15, 0], angle=sx * 0.25,
                                               color=INK, stroke_width=2.5) for sx in (-1, 1)])
        sea = water()
        elev = always_redraw(build_elev)
        static = VGroup(towers, cable_main, cable_side, sea)

        place = serif("Tacoma Narrows, Washington · 7 November 1940", 22, SEPIA, italic=True).move_to([0, 3.2, 0])
        prof = cameo("modern", 0.55)
        p_name = serif("F. B. Farquharson", 20, INK).next_to(prof, DOWN, buff=0.1)
        p_role = VGroup(note("engineering professor", 14), note("University of Washington", 14)).arrange(
            DOWN, buff=0.03).next_to(p_name, DOWN, buff=0.05)
        pw = VGroup(prof, p_name, p_role).move_to([-5.1, 2.0, 0])
        camera_icon = VGroup(RoundedRectangle(corner_radius=0.06, width=0.55, height=0.36, stroke_color=INK,
                                              stroke_width=2, fill_color=INK, fill_opacity=0.85),
                             Circle(radius=0.12, color=PAPER, stroke_width=2).shift(RIGHT * 0.05),
                             Polygon([0.27, 0.06, 0], [0.45, 0.16, 0], [0.45, -0.16, 0], [0.27, -0.06, 0],
                                     stroke_width=0, fill_color=INK, fill_opacity=0.85)).move_to([-3.75, 2.55, 0])

        line("November the seventh, 1940. Professor F. B. Farquharson arrives at the Tacoma Narrows Bridge with his cameras.",
             FadeIn(place), FadeIn(static), FadeIn(elev), run_time=1.2)
        self.play(FadeIn(pw, shift=UP * 0.1), FadeIn(camera_icon), run_time=0.8)
        self.vo_wait()

        nick = serif("“Galloping Gertie”", 34, RED_INK).move_to([3.3, 2.35, 0])
        opened = note("opened 1 July 1940", 17).next_to(nick, DOWN, buff=0.12)
        line("The bridge had opened that July. People already called it Galloping Gertie, because its deck bounced up and down in the wind.",
             FadeIn(opened), run_time=0.8)
        self.play(Write(nick), bounce.animate.set_value(0.28), run_time=1.6)
        self.vo_wait()

        model = VGroup(Rectangle(width=2.3, height=0.9, stroke_color=SEPIA, stroke_width=1.5, fill_color=PAPER_DARK,
                                 fill_opacity=0.6),
                       poly([(-0.95, -0.05), (-0.5, 0.25), (0, -0.05), (0.5, 0.25), (0.95, -0.05)], SEPIA, 2),
                       note("scale model (1:200)", 14).shift(DOWN * 0.28))
        model.next_to(pw, DOWN, buff=0.25).shift(RIGHT * 0.3)
        model.move_to([-4.9, -0.05, 0])
        line("Farquharson, an engineering professor at the University of Washington, had been studying that motion with scale models.",
             FadeIn(model, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()

        # wind
        def build_wind():
            t = clock.get_value()
            g = VGroup()
            for i, y in enumerate([0.15, 0.6, -0.35]):
                for k in range(3):
                    x = -6.0 + ((t * 2.2 + i * 1.7 + k * 4.1) % 12.0)
                    g.add(Arrow([x, y, 0], [x + 0.7, y, 0], buff=0, color=BLUE_INK, stroke_width=2.5,
                                tip_length=0.13, max_tip_length_to_length_ratio=0.3).set_opacity(0.75 if x <= 5.6 else 0))
            return g

        wind = always_redraw(build_wind)
        wind_l = serif("wind ≈ 40 mph, steady", 22, BLUE_INK, italic=True).move_to([0, 1.55, 0])
        line("That morning the wind is strong, but steady: about forty miles an hour.",
             FadeOut(model), FadeIn(wind), FadeIn(wind_l), run_time=0.9)
        self.vo_wait()

        # timeline at the top
        tl = Line([-4.5, 3.2, 0], [4.5, 3.2, 0], color=SEPIA, stroke_width=1.5)

        def tl_mark(x, t, label):
            tick = Line([x, 3.1, 0], [x, 3.3, 0], color=RED_INK, stroke_width=3)
            tt = serif(t, 18, RED_INK).next_to(tick, UP, buff=0.05)
            ll = note(label, 14).next_to(tick, DOWN, buff=0.06)
            return VGroup(tick, tt, ll)

        m1 = tl_mark(-3.6, "9:30", "Farquharson arrives")
        m2 = tl_mark(0.0, "10:03", "twisting begins")
        m3 = tl_mark(3.6, "≈ 11:02", "span falls")
        line("Just after ten o'clock, the motion changes.",
             FadeOut(place), FadeOut(nick), FadeOut(opened), FadeOut(wind_l), Create(tl), FadeIn(m1), run_time=0.9)
        self.play(FadeIn(m2, shift=DOWN * 0.1), run_time=0.6)
        self.vo_wait()

        # ================= the twist (ribbon view) =================
        elev.clear_updaters()
        wind.clear_updaters()
        self.play(FadeOut(VGroup(elev, static, wind, pw, camera_icon)), run_time=0.8)

        twist = ValueTracker(0.0)
        Y0, B, L = -1.15, 0.62, 5.0

        def theta(x):
            return twist.get_value() * np.sin(PI * (x + L) / L) * np.sin(TAU * clock.get_value() / 5.0)

        def scr(x, s, th):
            lat, vert = s * np.cos(th), s * np.sin(th)
            return np.array([x + 0.32 * lat, Y0 + vert + 0.55 * lat, 0])

        def cable_y(x):
            return Y0 + 0.75 + 1.9 * (x / L) ** 2

        def build_ribbon():
            xs = np.linspace(-L, L, 81)
            near = [scr(x, -B, theta(x)) for x in xs]
            far = [scr(x, B, theta(x)) for x in xs]
            surf = Polygon(*near, *far[::-1], stroke_width=0, fill_color=PAPER_DARK, fill_opacity=0.9)
            e1 = VMobject(stroke_color=INK, stroke_width=3).set_points_smoothly(near)
            e2 = VMobject(stroke_color=INK, stroke_width=2).set_points_smoothly(far)
            ribs = VGroup(*[Line(scr(x, -B, theta(x)), scr(x, B, theta(x)), color=INK, stroke_width=0.8,
                                 stroke_opacity=0.6) for x in xs[::4]])
            centre = VMobject(stroke_color=RED_INK, stroke_width=1.5).set_points_smoothly(
                [scr(x, 0, theta(x)) for x in xs])
            hx = xs[2:-2:4]
            hang = VGroup()
            for s in (B, -B):
                for x in hx:
                    top = scr(x, s, 0) + np.array([0, cable_y(x) - Y0, 0])
                    hang.add(Line(top, scr(x, s, theta(x)), color=INK, stroke_width=0.8))
            return VGroup(surf, ribs, e2, e1, centre, hang)

        cables = VGroup(*[VMobject(stroke_color=INK, stroke_width=2.2).set_points_smoothly(
            [scr(x, s, 0) + np.array([0, cable_y(x) - Y0, 0]) for x in np.linspace(-L, L, 41)]) for s in (B, -B)])
        tw_towers = VGroup(*[Rectangle(width=0.2, height=cable_y(L) - Y0 + 1.1, stroke_color=INK, stroke_width=2,
                                       fill_color=STEEL, fill_opacity=1).move_to(
            [sx * L, (cable_y(L) + Y0 - 1.1) / 2, 0]) for sx in (-1, 1)])
        ribbon = always_redraw(build_ribbon)
        rib_l = note("the main span, twisting (schematic, real timing)", 15).move_to([0, -2.55, 0])
        line("The deck stops bouncing, and starts to twist.", FadeIn(tw_towers), FadeIn(cables), FadeIn(ribbon),
             FadeIn(rib_l), run_time=0.9)
        self.play(twist.animate.set_value(30 * DEGREES), run_time=2.0)
        self.vo_wait()

        tilt_c = ink_card(VGroup(serif("tilt: up to 45°", 24, RED_INK), note("one cycle about every 5 seconds", 16))
                          .arrange(DOWN, buff=0.1)).move_to([0, 1.75, 0])
        line("Accounts say the roadway tilted as much as forty-five degrees, rocking back and forth about every five seconds.",
             FadeIn(tilt_c, shift=DOWN * 0.1), twist.animate.set_value(42 * DEGREES), run_time=1.5)
        self.vo_wait()

        # Coatsworth and Tubby
        car = VGroup(RoundedRectangle(corner_radius=0.1, width=1.0, height=0.32, stroke_color=INK, stroke_width=2,
                                      fill_color=SEPIA, fill_opacity=0.8),
                     Polygon([-0.28, 0.16, 0], [-0.15, 0.36, 0], [0.22, 0.36, 0], [0.33, 0.16, 0], stroke_color=INK,
                             stroke_width=2, fill_color=PAPER, fill_opacity=1),
                     Circle(radius=0.11, color=INK, stroke_width=2, fill_color=INK, fill_opacity=1).move_to([-0.3, -0.17, 0]),
                     Circle(radius=0.11, color=INK, stroke_width=2, fill_color=INK, fill_opacity=1).move_to([0.3, -0.17, 0]))
        c_text = VGroup(serif("Leonard Coatsworth", 20, INK), note("news editor · his car stays on the bridge", 14),
                        note("inside: Tubby, his daughter's dog", 14)).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        c_card = ink_card(VGroup(car, c_text).arrange(RIGHT, buff=0.3)).move_to([0, 1.75, 0])
        line("A newspaper editor, Leonard Coatsworth, abandons his car on the bridge and crawls to safety. His daughter's dog, Tubby, is still inside.",
             FadeOut(tilt_c), FadeIn(c_card, shift=DOWN * 0.1), run_time=1.0)
        self.vo_wait()
        f_card = ink_card(VGroup(serif("Farquharson walks out to the car", 20, INK),
                                 note("the frightened dog bites his finger", 14)).arrange(DOWN, buff=0.05)).move_to(
            [0, 1.75, 0])
        line("Farquharson walks out to rescue the dog, but the terrified animal bites him.",
             FadeOut(c_card), FadeIn(f_card, shift=DOWN * 0.1), run_time=0.9)
        self.vo_wait()

        # collapse, back in elevation
        ribbon.clear_updaters()
        self.play(FadeOut(VGroup(ribbon, cables, tw_towers, rib_l, f_card)), run_time=0.7)
        bounce.set_value(0.0)
        xs = np.linspace(-6.3, 6.3, 127)
        cut = 1.55
        d_left = smooth([(x, DY) for x in np.linspace(-6.3, -cut, 30)], INK, 4)
        d_mid = smooth([(x, DY) for x in np.linspace(-cut, cut, 30)], INK, 4)
        d_right = smooth([(x, DY) for x in np.linspace(cut, 6.3, 30)], INK, 4)
        hx = np.arange(-TX + 0.35, TX - 0.2, 0.35)
        h_out = VGroup(*[Line([x, main_cable_y(x), 0], [x, DY, 0], color=INK, stroke_width=1)
                         for x in hx if abs(x) > cut])
        h_in = VGroup(*[Line([x, main_cable_y(x) - 0.1, 0], [x, DY, 0], color=INK,
                             stroke_width=1) for x in hx if abs(x) <= cut])
        self.play(FadeIn(VGroup(static, d_left, d_mid, d_right, h_out, h_in)), run_time=0.7)
        span_l = note("≈ 600 feet of roadway", 18, RED_INK).move_to([0, -1.6, 0])
        line("Just after eleven, six hundred feet of roadway falls into the Narrows. No person dies, but Tubby is lost.",
             FadeIn(m3, shift=DOWN * 0.1), run_time=0.8)
        self.play(VGroup(d_mid, h_in).animate.shift(DOWN * 1.3).rotate(-6 * DEGREES).set_opacity(0.0),
                  FadeIn(span_l), run_time=1.6, rate_func=rate_functions.ease_in_quad)
        splash = VGroup(*[ArcBetweenPoints([x, -2.3, 0], [x + 0.3, -2.3, 0], angle=-1.4, color=WATER, stroke_width=2)
                          for x in (-1.2, -0.5, 0.2, 0.9)])
        self.play(FadeIn(splash, shift=UP * 0.15), run_time=0.5)
        self.play(FadeOut(splash), run_time=0.5)
        self.remove(d_mid, h_in)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(static, d_left, d_right, h_out, span_l, tl, m1, m2, m3)), run_time=0.8)

        # ================= the textbook answer: resonance =================
        q = serif("What destroyed the bridge?", 34, INK).move_to([0, 2.7, 0])
        line("So what destroyed the bridge? Many textbooks say: resonance.", Write(q), run_time=1.0)
        res = serif("“resonance”", 34, FADED, italic=True).move_to([0, 1.9, 0])
        self.play(FadeIn(res), run_time=0.6)
        self.vo_wait()

        swing_amp = ValueTracker(0.08)
        PIV = np.array([-3.2, 1.3, 0])
        RL = 2.3

        def phi():
            return swing_amp.get_value() * np.sin(TAU * clock.get_value() / 2.4)

        def build_swing():
            a = phi()
            seat_c = PIV + RL * np.array([np.sin(a), -np.cos(a), 0])
            rope = Line(PIV, seat_c, color=INK, stroke_width=2.5)
            seat = Rectangle(width=0.6, height=0.1, stroke_width=0, fill_color=SEPIA, fill_opacity=1).move_to(
                seat_c).rotate(a)
            g = VGroup(rope, seat)
            # a push arrow while the seat swings away to the right, near the back of its swing
            ph = (clock.get_value() / 2.4) % 1.0
            g.add(Arrow(seat_c + LEFT * 0.85, seat_c + LEFT * 0.3, buff=0, color=RED_INK, stroke_width=4,
                        tip_length=0.16).set_opacity(1 if 0.72 < ph < 0.95 else 0))
            return g

        beam = Line(PIV + LEFT * 0.8, PIV + RIGHT * 0.8, color=INK, stroke_width=5)
        swing = always_redraw(build_swing)
        sw_l = note("a push in time with the rhythm", 17).move_to([-3.2, -1.9, 0])
        line("Push a swing in time with its rhythm, and every push adds a little more.",
             FadeIn(beam), FadeIn(swing), FadeIn(sw_l), run_time=0.8)
        self.play(swing_amp.animate.set_value(0.5), run_time=5.0, rate_func=linear)
        self.vo_wait()

        rhythm = VGroup(*[Arrow([2.0 + 0.0 * i, 0.9 - 0.0, 0], [2.6, 0.9, 0], buff=0)
                          for i in range(0)])
        pulses = VGroup(*[Rectangle(width=0.18, height=0.5, stroke_width=0, fill_color=RED_INK,
                                    fill_opacity=0.85).move_to([1.4 + 0.6 * i, 0.55, 0]) for i in range(7)])
        pulses_l = note("needed: a rhythmic push", 17).next_to(pulses, UP, buff=0.15)
        steady = VGroup(*[Arrow([1.2, y, 0], [5.4, y, 0], buff=0, color=BLUE_INK, stroke_width=3, tip_length=0.18)
                          for y in (-0.6, -0.95, -1.3)])
        steady_l = note("1940: a steady wind", 17, BLUE_INK).next_to(steady, DOWN, buff=0.12)
        line("But resonance needs a push that repeats, in step with the bridge. The wind that morning was not a rhythm. It was a steady stream.",
             FadeIn(pulses, lag_ratio=0.15), FadeIn(pulses_l), run_time=1.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in steady], lag_ratio=0.2), FadeIn(steady_l), run_time=1.2)
        cross = note("not what the wind did", 17, RED_INK).next_to(pulses, DOWN, buff=0.12)
        self.play(pulses.animate.set_opacity(0.25), FadeIn(cross), run_time=0.6)
        self.vo_wait()
        st = VGroup(stamp(r"\text{resonance: improbable}", size=34), note("Federal Works Agency board, 1941", 15))
        st[1].next_to(st[0], DOWN, buff=0.15)
        st.move_to([0.6, 2.35, 0])
        line("The board that investigated the collapse called resonance improbable.", FadeOut(res), FadeOut(q),
             FadeIn(st[0], scale=1.2), FadeIn(st[1]), run_time=0.9)
        self.vo_wait()
        swing.clear_updaters()
        self.play(clear(), FadeOut(VGroup(st, beam, swing, sw_l, pulses, pulses_l, steady, steady_l, cross,
                                          rhythm)), run_time=0.8)

        # ================= the mechanism: cross-section =================
        amp = ValueTracker(10 * DEGREES)
        CX, CY = -0.6, 0.55
        W_SEC = 3.2
        PER = 2.5

        def ang():
            return amp.get_value() * np.sin(TAU * clock.get_value() / PER)

        def ang_rate():
            return np.cos(TAU * clock.get_value() / PER)

        def build_section():
            return h_section(W_SEC, 0.62).rotate(ang()).move_to([CX, CY, 0])

        def build_flow():
            t = clock.get_value()
            g = VGroup()
            for i, y in enumerate([-1.15, -0.65, 1.75, 2.25]):
                for k in range(4):
                    x = -6.2 + ((t * 2.0 + i * 1.3 + k * 3.2) % 12.4)
                    g.add(Line([x, y, 0], [x + 0.6, y, 0], color=BLUE_INK, stroke_width=2,
                               stroke_opacity=0.6 if x <= 5.9 else 0))
            for k in range(6):   # swirls shed from the trailing edges, alternately above and below
                j = int(np.floor(t / (PER / 2))) - k
                age = t - j * PER / 2
                sgn = 1 if j % 2 == 0 else -1
                x = CX + W_SEC / 2 + 0.35 + 0.9 * age
                op = max(0.0, 1.0 - age / (3 * PER)) if x <= 5.6 else 0.0
                g.add(spiral([x, CY + sgn * 0.5, 0], sgn, size=0.22, opacity=op))
            return g

        def build_push():
            r = ang_rate()
            ccw = r > 0
            c = np.array([CX, CY, 0])
            arc = Arc(radius=2.15, start_angle=(70 if ccw else 110) * DEGREES, angle=(40 if ccw else -40) * DEGREES,
                      arc_center=c, color=RED_INK, stroke_width=5)
            arc.add_tip(tip_length=0.22)
            if abs(r) < 0.25:
                arc.set_opacity(0)
            return arc

        sec = always_redraw(build_section)
        flow = always_redraw(build_flow)
        g_lab = note("solid plate girder, 8 ft deep", 17).move_to([CX - 2.6, -1.85, 0])
        g_arrow = Arrow(g_lab.get_top() + RIGHT * 0.6, [CX - W_SEC / 2 + 0.05, CY - 0.35, 0], buff=0.08,
                        color=FADED, stroke_width=2, tip_length=0.14)
        sec_l = note("cross-section of the 1940 deck (schematic)", 15).move_to([0, -2.45, 0])
        line("Here is the deck in cross-section. Its edges are solid steel girders, eight feet deep. To the wind, it is a blunt, flat wing.",
             FadeIn(sec), FadeIn(flow), FadeIn(sec_l), run_time=1.0)
        self.play(FadeIn(g_lab), GrowArrow(g_arrow), run_time=0.8)
        self.vo_wait()
        line("When the deck twists, the air peeling off its edges rolls into swirls, and the timing of those swirls is set by the deck's own motion.",
             FadeOut(g_lab), FadeOut(g_arrow), run_time=0.8)
        sw_l2 = note("swirls shed in time with the twist", 17).move_to([3.6, -1.85, 0])
        self.play(FadeIn(sw_l2), run_time=0.6)
        self.vo_wait()
        push = always_redraw(build_push)
        push_l = serif("wind's push, in step with the twist", 20, RED_INK, italic=True).move_to([CX, CY + 2.75, 0])
        line("So the wind's push arrives in step with the twist, every time. Nobody is pushing the bridge with a rhythm. The bridge makes its own.",
             FadeOut(sw_l2), FadeIn(push), FadeIn(push_l), amp.animate.set_value(18 * DEGREES), run_time=1.5)
        self.play(amp.animate.set_value(26 * DEGREES), run_time=3.0, rate_func=linear)
        self.vo_wait()
        name = ink_card(VGroup(serif("flutter", 34, RED_INK), note("a self-excited oscillation", 17)).arrange(
            DOWN, buff=0.08)).move_to([4.3, -1.45, 0])
        line("Engineers call this flutter: a self-excited oscillation.", FadeIn(name, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        for m in (sec, flow, push):
            m.clear_updaters()
        self.play(clear(), FadeOut(VGroup(sec, flow, push, push_l, sec_l, name)), run_time=0.8)

        # ================= the equation and the energy =================
        eq1 = MathTex(r"I\,\ddot\theta", "+", r"c\,\dot\theta", "+", r"k\,\theta", "=", "0", font_size=54, color=INK)
        eq1.move_to([0, 0.9, 0])
        labs = VGroup(note("inertia", 18).next_to(eq1[0], DOWN, buff=0.3),
                      note("friction (damping)", 18).next_to(eq1[2], DOWN, buff=0.75),
                      note("stiffness", 18).next_to(eq1[4], DOWN, buff=0.3))
        labs.add(*[Line(l.get_top() + UP * 0.05, e.get_bottom() + DOWN * 0.05, color=FADED, stroke_width=1)
                   for l, e in ((labs[1], eq1[2]),)])
        line("Write the twist as a spring with friction. Friction always takes energy out.", Write(eq1), run_time=1.2)
        self.play(FadeIn(labs), run_time=0.6)
        self.vo_wait()
        eq2 = MathTex(r"I\,\ddot\theta", "+", r"(c - c_{\mathrm{wind}})\,\dot\theta", "+", r"k\,\theta", "=", "0",
                      font_size=54, color=INK).move_to(eq1)
        eq2[2].set_color(RED_INK)
        lab2 = note("the wind's term grows with wind speed", 16, RED_INK).next_to(eq2[2], DOWN, buff=0.25)
        line("But the wind adds a term that depends on how fast the deck is turning. It acts like friction running backwards.",
             TransformMatchingTex(eq1, eq2), FadeOut(labs), run_time=1.2)
        self.play(FadeIn(lab2), run_time=0.6)
        self.vo_wait()

        def panel(x, fn, title, sub, color):
            ax = Axes(x_range=[0, 30, 5], y_range=[-1.2, 1.2, 1], x_length=4.8, y_length=2.1, tips=False,
                      axis_config={"color": INK, "stroke_width": 1.5, "include_ticks": False}).move_to([x, -0.75, 0])
            curve = ax.plot(fn, x_range=[0, 30, 0.05], color=color, stroke_width=3)
            t_l = serif(title, 20, color).next_to(ax, UP, buff=0.12)
            s_l = note(sub, 15).next_to(ax, DOWN, buff=0.08)
            yl = note("twist", 14).next_to(ax.y_axis, UP, buff=0.04)
            return ax, curve, VGroup(t_l, s_l, yl)

        w = TAU / 5.0
        ax1, c1, l1 = panel(-3.2, lambda t: 0.9 * np.exp(-0.12 * t) * np.sin(w * t), "low wind",
                            "damping wins: over time, the twist dies away", INK)
        ax2, c2, l2 = panel(3.2, lambda t: 0.08 * np.exp(0.085 * t) * np.sin(w * t), "above the critical speed",
                            "the wind wins: over time, the twist grows", RED_INK)
        illus = note("illustration, not measured data", 14).move_to([0, -2.55, 0])
        line("At low wind speed, friction wins, and any twist dies away.",
             VGroup(eq2, lab2).animate.move_to([0, 2.45, 0]).shift(DOWN * 0.2), run_time=0.7)
        self.play(FadeIn(ax1), FadeIn(l1), FadeIn(illus), run_time=0.6)
        self.play(Create(c1), run_time=2.2, rate_func=linear)
        self.vo_wait()
        line("Above a critical speed, the total damping turns negative. Each swing feeds the next, and the twist grows until something breaks.",
             FadeIn(ax2), FadeIn(l2), run_time=0.8)
        self.play(Create(c2), run_time=3.5, rate_func=linear)
        snap = Cross(Square(0.3), stroke_color=RED_INK, stroke_width=5).move_to(ax2.c2p(30, 1.0) + RIGHT * 0.15)
        self.play(FadeIn(snap, scale=1.5), run_time=0.4)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(eq2, lab2, ax1, c1, l1, ax2, c2, l2, illus, snap)), run_time=0.8)

        # ================= resonance vs flutter, side by side =================
        def mini_swing(x, ang_, color):
            piv = np.array([x, 1.9, 0])
            seat = piv + 1.5 * np.array([np.sin(ang_), -np.cos(ang_), 0])
            return VGroup(Line(piv + LEFT * 0.5, piv + RIGHT * 0.5, color=INK, stroke_width=4),
                          Line(piv, seat, color=INK, stroke_width=2.5),
                          Rectangle(width=0.45, height=0.08, stroke_width=0, fill_color=color,
                                    fill_opacity=1).move_to(seat).rotate(ang_))

        left = VGroup(mini_swing(-3.3, 0.35, SEPIA),
                      Arrow([-4.9, 0.55, 0], [-4.35, 0.55, 0], buff=0, color=RED_INK, stroke_width=4, tip_length=0.15),
                      serif("Resonance", 30, INK).move_to([-3.3, -0.55, 0]),
                      note("a swing pushed by a friend, in rhythm", 17).move_to([-3.3, -1.05, 0]))
        right = VGroup(mini_swing(3.3, -0.35, RED_INK),
                       *[Arrow([1.4, y, 0], [2.3, y, 0], buff=0, color=BLUE_INK, stroke_width=3, tip_length=0.14)
                         for y in (0.3, 0.7, 1.1)],
                       serif("Flutter", 30, RED_INK).move_to([3.3, -0.55, 0]),
                       note("a swing that pushes itself, fed by a steady wind", 17).move_to([3.3, -1.05, 0]))
        divider = DashedLine([0, 2.3, 0], [0, -1.4, 0], color=SEPIA, stroke_width=1.5)
        line("Resonance is a swing pushed by a friend. Flutter is a swing that pushes itself, with a steady wind as its fuel.",
             FadeIn(left, shift=RIGHT * 0.1), FadeIn(divider), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(right, shift=LEFT * 0.1), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(left, right, divider)), run_time=0.8)

        # ================= Farquharson's warning; the new bridge =================
        prof2 = cameo("modern", 0.6)
        pn2 = serif("F. B. Farquharson", 20, INK).next_to(prof2, DOWN, buff=0.1)
        pw2 = VGroup(prof2, pn2).move_to([-4.6, 0.9, 0])
        warn = ink_card(VGroup(note("He had seen the twist on his models, and said that if it ever", 18, INK),
                               note("happened on the real bridge, it would be the end of the bridge.", 18, INK),
                               note("(paraphrased from his recollection)", 14)).arrange(DOWN, buff=0.08)).move_to([1.3, 0.9, 0])
        line("Farquharson had seen this twist on his models. He had said that if it ever happened on the real bridge, it would be the end of the bridge.",
             FadeIn(pw2, shift=UP * 0.1), FadeIn(warn), run_time=1.0)
        self.vo_wait()
        self.play(FadeOut(pw2), FadeOut(warn), run_time=0.6)

        old = h_section(2.8, 0.55).move_to([-3.3, 0.9, 0])
        old_l = VGroup(serif("1940", 26, INK), note("solid 8-ft girders: a wall to the wind", 16)).arrange(
            DOWN, buff=0.08).next_to(old, DOWN, buff=0.75)
        new = truss_section(2.8, 1.9).move_to([3.3, 0.9, 0])
        new_l = VGroup(serif("1950", 26, INK), note("open 33-ft trusses, grates in the roadway", 16)).arrange(
            DOWN, buff=0.08).next_to(new, DOWN, buff=0.2).set_y(old_l.get_y())
        sch = note("cross-sections, schematic", 14).move_to([0, -2.5, 0])
        line("The new bridge, opened in 1950, used deep, open trusses and grates in the roadway, so the wind passes through instead of swirling around a solid wall.",
             FadeIn(old), FadeIn(old_l), FadeIn(sch), run_time=0.9)
        self.play(FadeIn(new, lag_ratio=0.1), FadeIn(new_l), run_time=1.2)
        thru = VGroup(*[Arrow([1.3, y, 0], [5.4, y, 0], buff=0, color=BLUE_INK, stroke_width=2.5, tip_length=0.15,
                              stroke_opacity=0.7) for y in (0.35, 0.95, 1.5)])
        self.play(LaggedStart(*[GrowArrow(a) for a in thru], lag_ratio=0.2), run_time=1.2)
        self.vo_wait()
        self.play(FadeOut(VGroup(old, old_l, new, new_l, thru, sch)), run_time=0.6)

        tunnel = VGroup(Rectangle(width=4.6, height=1.8, stroke_color=INK, stroke_width=2.5),
                        h_section(1.4, 0.3).move_to([0.2, 0, 0]),
                        *[Line([-2.1 + 0.0, y, 0], [-1.1, y, 0], color=BLUE_INK, stroke_width=2) for y in (-0.5, 0, 0.5)],
                        note("bridge model in a wind tunnel", 16).shift(DOWN * 1.2)).move_to([-3.0, 0.2, 0])
        wing = VGroup(smooth([(-1.6, 0), (-1.2, 0.22), (0, 0.3), (1.6, 0.04), (0, -0.08), (-1.2, -0.1), (-1.6, 0)],
                             INK, 2.5),
                      note("aircraft wings: tested against flutter too", 16).shift(DOWN * 0.75)).move_to([3.2, 0.2, 0])
        line("Since then, testing bridge models in wind tunnels has become standard practice. And aircraft designers guard against the same flutter in every wing.",
             FadeIn(tunnel), run_time=0.9)
        self.play(FadeIn(wing), run_time=0.9)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tunnel, wing)), run_time=0.8)

        # ================= try it yourself =================
        tiy = serif("Try it yourself", 34, RED_INK).move_to([0, 3.1, 0])
        strip = Rectangle(width=4.0, height=0.5, stroke_color=INK, stroke_width=2, fill_color=PAPER_DARK,
                          fill_opacity=1).move_to([-3.0, 1.6, 0])
        folds = VGroup(DashedLine(strip.get_corner(UL) + DOWN * 0.1, strip.get_corner(UR) + DOWN * 0.1, color=RED_INK,
                                  stroke_width=1.5),
                       DashedLine(strip.get_corner(DL) + UP * 0.1, strip.get_corner(DR) + UP * 0.1, color=RED_INK,
                                  stroke_width=1.5))
        len_l = note("card strip ≈ 40 cm", 16).next_to(strip, UP, buff=0.12)
        fold_l = note("fold both long edges down", 16).next_to(strip, DOWN, buff=0.12)
        xsec = h_section(1.5, 0.35).move_to([-3.0, -0.1, 0])
        xsec_l = note("end view: like Gertie's girders", 15).next_to(xsec, DOWN, buff=0.2)
        line("Try it yourself. Cut a strip of card about forty centimetres long, and fold its long edges down, like Gertie's solid girders.",
             FadeIn(tiy), FadeIn(strip), FadeIn(len_l), run_time=0.9)
        self.play(Create(folds), FadeIn(fold_l), run_time=0.8)
        self.play(FadeIn(xsec), FadeIn(xsec_l), run_time=0.7)
        self.vo_wait()

        # rig: side view with threads and a fan
        RX, RY = 2.7, 0.2
        post = VGroup(*[Line([RX + sx * 2.3, 2.3, 0], [RX + sx * 2.3, -0.6, 0], color=INK, stroke_width=4)
                        for sx in (-1, 1)])
        bar = Line([RX - 2.5, 2.3, 0], [RX + 2.5, 2.3, 0], color=INK, stroke_width=4)
        rig_twist = ValueTracker(0.0)

        def build_card():
            th = rig_twist.get_value() * np.sin(TAU * clock.get_value() / 1.2)
            xs_ = np.linspace(RX - 1.9, RX + 1.9, 41)

            def p(x, s):
                tt = th * np.sin(PI * (x - RX + 1.9) / 3.8)
                return np.array([x + 0.25 * s * np.cos(tt), RY + s * np.sin(tt) + 0.4 * s * np.cos(tt), 0])

            near = [p(x, -0.42) for x in xs_]
            far = [p(x, 0.42) for x in xs_]
            surf = Polygon(*near, *far[::-1], stroke_color=INK, stroke_width=1.5, fill_color=PAPER_DARK, fill_opacity=1)
            threads = VGroup(*[Line([x, 2.3, 0], p(x, s), color=SEPIA, stroke_width=1.2)
                               for x in (RX - 1.9, RX + 1.9) for s in (-0.42, 0.42)])
            return VGroup(threads, surf)

        card = always_redraw(build_card)
        fan = fan_icon([RX, -1.35], 0.42)
        fan_l = note("fan aimed at the deck's long edge", 15).next_to(fan, LEFT, buff=0.2).shift(UP * 0.2)
        line("Hang it by its ends from loops of thread, so it can twist, and aim a fan at its edge.",
             FadeIn(post), FadeIn(bar), FadeIn(card), run_time=0.9)
        self.play(FadeIn(fan), FadeIn(fan_l), run_time=0.7)
        self.vo_wait()
        grow_l = note("watch for a twist that grows", 17, RED_INK).move_to([RX, 1.75, 0])
        line("Turn the fan up slowly, and watch for a twist that grows on its own.", FadeIn(grow_l), run_time=0.6)
        self.play(rig_twist.animate.set_value(55 * DEGREES), run_time=3.5, rate_func=linear)
        self.vo_wait()

        strip2 = Rectangle(width=4.0, height=0.5, stroke_color=INK, stroke_width=2, fill_color=PAPER_DARK,
                           fill_opacity=1).move_to([-3.0, 1.6, 0])
        holes = VGroup(*[Rectangle(width=0.35, height=0.18, stroke_color=INK, stroke_width=1.2, fill_color=PAPER,
                                   fill_opacity=1).move_to([-4.6 + 0.55 * i, 1.6 + sy * 0.25, 0])
                         for i in range(7) for sy in (-1, 1)])
        win_l = note("deck 2: windows cut in the sides", 16).next_to(strip2, UP, buff=0.25)
        win_l2 = note("the air can pass through", 16).next_to(strip2, DOWN, buff=0.25)
        line("Then make a second deck with windows cut in its sides, and see whether it stays steadier.",
             FadeOut(VGroup(strip, folds, len_l, fold_l)), FadeIn(strip2), FadeIn(holes), FadeIn(win_l),
             FadeIn(win_l2), run_time=0.9)
        self.vo_wait()
        safe = ink_card(note("keep fingers and thread away from the fan blades · a small desk fan is enough", 16, INK)).move_to(
            [0, -2.45, 0])
        line("Keep fingers and thread well away from the fan blades.", FadeIn(safe), run_time=0.7)
        self.vo_wait()
        card.clear_updaters()
        self.play(clear(), FadeOut(VGroup(tiy, strip2, holes, win_l, win_l2, xsec, xsec_l, post, bar, card, fan, fan_l,
                                          grow_l, safe)), run_time=0.8)

        # ================= close =================
        last = VGroup(serif("A steady wind, a flat deck,", 36, INK),
                      serif("and a bridge that pushed itself apart.", 36, RED_INK)).arrange(DOWN, buff=0.2).move_to(
            [0, 0.6, 0])
        line("A steady wind, a flat deck, and a bridge that pushed itself apart. Failure taught engineers to listen to the air.",
             FadeIn(last, lag_ratio=0.2), run_time=1.2)
        self.vo_wait()
        self.play(clear(), FadeOut(last), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after Henry Petroski, To Engineer Is Human (1985) · sources in the episode notes", 17),
                     note("facts checked against WSDOT's Tacoma Narrows Bridge history, APS News, STRUCTURE and ASCE", 17),
                     note("silhouettes are stylised, not likenesses · bridge drawings are schematic · "
                          "animated with Manim · synthetic narration", 15)).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(1.6)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)
