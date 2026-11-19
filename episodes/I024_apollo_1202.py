"""I024 1202: The Alarm on the Way to the Moon, a Science Stories episode.

After D. A. Mindell, Digital Apollo: Human and Machine in Spaceflight (2008). Script and sources: episodes/I024_script.md

Render:  manim -qh --frame_rate 30 episodes/I024_apollo_1202.py Apollo1202
Then:    scripts/finish_video.sh media/videos/I024_apollo_1202/1080p30/Apollo1202.mp4 out/I024_apollo_1202.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

MONO = "DejaVu Sans Mono"
GOLD = "#b8892b"
GREEN_INK = "#3f6b3a"
MOON = "#d9cdb3"
AMBER = "#c9861a"


def note(text, size=17, color=FADED):
    return serif(text, size, color, italic=True)


def P(x, y):
    return np.array([x, y, 0.0])


def mono(text, size=20, color=INK):
    return Text(text.lstrip(" "), font=MONO, font_size=size, color=color)   # indent by shifting (see code card)


# ---------- drawings (schematic) ----------
def lunar_module(s=1.0):
    """A schematic lunar module: gold descent stage with legs, grey ascent stage, engine bell."""
    desc = Polygon(P(-0.75, 0.0), P(0.75, 0.0), P(0.9, 0.25), P(0.9, 0.55), P(-0.9, 0.55), P(-0.9, 0.25),
                   stroke_color=INK, stroke_width=2, fill_color=GOLD, fill_opacity=0.85)
    asc = Polygon(P(-0.6, 0.55), P(0.55, 0.55), P(0.7, 0.85), P(0.45, 1.25), P(-0.2, 1.3), P(-0.65, 1.0),
                  stroke_color=INK, stroke_width=2, fill_color="#bdb6a6", fill_opacity=1)
    window = Polygon(P(-0.45, 0.95), P(-0.15, 1.12), P(-0.12, 0.88), P(-0.42, 0.78), stroke_color=INK,
                     stroke_width=1.5, fill_color=INK, fill_opacity=0.85)
    dish = VGroup(Line(P(0.3, 1.27), P(0.45, 1.55), color=INK, stroke_width=1.5),
                  Arc(radius=0.14, start_angle=PI * 0.1, angle=PI * 0.8, color=INK, stroke_width=2)
                  .move_to(P(0.5, 1.6)))
    legs = VGroup()
    for sx in (-1, 1):
        legs.add(Line(P(sx * 0.8, 0.3), P(sx * 1.25, -0.45), color=INK, stroke_width=2.5))
        legs.add(Line(P(sx * 0.6, 0.0), P(sx * 1.2, -0.42), color=INK, stroke_width=1.5))
        legs.add(Ellipse(width=0.32, height=0.09, stroke_color=INK, stroke_width=2, fill_color=PAPER_DARK,
                         fill_opacity=1).move_to(P(sx * 1.27, -0.48)))
    bell = Polygon(P(-0.16, 0.0), P(0.16, 0.0), P(0.26, -0.3), P(-0.26, -0.3), stroke_color=INK, stroke_width=1.5,
                   fill_color=SEPIA, fill_opacity=0.7)
    return VGroup(legs, bell, desc, asc, window, dish).scale(s)


def flame(lm, s=1.0):
    b = lm[1].get_bottom()
    return Polygon(b + P(-0.2, 0) * s, b + P(0.2, 0) * s, b + P(0, -0.7) * s, stroke_width=0,
                   fill_color=AMBER, fill_opacity=0.7)


def moon_surface(y=-2.4, w=13.4):
    ground = VMobject(stroke_color=INK, stroke_width=2.5, fill_color=MOON, fill_opacity=1)
    xs = np.linspace(-w / 2, w / 2, 60)
    ys = y + 0.08 * np.sin(xs * 2.1) + 0.05 * np.sin(xs * 5.3)
    pts = [P(x, yy) for x, yy in zip(xs, ys)] + [P(w / 2, -2.8), P(-w / 2, -2.8)]
    ground.set_points_as_corners(pts + [pts[0]])
    craters = VGroup(*[Ellipse(width=wd, height=wd * 0.22, stroke_color=SEPIA, stroke_width=1.5).move_to(P(x, y - 0.2))
                       for x, wd in [(-4.8, 0.9), (-1.6, 0.5), (2.2, 1.1), (5.0, 0.6)]])
    return VGroup(ground, craters)


def dsky(code="1202"):
    """Schematic of the guidance computer's display and keyboard, with the PROG lamp and an alarm code."""
    body = RoundedRectangle(corner_radius=0.08, width=3.0, height=2.6, stroke_color=INK, stroke_width=2,
                            fill_color="#c9c1ae", fill_opacity=1)
    lamps = VGroup()
    names = ["UPLINK", "TEMP", "NO ATT", "GIMBAL", "STBY", "PROG", "KEY REL", "RESTART"]
    for i, n in enumerate(names):
        r = RoundedRectangle(corner_radius=0.03, width=0.62, height=0.24, stroke_color=INK, stroke_width=1,
                             fill_color=PAPER, fill_opacity=1)
        t = Text(n, font=MONO, font_size=8, color=FADED).move_to(r)
        lamps.add(VGroup(r, t))
    lamps.arrange_in_grid(4, 2, buff=(0.08, 0.08)).move_to(body.get_center() + P(-0.85, 0.35))
    screen = Rectangle(width=1.3, height=1.5, stroke_color=INK, stroke_width=1.2, fill_color="#2b2a24",
                       fill_opacity=1).move_to(body.get_center() + P(0.65, 0.35))
    digits = Text(code, font=MONO, font_size=34, color="#9fd38a").move_to(screen.get_center() + P(0, -0.05))
    lab = Text("ALARM", font=MONO, font_size=10, color="#9fd38a").next_to(digits, UP, buff=0.12)
    keys = VGroup(*[RoundedRectangle(corner_radius=0.03, width=0.26, height=0.2, stroke_color=INK, stroke_width=1,
                                     fill_color=PAPER_DARK, fill_opacity=1) for _ in range(14)])
    keys.arrange_in_grid(2, 7, buff=0.06).move_to(body.get_center() + P(0, -0.9))
    return VGroup(body, lamps, screen, digits, lab, keys)


def console(w=2.6):
    desk = Polygon(P(-w / 2, 0), P(w / 2, 0), P(w / 2 - 0.15, 0.35), P(-w / 2 + 0.15, 0.35), stroke_color=INK,
                   stroke_width=1.8, fill_color=PAPER_DARK, fill_opacity=1)
    tower = Rectangle(width=w - 0.3, height=0.9, stroke_color=INK, stroke_width=1.8, fill_color="#c9c1ae",
                      fill_opacity=1).next_to(desk, UP, buff=0)
    scr = VGroup(*[Rectangle(width=0.62, height=0.5, stroke_color=INK, stroke_width=1.2, fill_color="#2b2a24",
                             fill_opacity=1) for _ in range(3)]).arrange(RIGHT, buff=0.12).move_to(tower)
    return VGroup(desk, tower, scr)


def job_box(name, prio, vital, w=1.9):
    col = BLUE_INK if vital else FADED
    r = RoundedRectangle(corner_radius=0.06, width=w, height=0.38, stroke_color=col, stroke_width=1.8,
                         fill_color=PAPER, fill_opacity=1)
    t = serif(name, 16, INK).move_to(r.get_center() + P(-0.15, 0))
    badge = VGroup(Circle(radius=0.13, stroke_width=0, fill_color=col, fill_opacity=1),
                   Text(str(prio), font=MONO, font_size=13, color=PAPER)).move_to(r.get_right() + P(-0.22, 0))
    return VGroup(r, t, badge)


def slot(i):
    return RoundedRectangle(corner_radius=0.05, width=2.1, height=0.48, stroke_color=INK, stroke_width=1.6,
                            fill_color=PAPER_DARK, fill_opacity=0.5)


def cameo_label(name, sub):
    return VGroup(serif(name, 20, INK), note(sub, 15)).arrange(DOWN, buff=0.05)


class Apollo1202(NarratedScene):
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
        title = serif("1202: The Alarm on the Way to the Moon", 50)
        if title.width > 12.4:
            title.scale_to_fit_width(12.4)
        title.next_to(orn1, DOWN, buff=0.35)
        sub = serif("Apollo 11 and the computer that knew what to drop", 26, FADED, italic=True).next_to(title, DOWN,
                                                                                                        buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("after D. A. Mindell, Digital Apollo: Human and Machine in Spaceflight (2008)", 16
                      ).move_to([0, -2.6, 0])
        self.vo("Science Stories. 1202: the alarm on the way to the Moon.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.3)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= the descent =================
        surface = moon_surface()
        stars = VGroup(*[Dot(P(RNG.uniform(-6.4, 6.4), RNG.uniform(0.4, 3.4)), radius=0.018, color=FADED)
                         for _ in range(40)])
        lm = lunar_module(0.75).move_to(P(-4.6, 2.3))
        fl = always_redraw(lambda: flame(lm, 0.75))
        path = ArcBetweenPoints(P(-4.6, 2.3), P(3.6, -1.75), angle=-0.55, stroke_color=SEPIA, stroke_width=1.5)
        path_d = DashedVMobject(path, num_dashes=40)
        date = VGroup(spaced("20 July 1969", 18, SEPIA), serif("Eagle, descending to the Moon", 24, INK, italic=True)
                      ).arrange(DOWN, buff=0.1).move_to(P(2.6, 2.9))
        crew = note("Neil Armstrong and Buzz Aldrin on board · drawing schematic", 15).next_to(date, DOWN, buff=0.1)
        line("The twentieth of July, 1969. Neil Armstrong and Buzz Aldrin are dropping towards the Moon in the lunar "
             "module, Eagle.", FadeIn(surface), FadeIn(stars), FadeIn(lm), FadeIn(date), FadeIn(crew),
             run_time=1.0)
        self.add(fl)
        self.play(Create(path_d), run_time=1.0)
        self.play(MoveAlongPath(lm, Line(P(-4.6, 2.3), path.point_from_proportion(0.25))), run_time=2.5,
                  rate_func=linear)
        self.vo_wait()
        dk = dsky("1202").scale(0.85).move_to(P(3.3, 0.35))
        prog = dk[1][5][0]
        quote = serif("“Program alarm. … It's a 1202.”", 26, RED_INK, italic=True).move_to(P(-1.2, -1.3))
        q_src = note("Armstrong, about five minutes into the descent", 14).next_to(quote, DOWN, buff=0.08)
        line("About five minutes into the descent, a warning light comes on. Armstrong: Program alarm. It's a 1202.",
             FadeOut(date), FadeOut(crew), FadeOut(path_d), FadeIn(dk, shift=LEFT * 0.2), run_time=0.9)
        self.play(prog.animate.set_fill(AMBER, 1), run_time=0.3)
        self.play(prog.animate.set_fill(PAPER, 1), run_time=0.3)
        self.play(prog.animate.set_fill(AMBER, 1), FadeIn(quote), FadeIn(q_src), run_time=0.4)
        self.vo_wait()
        dk_l = note("the computer's display and keyboard · schematic", 14).next_to(dk, DOWN, buff=0.1)
        clock = VGroup(serif("≈ 7 minutes", 30, INK), note("to the surface", 15)).arrange(DOWN, buff=0.05
                                                                                          ).move_to(P(-4.2, -0.3))
        line("He asks Houston for a reading on it. The surface is about seven minutes away.", FadeIn(dk_l),
             FadeIn(clock), run_time=0.8)
        self.play(MoveAlongPath(lm, Line(lm.get_center(), path.point_from_proportion(0.33))), run_time=2.0,
                  rate_func=linear)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(quote, q_src, dk_l, clock, stars, surface)), FadeOut(fl),
                  FadeOut(lm), dk.animate.scale(0.6).move_to(P(5.3, 2.6)), run_time=0.8)

        # ================= Mission Control =================
        con1 = console().move_to(P(-2.6, -0.9))
        con2 = console(2.2).move_to(P(3.2, -0.9))
        bales = cameo("collar", 0.62).move_to(P(-2.6, 1.6))
        bales_l = cameo_label("Steve Bales", "guidance officer · age 26").next_to(bales, LEFT, buff=0.25)
        q2 = VGroup(serif("Abort", 34, RED_INK), serif("or", 22, FADED, italic=True), serif("go?", 34, GREEN_INK)
                    ).arrange(RIGHT, buff=0.25).move_to(P(0.6, 2.9))
        place = spaced("Mission Control, Houston", 16, SEPIA).move_to(P(-2.6, 3.25))
        line("In Mission Control, the question lands on Steve Bales, the guidance officer. He is twenty-six. Abort, or "
             "keep going?", FadeIn(place), FadeIn(con1), FadeIn(bales), FadeIn(bales_l), run_time=0.9)
        self.play(FadeIn(q2, lag_ratio=0.3), run_time=1.0)
        self.vo_wait()
        garman = cameo("plain", 0.62).move_to(P(3.2, 1.6))
        garman_l = cameo_label("Jack Garman", "computer support · age 24").next_to(garman, RIGHT, buff=0.25)
        room = note("a back room, on the voice loop", 15).next_to(con2, DOWN, buff=0.15)
        wire = DashedLine(con2.get_left() + P(0, 0.4), con1.get_right() + P(0, 0.4), color=SEPIA, dash_length=0.08)
        sil_l = note("silhouettes stylised, not likenesses", 13).move_to(P(0.3, -2.55))
        line("In a back room sits his support engineer, Jack Garman, a computer specialist. He is twenty-four.",
             FadeIn(con2), FadeIn(garman), FadeIn(garman_l), FadeIn(room), Create(wire), FadeIn(sil_l), run_time=1.0)
        self.vo_wait()
        mc = VGroup(con1, con2, bales, bales_l, garman, garman_l, room, wire, place, q2, sil_l)
        self.play(clear(), FadeOut(mc), run_time=0.7)

        # ================= the simulation =================
        flash = VGroup(spaced("Two weeks earlier", 18, SEPIA), serif("5 July 1969 · a practice landing", 28, INK)
                       ).arrange(DOWN, buff=0.1).move_to(P(0, 2.85))
        sim_con = console().move_to(P(-3.2, -0.6))
        sim_b = cameo("collar", 0.55).move_to(P(-3.2, 1.6))
        koos = cameo("plain", 0.55).flip(UP).move_to(P(3.4, 1.4))
        koos_l = cameo_label("Dick Koos", "simulation supervisor").next_to(koos, DOWN, buff=0.15)
        card1201 = ink_card(mono("1201", 34, RED_INK), pad=0.18).move_to(P(0.3, 1.2))
        line("Two weeks earlier, they had been here before. On the fifth of July, in a practice landing, the simulation "
             "supervisor, Dick Koos, slipped in a 1201 alarm.", FadeIn(flash), FadeIn(sim_con), FadeIn(sim_b),
             FadeIn(koos), FadeIn(koos_l), dk.animate.set_opacity(0), run_time=1.0)
        self.play(FadeIn(card1201, shift=LEFT * 0.6), run_time=0.8)
        self.play(card1201.animate.move_to(sim_con[1].get_center() + P(0, 0.05)).scale(0.7), run_time=1.0)
        self.vo_wait()
        abort = stamp(r"\text{ABORT}", RED_INK, size=44).move_to(P(-0.2, -0.2))
        wrong = VGroup(serif("the wrong call:", 22, INK, italic=True),
                       serif("the landing could have gone on", 22, INK, italic=True)).arrange(DOWN, buff=0.05)
        wrong.move_to(P(2.9, -1.0))
        line("Bales did not know what it meant, so he called an abort. It was the wrong call. The landing could have "
             "gone on.", FadeIn(abort, scale=1.4), run_time=0.8)
        self.play(FadeIn(wrong), run_time=0.7)
        self.vo_wait()
        self.play(FadeOut(VGroup(abort, wrong, koos, koos_l, card1201)), run_time=0.6)
        sheet_lines = VGroup(
            mono("1201  executive overflow: no work areas", 15),
            mono("1202  executive overflow: no core sets", 15),
            mono("      -> GO, if it doesn't come back too often", 15, RED_INK),
            mono("....  and so on, for every alarm", 15, FADED),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        sheet = ink_card(sheet_lines, pad=0.3).move_to(P(2.0, 0.2))
        sheet_l = note("our reconstruction, not Garman's own sheet", 14).next_to(sheet, DOWN, buff=0.15)
        line("So flight director Gene Kranz had them study every alarm the computer could raise. Garman wrote them all "
             "down by hand.", FadeIn(sheet, shift=UP * 0.2), FadeIn(sheet_l), run_time=1.0)
        self.vo_wait()
        rule = sheet[2][2]
        box = SurroundingRectangle(rule, color=RED_INK, buff=0.06, stroke_width=2)
        line("For this one, his rule was simple: if it doesn't come back too often, we're fine.", Create(box),
             run_time=0.9)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(flash, sim_con, sim_b, sheet, sheet_l, box)), run_time=0.7)

        # ================= go =================
        mc_core = VGroup(con1, con2, bales, bales_l, garman, garman_l, wire, place).copy()
        wire = mc_core[6]
        go1 = serif("“We're go on that, Flight.”", 26, GREEN_INK, italic=True).move_to(P(-1.8, -2.35))
        go1_l = note("Bales to the flight director", 14).next_to(go1, DOWN, buff=0.05)
        go2 = serif("“We're go on that alarm.”", 26, GREEN_INK, italic=True).move_to(P(0, 2.7))
        go2_l = note("Houston to Eagle", 14).next_to(go2, DOWN, buff=0.05)
        g_say = serif("go", 30, GREEN_INK).move_to(wire.get_center() + P(0, 0.3))
        line("Now, for real, Garman says go. Bales calls it: We're go on that, Flight. And up to Eagle: We're go on that "
             "alarm.", FadeIn(mc_core), run_time=0.8)
        self.play(FadeIn(g_say, shift=LEFT * 1.5), run_time=0.8)
        self.play(FadeIn(go1), FadeIn(go1_l), run_time=0.8)
        self.wait(0.6)
        self.play(FadeIn(go2, shift=UP * 0.2), FadeIn(go2_l), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(mc_core, go1, go1_l, go2, go2_l, g_say)), run_time=0.7)

        # ================= inside the computer =================
        head = VGroup(spaced("Inside the guidance computer", 18, SEPIA),
                      note("a simplified picture of its scheduler · illustration, not the real program", 14)
                      ).arrange(DOWN, buff=0.08).move_to(P(0, 3.15))
        self.remove(dk)
        dk = dsky("1202").scale(0.85 * 0.6).move_to(P(5.3, 2.6))
        dk[1][5][0].set_fill(AMBER, 1)
        line("But what was the computer complaining about?", FadeIn(head), FadeIn(dk), run_time=0.8)
        self.vo_wait()
        jobs_spec = [("navigation", 1, True), ("steering", 2, True), ("engine throttle", 3, True),
                     ("displays", 6, False)]
        jobs = VGroup(*[job_box(n, p, v, w=2.4) for n, p, v in jobs_spec]).arrange(DOWN, buff=0.18)
        jobs.move_to(P(-4.6, 0.6))
        jobs_l = VGroup(note("jobs it must keep doing", 15),
                        note("number = priority (1 runs first)", 14)).arrange(DOWN, buff=0.03).next_to(jobs, UP,
                                                                                                         buff=0.2)
        vital_l = VGroup(Square(0.16, stroke_width=0, fill_color=BLUE_INK, fill_opacity=1), note("vital", 14),
                         Square(0.16, stroke_width=0, fill_color=FADED, fill_opacity=1), note("can wait", 14)
                         ).arrange(RIGHT, buff=0.1).next_to(jobs, DOWN, buff=0.25)
        line("The guidance computer had to do many jobs at once: work out where they were, steer, throttle the engine, "
             "and update the displays.", run_time=0.4)
        self.play(LaggedStart(*[FadeIn(j, shift=RIGHT * 0.2) for j in jobs], lag_ratio=0.3), FadeIn(jobs_l),
                  FadeIn(vital_l), run_time=1.6)
        self.vo_wait()
        laning = VGroup(serif("The Executive", 26, INK), note("scheduler designed by Hal Laning, M.I.T.", 15),
                        note("highest-priority waiting job runs first", 15, RED_INK)).arrange(DOWN, buff=0.06)
        laning.move_to(P(0.1, 2.2))
        cpu = RoundedRectangle(corner_radius=0.1, width=1.8, height=1.0, stroke_color=INK, stroke_width=2.2,
                               fill_color="#c9c1ae", fill_opacity=1).move_to(P(0.1, 0.9))
        cpu_l = serif("runs", 18, INK).move_to(cpu)
        arrows = VGroup(*[Arrow(j.get_right(), cpu.get_left(), buff=0.1, stroke_width=2, color=SEPIA,
                                max_tip_length_to_length_ratio=0.08) for j in jobs])
        line("Its scheduler, designed by Hal Laning at M.I.T., gave every job a priority. The most important waiting "
             "job always ran first.", FadeIn(laning), FadeIn(cpu), FadeIn(cpu_l), run_time=0.9)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25), run_time=1.2)
        for k in range(3):
            self.play(Indicate(jobs[k], color=BLUE_INK, scale_factor=1.06), Indicate(cpu, color=BLUE_INK), run_time=0.5)
        self.vo_wait()
        slots = VGroup(*[slot(i) for i in range(8)]).arrange_in_grid(4, 2, buff=(0.14, 0.12)).move_to(P(4.2, 0.35))
        slots_l = VGroup(serif("waiting slots in memory", 18, INK),
                         note("“core sets”: 8 (Eyles); one account says 7", 13)).arrange(DOWN, buff=0.04)
        slots_l.next_to(slots, UP, buff=0.18)
        line("But every waiting job needed a slot of memory, and there were only a handful of slots.",
             FadeIn(slots, lag_ratio=0.1), FadeIn(slots_l), dk.animate.set_opacity(0), run_time=1.0)
        self.remove(dk)
        # a normal cycle: two slots filled and emptied
        fills = [job_box(jobs_spec[k][0], jobs_spec[k][1], jobs_spec[k][2], w=2.0).move_to(slots[k]) for k in range(3)]
        self.play(*[FadeIn(f) for f in fills], run_time=0.6)
        self.play(*[FadeOut(f, shift=LEFT * 0.4) for f in fills], run_time=0.6)
        self.vo_wait()

        # time budget bar
        bar_x0, bar_w, bar_y = -6.0, 9.0, -1.95
        seg = [("navigation", 0.32, BLUE_INK), ("steering", 0.2, BLUE_INK), ("engine", 0.18, BLUE_INK),
               ("displays", 0.15, FADED)]
        bar = VGroup()
        x = bar_x0
        for name, frac, col in seg:
            r = Rectangle(width=bar_w * frac, height=0.42, stroke_color=INK, stroke_width=1.2, fill_color=col,
                          fill_opacity=0.55).move_to(P(x + bar_w * frac / 2, bar_y))
            t = serif(name, 14, PAPER if col == BLUE_INK else INK).move_to(r)
            bar.add(VGroup(r, t))
            x += bar_w * frac
        spare = Rectangle(width=bar_w * 0.15, height=0.42, stroke_color=INK, stroke_width=1.2, fill_opacity=0
                          ).move_to(P(x + bar_w * 0.075, bar_y))
        spare_t = note("spare", 14).move_to(spare)
        bar_l = note("each second of computer time · proportions schematic", 14).next_to(
            VGroup(bar, spare), UP, buff=0.08).align_to(bar, LEFT)
        radar_dish = VGroup(Arc(radius=0.35, start_angle=PI * 0.15, angle=PI * 0.7, color=INK, stroke_width=3),
                            Line(P(0, 0), P(0, -0.45), color=INK, stroke_width=2.5),
                            Line(P(-0.2, -0.45), P(0.2, -0.45), color=INK, stroke_width=2.5)).move_to(P(5.7, -2.0))
        radar_l = VGroup(serif("rendezvous radar", 17, INK), note("on in case of an abort", 13)).arrange(
            DOWN, buff=0.02).next_to(radar_dish, UP, buff=0.08)
        line("During the landing, a second radar was switched on: the rendezvous radar, there to find the command "
             "module if they had to abort.", FadeIn(bar, lag_ratio=0.2), FadeIn(spare), FadeIn(spare_t),
             FadeIn(bar_l), run_time=1.0)
        self.play(FadeIn(radar_dish), FadeIn(radar_l), run_time=0.8)
        self.vo_wait()
        # radar steals ~13%
        pulses = VGroup(*[Dot(radar_dish.get_left() + P(-0.2 - 0.25 * i, 0), radius=0.05, color=RED_INK)
                          for i in range(8)])
        steal = Rectangle(width=bar_w * 0.13, height=0.42, stroke_color=RED_INK, stroke_width=1.5,
                          fill_color=RED_INK, fill_opacity=0.7).move_to(P(bar_x0 + bar_w * 0.065, bar_y))
        steal_t = serif("radar ≈13%", 14, PAPER).move_to(steal)
        thirteen = VGroup(serif("≈ 13% of its time", 22, RED_INK),
                          note("Eyles's working figure (≈15% at the peak rate)", 13),
                          note("accounts differ on whom to blame: wiring documents or switch setting", 13)
                          ).arrange(DOWN, buff=0.03).move_to(P(0.45, -0.85))
        line("A mismatch in its electrical interface made it send a stream of meaningless signals, and the computer "
             "paused to count every one. That ate about thirteen percent of its time.",
             LaggedStart(*[FadeIn(p) for p in pulses], lag_ratio=0.1), run_time=1.0)
        self.play(pulses.animate.shift(LEFT * 1.4).set_opacity(0), run_time=0.8)
        self.remove(pulses)
        self.play(FadeIn(steal), FadeIn(steal_t), VGroup(bar, spare, spare_t).animate.shift(RIGHT * bar_w * 0.13),
                  run_time=1.0)
        self.play(FadeIn(thirteen), spare.animate.set_stroke(RED_INK), run_time=0.6)
        self.vo_wait()
        # spare is gone: the bar overruns the second
        edge = DashedLine(P(bar_x0 + bar_w, bar_y + 0.4), P(bar_x0 + bar_w, bar_y - 0.4), color=INK)
        edge_l = note("end of the second", 13).next_to(edge, DOWN, buff=0.04)
        # fill slots with late copies
        late = []
        order = [3, 3, 0, 3, 1, 3, 2, 3]
        for i, k in enumerate(order):
            b = job_box(jobs_spec[k][0], jobs_spec[k][1], jobs_spec[k][2], w=2.0).move_to(slots[i])
            late.append(b)
        line("With less time, jobs finished late. New copies arrived before the old ones were done. The slots filled "
             "up.", FadeOut(thirteen), Create(edge), FadeIn(edge_l), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.3) for b in late], lag_ratio=0.25), run_time=2.6)
        self.vo_wait()
        newjob = job_box("navigation", 1, True, w=2.0).move_to(P(4.2, 2.65))
        self.remove(slots_l)
        alarm = stamp(r"1202", RED_INK, size=50).move_to(P(1.0, -0.4))
        alarm_l = note("no free slot", 16, RED_INK).next_to(alarm, DOWN, buff=0.1)
        line("When a new job found no free slot, the computer raised alarm 1202. When it ran out of working space, "
             "1201.", FadeIn(newjob, shift=DOWN * 0.3), run_time=0.8)
        self.play(newjob.animate.shift(DOWN * 0.25), run_time=0.3)
        self.play(newjob.animate.shift(UP * 0.25), FadeIn(alarm, scale=1.5), FadeIn(alarm_l), run_time=0.5)
        self.vo_wait()
        alarm2 = note("1201 · no free work area", 16, RED_INK).next_to(alarm_l, DOWN, buff=0.08)
        self.play(FadeIn(alarm2), run_time=0.4)
        self.wait(0.6)

        # ================= restart =================
        restart = serif("RESTART", 30, RED_INK).move_to(P(1.0, -0.4))
        line("And then it did something clever. It restarted. It cleared the queue, and rebuilt only the jobs marked as "
             "vital, from where they had last saved their place.", FadeOut(alarm), FadeOut(alarm_l), FadeOut(alarm2),
             FadeIn(restart, scale=1.3), run_time=0.8)
        self.play(*[b.animate.set_opacity(0) for b in late], newjob.animate.set_opacity(0), run_time=0.8)
        self.remove(*late, newjob)
        keep = [job_box(jobs_spec[k][0], jobs_spec[k][1], jobs_spec[k][2], w=2.0).move_to(slots[k]) for k in range(3)]
        saved = note("each vital job restarts from its last saved point", 14, BLUE_INK).next_to(slots, UP, buff=0.2)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in keep], lag_ratio=0.3), FadeIn(saved),
                  run_time=1.4)
        self.vo_wait()
        gone = Cross(jobs[3], stroke_color=RED_INK, stroke_width=4)
        gone_l = note("not restored", 14, RED_INK).next_to(jobs[3], RIGHT, buff=0.1)
        line("Less important work simply disappeared. Guidance, steering and the engine carried on.", Create(gone),
             FadeIn(gone_l), bar[3].animate.set_opacity(0.15), run_time=0.9)
        self.play(*[Indicate(b, color=BLUE_INK, scale_factor=1.05) for b in keep], run_time=0.9)
        self.vo_wait()
        comp = VGroup(head, jobs, jobs_l, vital_l, laning, cpu, cpu_l, arrows, slots, bar, spare, spare_t, bar_l,
                      radar_dish, radar_l, steal, steal_t, edge, edge_l, restart, saved, gone, gone_l, *keep)
        self.play(clear(), comp.animate.set_opacity(0), run_time=0.7)
        self.remove(comp)

        # ================= five alarms, landing =================
        seq = ["1202", "1202", "1201", "1202", "1202"]
        lamps = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.06, width=1.4, height=0.6, stroke_color=INK,
                                                 stroke_width=1.6, fill_color="#2b2a24", fill_opacity=1),
                                Text(c, font=MONO, font_size=24, color="#9fd38a")) for c in seq]).arrange(RIGHT, buff=0.3)
        for l_ in lamps:
            l_[1].move_to(l_[0])
        lamps.scale(1.25).move_to(P(0, 1.2))
        lamps_l = note("in order, per Eyles (2004) · each followed by a restart", 14).next_to(lamps, DOWN, buff=0.12)
        gos = VGroup(*[serif("go", 22, GREEN_INK).next_to(l_, DOWN, buff=0.5) for l_ in lamps])
        line("There were five alarms in all: four of them 1202, and one 1201. Each time, the answer from Houston was the "
             "same. Go.", run_time=0.4)
        self.play(LaggedStart(*[FadeIn(l_, scale=1.2) for l_ in lamps], lag_ratio=0.4), FadeIn(lamps_l), run_time=2.4)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in gos], lag_ratio=0.3), run_time=1.6)
        self.vo_wait()
        self.play(FadeOut(VGroup(lamps, lamps_l, gos)), run_time=0.5)
        surface2 = moon_surface(-1.9)
        lm2 = lunar_module(0.75).move_to(P(0.3, 1.6))
        fl2 = always_redraw(lambda: flame(lm2, 0.75))
        fuel = VGroup(serif("“30 seconds”", 26, RED_INK, italic=True), note("Houston's fuel call", 14)
                      ).arrange(DOWN, buff=0.04).move_to(P(-4.3, 2.6))
        line("Then the call: thirty seconds of fuel. Contact light. Houston, Tranquility Base here. The Eagle has landed.",
             FadeIn(surface2), FadeIn(lm2), FadeIn(fuel), run_time=0.8)
        self.add(fl2)
        foot = surface2[0].get_top()[1]
        self.play(lm2.animate.shift(DOWN * (lm2.get_bottom()[1] - foot + 0.12)), run_time=3.0, rate_func=smooth)
        self.remove(fl2)
        dust = VGroup(*[Dot(P(lm2.get_center()[0] + RNG.uniform(-1.6, 1.6), foot + RNG.uniform(0, 0.3)), radius=0.03,
                            color=SEPIA, fill_opacity=0.5) for _ in range(30)])
        self.play(FadeIn(dust, lag_ratio=0.05), run_time=0.6)
        self.play(FadeOut(dust), run_time=0.8)
        landed = VGroup(serif("“Houston, Tranquility Base here.", 28, INK, italic=True),
                        serif("The Eagle has landed.”", 28, INK, italic=True)).arrange(DOWN, buff=0.06)
        landed.move_to(P(3.4, 2.5))
        self.play(FadeIn(landed, lag_ratio=0.2), run_time=1.0)
        self.vo_wait()
        point = serif("overloaded, and it landed anyway", 26, RED_INK).move_to(P(-3.6, 0.9))
        line("The computer was overloaded, and it landed anyway, because it had been told in advance what mattered "
             "most.", FadeIn(point), run_time=0.9)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(surface2, lm2, fuel, landed, point)), run_time=0.7)

        # ================= now =================
        def icon_plane():
            return VGroup(Polygon(P(-0.9, 0), P(0.9, 0.08), P(0.9, -0.08), stroke_color=INK, stroke_width=2,
                                  fill_color=PAPER_DARK, fill_opacity=1),
                          Polygon(P(0.1, 0), P(-0.3, 0.6), P(-0.45, 0.6), P(-0.2, 0), stroke_color=INK, stroke_width=2,
                                  fill_color=PAPER_DARK, fill_opacity=1),
                          Polygon(P(0.1, 0), P(-0.3, -0.6), P(-0.45, -0.6), P(-0.2, 0), stroke_color=INK,
                                  stroke_width=2, fill_color=PAPER_DARK, fill_opacity=1))

        def icon_car():
            body = Polygon(P(-0.9, -0.15), P(0.9, -0.15), P(0.9, 0.15), P(0.45, 0.2), P(0.25, 0.45), P(-0.4, 0.45),
                           P(-0.65, 0.18), P(-0.9, 0.12), stroke_color=INK, stroke_width=2, fill_color=PAPER_DARK,
                           fill_opacity=1)
            return VGroup(body, *[Circle(radius=0.17, stroke_color=INK, stroke_width=2, fill_color=INK,
                                         fill_opacity=1).move_to(P(sx, -0.17)) for sx in (-0.5, 0.5)])

        def icon_phone():
            return VGroup(RoundedRectangle(corner_radius=0.1, width=0.65, height=1.15, stroke_color=INK,
                                           stroke_width=2, fill_color=PAPER_DARK, fill_opacity=1),
                          Rectangle(width=0.5, height=0.8, stroke_color=INK, stroke_width=1, fill_color="#2b2a24",
                                    fill_opacity=1).shift(UP * 0.05))
        icons = VGroup(icon_plane(), icon_car(), icon_phone()).arrange(RIGHT, buff=2.2).scale(1.3).move_to(P(0, 1.0))
        labs = VGroup(*[note(t, 16) for t in ["flight computers", "car controllers", "phones"]])
        for l_, ic in zip(labs, icons):
            l_.next_to(ic, DOWN, buff=0.3)
        prio = VGroup(*[VGroup(*[Rectangle(width=0.22, height=h, stroke_width=0, fill_color=c, fill_opacity=0.8)
                                 for h, c in [(0.6, BLUE_INK), (0.4, BLUE_INK), (0.2, FADED)]]
                               ).arrange(RIGHT, buff=0.06, aligned_edge=DOWN).next_to(l_, DOWN, buff=0.2)
                        for l_ in labs])
        now_l = note("time shared out by priority", 18, RED_INK).move_to(P(0, -1.75))
        line("That idea is everywhere now. Flight computers, car controllers, even your phone, share out their time by "
             "priority.", FadeIn(icons, lag_ratio=0.3), FadeIn(labs), run_time=1.2)
        self.play(FadeIn(prio, lag_ratio=0.2), FadeIn(now_l), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(icons, labs, prio, now_l)), run_time=0.7)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 22, RED_INK).move_to([0, 3.2, 0])
        code_lines = [
            ("jobs = {  # name: (priority, cost, vital)", FADED),
            ('  "guidance": (1, 3, True), "steering": (2, 2, True),', INK),
            ('  "engine":   (3, 2, True), "display":  (9, 2, False)}', INK),
            ("SLOTS, BUDGET, THIEF = 8, 10, 0.13", INK),
            ("queue = []", INK),
            ("for tick in range(60):", INK),
            ("    queue += list(jobs)          # every job wanted again", INK),
            ("    queue.sort(key=lambda j: jobs[j][0])", INK),
            ("    time = BUDGET * (1 - THIEF)  # the thief's share", RED_INK),
            ("    while queue and jobs[queue[0]][1] <= time:", INK),
            ("        time -= jobs[queue.pop(0)][1]", INK),
            ("    if len(queue) > SLOTS:       # no free slot: 1202", RED_INK),
            ("        queue = [j for j in queue if jobs[j][2]]", BLUE_INK),
        ]
        code = VGroup(*[mono(t, 15, c) for t, c in code_lines]).arrange(DOWN, buff=0.07, aligned_edge=LEFT)
        cw = mono("MMMMMMMMMM", 15).width / 10
        for (t, _), m in zip(code_lines, code):
            m.shift(RIGHT * cw * (len(t) - len(t.lstrip(" "))))
        code_card = ink_card(code, pad=0.22).move_to(P(-3.0, 0.5))
        code_l = note("our own toy, not Apollo code", 13).next_to(code_card, DOWN, buff=0.08)
        if code_card.width > 6.9:
            code_card.scale_to_fit_width(6.9).move_to(P(-3.0, 0.5))
            code_l.next_to(code_card, DOWN, buff=0.08)
        line("Try it yourself. Write a tiny priority scheduler in Python.", FadeIn(tiy), run_time=0.6)
        self.play(FadeIn(code_card[0]), FadeIn(code_card[1]), FadeIn(code_l), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(m) for m in code_card[2][:3]], lag_ratio=0.3), run_time=0.9)
        self.vo_wait()
        line("Give each job a priority and a cost, and give the computer a fixed amount of time every tick.",
             LaggedStart(*[FadeIn(m) for m in code_card[2][3:8]], lag_ratio=0.2), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(m) for m in code_card[2][9:11]], lag_ratio=0.3), run_time=0.8)
        self.vo_wait()

        # run the same toy, for the plot
        spec = {"guidance": (1, 3, True), "steering": (2, 2, True), "engine": (3, 2, True), "display": (9, 2, False)}

        def run(thief, restart=True, n=40):
            q, hist, al = [], [], []
            for tick in range(n):
                q += list(spec)
                q.sort(key=lambda j: spec[j][0])
                tm = 10 * (1 - thief)
                while q and spec[q[0]][1] <= tm:
                    tm -= spec[q.pop(0)][1]
                if len(q) > 8 and restart:
                    al.append(tick)
                    q = [j for j in q if spec[j][2]]
                hist.append(len(q))
            return hist, al

        ax = Axes(x_range=[0, 40, 10], y_range=[0, 10, 2], x_length=4.6, y_length=2.7,
                  axis_config={"color": INK, "stroke_width": 2, "include_tip": False, "font_size": 18,
                               "decimal_number_config": {"color": INK, "num_decimal_places": 0}},
                  ).add_coordinates().move_to(P(3.6, 0.75))
        ax_x = note("tick", 14).next_to(ax.x_axis, DOWN, buff=0.35)
        ax_y = note("jobs waiting", 14).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.35)
        slots_line = DashedLine(ax.c2p(0, 8), ax.c2p(40, 8), color=SEPIA)
        slots_t = note("8 slots", 13).next_to(ax.c2p(40, 8), RIGHT, buff=0.08)
        h0, _ = run(0.0)
        h1, al1 = run(0.13)
        calm = ax.plot_line_graph(list(range(40)), [h + 0.12 for h in h0], line_color=BLUE_INK,
                                  add_vertex_dots=False, stroke_width=5)
        calm_l = note("blue: no thief, nothing waits · red: with the thief", 13).next_to(ax_x, DOWN, buff=0.06)
        saw = ax.plot_line_graph(list(range(40)), h1, line_color=RED_INK, add_vertex_dots=False, stroke_width=3)
        marks = VGroup(*[serif("1202", 12, RED_INK).next_to(ax.c2p(t, 9), UP, buff=0.02) for t in al1])
        plot_l = note("output of the code at left", 13).next_to(ax, UP, buff=0.12)
        line("Add a thief that steals thirteen percent, and watch the queue grow.",
             FadeIn(code_card[2][8]), Create(ax), FadeIn(ax_x), FadeIn(ax_y), FadeIn(plot_l), run_time=1.0)
        self.play(Create(calm), FadeIn(calm_l), Create(slots_line), FadeIn(slots_t), run_time=1.0)
        self.play(Create(saw), run_time=2.0, rate_func=linear)
        self.vo_wait()
        line("Then add a restart that keeps only the vital jobs, and check whether guidance ever misses a tick.",
             FadeIn(code_card[2][11:]), FadeIn(marks, lag_ratio=0.2), run_time=1.2)
        ok = note("guidance ran every tick · the display never did", 14, BLUE_INK).next_to(calm_l, DOWN, buff=0.06)
        self.play(FadeIn(ok), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tiy, code_card, code_l, ax, ax_x, ax_y, slots_line, slots_t, calm, calm_l,
                                          saw, marks, plot_l, ok)), run_time=0.8)

        # ================= close =================
        last = VGroup(serif("Five alarms, two young engineers who had done their homework,", 32, INK),
                      serif("and a computer that knew what to drop.", 32, RED_INK)).arrange(DOWN, buff=0.25)
        last.move_to([0, 0.6, 0])
        line("Five alarms, two young engineers who had done their homework, and a computer that knew what to drop.",
             FadeIn(last, lag_ratio=0.2), run_time=1.2)
        self.vo_wait()
        self.play(clear(), FadeOut(last), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after D. A. Mindell, Digital Apollo: Human and Machine in Spaceflight (2008) · sources "
                          "in the episode notes", 17),
                     note("facts checked against D. Eyles (2004), the Apollo Lunar Surface Journal, NASA SP-350, "
                          "collectSPACE, Space.com, Monash Lens and Air & Space", 17),
                     note("silhouettes stylised, not likenesses · spacecraft, consoles and scheduler drawn schematically "
                          "· Manim · synthetic narration", 15)
                     ).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        for m in end:
            if m.width > 12.8:
                m.scale_to_fit_width(12.8)
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(3.0)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)
