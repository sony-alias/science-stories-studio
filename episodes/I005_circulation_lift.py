"""I005, Plate V: Circulation and Lift (Worlds of Flow).

Render:  manim -qh --frame_rate 30 episodes/I005_circulation_lift.py CirculationLift
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403

R = 1.0           # cylinder radius
U = 1.0           # free-stream speed
G_FINAL = 4 * PI * 0.5   # circulation that puts the stagnation points at 30 degrees below the axis


def velocity(x, y, G):
    """Uniform stream past a cylinder, plus a clockwise point vortex of strength G (lift upward)."""
    r2 = max(x * x + y * y, 1e-9)
    u = U * (1 - R * R * (x * x - y * y) / (r2 * r2)) + G * y / (2 * PI * r2)
    v = -U * 2 * R * R * x * y / (r2 * r2) - G * x / (2 * PI * r2)
    return u, v


def flow_lines(G, seeds=17, dt=0.05):
    lines = []
    for y0 in np.linspace(-2.4, 2.4, seeds):
        x, y = -5.6, float(y0)
        pts = [(x, y)]
        for _ in range(1000):
            k1 = velocity(x, y, G)
            k2 = velocity(x + dt / 2 * k1[0], y + dt / 2 * k1[1], G)
            k3 = velocity(x + dt / 2 * k2[0], y + dt / 2 * k2[1], G)
            k4 = velocity(x + dt * k3[0], y + dt * k3[1], G)
            x += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            y += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            if x > 5.6 or np.hypot(x, y) < R:
                break
            pts.append((x, y))
        lines.append(pts)
    return lines


def streams_mob(G):
    return VGroup(*[
        VMobject().set_points_as_corners([np.array([x, y, 0]) for x, y in pts])
        .set_stroke(color=BLUE_INK, width=1.4, opacity=0.85)
        for pts in flow_lines(G)
    ])


def stagnation_dots(G):
    s = min(G / (4 * PI * R * U), 1.0)
    a1, a2 = PI + np.arcsin(s), -np.arcsin(s)
    return VGroup(*[Dot(R * np.array([np.cos(a), np.sin(a), 0]), radius=0.075, color=RED_INK)
                    for a in (a1, a2)])


def airfoil_points(n=240):
    """Joukowski map zeta = z + 1/z of a circle through z = 1 (sharp trailing edge at zeta = 2)."""
    z0 = -0.12 + 0.12j
    rad = abs(1 - z0)
    out = []
    for t in np.linspace(0, TAU, n):
        z = z0 + rad * np.exp(1j * t)
        zeta = (z + 1 / z) * 1.3
        out.append(np.array([zeta.real - 0.3, zeta.imag, 0]))
    return out


class CirculationLift(NarratedScene):
    def construct(self):
        self.camera.background_color = PAPER
        paper, frame = paper_background()
        self.add(paper)
        self.play(FadeIn(frame), run_time=0.8)

        caption = [None]

        def say(text):
            self.vo(text)
            lines = wrap_two(text) if NARRATE else [text]
            new = VGroup(*[serif(l, 22 if NARRATE else 24, FADED, italic=True) for l in lines]).arrange(DOWN, buff=0.06)
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

        # ================= title =================
        series = spaced("Worlds of Flow", 22).move_to([0, 1.75, 0])
        plate_no = serif("Plate V", 22, SEPIA, italic=True).next_to(series, DOWN, buff=0.22)
        orn1 = ornament(3.4).next_to(plate_no, DOWN, buff=0.25)
        title = serif("Circulation and Lift", 60).next_to(orn1, DOWN, buff=0.35)
        sub = serif("How a swirl added to a flow can hold a wing up", 26, FADED, italic=True)
        sub.next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = serif("after O. Darrigol, Worlds of Flow (Oxford, 2005)", 16, FADED,
                       italic=True).move_to([0, -3.2, 0])
        self.vo("Worlds of Flow. Plate five: circulation and lift. "
                "How a swirl added to a flow can hold a wing up.")
        self.play(FadeIn(series, shift=DOWN * 0.1), FadeIn(plate_no), run_time=0.9)
        self.play(GrowFromCenter(orn1), run_time=0.5)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.wait(0.8)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, plate_no, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= the two people, 1902 and 1906 =================
        story = VGroup(
            serif("In 1902, Martin Kutta works out why a wing holds a plane up.", 30),
            serif("In 1906, Nikolai Joukowski, in Moscow, reaches the same answer on his own.", 30),
            serif("Aviators are already flying. The theory is catching up.", 30),
        ).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        story.scale_to_fit_width(11.8)
        self.vo("In 1902, Martin Kutta works out why a wing holds a plane up. "
                "In 1906, Nikolai Joukowski, in Moscow, reaches the same answer on his own. "
                "Aviators are already flying, and the theory is catching up.")
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in story], lag_ratio=0.5), run_time=3.0)
        self.vo_wait()
        self.play(FadeOut(story), run_time=0.8)

        # ================= cylinder with circulation =================
        G = ValueTracker(0.0)
        body = engraved_cylinder(ORIGIN, R)
        streams = always_redraw(lambda: streams_mob(G.get_value()))
        dots = always_redraw(lambda: stagnation_dots(G.get_value()))

        def lift_arrow():
            L = 2.0 * G.get_value() / G_FINAL
            if L < 0.05:
                return VGroup()
            return Arrow(np.array([2.6, -0.6, 0]), np.array([2.6, -0.6 + L, 0]), buff=0,
                         color=RED_INK, stroke_width=6, tip_length=0.28, max_tip_length_to_length_ratio=0.5)

        lift = always_redraw(lift_arrow)
        lift_label = serif("lift", 24, RED_INK, italic=True).move_to([2.6, -1.05, 0])

        self.add(streams)
        self.add(body, dots)
        self.play(FadeIn(body), run_time=0.6)
        self.play(say("Start with the cylinder again. With no swirl, the flow is symmetric, top and bottom. "
                      "So there is no lift."), run_time=0.8)
        self.vo_wait()
        self.add(lift, lift_label)
        self.play(clear(), run_time=0.3)

        self.play(say("Now add circulation: a swirl around the body. On top it adds to the stream, "
                      "underneath it takes away. The top flow speeds up, the pressure falls, and the body is lifted."),
                  G.animate.set_value(G_FINAL), run_time=7.0)
        self.vo_wait()

        # ================= the law =================
        self.play(clear(), run_time=0.3)
        law = ink_card(MathTex(r"L' = \rho\, U\, \Gamma", font_size=60, color=INK), pad=0.3)
        law.move_to([4.0, 2.0, 0])
        self.play(FadeIn(law, shift=DOWN * 0.1), run_time=0.8)
        self.play(say("Lift per unit length is the density of the air, times its speed, times the circulation. "
                      "This is the Kutta-Joukowski law."), run_time=0.8)
        self.vo_wait()
        self.play(clear(), run_time=0.3)

        # ================= the Kutta condition and the wing =================
        question = serif("Which circulation? Nothing so far fixes it.", 34, INK)
        answer = VGroup(
            serif("The flow must leave a sharp trailing edge smoothly.", 26, FADED, italic=True),
            serif("The circulation adjusts until it does.", 26, FADED, italic=True),
        ).arrange(DOWN, buff=0.15).next_to(question, DOWN, buff=0.35)
        self.play(FadeOut(VGroup(streams, dots, lift, lift_label, law)), FadeOut(body), run_time=0.8)
        self.play(say("Which circulation? The flow must leave a sharp trailing edge smoothly. "
                      "The circulation adjusts until it does. That is the Kutta condition."),
                  FadeIn(question), FadeIn(answer), run_time=0.8)
        self.vo_wait()
        self.play(FadeOut(VGroup(question, answer)), run_time=0.6)

        circle = VMobject(fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=3)
        circle.set_points_smoothly([np.array([np.cos(t), np.sin(t), 0]) for t in np.linspace(0, TAU, 240)])
        wing = VMobject(fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=3)
        wing.set_points_smoothly(airfoil_points())
        self.play(FadeIn(circle), run_time=0.6)
        self.play(say("Joukowski showed that a circle, pushed through a simple formula, becomes a wing section. "
                      "Same flow, same lift."), Transform(circle, wing), run_time=6.0)
        self.vo_wait()
        self.play(FadeOut(circle), clear(), run_time=0.6)

        # ================= try it =================
        card_title = serif("Try it yourself", 36, INK)
        card_body = serif("Spin a paper cup or a tennis ball and throw it sideways.", 26, FADED, italic=True)
        card_body2 = serif("It curves, and you can feel the push. That push is circulation.", 26, FADED, italic=True)
        card = VGroup(card_title, card_body, card_body2).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        card_ink = ink_card(card, pad=0.5)
        self.play(FadeIn(card_ink), run_time=0.8)
        self.play(say("Try it yourself. Spin a paper cup or a tennis ball and throw it sideways. "
                      "It curves, and you can feel the push. That push is circulation."), run_time=0.8)
        self.vo_wait()
        self.wait(1.0)
        self.play(FadeOut(card_ink), run_time=0.8)
