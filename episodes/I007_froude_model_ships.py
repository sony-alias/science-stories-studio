"""I007, Plate VII: Froude's Model Ships (Worlds of Flow).

Render:  manim -qh --frame_rate 30 episodes/I007_froude_model_ships.py FroudeModelShipsPlate
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403

G_ACC = 9.81
L_MODEL, L_SHIP = 2.2, 4.4          # hull lengths in frame units (the ship is exactly twice the model)
U_MODEL = 1.0
U_SHIP = U_MODEL * np.sqrt(L_SHIP / L_MODEL)   # the speed that keeps the Froude number the same
FR_MODEL = U_MODEL / np.sqrt(G_ACC * L_MODEL)
FR_SHIP = U_SHIP / np.sqrt(G_ACC * L_SHIP)
WATER_MODEL_Y, WATER_SHIP_Y = 1.7, -1.1
SPEED_SCALE = 0.9                    # frame units per second for the model


def hull(x_stern, L, y_water):
    """Side view of a simple hull floating on the water line y_water, stern at x_stern."""
    pts = [(0, 0.2), (0.82 * L, 0.2), (L, 0.5), (0.8 * L, -0.12), (0, -0.12)]
    return [np.array([x_stern + px, y_water + py, 0]) for px, py in pts]


def wave_train(x_stern, L, y_water, span=6.0):
    """Waves trailing behind the stern. The wavelength is 2 pi Fr^2 L, so it scales with the hull."""
    fr2 = FR_MODEL ** 2          # both hulls share this Froude number
    lam = 2 * PI * fr2 * L
    xs = np.linspace(x_stern - 0.05 * L, x_stern - span, 400)
    pts = []
    for x in xs:
        d = (x_stern - 0.05 * L) - x
        amp = 0.18 * np.exp(-d / (2.2 * lam + 0.4))
        pts.append(np.array([x, y_water + amp * np.sin(2 * PI * d / lam), 0]))
    return pts


class FroudeModelShipsPlate(NarratedScene):
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
        plate_no = serif("Plate VII", 22, SEPIA, italic=True).next_to(series, DOWN, buff=0.22)
        orn1 = ornament(3.4).next_to(plate_no, DOWN, buff=0.25)
        title = serif("Froude's Model Ships", 60).next_to(orn1, DOWN, buff=0.35).set_x(0)
        sub = serif("How a small hull in a tank can tell the truth about a real ship", 26, FADED, italic=True)
        sub.next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = serif("after O. Darrigol, Worlds of Flow (Oxford, 2005)", 16, FADED,
                       italic=True).move_to([0, -3.2, 0])
        self.vo("Worlds of Flow. Plate seven: Froude's model ships. "
                "How a small hull in a tank can tell the truth about a real ship.")
        self.play(FadeIn(series, shift=DOWN * 0.1), FadeIn(plate_no), run_time=0.9)
        self.play(GrowFromCenter(orn1), run_time=0.5)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.wait(0.8)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, plate_no, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= the doubt, at Torquay =================
        story = VGroup(
            serif("In the 1870s, William Froude tows model hulls along a long tank at Torquay.", 28),
            serif("Many engineers doubt that a small model can tell the truth about a ship.", 28),
            serif("Froude's answer is to match one number, not the size.", 28),
        ).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        story.scale_to_fit_width(11.8)
        self.vo("In the 1870s, William Froude tows model hulls along a long tank at Torquay. "
                "Many engineers doubt that a small model can tell the truth about a ship. "
                "Froude's answer is to match one number, not the size.")
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.15) for l in story], lag_ratio=0.5), run_time=3.0)
        self.vo_wait()
        self.play(FadeOut(story), run_time=0.8)

        # ================= the Froude number =================
        eq = MathTex(r"\mathrm{Fr}=\frac{U}{\sqrt{g\,L}}", font_size=60, color=INK)
        eq_card = ink_card(eq, pad=0.35).move_to([0, 1.3, 0])
        explain = serif("Speed against the square root of length. Match Fr, and the waves match, at any size.",
                        24, FADED, italic=True).next_to(eq_card, DOWN, buff=0.4)
        self.play(FadeIn(eq_card, shift=DOWN * 0.1), run_time=0.9)
        self.play(say("His single number is speed divided by the square root of length times gravity. "
                      "Match it, and the waves match, at any size."),
                  FadeIn(explain), run_time=0.8)
        self.vo_wait()
        self.play(FadeOut(VGroup(eq_card, explain)), clear(), run_time=0.6)

        # ================= model and ship at the same Froude number =================
        T = ValueTracker(0.0)

        def model_x():
            return -5.8 + SPEED_SCALE * T.get_value()

        def ship_x():
            return -5.8 + SPEED_SCALE * (U_SHIP / U_MODEL) * T.get_value()

        water_m = Line([-6.4, WATER_MODEL_Y, 0], [6.4, WATER_MODEL_Y, 0], color=BLUE_INK, stroke_width=2)
        water_s = Line([-6.4, WATER_SHIP_Y, 0], [6.4, WATER_SHIP_Y, 0], color=BLUE_INK, stroke_width=2)
        label_m = serif("model", 22, SEPIA, italic=True).move_to([-5.6, WATER_MODEL_Y + 0.9, 0])
        label_s = serif("ship", 22, SEPIA, italic=True).move_to([-5.6, WATER_SHIP_Y + 0.9, 0])
        fr_text = serif(f"Fr = {FR_MODEL:.2f} for both", 24, INK).move_to([3.6, 3.0, 0])

        hull_m = always_redraw(lambda: Polygon(*hull(model_x(), L_MODEL, WATER_MODEL_Y),
                                               fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK,
                                               stroke_width=2))
        hull_s = always_redraw(lambda: Polygon(*hull(ship_x(), L_SHIP, WATER_SHIP_Y),
                                               fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK,
                                               stroke_width=2))
        waves_m = always_redraw(lambda: VMobject(color=BLUE_INK, stroke_width=2.5).set_points_as_corners(
            wave_train(model_x(), L_MODEL, WATER_MODEL_Y)))
        waves_s = always_redraw(lambda: VMobject(color=BLUE_INK, stroke_width=2.5).set_points_as_corners(
            wave_train(ship_x(), L_SHIP, WATER_SHIP_Y)))

        self.add(water_m, water_s, label_m, label_s, waves_m, waves_s, hull_m, hull_s)
        self.play(FadeIn(fr_text), run_time=0.6)
        self.play(say("Here is a model and a ship at the same Froude number. Their waves come out the same, "
                      "one scaled from the other, even though the ship is twice as long."),
                  T.animate.set_value(7.5), run_time=8.0, rate_func=linear)
        self.vo_wait()
        self.play(FadeOut(VGroup(water_m, water_s, label_m, label_s, waves_m, waves_s, hull_m, hull_s, fr_text)),
                  clear(), run_time=0.6)

        # ================= try it =================
        card_title = serif("Try it yourself", 36, INK)
        card_body = serif("Tow toy boat hulls along a rain gutter and time them.", 26, FADED, italic=True)
        card_body2 = serif("Do the longer hulls go faster, and by how much?", 26, FADED, italic=True)
        card = VGroup(card_title, card_body, card_body2).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        card_ink = ink_card(card, pad=0.5)
        self.play(FadeIn(card_ink), run_time=0.8)
        self.play(say("Try it yourself. Tow toy boat hulls along a rain gutter and time them. "
                      "Do the longer hulls go faster, and by how much?"), run_time=0.8)
        self.vo_wait()
        self.wait(1.0)
        self.play(FadeOut(card_ink), run_time=0.8)
