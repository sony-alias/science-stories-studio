"""I006, Plate VI: Navier, Stokes and the Equations of Viscous Flow (Worlds of Flow).

Render:  manim -qh --frame_rate 30 episodes/I006_navier_stokes.py NavierStokesPlate
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403

PIPE_R = 1.0


def pipe_profile(y):
    """Poiseuille profile: speed falls with the square of the distance from the wall-to-wall centre."""
    return 1 - (y / PIPE_R) ** 2


class NavierStokesPlate(NarratedScene):
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
        plate_no = serif("Plate VI", 22, SEPIA, italic=True).next_to(series, DOWN, buff=0.22)
        orn1 = ornament(3.4).next_to(plate_no, DOWN, buff=0.25)
        title = serif("Navier, Stokes and Viscous Flow", 56).next_to(orn1, DOWN, buff=0.35).set_x(0)
        sub = serif("Why honey resists the spoon, and the equation that says so", 26, FADED, italic=True)
        sub.next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = serif("after O. Darrigol, Worlds of Flow (Oxford, 2005)", 16, FADED,
                       italic=True).move_to([0, -3.2, 0])
        self.vo("Worlds of Flow. Plate six: Navier, Stokes, and the equations of viscous flow. "
                "Why honey resists the spoon, and the equation that says so.")
        self.play(FadeIn(series, shift=DOWN * 0.1), FadeIn(plate_no), run_time=0.9)
        self.play(GrowFromCenter(orn1), run_time=0.5)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.wait(0.8)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, plate_no, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= two routes to one equation =================
        story = VGroup(
            serif("In 1822, Claude-Louis Navier derives the equations from forces between molecules.", 28),
            serif("In 1845, George Stokes reaches the same equations from the behaviour of a continuous fluid.", 28),
            serif("Two routes, one answer. Yet for decades few engineers trust them.", 28),
        ).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        story.scale_to_fit_width(11.8)
        self.vo("In 1822, Navier derives the equations from forces between molecules. "
                "In 1845, Stokes reaches the same equations from the behaviour of a continuous fluid. "
                "Two routes, one answer. Yet for decades few engineers trust them.")
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in story], lag_ratio=0.5), run_time=3.0)
        self.vo_wait()
        self.play(FadeOut(story), run_time=0.8)

        # ================= the equation =================
        eq = MathTex(r"\rho\left(\frac{\partial \mathbf{u}}{\partial t}+\mathbf{u}\cdot\nabla\mathbf{u}\right)"
                     r"=-\nabla p+\mu\,\nabla^{2}\mathbf{u}", font_size=44, color=INK)
        eq_card = ink_card(eq, pad=0.35).move_to([0, 1.2, 0])
        viscous = serif("The term with the viscosity μ is the one that spreads motion through the fluid.", 24,
                        FADED, italic=True).next_to(eq_card, DOWN, buff=0.4)
        self.play(FadeIn(eq_card, shift=DOWN * 0.1), run_time=1.0)
        self.play(say("Here it is: the fluid's acceleration, on one side, and the pressure push and the viscous "
                      "spreading on the other. The term with the viscosity spreads motion through the fluid."),
                  FadeIn(viscous), run_time=0.8)
        self.vo_wait()
        self.play(FadeOut(VGroup(eq_card, viscous)), clear(), run_time=0.6)

        # ================= shear layers =================
        plates_y = (-2.4, 2.4)
        bottom = Line([-4.5, plates_y[0], 0], [4.5, plates_y[0], 0], color=INK, stroke_width=4)
        top = Line([-4.5, plates_y[1], 0], [4.5, plates_y[1], 0], color=INK, stroke_width=4)
        layer_ys = np.linspace(plates_y[0] + 0.25, plates_y[1] - 0.25, 7)
        arrows = VGroup()
        for i, y in enumerate(layer_ys):
            speed = (i + 1) / len(layer_ys)              # linear profile: 0 at the bottom plate, 1 at the top
            arrows.add(Arrow([-4.0, y, 0], [-4.0 + 6.0 * speed, y, 0], buff=0, color=BLUE_INK,
                             stroke_width=4, tip_length=0.22, max_tip_length_to_length_ratio=0.4))
        bottom_label = serif("still plate", 20, FADED, italic=True).next_to(bottom, DOWN, buff=0.1).shift(LEFT * 3.4)
        top_label = serif("moving plate", 20, FADED, italic=True).next_to(top, UP, buff=0.1).shift(LEFT * 3.4)
        self.play(Create(bottom), Create(top), run_time=0.8)
        self.play(say("Put a fluid between two plates. The one at the bottom is still, the one on top moves. "
                      "Each layer drags on the layer below, so the speed grows steadily from the bottom up."),
                  LaggedStart(*[GrowFromPoint(a, a.get_start()) for a in arrows], lag_ratio=0.12),
                  FadeIn(bottom_label), FadeIn(top_label), run_time=1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(bottom, top, arrows, bottom_label, top_label)), clear(), run_time=0.6)

        # ================= pipe, the parabola =================
        pipe_top = Line([-4.5, PIPE_R, 0], [4.5, PIPE_R, 0], color=INK, stroke_width=4)
        pipe_bot = Line([-4.5, -PIPE_R, 0], [4.5, -PIPE_R, 0], color=INK, stroke_width=4)
        ys = np.linspace(-PIPE_R + 0.12, PIPE_R - 0.12, 9)
        pipe_arrows = VGroup()
        for y in ys:
            s = pipe_profile(y)
            pipe_arrows.add(Arrow([-4.2, y, 0], [-4.2 + 3.6 * s + 0.05, y, 0], buff=0, color=BLUE_INK,
                                  stroke_width=3.5, tip_length=0.2, max_tip_length_to_length_ratio=0.4))
        parabola = VMobject(color=RED_INK, stroke_width=3).set_points_smoothly(
            [np.array([-4.2 + 3.6 * pipe_profile(y) + 0.05, y, 0]) for y in np.linspace(-PIPE_R, PIPE_R, 40)])
        pipe_label = serif("Pipe flow: the speed is a parabola across the pipe", 24, FADED, italic=True)
        pipe_label.move_to([0, -2.9, 0])
        self.play(Create(pipe_top), Create(pipe_bot), run_time=0.7)
        self.play(say("In a pipe, the same friction shapes a parabola. The fluid sticks to the wall, "
                      "and the centre runs fastest."),
                  LaggedStart(*[GrowFromPoint(a, a.get_start()) for a in pipe_arrows], lag_ratio=0.1),
                  Create(parabola), run_time=1.2)
        self.vo_wait()
        self.play(FadeIn(pipe_label), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(VGroup(pipe_top, pipe_bot, pipe_arrows, parabola, pipe_label)), clear(), run_time=0.6)

        # ================= the marble in honey =================
        column_top, column_bot = 2.9, -2.6
        column = Rectangle(width=2.2, height=column_top - column_bot, stroke_color=INK, stroke_width=2,
                           fill_color=BLUE_INK, fill_opacity=0.12).move_to([-2.6, (column_top + column_bot) / 2, 0])
        honey = serif("honey", 22, FADED, italic=True).next_to(column, RIGHT, buff=0.3).shift(UP * 2.4)

        tau = 0.7
        vt = 1.6
        clock = ValueTracker(0.0)

        def marble_y():
            t = clock.get_value()
            return column_top - 0.25 - vt * (t - tau * (1 - np.exp(-t / tau)))

        marble = always_redraw(lambda: Circle(radius=0.22, fill_color=RED_INK, fill_opacity=1, stroke_color=INK,
                                              stroke_width=2).move_to([-2.6, max(marble_y(), column_bot + 0.25), 0]))
        drag_note = serif("Drag grows with speed until it balances the weight.", 24, FADED, italic=True)
        drag_note.scale_to_fit_width(4.6).move_to([1.4, 0.5, 0])
        self.play(FadeIn(column), FadeIn(honey), FadeIn(marble), run_time=0.8)
        self.play(say("Drop a marble into honey. Viscosity drags on it, and the drag grows with its speed. "
                      "Soon the drag balances the weight, and the marble falls at a steady pace."),
                  clock.animate.set_value(3.2), FadeIn(drag_note, shift=UP * 0.1), run_time=7.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(column, honey, marble, drag_note)), clear(), run_time=0.6)

        # ================= try it =================
        card_title = serif("Try it yourself", 36, INK)
        card_body = serif("Time a marble falling through honey, oil and water.", 26, FADED, italic=True)
        card_body2 = serif("Which fluid is most viscous? Let the clock decide.", 26, FADED, italic=True)
        card = VGroup(card_title, card_body, card_body2).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        card_ink = ink_card(card, pad=0.5)
        self.play(FadeIn(card_ink), run_time=0.8)
        self.play(say("Try it yourself. Time a marble falling through honey, oil and water. "
                      "Which fluid is most viscous? Let the clock decide."), run_time=0.8)
        self.vo_wait()
        self.wait(1.0)
        self.play(FadeOut(card_ink), run_time=0.8)
