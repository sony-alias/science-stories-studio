"""I040 Time Is Position, a Science Stories episode.

After D. Sobel, Longitude (1995). Script and sources: episodes/I040_script.md

Render:  manim -qh --frame_rate 30 episodes/I040_time_is_position.py TimeIsPosition
Then:    scripts/finish_video.sh media/videos/I040_time_is_position/1080p30/TimeIsPosition.mp4 out/I040_time_is_position.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

SEA = "#6d8299"
GOLD = "#c99a2e"


def note(text, size=17, color=FADED):
    return serif(text, size, color, italic=True)


def P(x, y):
    return np.array([x, y, 0.0])


# ---------- the numbers, computed and checked at render time ----------
DEG_PER_HOUR = 360 / 24
MIN_PER_DEG = 60 / DEG_PER_HOUR
assert DEG_PER_HOUR == 15 and MIN_PER_DEG == 4
HOURS_BEHIND = 3
SHIP_LON = -HOURS_BEHIND * DEG_PER_HOUR
assert SHIP_LON == -45
KM_PER_DEG = 2 * np.pi * 6371 / 360
NMI_PER_DEG = KM_PER_DEG / 1.852
assert abs(NMI_PER_DEG - 60) < 0.2                      # 60.0 nautical miles per degree at the equator
PRIZE_DEG = 0.5
PRIZE_MIN = PRIZE_DEG * MIN_PER_DEG
assert PRIZE_MIN == 2
VOYAGE_DAYS = 42
DRIFT = PRIZE_MIN * 60 / VOYAGE_DAYS
assert 2.8 < DRIFT < 2.9                                # "about three seconds a day"
IST_MERIDIAN = 5.5 * DEG_PER_HOUR
assert IST_MERIDIAN == 82.5
EX_LATE_MIN = 20                                        # worked example: corrected noon at 12:20 IST
EX_LON = IST_MERIDIAN - EX_LATE_MIN / MIN_PER_DEG
assert EX_LON == 77.5


# ---------- small drawings ----------
def ship(scale=1.0, color=INK):
    hull = Polygon(P(-0.5, 0), P(0.5, 0), P(0.36, -0.16), P(-0.38, -0.16), fill_color=color, fill_opacity=1,
                   stroke_width=0)
    mast = Line(P(0, 0), P(0, 0.62), color=color, stroke_width=2)
    s1 = Polygon(P(0.03, 0.58), P(0.03, 0.12), P(0.34, 0.14), fill_color=PAPER, fill_opacity=1, stroke_color=color,
                 stroke_width=1.5)
    s2 = Polygon(P(-0.03, 0.5), P(-0.03, 0.12), P(-0.3, 0.14), fill_color=PAPER, fill_opacity=1, stroke_color=color,
                 stroke_width=1.5)
    return VGroup(hull, mast, s1, s2).scale(scale)


def rock(x, y, s=0.18):
    return Polygon(P(x - s, y - 0.05), P(x - s * 0.4, y + s * 0.8), P(x + s * 0.3, y + s * 0.5), P(x + s, y - 0.05),
                   fill_color=INK, fill_opacity=0.85, stroke_width=0)


def clock_face(r=0.7, label=None, hours_fn=None):
    face = Circle(radius=r, color=INK, stroke_width=3, fill_color=PAPER, fill_opacity=1)
    ticks = VGroup(*[Line(P(0, r * 0.82), P(0, r * 0.95), color=INK, stroke_width=2 if i % 3 else 3)
                     .rotate(-i * TAU / 12, about_point=ORIGIN) for i in range(12)])
    g = VGroup(face, ticks)
    if label:
        g.add(note(label, 15, INK).next_to(face, DOWN, buff=0.12))
    return g


def hands(center_fn, r, hours_fn):
    def make():
        h = hours_fn()
        c = center_fn()
        a_h = -TAU * (h % 12) / 12
        a_m = -TAU * (h % 1)
        hh = Line(c, c + 0.5 * r * np.array([np.sin(-a_h), np.cos(a_h), 0]), color=INK, stroke_width=5)
        mm = Line(c, c + 0.78 * r * np.array([np.sin(-a_m), np.cos(a_m), 0]), color=RED_INK, stroke_width=3)
        return VGroup(hh, mm, Dot(c, radius=0.05, color=INK))
    return always_redraw(make)


def sun_glyph(r=0.3):
    core = Circle(radius=r, fill_color=GOLD, fill_opacity=1, stroke_color=INK, stroke_width=1.5)
    rays = VGroup(*[Line(P(0, r * 1.25), P(0, r * 1.7), color=GOLD, stroke_width=3).rotate(i * TAU / 12,
                                                                                         about_point=ORIGIN)
                    for i in range(12)])
    return VGroup(rays, core)


def satellite(scale=1.0):
    body = Square(0.3, fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=1.5)
    p1 = Rectangle(width=0.5, height=0.18, fill_color=BLUE_INK, fill_opacity=1, stroke_width=0).next_to(body, LEFT, 0.05)
    p2 = p1.copy().next_to(body, RIGHT, 0.05)
    return VGroup(p1, p2, body).scale(scale)


class TimeIsPosition(NarratedScene):
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
        title = serif("Time Is Position", 56).next_to(orn1, DOWN, buff=0.35)
        sub = serif("Why a clock can tell a ship where it is", 26, FADED, italic=True).next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("story after D. Sobel, Longitude (1995)", 16).move_to([0, -2.6, 0])
        self.vo("Science Stories. Time is position.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.wait(0.5)
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= 1707 =================
        place = spaced("22 October 1707 · evening", 18, SEPIA).move_to(P(0, 3.05))
        cal = note("Julian calendar, as used in Britain then", 13).next_to(place, DOWN, buff=0.08)
        shov = cameo("wig", 0.62).move_to(P(-5.0, 1.0))
        shov_l = VGroup(serif("Sir Cloudesley Shovell", 19, INK), note("admiral, d. 1707", 14)
                        ).arrange(DOWN, buff=0.04).next_to(shov, DOWN, buff=0.12)
        sil_n = note("silhouette stylised, not a likeness", 12).next_to(shov_l, DOWN, buff=0.08)
        # stylised sea chart: Cornwall's tip at right, Scilly at left
        coast = VMobject(fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=2).set_points_smoothly([
            P(6.6, 2.4), P(4.6, 2.0), P(3.4, 1.3), P(2.7, 0.75), P(2.4, 0.2), P(2.9, -0.15), P(3.9, -0.3),
            P(5.2, 0.1), P(6.6, 0.3), P(6.6, 2.4)])
        corn = note("Cornwall", 15, INK).move_to(P(4.9, 1.0))
        scilly = VGroup(*[Circle(radius=r, fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=1.5)
                          .move_to(P(x, y)) for x, y, r in [(0.1, 0.3, 0.22), (0.55, 0.05, 0.14), (-0.3, 0.0, 0.12),
                                                            (0.35, 0.55, 0.1)]])
        rocks = VGroup(rock(-0.75, -0.45), rock(-0.45, -0.7, 0.14), rock(-1.0, -0.25, 0.12))
        sc_l = note("Isles of Scilly", 15, INK).move_to(P(0.15, 1.05))
        chart_n = note("stylised chart, not to scale", 12).move_to(P(4.6, -2.45))
        fleet = VGroup(*[ship(0.42).move_to(P(-4.0 + dx, -1.9 + dy)) for dx, dy in
                         [(0, 0), (0.7, 0.35), (1.3, -0.15), (0.4, -0.6), (1.6, 0.5)]])
        line("The evening of the twenty-second of October, 1707. Admiral Sir Cloudesley Shovell is bringing his fleet "
             "home from Gibraltar.", FadeIn(place), FadeIn(cal), FadeIn(shov), FadeIn(shov_l), FadeIn(sil_n),
             run_time=1.0)
        self.play(FadeIn(coast), FadeIn(corn), FadeIn(scilly), FadeIn(sc_l), FadeIn(chart_n), run_time=1.0)
        self.play(FadeIn(fleet, lag_ratio=0.2), run_time=1.0)
        self.play(fleet.animate.shift(RIGHT * 2.2 + UP * 1.0), run_time=3.0, rate_func=linear)
        self.vo_wait()
        dark = Rectangle(width=14.2, height=8.0, fill_color="#1a1410", fill_opacity=0, stroke_width=0)
        self.add(dark)
        line("In the dark, off the Isles of Scilly, his ships strike the rocks.",
             dark.animate.set_fill(opacity=0.28), FadeIn(rocks), run_time=1.0)
        self.play(fleet.animate.shift(RIGHT * 0.9 + UP * 0.55), run_time=1.6, rate_func=linear)
        crash = VGroup(*[Cross(scale_factor=0.12, stroke_color=RED_INK, stroke_width=5).move_to(s.get_center())
                         for s in fleet[:4]])
        self.play(FadeIn(crash), run_time=0.4)
        self.vo_wait()
        toll = ink_card(VGroup(serif("4 ships lost", 24, INK),
                               serif("more than 1,400 men", 24, RED_INK),
                               note("estimates run from 1,400 to 2,000", 14)).arrange(DOWN, buff=0.08),
                        pad=0.2).move_to(P(4.3, -1.4))
        line("Four go down. More than fourteen hundred men are lost, the admiral among them.",
             *[s.animate.shift(DOWN * 0.25).set_opacity(0.15) for s in fleet[:4]], FadeOut(crash),
             FadeIn(toll), run_time=1.6)
        self.vo_wait()
        self.play(FadeOut(dark), run_time=0.5)

        # myth vs history
        myth = ink_card(VGroup(note("the story often told", 15),
                               serif("They did not know their longitude.", 22, INK)).arrange(DOWN, buff=0.08),
                        pad=0.2).move_to(P(0, 2.0))
        line("The story often told is that the navigators did not know their longitude.",
             FadeOut(VGroup(toll, fleet, rocks, coast, corn, scilly, sc_l, chart_n)),
             FadeIn(myth, shift=DOWN * 0.1), run_time=1.0)
        self.vo_wait()
        hist = ink_card(VGroup(note("historians today", 15),
                               serif("Faulty charts, and a mistake in latitude.", 22, INK)).arrange(DOWN, buff=0.08),
                        pad=0.2).move_to(P(0, 0.2))
        real = serif("But the longitude problem was real.", 26, RED_INK).move_to(P(0, -1.5))
        line("Historians now point more to faulty charts and a mistake in latitude. But the longitude problem itself "
             "was real.", myth.animate.set_opacity(0.45), FadeIn(hist, shift=UP * 0.1), run_time=1.0)
        self.wait(2.0)
        self.play(FadeIn(real), run_time=0.7)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(myth, hist, real, place, cal, shov, shov_l, sil_n)), run_time=0.7)

        # ================= latitude easy, longitude hard =================
        E = P(-3.2, 0.2)
        RE = 1.8
        earth = Circle(radius=RE, color=INK, stroke_width=3, fill_color=PAPER_DARK, fill_opacity=1).move_to(E)
        eq = DashedLine(E + LEFT * RE, E + RIGHT * RE, color=FADED, stroke_width=1.5)
        lat = 40 * DEGREES
        obs = E + RE * np.array([np.cos(lat), np.sin(lat), 0])
        obs_d = Dot(obs, radius=0.07, color=RED_INK)
        horiz = Line(obs - 1.1 * np.array([-np.sin(lat), np.cos(lat), 0]),
                     obs + 1.1 * np.array([-np.sin(lat), np.cos(lat), 0]), color=INK, stroke_width=2)
        rays = VGroup(*[Arrow(P(1.6, y), P(-0.4, y), color=GOLD, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.08)
                        for y in (1.7, 0.9, 0.1)])
        sun_l = note("noon sunlight (equinox)", 15, INK).move_to(P(0.7, 2.25))
        radius_l = Line(E, obs, color=FADED, stroke_width=1.5)
        ang = Angle(Line(E, E + RIGHT), Line(E, obs), radius=0.5, color=RED_INK)
        ang_l = MathTex(r"\varphi", font_size=32, color=RED_INK).move_to(E + 0.75 * np.array([np.cos(lat / 2), np.sin(lat / 2), 0]))
        alt_ang = Angle(horiz, Line(obs, obs + RIGHT), radius=0.45, quadrant=(-1, 1), color=BLUE_INK)
        rule = VGroup(serif("Latitude: easy", 26, INK),
                      MathTex(r"\text{noon sun height} = 90^\circ - \varphi", font_size=32, color=INK),
                      note("at the equinox; tables correct it for the date", 14)).arrange(DOWN, buff=0.15).move_to(P(3.6, 1.2))
        line("Latitude was easy. Measure how high the noon sun stands, and you know how far north you are.",
             FadeIn(earth), FadeIn(eq), FadeIn(rays), FadeIn(sun_l), run_time=1.0)
        self.play(FadeIn(obs_d), Create(horiz), Create(radius_l), Create(ang), FadeIn(ang_l), run_time=1.0)
        self.play(Create(alt_ang), FadeIn(rule), run_time=1.0)
        self.vo_wait()
        # longitude: a circle of latitude, top view
        ring = Circle(radius=1.9, color=INK, stroke_width=3).move_to(P(-3.2, 0.2))
        pole = Dot(ring.get_center(), radius=0.06, color=INK)
        pole_l = note("North Pole, seen from above", 14).next_to(pole, DOWN, buff=0.15)
        spots = VGroup(*[Dot(ring.get_center() + 1.9 * np.array([np.cos(a), np.sin(a), 0]), radius=0.08,
                             color=RED_INK) for a in np.linspace(0, TAU, 8, endpoint=False)])
        rule2 = VGroup(serif("Longitude: hard", 26, INK),
                       note("every place on a circle of latitude", 16, INK),
                       note("sees the same sky, only at a different time", 16, INK)).arrange(DOWN, buff=0.12).move_to(P(3.6, -1.0))
        line("East and west were different. Every point on a circle of latitude sees the same sky, just at a "
             "different time.", FadeOut(VGroup(earth, eq, obs_d, horiz, radius_l, ang, ang_l, alt_ang, rays, sun_l)),
             rule.animate.set_opacity(0.5), FadeIn(ring), FadeIn(pole), FadeIn(pole_l), run_time=1.0)
        self.play(FadeIn(spots, lag_ratio=0.15), FadeIn(rule2), run_time=1.2)
        self.play(Rotate(spots, angle=TAU / 8, about_point=ring.get_center()), run_time=2.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(ring, pole, pole_l, spots, rule, rule2)), run_time=0.6)

        # ================= the Act =================
        act_t = VGroup(spaced("9 July 1714", 20, SEPIA),
                       serif("An Act for providing a publick reward", 26, INK),
                       note("for such person or persons as shall discover the longitude at sea · royal assent of Queen Anne", 15)
                       ).arrange(DOWN, buff=0.12).move_to(P(0, 2.4))
        whis = note("after lobbying by mathematicians such as William Whiston", 16, INK).next_to(act_t, DOWN, buff=0.2)
        rows = [("within 1°", "60 miles", "£10,000"), ("within ⅔°", "40 miles", "£15,000"),
                ("within ½°", "30 miles", "£20,000")]
        table = VGroup(*[VGroup(serif(a, 24, INK), serif(b, 24, FADED), serif(c, 24, RED_INK if i == 2 else INK))
                         .arrange(RIGHT, buff=0.9) for i, (a, b, c) in enumerate(rows)]).arrange(DOWN, buff=0.22)
        for r in table:
            r[0].set_x(-2.6)
            r[1].set_x(0.0)
            r[2].set_x(2.6)
        table.move_to(P(0, -0.6))
        tab_n = note("“geographical miles”, i.e. nautical miles · from the text of the Act", 14).next_to(table, DOWN, buff=0.25)
        line("On the ninth of July, 1714, after lobbying by mathematicians like William Whiston, Britain offered up "
             "to twenty thousand pounds for a way to find longitude at sea.", FadeIn(act_t, lag_ratio=0.2),
             run_time=1.0)
        self.play(FadeIn(whis), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in table], lag_ratio=0.35), FadeIn(tab_n),
                  run_time=1.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(act_t, whis, table, tab_n)), run_time=0.6)

        # ================= Gemma Frisius =================
        gem = cameo("plain", 0.75).move_to(P(-4.3, 0.8))
        gem_l = VGroup(serif("Gemma Frisius", 22, INK), note("1508 – 1555 · from Friesland, worked at Leuven", 14),
                       note("silhouette stylised", 12)).arrange(DOWN, buff=0.05).next_to(gem, DOWN, buff=0.15)
        book = ink_card(VGroup(spaced("1530", 18, SEPIA),
                               serif("De Principiis Astronomiae", 22, INK, italic=True),
                               serif("Cosmographicae", 22, INK, italic=True),
                               note("chapter 19: longitude by a clock", 15)).arrange(DOWN, buff=0.08),
                        pad=0.25).move_to(P(1.8, 1.3))
        line("The key idea was already old. In 1530 a young scholar from Friesland, Gemma Frisius, aged twenty-one, "
             "wrote it down.", FadeIn(gem), FadeIn(gem_l), run_time=1.0)
        self.play(FadeIn(book, shift=LEFT * 0.1), run_time=0.9)
        self.vo_wait()
        home_t = ValueTracker(15.0)
        c1 = clock_face(0.65, "clock set to home time").move_to(P(0.2, -1.3))
        c2 = clock_face(0.65, "local time from the sun").move_to(P(3.4, -1.3))
        h1 = hands(lambda: c1[0].get_center(), 0.65, lambda: home_t.get_value())
        h2 = hands(lambda: c2[0].get_center(), 0.65, lambda: 12.0)
        s_sun = sun_glyph(0.16).next_to(c2[0], UP, buff=0.12)
        vs = MathTex(r"\neq", font_size=44, color=RED_INK).move_to(P(1.8, -1.2))
        line("Carry a clock set to the time at home. Wherever you are, compare it with the local time from the sun.",
             FadeIn(c1), FadeIn(h1), run_time=0.9)
        self.play(FadeIn(c2), FadeIn(h2), FadeIn(s_sun), run_time=0.9)
        self.play(FadeIn(vs), run_time=0.5)
        self.vo_wait()
        h1.clear_updaters()
        h2.clear_updaters()
        self.play(clear(), FadeOut(VGroup(gem, gem_l, book, c1, c2, h1, h2, s_sun, vs)), run_time=0.6)

        # ================= the turning Earth =================
        C = P(-2.6, 0.15)
        R = 2.35
        t = ValueTracker(0.0)              # hours since noon at home
        disc = Circle(radius=R, fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to(C)
        night = Sector(radius=R, angle=PI, start_angle=PI / 2, fill_color=INK, fill_opacity=0.18, stroke_width=0,
                       arc_center=C)
        sun = sun_glyph(0.3).move_to(P(4.6, 0.15))
        sunrays = VGroup(*[Arrow(P(3.9, y), P(C[0] + R + 0.85, y), buff=0, color=GOLD, stroke_width=2.5,
                                 max_tip_length_to_length_ratio=0.08) for y in (0.95, 0.15, -0.65)])
        noon_line = DashedLine(C, C + RIGHT * (R + 0.35), color=GOLD, stroke_width=4)
        noon_l = note("noon: the meridian facing the sun", 15, INK).move_to(P(C[0] + R + 0.2, 2.75))

        def mer_angle(lon):
            return (lon + DEG_PER_HOUR * t.get_value()) * DEGREES

        def meridians():
            g = VGroup()
            for lon in range(0, 360, 15):
                a = mer_angle(lon)
                g.add(Line(C, C + R * np.array([np.cos(a), np.sin(a), 0]), color=INK, stroke_width=0.8,
                           stroke_opacity=0.45))
            return g

        mers = always_redraw(meridians)

        def marker(lon, color, label):
            def make():
                a = mer_angle(lon)
                d = np.array([np.cos(a), np.sin(a), 0])
                ln = Line(C, C + R * d, color=color, stroke_width=4)
                dot = Dot(C + R * d, radius=0.1, color=color)
                lab = serif(label, 18, color).move_to(C + (R + 0.45) * d)
                return VGroup(ln, dot, lab)
            return always_redraw(make)

        home_m = marker(0, BLUE_INK, "home")
        ship_m = marker(SHIP_LON, RED_INK, "ship")
        pole = Dot(C, radius=0.06, color=INK)
        view = note("Earth seen from above the North Pole · turning west to east", 14).move_to(P(C[0], -2.6))
        line("Here is why that works. The Earth turns once, three hundred and sixty degrees, in twenty-four hours.",
             FadeIn(disc), FadeIn(night), FadeIn(mers), FadeIn(pole), FadeIn(view), FadeIn(sun), FadeIn(sunrays),
             run_time=1.0)
        self.play(FadeIn(noon_line), FadeIn(noon_l), run_time=0.6)
        self.play(t.animate.set_value(24), run_time=3.5, rate_func=linear)
        t.set_value(0)
        self.vo_wait()
        rate = VGroup(MathTex(r"\frac{360^\circ}{24\ \text{h}} = 15^\circ \text{ per hour}", font_size=34, color=INK),
                      MathTex(r"1^\circ = 4 \text{ minutes}", font_size=34, color=RED_INK)
                      ).arrange(DOWN, buff=0.3).move_to(P(3.9, -1.75))
        line("That is fifteen degrees every hour, or one degree every four minutes.", Write(rate[0]), run_time=1.2)
        self.play(FadeIn(rate[1], shift=UP * 0.1), run_time=0.6)
        self.vo_wait()
        line("So noon sweeps around the world from east to west. Each meridian gets its noon a little later.",
             FadeIn(home_m), FadeIn(ship_m), rate.animate.set_opacity(0.4), run_time=0.9)
        self.play(t.animate.set_value(1.5), run_time=2.0, rate_func=smooth)
        self.play(t.animate.set_value(0), run_time=1.2)
        self.vo_wait()
        # ship's clock
        sc = clock_face(0.6, "ship's clock: home time").move_to(P(3.9, 1.35))
        sh = hands(lambda: sc[0].get_center(), 0.6, lambda: 12 + t.get_value())
        line("Suppose the sun is highest at your ship, and your clock from home says three in the afternoon.",
             FadeOut(rate), FadeIn(sc), FadeIn(sh), run_time=0.9)
        self.play(t.animate.set_value(HOURS_BEHIND), run_time=3.2, rate_func=smooth)
        self.vo_wait()
        calc = VGroup(MathTex(r"3\ \text{h} \times 15^\circ/\text{h} = 45^\circ", font_size=36, color=INK),
                      serif("west of home", 24, RED_INK)).arrange(DOWN, buff=0.15).move_to(P(3.9, -1.5))
        wedge = always_redraw(lambda: Sector(radius=1.0, angle=-SHIP_LON * DEGREES, start_angle=mer_angle(SHIP_LON),
                                             fill_color=RED_INK, fill_opacity=0.3, stroke_width=0, arc_center=C))
        line("Noon at home was three hours ago. Three hours times fifteen degrees: you are forty-five degrees west "
             "of home.", FadeIn(wedge), Write(calc[0]), run_time=1.2)
        self.play(FadeIn(calc[1]), run_time=0.6)
        self.vo_wait()
        big = serif("time difference  →  position", 30, RED_INK).move_to(P(3.9, -2.45))
        line("Time difference becomes position.", FadeIn(big, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        self.wait(0.4)
        for m in (mers, home_m, ship_m, wedge, sh):
            m.clear_updaters()
        self.play(clear(), FadeOut(VGroup(disc, night, mers, home_m, ship_m, wedge, pole, view, sun, sunrays,
                                          noon_line, noon_l, sc, sh, calc, big)), run_time=0.7)

        # ================= how good must the clock be =================
        nl = NumberLine(x_range=[0, 60, 10], length=9.0, color=INK, include_numbers=True, font_size=24,
                        decimal_number_config={"color": INK, "num_decimal_places": 0}).move_to(P(0, 1.6))
        nl_l = note("nautical miles along the equator", 15).next_to(nl, DOWN, buff=0.45)
        one = Brace(nl, UP, color=INK)
        one_l = MathTex(r"1^\circ \approx 60\ \text{nautical miles}", font_size=32, color=INK).next_to(one, UP, buff=0.1)
        line("But how good must the clock be? At the equator, one degree of longitude is about sixty nautical miles.",
             Create(nl), FadeIn(nl_l), run_time=1.0)
        self.play(GrowFromCenter(one), FadeIn(one_l), run_time=0.8)
        self.vo_wait()
        half = Line(nl.n2p(0), nl.n2p(30), color=RED_INK, stroke_width=10).shift(DOWN * 0.0)
        half_l = VGroup(MathTex(r"\tfrac12^\circ = 30\ \text{miles}", font_size=34, color=RED_INK),
                        MathTex(r"= 2\ \text{minutes of clock time}", font_size=34, color=RED_INK)
                        ).arrange(RIGHT, buff=0.2).move_to(P(0, -0.1))
        line("The top prize asked for half a degree: thirty miles, which is just two minutes of clock time.",
             Create(half), FadeIn(half_l[0]), run_time=1.0)
        self.play(FadeIn(half_l[1]), run_time=0.6)
        self.vo_wait()
        drift = VGroup(MathTex(r"\frac{120\ \text{s}}{42\ \text{days}} \approx 3\ \text{seconds a day}",
                               font_size=36, color=INK),
                       note("a six-week voyage, as an example of scale", 14)).arrange(DOWN, buff=0.1).move_to(P(0, -1.45))
        line("Spread two minutes over a six-week voyage, and the clock may drift by only about three seconds a day.",
             Write(drift[0]), run_time=1.2)
        self.play(FadeIn(drift[1]), run_time=0.5)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(nl, nl_l, one, one_l, half, half_l, drift)), run_time=0.6)

        # ================= the catch =================
        quote = ink_card(VGroup(serif("“… it must be a very finely made clock", 24, INK, italic=True),
                                serif("which does not vary with change of air.”", 24, INK, italic=True),
                                note("Gemma Frisius, 1530 · English translation quoted by MacTutor", 14)
                                ).arrange(DOWN, buff=0.1), pad=0.3).move_to(P(0, 1.8))
        line("Gemma saw the catch. It must be, he wrote, a very finely made clock which does not vary with change of "
             "air.", FadeIn(quote, shift=DOWN * 0.1), run_time=1.0)
        self.vo_wait()
        roll = ValueTracker(0.0)
        deck_c = P(-2.2, -1.5)

        def rocking():
            s = roll.get_value()
            tilt = 0.18 * np.sin(1.3 * s)
            g = VGroup()
            hull = Polygon(P(-4.2, -0.7), P(-0.2, -0.7), P(-0.7, -1.4), P(-3.8, -1.4), fill_color=SEPIA,
                           fill_opacity=0.8, stroke_color=INK, stroke_width=2)
            box = Rectangle(width=1.5, height=1.6, stroke_color=INK, stroke_width=2, fill_color=PAPER,
                            fill_opacity=1).move_to(P(-2.2, 0.1))
            face = Circle(radius=0.2, stroke_color=INK, stroke_width=1.5).move_to(box.get_top() + DOWN * 0.3)
            g.add(hull, box, face)
            g.rotate(tilt, about_point=deck_c)
            pivot = face.get_center()
            swing = tilt * 1.5 + 0.22 * np.sin(2.1 * s) + 0.1 * np.sin(3.7 * s + 1)
            bob = pivot + 1.0 * np.array([np.sin(swing), -np.cos(swing), 0])
            g.add(Line(pivot, bob, color=INK, stroke_width=2), Dot(bob, radius=0.11, color=RED_INK))
            return g

        rock_ship = always_redraw(rocking)
        waves = VGroup(*[FunctionGraph(lambda x, k=k: -2.35 + 0.08 * np.sin(2.2 * x + k), x_range=[-5.8, 1.4],
                                       color=SEA, stroke_width=2) for k in (0, 1.5)])
        waves[1].shift(DOWN * 0.15)
        q_n = note("drawn qualitatively", 13).move_to(P(3.6, -2.3))
        line("On a rolling ship, the best clocks of the day, pendulum clocks, were useless.",
             FadeIn(rock_ship), FadeIn(waves), FadeIn(q_n), quote.animate.set_opacity(0.5), run_time=1.0)
        self.play(roll.animate.set_value(9), run_time=4.0, rate_func=linear)
        self.vo_wait()
        moral = VGroup(serif("The idea was simple.", 28, INK), serif("The machine was the problem.", 28, RED_INK)
                       ).arrange(DOWN, buff=0.15).move_to(P(3.4, -0.4))
        assert moral.get_right()[0] < 6.3
        line("The idea was simple. The machine was the problem.", roll.animate.set_value(13), FadeIn(moral[0]),
             run_time=1.2, )
        self.play(FadeIn(moral[1]), roll.animate.set_value(15), run_time=1.0, rate_func=linear)
        self.vo_wait()
        rock_ship.clear_updaters()
        self.play(clear(), FadeOut(VGroup(quote, rock_ship, waves, q_n, moral)), run_time=0.6)

        # ================= Harrison teaser =================
        har = cameo("plain", 0.75).move_to(P(-2.6, 0.7))
        har_l = VGroup(serif("John Harrison", 24, INK), note("1693 – 1776 · carpenter, self-taught clockmaker", 15),
                       note("silhouette stylised", 12)).arrange(DOWN, buff=0.05).next_to(har, DOWN, buff=0.15)
        nxt = ink_card(VGroup(spaced("Next", 16, SEPIA), serif("Harrison's clocks, H1 to H4", 26, INK)
                              ).arrange(DOWN, buff=0.1), pad=0.25).move_to(P(2.8, 0.7))
        line("A carpenter who had taught himself clockmaking, John Harrison, would give decades of his life to that "
             "machine. That is our next story.", FadeIn(har), FadeIn(har_l), run_time=1.0)
        self.play(FadeIn(nxt, shift=LEFT * 0.1), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(har, har_l, nxt)), run_time=0.6)

        # ================= GPS =================
        ge = Circle(radius=1.4, fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to(P(0, -0.6))
        rx = Dot(ge.get_top(), radius=0.09, color=RED_INK)
        rx_l = note("receiver", 14, RED_INK).next_to(rx, DOWN, buff=0.15)
        sats = VGroup(*[satellite(0.8).move_to(p) for p in (P(-4.2, 2.3), P(0.3, 3.0), P(4.3, 2.0))])
        sat_l = note("satellites carrying atomic clocks", 15, INK).move_to(P(-4.0, 1.4))
        line("The idea never went away. A G P S receiver also finds where it is from time: from signals sent by "
             "satellites carrying atomic clocks.", FadeIn(ge), FadeIn(rx), FadeIn(rx_l), FadeIn(sats, lag_ratio=0.2),
             FadeIn(sat_l), run_time=1.2)
        pulses = []
        for s in sats:
            ln = DashedLine(s.get_center(), rx.get_center(), color=BLUE_INK, stroke_width=2)
            pulses.append(ln)
        self.play(*[Create(p) for p in pulses], run_time=1.2)
        tlab = note("position from the travel times of the signals", 16, INK).move_to(P(3.6, -1.2))
        self.play(FadeIn(tlab), *[Indicate(s, color=BLUE_INK) for s in sats], run_time=1.2)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(ge, rx, rx_l, sats, sat_l, tlab, *pulses)), run_time=0.6)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 22, RED_INK).move_to(P(0, 3.05))
        # top view of the ground: shadow tips through the day, computed for 13 N in late November
        G0 = P(-3.6, -0.1)
        phi, dec, h = 13 * DEGREES, -21 * DEGREES, 1.3
        tips, times = [], []
        for mins in range(-150, 151, 15):
            H = mins / 60 * DEG_PER_HOUR * DEGREES
            e = -np.cos(dec) * np.sin(H)
            n = np.cos(phi) * np.sin(dec) - np.sin(phi) * np.cos(dec) * np.cos(H)
            u = np.sin(phi) * np.sin(dec) + np.cos(phi) * np.cos(dec) * np.cos(H)
            tips.append(G0 + h * np.array([-e / u, -n / u, 0]))
            times.append(mins)
        lens = [np.linalg.norm(p - G0) for p in tips]
        k_min = int(np.argmin(lens))
        assert times[k_min] == 0                       # shortest shadow at local solar noon
        ground = RoundedRectangle(corner_radius=0.1, width=4.6, height=3.4, fill_color=PAPER_DARK, fill_opacity=0.6,
                                  stroke_color=INK, stroke_width=1.2).move_to(P(-3.6, 1.0))
        stick = Dot(G0, radius=0.09, color=INK)
        stick_l = note("stick", 14, INK).next_to(stick, DOWN, buff=0.08)
        compass = VGroup(Arrow(P(-1.55, 1.95), P(-1.55, 2.5), buff=0, color=INK, stroke_width=2,
                               max_tip_length_to_length_ratio=0.25), note("N", 13, INK).move_to(P(-1.55, 2.62)))
        gv = note("seen from above · computed for 13° N in late November", 12).move_to(P(-3.6, -0.85))
        shadow = Line(G0, tips[0], color=INK, stroke_width=3)
        line("Try it yourself. Push a straight stick upright into flat ground on a sunny day.", FadeIn(tiy),
             FadeIn(ground), FadeIn(stick), FadeIn(stick_l), FadeIn(compass), FadeIn(gv), run_time=1.0)
        self.vo_wait()
        dots = VGroup()
        line("Every few minutes around midday, mark the tip of its shadow and note the time. The shortest shadow is "
             "your local noon.", FadeIn(shadow), run_time=0.6)
        for p in tips:
            d = Dot(p, radius=0.045, color=SEPIA)
            dots.add(d)
            self.play(shadow.animate.put_start_and_end_on(G0, p), FadeIn(d), run_time=0.22, rate_func=linear)
        best = Line(G0, tips[k_min], color=RED_INK, stroke_width=5)
        best_l = note("shortest:", 14, RED_INK).next_to((G0 + tips[k_min]) / 2, RIGHT, buff=0.15).shift(UP * 0.12)
        best_l.add(note("local noon", 14, RED_INK).next_to(best_l, DOWN, buff=0.04))
        self.play(FadeOut(shadow), Create(best), FadeIn(best_l), run_time=0.7)
        self.vo_wait()
        steps = VGroup(
            serif("1.  Time the shortest shadow.", 22, INK),
            serif("2.  Correct for the equation of time", 22, INK),
            note("     (up to about 16 minutes; look up today's value)", 15, INK),
            serif("3.  Compare with your time zone's meridian:", 22, INK),
            note("     4 minutes later = 1° further west", 15, RED_INK),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(P(2.6, 1.45))
        line("Correct for the equation of time: through the year, the sun can run up to about sixteen minutes ahead "
             "of the clock, or about fourteen behind. Look it up for today's date.", FadeIn(steps[0]), run_time=0.8)
        self.play(FadeIn(steps[1]), FadeIn(steps[2]), run_time=0.8)
        self.vo_wait()
        ex = ink_card(VGroup(MathTex(r"\text{IST} = \text{UTC} + 5\text{:}30 \;\Rightarrow\; 5.5 \times 15^\circ = "
                                     r"82.5^\circ\,\text{E}", font_size=28, color=INK),
                             MathTex(r"\text{e.g. noon at 12:20} \;\Rightarrow\; 20 \div 4 = 5^\circ \text{ west}"
                                     r" \;\Rightarrow\; 77.5^\circ\,\text{E}", font_size=28, color=RED_INK),
                             note("example numbers, after the equation-of-time correction", 13)
                             ).arrange(DOWN, buff=0.12), pad=0.2).move_to(P(1.2, -1.75))
        line("In India, clock noon is the sun's noon at eighty-two and a half degrees east. Each four minutes later is "
             "one degree further west.", FadeIn(steps[3]), FadeIn(steps[4]), run_time=0.8)
        self.play(FadeIn(ex, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tiy, ground, stick, stick_l, compass, gv, dots, best, best_l, steps, ex)),
                  run_time=0.6)

        # ================= close =================
        ss = Line(P(-1.2, 0.6), P(1.2, 0.6), color=INK, stroke_width=3)
        st = Line(P(0, 0.6), P(0, 1.6), color=INK, stroke_width=4)
        shd = Line(P(0, 0.6), P(1.0, 0.6), color=INK, stroke_width=6, stroke_opacity=0.5)
        sw = clock_face(0.45).move_to(P(-2.8, 1.1))
        swh = hands(lambda: sw[0].get_center(), 0.45, lambda: 12.0)
        gl = Circle(radius=0.5, color=INK, stroke_width=2.5, fill_color=PAPER_DARK, fill_opacity=1).move_to(P(2.8, 1.1))
        glm = VGroup(*[Line(P(2.8, 1.1), P(2.8, 1.1) + 0.5 * np.array([np.cos(a), np.sin(a), 0]), color=INK,
                            stroke_width=0.8) for a in np.linspace(0, TAU, 12, endpoint=False)])
        last = serif("A stick, a watch, and the turning Earth.", 32, INK).move_to(P(0, -0.5))
        last2 = serif("Time is position.", 36, RED_INK).next_to(last, DOWN, buff=0.25)
        line("A stick, a watch, and the turning Earth. Time is position.", FadeIn(ss), FadeIn(st), FadeIn(shd),
             FadeIn(sw), FadeIn(swh), FadeIn(gl), FadeIn(glm), FadeIn(last), run_time=1.0)
        self.play(Rotate(glm, angle=TAU / 6, about_point=P(2.8, 1.1)), FadeIn(last2), run_time=1.6)
        self.vo_wait()
        swh.clear_updaters()
        self.wait(0.5)
        self.play(clear(), FadeOut(VGroup(ss, st, shd, sw, swh, gl, glm, last, last2)), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after D. Sobel, Longitude (1995) · sources in the episode notes", 17),
                     note("facts checked against Royal Museums Greenwich, the Smithsonian, MacTutor, Museo Galileo, "
                          "USNO, Physics Today, Westminster Abbey and Wikipedia", 17),
                     note("silhouettes and chart stylised · pendulum drawn qualitatively · arithmetic and shadows "
                          "computed · Manim · synthetic narration", 15)
                     ).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        for m in end:
            if m.width > 12.8:
                m.scale_to_fit_width(12.8)
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(3.0)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)


class Thumbnail(Scene):
    """Still for the thumbnail: manim -qh -s episodes/I040_time_is_position.py Thumbnail"""

    def construct(self):
        self.camera.background_color = PAPER
        paper, frame = paper_background()
        self.add(paper, frame)
        C, R = P(-3.3, 0.0), 2.8
        disc = Circle(radius=R, fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(C)
        night = Sector(radius=R, angle=PI, start_angle=PI / 2, fill_color=INK, fill_opacity=0.18, stroke_width=0,
                       arc_center=C)
        mers = VGroup(*[Line(C, C + R * np.array([np.cos(a), np.sin(a), 0]), color=INK, stroke_width=1,
                             stroke_opacity=0.45) for a in np.arange(0, TAU, TAU / 24)])
        home = Line(C, C + R * np.array([np.cos(PI / 4), np.sin(PI / 4), 0]), color=BLUE_INK, stroke_width=7)
        shipl = Line(C, C + R * RIGHT, color=RED_INK, stroke_width=7)
        wedge = Sector(radius=1.3, angle=PI / 4, start_angle=0, fill_color=RED_INK, fill_opacity=0.35,
                       stroke_width=0, arc_center=C)
        lab = MathTex(r"45^\circ", font_size=44, color=RED_INK).move_to(C + 1.7 * np.array([np.cos(PI / 8), np.sin(PI / 8), 0]))
        hl = serif("home", 30, BLUE_INK).move_to(C + (R + 0.45) * np.array([np.cos(PI / 4), np.sin(PI / 4), 0]))
        sl = serif("ship", 30, RED_INK).next_to(shipl, RIGHT, buff=0.15)
        sun = sun_glyph(0.45).move_to(P(5.6, 2.6))
        t1 = serif("Time Is", 84, INK, bold=True)
        t2 = serif("Position", 84, RED_INK, bold=True)
        t3 = serif("3 hours = 45° of longitude", 32, INK, italic=True)
        txt = VGroup(t1, t2, t3).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(P(3.6, -0.6))
        self.add(disc, night, mers, wedge, home, shipl, lab, hl, sl, sun, txt)
