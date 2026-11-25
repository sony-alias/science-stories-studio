"""I039 Secret Keys in Public, a Science Stories episode.

After S. Singh, The Code Book (1999). Script and sources: episodes/I039_script.md

Render:  manim -qh --frame_rate 30 episodes/I039_secret_keys.py SecretKeys
Then:    scripts/finish_video.sh media/videos/I039_secret_keys/1080p30/SecretKeys.mp4 out/I039_secret_keys.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

MONO = "DejaVu Sans Mono"
GREEN_INK = "#4f6b3a"


def note(text, size=17, color=FADED):
    return serif(text, size, color, italic=True)


def P(x, y):
    return np.array([x, y, 0.0])


def mono(text, size=20, color=INK):
    return Text(text, font=MONO, font_size=size, color=color)


# ---------- the mathematics, computed and checked at render time ----------
Q, G = 23, 5
POWERS = [pow(G, k, Q) for k in range(1, Q)]                 # 5^1 .. 5^22 mod 23
assert POWERS == [5, 2, 10, 4, 20, 8, 17, 16, 11, 9, 22, 18, 21, 13, 19, 3, 15, 6, 7, 12, 14, 1]
assert sorted(POWERS) == list(range(1, Q))                   # 5 is a primitive root mod 23
A_SECRET, B_SECRET = 6, 15
A_PUB, B_PUB = pow(G, A_SECRET, Q), pow(G, B_SECRET, Q)
KEY = pow(B_PUB, A_SECRET, Q)
assert (A_PUB, B_PUB, KEY) == (8, 19, 2) and pow(A_PUB, B_SECRET, Q) == KEY == pow(G, A_SECRET * B_SECRET, Q)
EVE_TRIES = POWERS.index(A_PUB) + 1
assert EVE_TRIES == 6
USERS = 1000
PAIRS = USERS * (USERS - 1) // 2
assert PAIRS == 499500
DIGITS_2048 = len(str(2 ** 2048))
assert DIGITS_2048 == 617

# paint (an analogy): equal parts of each colour
C_COMMON = "#d9b44a"
C_ALICE = "#b0392b"
C_BOB = "#2f5d8c"


def mix(*cols):
    rgb = np.mean([color_to_rgb(c) for c in cols], axis=0)
    return rgb_to_color(rgb)


C_A_PUB, C_B_PUB = mix(C_COMMON, C_ALICE), mix(C_COMMON, C_BOB)
C_FINAL = mix(C_COMMON, C_ALICE, C_BOB)


# ---------- small drawings ----------
def pot(color, label=None, r=0.42):
    jar = VGroup(
        RoundedRectangle(corner_radius=0.12, width=2 * r, height=1.5 * r, fill_color=PAPER, fill_opacity=1,
                         stroke_color=INK, stroke_width=2),
    )
    paint = RoundedRectangle(corner_radius=0.08, width=2 * r - 0.12, height=1.5 * r * 0.62, fill_color=color,
                             fill_opacity=1, stroke_width=0)
    paint.align_to(jar[0], DOWN).shift(UP * 0.06)
    rim = Line(jar[0].get_corner(UL) + LEFT * 0.04, jar[0].get_corner(UR) + RIGHT * 0.04, color=INK, stroke_width=3)
    g = VGroup(jar, paint, rim)
    g.paint = paint
    if label:
        g.add(note(label, 15, INK).next_to(jar, DOWN, buff=0.1))
    return g


def person(name, color=INK, sub=None):
    head = Circle(radius=0.22, fill_color=color, fill_opacity=1, stroke_width=0)
    body = VMobject(fill_color=color, fill_opacity=1, stroke_width=0).set_points_smoothly(
        [P(-0.4, -0.9), P(-0.34, -0.45), P(0, -0.3), P(0.34, -0.45), P(0.4, -0.9), P(-0.4, -0.9)])
    head.move_to(P(0, -0.02))
    fig = VGroup(head, body)
    lab = serif(name, 22, color).next_to(fig, DOWN, buff=0.1)
    g = VGroup(fig, lab)
    if sub:
        g.add(note(sub, 14).next_to(lab, DOWN, buff=0.04))
    return g


def padlock(scale=1.0, color=INK):
    body = RoundedRectangle(corner_radius=0.08, width=0.9, height=0.7, fill_color=color, fill_opacity=1,
                            stroke_width=0)
    shackle = Arc(radius=0.3, start_angle=0, angle=PI, color=color, stroke_width=10).next_to(body, UP, buff=-0.02)
    hole = Circle(radius=0.08, fill_color=PAPER, fill_opacity=1, stroke_width=0).move_to(body).shift(UP * 0.05)
    slot = Rectangle(width=0.05, height=0.16, fill_color=PAPER, fill_opacity=1, stroke_width=0).next_to(
        hole, DOWN, buff=-0.02)
    return VGroup(shackle, body, hole, slot).scale(scale)


def key_icon(scale=1.0, color=SEPIA):
    bow = Circle(radius=0.18, color=color, stroke_width=5)
    shaft = Line(P(0.18, 0), P(0.85, 0), color=color, stroke_width=5)
    t1 = Line(P(0.65, 0), P(0.65, -0.18), color=color, stroke_width=5)
    t2 = Line(P(0.8, 0), P(0.8, -0.14), color=color, stroke_width=5)
    return VGroup(bow, shaft, t1, t2).scale(scale)


def briefcase(scale=1.0):
    box = RoundedRectangle(corner_radius=0.06, width=1.0, height=0.7, fill_color="#7a5534", fill_opacity=1,
                           stroke_color=INK, stroke_width=2)
    handle = Arc(radius=0.16, start_angle=0, angle=PI, color=INK, stroke_width=4).next_to(box, UP, buff=0)
    lock = Square(0.12, fill_color="#d9b44a", fill_opacity=1, stroke_width=0).move_to(box.get_top() + DOWN * 0.15)
    return VGroup(handle, box, lock).scale(scale)


def ear(scale=1.0, color=RED_INK):
    outer = Arc(radius=0.3, start_angle=-PI / 2, angle=1.6 * PI, color=color, stroke_width=5)
    inner = Arc(radius=0.13, start_angle=-PI / 3, angle=1.3 * PI, color=color, stroke_width=4).shift(RIGHT * 0.03)
    return VGroup(outer, inner).scale(scale)


def name_card(name, sub=None, size=20):
    parts = [serif(name, size, INK)]
    if sub:
        parts.append(note(sub, size - 6))
    return ink_card(VGroup(*parts).arrange(DOWN, buff=0.06), pad=0.16)


class SecretKeys(NarratedScene):
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
        title = serif("Secret Keys in Public", 52).next_to(orn1, DOWN, buff=0.35)
        sub = serif("How two strangers can agree a secret while everyone listens", 26, FADED, italic=True
                    ).next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("after S. Singh, The Code Book (1999)", 16).move_to([0, -2.6, 0])
        self.vo("Science Stories. Secret keys in public.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.wait(0.6)
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= the person and the meeting =================
        place = spaced("Stanford · autumn 1974", 18, SEPIA).move_to(P(0, 3.05))
        dif = cameo("beard", 0.75).move_to(P(-3.6, 0.9))
        dif_l = VGroup(serif("Whitfield Diffie", 22, INK), note("b. 1944 · independent researcher", 14)
                       ).arrange(DOWN, buff=0.05).next_to(dif, DOWN, buff=0.15)
        hel = cameo("plain", 0.75).move_to(P(3.6, 0.9))
        hel_l = VGroup(serif("Martin Hellman", 22, INK), note("professor of electrical engineering", 14)
                       ).arrange(DOWN, buff=0.05).next_to(hel, DOWN, buff=0.15)
        sil_n = note("silhouettes stylised, not likenesses", 13).move_to(P(0, -2.55))
        line("Stanford, autumn 1974. Whitfield Diffie, an independent researcher fascinated by codes, visits a "
             "professor, Martin Hellman.", FadeIn(place), FadeIn(dif), FadeIn(dif_l), FadeIn(sil_n), run_time=1.0)
        self.play(FadeIn(hel), FadeIn(hel_l), run_time=0.9)
        self.vo_wait()

        clock = VGroup(Circle(radius=0.85, color=INK, stroke_width=3, fill_color=PAPER, fill_opacity=1),
                       *[Line(P(0, 0.72), P(0, 0.82), color=INK, stroke_width=2).rotate(i * TAU / 12, about_point=ORIGIN)
                         for i in range(12)]).move_to(P(0, 0.9))
        hand_t = ValueTracker(0.0)
        hand = always_redraw(lambda: Line(clock.get_center(),
                                          clock.get_center() + 0.68 * np.array([np.sin(hand_t.get_value() * TAU),
                                                                                np.cos(hand_t.get_value() * TAU), 0]),
                                          color=RED_INK, stroke_width=4))
        hub = Dot(clock.get_center(), radius=0.06, color=INK)
        plan = note("planned: half an hour", 16, INK).next_to(clock, UP, buff=0.2)
        real = note("actual: all afternoon, then dinner", 16, RED_INK).next_to(clock, DOWN, buff=0.2)
        line("A half-hour meeting runs all afternoon, and into dinner.",
             FadeIn(clock), FadeIn(hand), FadeIn(hub), FadeIn(plan), run_time=0.8)
        self.play(hand_t.animate.set_value(0.5), run_time=1.2)
        self.play(hand_t.animate.set_value(5.5), FadeIn(real), run_time=2.6, rate_func=smooth)
        self.vo_wait()
        hand.clear_updaters()
        self.play(FadeOut(VGroup(clock, hand, hub, plan, real, hel, hel_l, place, sil_n)),
                  VGroup(dif, dif_l).animate.scale(0.75).move_to(P(-4.9, 1.2)), run_time=0.8)

        # travels
        road = VMobject(color=FADED, stroke_width=2.5).set_points_smoothly(
            [P(-3.4, -0.6), P(-1.8, 0.6), P(0.2, -0.2), P(2.0, 0.9), P(4.6, 0.1)])
        road_d = DashedVMobject(road, num_dashes=40)
        books = VGroup()
        for t in (0.12, 0.38, 0.62, 0.88):
            p = road.point_from_proportion(t)
            b = VGroup(*[Rectangle(width=0.09, height=0.32 + 0.05 * (i % 2), fill_color=c, fill_opacity=1,
                                   stroke_color=INK, stroke_width=0.6) for i, c in
                         enumerate([SEPIA, RED_INK, BLUE_INK, SEPIA])]).arrange(RIGHT, buff=0.01)
            books.add(b.move_to(p + UP * 0.35))
        yrs = note("1973 – 1974: libraries, universities, laboratories", 17, INK).move_to(P(0.6, 2.2))
        line("Diffie had spent two years travelling to learn all he could about codes.", Create(road_d), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in books], lag_ratio=0.3), FadeIn(yrs),
                  run_time=1.6)
        self.vo_wait()
        self.play(FadeOut(VGroup(road_d, books, yrs)), run_time=0.6)

        # ================= the key problem =================
        al = person("A", INK).move_to(P(-4.0, 0.3))
        bo = person("B", INK).move_to(P(4.0, 0.3))
        lk1 = padlock(0.55).next_to(al, UP, buff=0.25)
        lk2 = padlock(0.55).next_to(bo, UP, buff=0.25)
        k1 = key_icon(0.7).next_to(lk1, RIGHT, buff=0.2)
        k2 = key_icon(0.7).next_to(lk2, LEFT, buff=0.2)
        same = note("the same key, at both ends, in advance", 18, RED_INK).move_to(P(0, 2.4))
        line("One problem gripped him. Every cipher needs a key, and both sides must share it before they can talk "
             "in secret.", FadeOut(VGroup(dif, dif_l)), FadeIn(al), FadeIn(bo), run_time=0.9)
        self.play(FadeIn(lk1), FadeIn(lk2), run_time=0.6)
        self.play(FadeIn(k1, shift=RIGHT * 0.1), FadeIn(k2, shift=LEFT * 0.1), FadeIn(same), run_time=0.8)
        self.vo_wait()
        case = briefcase(0.8).move_to(P(-2.8, -0.9))
        courier = note("a courier with a locked briefcase", 17, INK).move_to(P(0, -1.75))
        line("That meant meeting in person, or trusting a courier with a locked briefcase.",
             FadeIn(case), FadeIn(courier), run_time=0.8)
        self.play(case.animate.move_to(P(2.8, -0.9)), run_time=2.4)
        self.vo_wait()
        self.play(FadeOut(VGroup(al, bo, lk1, lk2, k1, k2, same, case, courier)), run_time=0.6)

        # network
        rng = np.random.default_rng(1976)
        n_show = 14
        ang = np.linspace(0, TAU, n_show, endpoint=False) + 0.1
        nodes = VGroup(*[Dot(P(-2.6 + 2.0 * np.cos(a), 0.55 + 2.0 * np.sin(a)), radius=0.09, color=INK) for a in ang])
        links = VGroup(*[Line(nodes[i].get_center(), nodes[j].get_center(), color=SEPIA, stroke_width=0.9,
                              stroke_opacity=0.7) for i in range(n_show) for j in range(i + 1, n_show)])
        assert len(links) == n_show * (n_show - 1) // 2 == 91
        n_lab = note(f"{n_show} users: {len(links)} keys", 17, INK).next_to(nodes, DOWN, buff=0.25)
        f1 = MathTex(r"\text{keys} = \frac{n(n-1)}{2}", font_size=40, color=INK).move_to(P(3.0, 1.6))
        f2 = MathTex(r"n = 1000:\ \ 499{,}500\ \text{keys}", font_size=40, color=RED_INK).move_to(P(3.0, 0.4))
        f_n = note("one separate key for every pair, each delivered by hand", 15).move_to(P(3.0, -0.4))
        line("On a network, a thousand users would need almost half a million keys.", FadeIn(nodes), run_time=0.8)
        self.play(Create(links, lag_ratio=0.01), FadeIn(n_lab), run_time=1.6)
        self.play(Write(f1), run_time=0.9)
        self.play(FadeIn(f2, shift=UP * 0.1), FadeIn(f_n), run_time=0.8)
        self.vo_wait()
        self.play(FadeOut(VGroup(nodes, links, n_lab, f1, f2, f_n)), run_time=0.6)

        # the puzzle
        al = person("A", INK).move_to(P(-4.3, 0.4))
        bo = person("B", INK).move_to(P(4.3, 0.4))
        wire = Line(P(-3.5, 0.6), P(3.5, 0.6), color=INK, stroke_width=3)
        eve = person("E", RED_INK, "listening").move_to(P(0, -1.2))
        e_ear = ear(0.7).next_to(eve[0], UP, buff=0.15)
        q = serif("Can two strangers agree on a secret", 34, INK).move_to(P(0, 2.65))
        q2 = serif("when every word can be overheard?", 34, INK).next_to(q, DOWN, buff=0.12)
        line("So, the puzzle: can two strangers agree on a secret when every word they send is overheard?",
             FadeIn(al), FadeIn(bo), Create(wire), run_time=0.9)
        self.play(FadeIn(q), FadeIn(q2), FadeIn(eve), FadeIn(e_ear), run_time=0.9)
        msgs = VGroup(*[Dot(P(-3.4, 0.6), radius=0.08, color=SEPIA) for _ in range(2)])
        for m in msgs:
            self.add(m)
            leak = DashedLine(P(0, 0.55), e_ear.get_top() + UP * 0.05, color=RED_INK, stroke_width=2)
            self.play(m.animate.move_to(P(3.4, 0.6)), Create(leak), run_time=0.8)
            self.play(FadeOut(leak), FadeOut(m), run_time=0.25)
        self.vo_wait()
        self.play(FadeOut(VGroup(q, q2, wire)), run_time=0.5)

        # ================= paint =================
        alice = person("Alice", INK).scale(0.8).move_to(P(-5.2, 0.9))
        bob = person("Bob", INK).scale(0.8).move_to(P(5.2, 0.9))
        eve2 = person("Eve", RED_INK).scale(0.8).move_to(P(0, -1.55))
        names_n = note("names used by cryptographers today · paint is an analogy", 13).move_to(P(0, 3.15))
        common = pot(C_COMMON, "agreed in public").move_to(P(0, 2.0))
        line("Picture it with paint. Alice and Bob agree, in public, on a starting colour.",
             ReplacementTransform(al, alice), ReplacementTransform(bo, bob), ReplacementTransform(eve, eve2),
             FadeOut(e_ear), FadeIn(names_n), run_time=1.0)
        self.play(FadeIn(common, shift=DOWN * 0.1), run_time=0.7)
        self.vo_wait()
        ca = pot(C_COMMON).move_to(P(-3.6, 0.9))
        cb = pot(C_COMMON).move_to(P(3.6, 0.9))
        sa = pot(C_ALICE, "secret").move_to(P(-3.6, -0.75))
        sb = pot(C_BOB, "secret").move_to(P(3.6, -0.75))
        line("Each stirs in a secret colour and sends the mixture across.",
             FadeIn(ca, target_position=common.get_center()), FadeIn(cb, target_position=common.get_center()),
             run_time=0.9)
        self.play(FadeIn(sa), FadeIn(sb), run_time=0.6)
        self.play(ca.paint.animate.set_fill(C_A_PUB), cb.paint.animate.set_fill(C_B_PUB),
                  Indicate(sa[0], color=C_ALICE, scale_factor=1.05), Indicate(sb[0], color=C_BOB, scale_factor=1.05),
                  run_time=0.9)
        pa_lab = note("public", 14, RED_INK).next_to(ca, UP, buff=0.08)
        pb_lab = note("public", 14, RED_INK).next_to(cb, UP, buff=0.08)
        self.play(ca.animate.move_to(P(1.6, 0.9)), cb.animate.move_to(P(-1.6, 0.9)), run_time=1.3)
        pa_lab.next_to(ca, UP, buff=0.08)
        pb_lab.next_to(cb, UP, buff=0.08)
        self.play(FadeIn(pa_lab), FadeIn(pb_lab), run_time=0.4)
        self.vo_wait()
        # each receives the other's mixture
        self.play(ca.animate.move_to(P(3.6, 0.9)), cb.animate.move_to(P(-3.6, 0.9)), FadeOut(pa_lab), FadeOut(pb_lab),
                  run_time=0.8)
        line("Each then adds their own secret to what arrived. Both end with the same shade.",
             run_time=0.5)
        self.play(cb.paint.animate.set_fill(C_FINAL), ca.paint.animate.set_fill(C_FINAL),
                  Indicate(sa[0], color=C_ALICE, scale_factor=1.05), Indicate(sb[0], color=C_BOB, scale_factor=1.05),
                  run_time=1.2)
        eq = MathTex(r"=", font_size=72, color=RED_INK).move_to(P(0, 0.6))
        shared = note("shared secret colour", 17, RED_INK).next_to(eq, DOWN, buff=0.3)
        self.play(cb.animate.move_to(P(-1.1, 0.6)), ca.animate.move_to(P(1.1, 0.6)), FadeIn(eq), FadeIn(shared),
                  run_time=1.0)
        self.vo_wait()
        seen = VGroup(pot(C_A_PUB, None, 0.3), pot(C_B_PUB, None, 0.3)).arrange(RIGHT, buff=0.25)
        seen.next_to(eve2, RIGHT, buff=0.5)
        seen_l = note("Eve saw these", 15, RED_INK).next_to(seen, DOWN, buff=0.1)
        unmix = note("mixing is easy · unmixing is not", 20, INK).move_to(P(0, -2.5))
        line("Eve sees both mixtures. But mixing is easy, and unmixing is not.", FadeIn(seen),
             FadeIn(seen_l), run_time=0.8)
        self.play(FadeIn(unmix), run_time=0.6)
        self.vo_wait()
        paint_all = VGroup(alice, bob, eve2, names_n, common, ca, cb, sa, sb, eq, shared, seen, seen_l, unmix)
        need = serif("a mathematical paint: easy to mix, hard to unmix", 32, INK).move_to(P(0, 0.4))
        line("Diffie and Hellman needed a mathematical paint. They found it on a clock.",
             FadeOut(paint_all), run_time=0.8)
        self.play(FadeIn(need, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(need), run_time=0.6)

        # ================= clock arithmetic =================
        C0, R = P(-3.3, 0.35), 2.25

        def cpos(n, r=R):
            a = PI / 2 - n * TAU / Q
            return C0 + r * np.array([np.cos(a), np.sin(a), 0])

        dial = Circle(radius=R, color=INK, stroke_width=2.5).move_to(C0)
        ticks = VGroup(*[Dot(cpos(n), radius=0.045, color=INK) for n in range(Q)])
        nums = VGroup(*[serif(str(n), 16, FADED).move_to(cpos(n, R + 0.3)) for n in range(Q)])
        head = spaced("clock arithmetic", 18, SEPIA).move_to(P(2.9, 3.05))
        rule = MathTex(r"\times 5,\ \text{then wrap around } 23", font_size=32, color=INK).move_to(P(2.9, 2.45))
        line("Take a clock with twenty-three positions. Start at one and keep multiplying by five, wrapping around "
             "past twenty-three.", Create(dial), FadeIn(ticks), FadeIn(nums), FadeIn(head),
             run_time=1.2)
        self.play(Write(rule), run_time=0.9)
        marker = Dot(cpos(1), radius=0.13, color=RED_INK)
        self.play(FadeIn(marker, scale=1.4), Indicate(nums[1], color=RED_INK), run_time=0.6)
        # table of steps on the right
        tbl = VGroup()
        for k, v in enumerate(POWERS, start=1):
            col, row = (k - 1) // 11, (k - 1) % 11
            e = MathTex(r"5^{%d}" % k, r"\to", str(v), font_size=26, color=INK)
            e[2].set_color(RED_INK)
            e.move_to(P(1.6 + col * 2.6, 1.85 - row * 0.37), aligned_edge=LEFT)
            tbl.add(e)
        trail = VGroup()
        prev = 1
        for k, v in enumerate(POWERS, start=1):
            seg = Line(cpos(prev, R - 0.02), cpos(v, R - 0.02), color=SEPIA, stroke_width=1.6, stroke_opacity=0.8)
            trail.add(seg)
            rt = 0.42 if k <= 6 else 0.2
            self.play(Create(seg), marker.animate.move_to(cpos(v)), FadeIn(tbl[k - 1]), run_time=rt)
            prev = v
            if k == 6:
                self.vo_wait()
                line("The answers jump around with no obvious pattern. Forward is easy.", run_time=0.4)
        self.vo_wait()
        back = ink_card(VGroup(note("landed on", 17, INK), MathTex(r"8", font_size=40, color=RED_INK),
                               note("how many steps?", 17, INK), MathTex(r"5^{\,?} \to 8", font_size=36, color=INK)
                               ).arrange(DOWN, buff=0.08), pad=0.2).move_to(P(-3.3, 0.35))
        hard = note("this backward search is called the discrete logarithm", 15, BLUE_INK).move_to(P(2.9, -2.35))
        line("Backward is hard: told only where you landed, you must find how many steps it took.",
             tbl.animate.set_opacity(0.25), run_time=0.8)
        self.play(FadeIn(back, scale=0.9), FadeIn(hard), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(dial, ticks, nums, head, rule, marker, trail, tbl, back, hard)),
                  run_time=0.7)

        # ================= the exchange =================
        XA, XP, XB = -4.4, 0.0, 4.4
        hA = serif("Alice", 26, INK).move_to(P(XA, 3.0))
        hP = spaced("public", 18, RED_INK).move_to(P(XP, 3.0))
        hB = serif("Bob", 26, INK).move_to(P(XB, 3.0))
        div1 = DashedLine(P(-2.2, 3.2), P(-2.2, -2.6), color=FADED, stroke_width=1.5)
        div2 = DashedLine(P(2.2, 3.2), P(2.2, -2.6), color=FADED, stroke_width=1.5)
        pub1 = MathTex(r"\text{clock } 23,\ \ \text{number } 5", font_size=32, color=INK).move_to(P(XP, 2.3))
        line("Now the exchange. In public: clock twenty-three, number five.",
             FadeIn(hA), FadeIn(hP), FadeIn(hB), Create(div1), Create(div2), run_time=0.9)
        self.play(Write(pub1), run_time=0.9)
        self.vo_wait()
        a1 = MathTex(r"\text{secret } a = 6", font_size=32, color=RED_INK).move_to(P(XA, 2.3))
        a2 = MathTex(r"5^{6} \to 8", font_size=36, color=INK).move_to(P(XA, 1.45))
        a_send = MathTex(r"8", font_size=44, color=INK).move_to(P(XA, 1.45))
        line("Alice's secret is six. Five to the sixth, on the clock, is eight. She sends eight.", FadeIn(a1),
             run_time=0.7)
        self.play(Write(a2), run_time=0.8)
        a8 = a2[0][-1].copy()
        self.play(a8.animate.scale(1.3).move_to(P(XP - 0.7, 1.3)), run_time=1.0)
        self.vo_wait()
        b1 = MathTex(r"\text{secret } b = 15", font_size=32, color=BLUE_INK).move_to(P(XB, 2.3))
        b2 = MathTex(r"5^{15} \to 19", font_size=36, color=INK).move_to(P(XB, 1.45))
        line("Bob's secret is fifteen. Five to the fifteenth is nineteen. He sends nineteen.", FadeIn(b1),
             run_time=0.7)
        self.play(Write(b2), run_time=0.8)
        b19 = b2[0][-2:].copy()
        self.play(b19.animate.scale(1.3).move_to(P(XP + 0.7, 1.3)), run_time=1.0)
        self.vo_wait()
        a3 = MathTex(r"19^{6} \to 2", font_size=36, color=INK).move_to(P(XA, 0.2))
        b3 = MathTex(r"8^{15} \to 2", font_size=36, color=INK).move_to(P(XB, 0.2))
        line("Alice raises nineteen to her six. Bob raises eight to his fifteen. Both get two: their shared key.", TransformFromCopy(b19, a3[0][0:2]), TransformFromCopy(a8, b3[0][0]), run_time=1.0)
        self.play(FadeIn(a3), FadeIn(b3), run_time=0.8)
        kA = SurroundingRectangle(a3[0][-1], color=RED_INK, buff=0.1)
        kB = SurroundingRectangle(b3[0][-1], color=RED_INK, buff=0.1)
        keyl = VGroup(note("shared key", 17, RED_INK).move_to(P(XA, -0.55)),
                      note("shared key", 17, RED_INK).move_to(P(XB, -0.55)))
        self.play(Create(kA), Create(kB), FadeIn(keyl), run_time=0.8)
        self.vo_wait()
        eveX = VGroup(serif("Eve hears:", 20, RED_INK), MathTex(r"5,\ 23,\ 8,\ 19", font_size=34, color=INK)
                      ).arrange(DOWN, buff=0.12).move_to(P(XP, -0.15))
        need_k = MathTex(r"5^{\,?} \to 8", font_size=34, color=RED_INK).next_to(eveX, DOWN, buff=0.3)
        line("Eve heard five, twenty-three, eight and nineteen. She must run the clock backwards.",
             FadeIn(eveX), run_time=0.8)
        self.play(FadeIn(need_k), run_time=0.6)
        self.vo_wait()
        tries = VGroup(*[MathTex(r"5^{%d}\to%d" % (k, POWERS[k - 1]), font_size=24,
                                 color=RED_INK if k == EVE_TRIES else FADED) for k in range(1, EVE_TRIES + 1)]
                       ).arrange(RIGHT, buff=0.22).move_to(P(XP, -1.55))
        found = note(f"found after {EVE_TRIES} tries", 15, RED_INK).next_to(tries, DOWN, buff=0.1)
        line("On this small clock she can try every step. With primes hundreds of digits long, even the best known "
             "methods would take ordinary computers far too long.",
             FadeOut(need_k), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(t) for t in tries], lag_ratio=0.35), run_time=1.8)
        self.play(FadeIn(found), run_time=0.4)
        self.wait(0.6)
        exch = VGroup(hA, hP, hB, div1, div2, pub1, a1, a2, a8, b1, b2, b19, a3, b3, kA, kB, keyl, eveX, tries, found)
        self.play(exch.animate.set_opacity(0.0), run_time=0.6)
        self.remove(exch)
        big1 = VGroup(note("a typical modern prime: 2048 bits", 20, INK),
                      serif(f"{DIGITS_2048} digits long", 40, RED_INK)).arrange(DOWN, buff=0.15).move_to(P(0, 1.5))
        dl = VGroup(*[mono(str(2 ** 2047 + 11)[i:i + 75], 14, FADED) for i in range(0, 300, 75)]).arrange(
            DOWN, buff=0.05).move_to(P(0, 0.1))
        dl_n = note("for scale: the first 300 of 617 digits of a 2048-bit number (not itself a prime)", 13).next_to(dl, DOWN, buff=0.1)
        best = VGroup(note("best known attacks: about", 18, BLUE_INK), MathTex(r"2^{112}", font_size=30, color=BLUE_INK),
                      note("steps (NIST estimate)", 18, BLUE_INK)).arrange(RIGHT, buff=0.12).move_to(P(0, -1.5))
        self.play(FadeIn(big1), FadeIn(dl, lag_ratio=0.02), FadeIn(dl_n), run_time=1.2)
        self.play(FadeIn(best), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(big1, dl, dl_n, best)), run_time=0.6)

        # ================= the paper =================
        pg = VGroup(serif("New Directions in Cryptography", 30, INK),
                    note("Whitfield Diffie and Martin E. Hellman", 18, INK),
                    note("IEEE Transactions on Information Theory · November 1976", 15)).arrange(DOWN, buff=0.12)
        paper_card = ink_card(pg, pad=0.3).move_to(P(0, 1.9))
        quote = serif("“We stand today on the brink of a revolution in cryptography.”", 28, RED_INK, italic=True
                      ).move_to(P(0, 0.35))
        q_n = note("the paper's first sentence", 14).next_to(quote, DOWN, buff=0.1)
        line("In November 1976 they published it. The paper begins: \"We stand today on the brink of a revolution "
             "in cryptography.\"", FadeIn(paper_card, shift=UP * 0.1), run_time=1.0)
        self.wait(1.5)
        self.play(Write(quote), FadeIn(q_n), run_time=2.0)
        self.vo_wait()
        mer = name_card("Ralph Merkle", "worked on the same problem independently", 20).move_to(P(0, -1.3))
        mer_n = note("the paper: “Merkle has independently studied the problem”", 14).next_to(mer, DOWN, buff=0.1)
        line("It credits Ralph Merkle, who attacked the problem independently. Hellman later said Merkle's name "
             "belongs on it too.", FadeIn(mer, shift=UP * 0.1),
             FadeIn(mer_n), run_time=0.9)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(paper_card, quote, q_n, mer, mer_n)), run_time=0.6)

        # ================= GCHQ =================
        X0, X1, Y = -6.0, 6.0, -0.7

        def tx(y):
            return X0 + (X1 - X0) * (y - 1968) / (1999 - 1968)

        axis = Line(P(X0, Y), P(X1, Y), color=INK, stroke_width=2)
        tks = VGroup(*[VGroup(Line(P(tx(y), Y - 0.07), P(tx(y), Y + 0.07), color=INK, stroke_width=1.2),
                              note(str(y), 13, FADED).move_to(P(tx(y), Y - 0.28))) for y in range(1970, 2000, 5)])
        secret_band = Rectangle(width=tx(1997) - tx(1970), height=2.4, fill_color=INK, fill_opacity=0.07,
                                stroke_width=0).move_to(P((tx(1970) + tx(1997)) / 2, Y + 1.35))
        sb_l = note("GCHQ: classified", 15, INK).move_to(P(tx(1987), Y + 2.35))

        def ev(year, text, sub, y, color=INK, side=True):
            d = Dot(P(tx(year), Y), radius=0.08, color=color)
            lab = VGroup(serif(text, 17, color), note(sub, 13)).arrange(DOWN, buff=0.03, aligned_edge=LEFT)
            if side:      # label to the right of the top of its stem, clear of later stems
                stem = Line(P(tx(year), Y), P(tx(year), y), color=color, stroke_width=1.2)
                lab.next_to(P(tx(year), y), RIGHT, buff=0.1)
            else:
                stem = Line(P(tx(year), Y), P(tx(year), y - 0.25), color=color, stroke_width=1.2)
                lab.move_to(P(tx(year), y))
            return VGroup(stem, d, lab)

        rev = ev(1997, "made public", "1997", 0.65, RED_INK, side=False)
        gchq = serif("GCHQ, Britain's codebreaking agency", 24, INK).move_to(P(0, 2.9))
        line("In 1997 came a twist. Britain's codebreaking agency, GCHQ, revealed its own people had got there "
             "first, in secret.", Create(axis), FadeIn(tks), FadeIn(gchq), run_time=1.0)
        self.play(FadeIn(rev), run_time=0.7)
        self.vo_wait()
        e1 = ev(1970, "James Ellis", "1970 · 'non-secret encryption' is possible", 1.35)
        line("In 1970, James Ellis showed encryption without a shared secret should be possible.",
             FadeIn(secret_band), FadeIn(sb_l), run_time=0.8)
        self.play(FadeIn(e1), run_time=0.7)
        self.vo_wait()
        e2 = ev(1973, "Clifford Cocks", "1973 · a method close to RSA", 0.65)
        line("In 1973, Clifford Cocks found a working method, close to what became RSA.", FadeIn(e2), run_time=0.8)
        self.vo_wait()
        e3 = ev(1974, "Malcolm Williamson", "1974 · a key exchange", -0.05)
        dh = ev(1976, "Diffie and Hellman", "1976 · published", -1.6, BLUE_INK, side=False)
        dh[0].put_start_and_end_on(P(tx(1976), Y), P(tx(1976), -1.35))
        line("In 1974, Malcolm Williamson found a key exchange much like Diffie and Hellman's.", FadeIn(e3),
             run_time=0.8)
        self.play(FadeIn(dh), run_time=0.7)
        self.vo_wait()
        died = note("Ellis died 25 November 1997", 15, RED_INK).move_to(P(tx(1993), -1.6))
        line("Ellis died in November 1997, about a month before it was made public.",
             Indicate(secret_band, color=INK), run_time=0.8)
        self.play(FadeIn(died), run_time=0.6)
        self.vo_wait()
        twice = VGroup(serif("found twice:", 26, INK), serif("in secret", 26, FADED),
                       serif("and in the open", 26, BLUE_INK)).arrange(RIGHT, buff=0.3).move_to(P(0, -2.4))
        line("Found twice, but only the open version could be used by everyone.", FadeIn(twice[0]), FadeIn(twice[1]), run_time=0.8)
        self.play(FadeIn(twice[2]), Indicate(dh[2], color=BLUE_INK), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(axis, tks, secret_band, sb_l, rev, gchq, e1, e2, e3, dh, died, twice)),
                  run_time=0.7)

        # ================= today =================
        bar = RoundedRectangle(corner_radius=0.2, width=7.0, height=0.7, fill_color=PAPER_DARK, fill_opacity=1,
                               stroke_color=INK, stroke_width=1.5).move_to(P(0, 1.9))
        lock = padlock(0.42, GREEN_INK).move_to(bar.get_left() + RIGHT * 0.5)
        url = mono("https://", 22, GREEN_INK).next_to(lock, RIGHT, buff=0.25)
        tls = VGroup(note("TLS 1.3: every connection agrees a fresh key", 18, INK),
                     note("with Diffie-Hellman over numbers or elliptic curves (RFC 8446)", 15)).arrange(
            DOWN, buff=0.06).move_to(P(0, 0.75))
        line("Today, secure web connections agree a fresh key with a descendant of this exchange.", FadeIn(bar), FadeIn(lock), FadeIn(url), run_time=0.9)
        self.play(FadeIn(tls), run_time=0.7)
        self.vo_wait()
        award = name_card("ACM A.M. Turing Award", "the 2015 award, announced March 2016", 24).move_to(P(0, -1.15))
        line("In 2016, Diffie and Hellman received the Turing Award.", FadeIn(award, shift=UP * 0.1),
             run_time=0.9)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(bar, lock, url, tls, award)), run_time=0.6)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 22, RED_INK).move_to(P(0, 3.0))
        steps = VGroup(
            serif("1.  Agree out loud: clock 23, number 5.", 24, INK),
            serif("2.  Each picks a secret from 1 to 22.", 24, INK),
            serif("3.  Raise 5 to your secret on the clock; swap answers.", 24, INK),
            serif("4.  Raise what you receive to your secret.", 24, INK),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(P(-2.4, 1.15))
        tip = VGroup(note("one step at a time:", 16, INK),
                     MathTex(r"5^1 = 5", font_size=26, color=INK),
                     MathTex(r"5\times5 = 25 \to 2", font_size=26, color=INK),
                     MathTex(r"2\times5 = 10", font_size=26, color=INK),
                     MathTex(r"10\times5 = 50 \to 4", font_size=26, color=INK),
                     MathTex(r"\dots", font_size=26, color=INK)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        tip_card = ink_card(tip, pad=0.2).move_to(P(4.4, 1.05))
        line("Try it yourself. With a friend, agree out loud on clock twenty-three and the number five, and each pick "
             "a secret from one to twenty-two.", FadeIn(tiy), FadeIn(steps[0]), run_time=0.9)
        self.wait(1.5)
        self.play(FadeIn(steps[1]), run_time=0.6)
        self.vo_wait()
        line("Raise five to your secret, one step at a time, and swap answers. Then raise what you receive to your "
             "secret.", FadeIn(steps[2]), run_time=0.8)
        self.play(FadeIn(tip_card, shift=LEFT * 0.1), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(steps[3]), run_time=0.6)
        self.vo_wait()
        check = serif("Same number?  You share a secret nobody said aloud.", 24, RED_INK).move_to(P(0, -1.2))
        example = note("our example: secrets 6 and 15 · sent 8 and 19 · both get 2", 16, INK).next_to(check, DOWN,
                                                                                                      buff=0.25)
        line("If you match, you share a secret you never said.", FadeIn(check), run_time=0.8)
        self.play(FadeIn(example), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tiy, steps, tip_card, check, example)), run_time=0.6)

        # ================= close =================
        pa = pot(C_FINAL, None, 0.4).move_to(P(-1.5, 1.4))
        pb = pot(C_FINAL, None, 0.4).move_to(P(1.5, 1.4))
        eqc = MathTex(r"=", font_size=60, color=RED_INK).move_to(P(0, 1.4))
        last = serif("Two strangers, a public line, and a secret that never travelled.", 30, INK).move_to(P(0, -0.3))
        line("Two strangers, a public line, and a secret that never travelled.", FadeIn(pa), FadeIn(pb), run_time=0.8)
        self.play(FadeIn(eqc), FadeIn(last, shift=UP * 0.1), run_time=1.0)
        self.vo_wait()
        self.wait(0.6)
        self.play(clear(), FadeOut(VGroup(pa, pb, eqc, last)), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after S. Singh, The Code Book (1999) · sources in the episode notes", 17),
                     note("facts checked against Diffie and Hellman (1976), ACM Turing Award pages, GCHQ, NSA, "
                          "Wikipedia, B. Schneier, NIST and RFC 8446", 17),
                     note("silhouettes invented · paint is an analogy · clock arithmetic computed · Manim · "
                          "synthetic narration", 15)
                     ).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        for m in end:
            if m.width > 12.8:
                m.scale_to_fit_width(12.8)
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(3.0)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)
