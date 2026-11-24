"""I037 The Cipher That Cost a Queen Her Head, a Science Stories episode.

After S. Singh, The Code Book (1999). Script and sources: episodes/I037_script.md

Render:  manim -qh --frame_rate 30 episodes/I037_mary_cipher.py MaryCipher
Then:    scripts/finish_video.sh media/videos/I037_mary_cipher/1080p30/MaryCipher.mp4 out/I037_mary_cipher.mp4
"""
import collections
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers

GLYPH_FONT = "DejaVu Serif"
MONO = "DejaVu Sans Mono"


def note(text, size=17, color=FADED):
    return serif(text, size, color, italic=True)


def P(x, y):
    return np.array([x, y, 0.0])


def mono(text, size=20, color=INK):
    return Text(text, font=MONO, font_size=size, color=color)


def glyph(g, size=26, color=INK):
    return Text(g, font=GLYPH_FONT, font_size=size, color=color)


# ---------- data, computed and checked at render time ----------
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# English letter frequencies, per cent (Emory table; E 12.702, J+Q+X+Z = 0.472)
ENGLISH = dict(zip(ALPHA, [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025,
                           2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150,
                           1.974, 0.074]))
assert abs(sum(ENGLISH[c] for c in "JQXZ") - 0.472) < 1e-9

MESSAGE = ("THE LETTERS WERE HIDDEN IN A BEER BARREL AND CARRIED TO THE QUEEN SHE TRUSTED THE CIPHER AND THE "
           "MAN WHO BROUGHT THEM BUT EVERY LETTER WENT FIRST TO THE SECRETARY OF THE SPYMASTER WHO COUNTED THE "
           "SYMBOLS ONE BY ONE AND READ THE PLOT BEFORE THE QUEEN HERSELF")
LETTERS = [c for c in MESSAGE if c.isalpha()]
COUNTS = collections.Counter(LETTERS)
RANKED = [c for c, _ in COUNTS.most_common()]
assert len(LETTERS) == 209 and RANKED[:4] == ["E", "T", "R", "H"] and COUNTS["E"] == 42 and COUNTS["T"] == 26

GLYPHS = "αβγδεζηθικλμνξπρστφχψωΔΘΛΣ"
_perm = np.random.default_rng(1586).permutation(26)
KEY = {ALPHA[i]: GLYPHS[_perm[i]] for i in range(26)}
assert len(set(KEY.values())) == 26

N_SWAPS = math.factorial(26)
assert N_SWAPS == 403291461126605635584000000
YEARS = N_SWAPS / 1e6 / (365.25 * 24 * 3600)
assert 1.2e13 < YEARS < 1.3e13


def wrap_words(text, width=38):
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w) if cur else w
    lines.append(cur)
    return lines


def aes_counts(reps=300):
    """Real AES-128-CTR output of the demo message, counted by byte value (fixed demo key)."""
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    data = ((MESSAGE + " ") * reps).encode()
    enc = Cipher(algorithms.AES(bytes(range(16))), modes.CTR(bytes(16))).encryptor()
    out = enc.update(data) + enc.finalize()
    c = collections.Counter(out)
    return [c.get(b, 0) for b in range(256)], len(out)


AES_COUNTS, AES_LEN = aes_counts()
assert min(AES_COUNTS) > 0.75 * AES_LEN / 256 and max(AES_COUNTS) < 1.25 * AES_LEN / 256


# ---------- small drawings ----------
def barrel(scale=1.0):
    body = VMobject(fill_color="#b98a52", fill_opacity=1, stroke_color=INK, stroke_width=2)
    body.set_points_smoothly([P(-0.45, -0.65), P(-0.55, 0), P(-0.45, 0.65), P(0.45, 0.65), P(0.55, 0),
                              P(0.45, -0.65), P(-0.45, -0.65)])
    hoops = VGroup(*[Line(P(-0.5 if abs(y) < 0.4 else -0.46, y), P(0.5 if abs(y) < 0.4 else 0.46, y), color=INK,
                          stroke_width=2) for y in (-0.42, -0.14, 0.14, 0.42)])
    staves = VGroup(*[Line(P(x, -0.62), P(x * 1.12, 0), color=SEPIA, stroke_width=0.8) for x in (-0.2, 0.0, 0.2)],
                    *[Line(P(x * 1.12, 0), P(x, 0.62), color=SEPIA, stroke_width=0.8) for x in (-0.2, 0.0, 0.2)])
    return VGroup(body, staves, hoops).scale(scale)


def seal(letter="M", r=0.75):
    outer = Circle(radius=r, fill_color="#b84a3a", fill_opacity=1, stroke_color=RED_INK, stroke_width=3)
    inner = Circle(radius=r * 0.8, stroke_color=PAPER, stroke_width=1.5, stroke_opacity=0.8)
    m = serif(letter, int(48 * r / 0.75), PAPER, italic=True)
    crown = VMobject(fill_color=PAPER, fill_opacity=0.9, stroke_width=0).set_points_as_corners([
        P(-0.3, 0), P(-0.3, 0.2), P(-0.18, 0.08), P(0, 0.26), P(0.18, 0.08), P(0.3, 0.2), P(0.3, 0), P(-0.3, 0)])
    crown.scale(r / 0.75).move_to(outer.get_center() + UP * r * 0.55)
    m.move_to(outer.get_center() + DOWN * r * 0.1)
    return VGroup(outer, inner, m, crown)


def gallows(h=0.9, color=RED_INK, width=3):
    post = Line(P(0, 0), P(0, h), color=color, stroke_width=width)
    beam = Line(P(0, h), P(h * 0.55, h), color=color, stroke_width=width)
    brace = Line(P(0, h * 0.72), P(h * 0.2, h), color=color, stroke_width=width * 0.7)
    rope = Line(P(h * 0.48, h), P(h * 0.48, h * 0.7), color=color, stroke_width=width * 0.7)
    base = Line(P(-h * 0.2, 0), P(h * 0.25, 0), color=color, stroke_width=width)
    return VGroup(base, post, beam, brace, rope)


def name_card(name, sub=None, size=20):
    parts = [serif(name, size, INK)]
    if sub:
        parts.append(note(sub, size - 6))
    return ink_card(VGroup(*parts).arrange(DOWN, buff=0.06), pad=0.16)


def bar_chart(labels, values, k, width, gap, base_y, color=SEPIA, label_size=18, label_font=None):
    bars, labs = VGroup(), VGroup()
    n = len(values)
    x0 = -(n - 1) * gap / 2
    for i, (lab, v) in enumerate(zip(labels, values)):
        x = x0 + i * gap
        b = Rectangle(width=width, height=max(v * k, 0.01), fill_color=color, fill_opacity=0.85,
                      stroke_color=INK, stroke_width=0.8)
        b.move_to(P(x, base_y + b.height / 2))
        bars.add(b)
        t = Text(lab, font=label_font or SERIF, font_size=label_size, color=INK)
        t.move_to(P(x, base_y - 0.22))
        labs.add(t)
    axis = Line(P(x0 - gap * 0.7, base_y), P(-x0 + gap * 0.7, base_y), color=INK, stroke_width=1.5)
    return bars, labs, axis


class MaryCipher(NarratedScene):
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
        title = serif("The Cipher That Cost a Queen Her Head", 48).next_to(orn1, DOWN, buff=0.35)
        sub = serif("How counting letters broke a secret code", 26, FADED, italic=True).next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = note("after S. Singh, The Code Book (1999)", 16).move_to([0, -2.6, 0])
        self.vo("Science Stories. The cipher that cost a queen her head.")
        self.play(FadeIn(series, shift=DOWN * 0.1), GrowFromCenter(orn1), run_time=0.9)
        self.play(Write(title), run_time=1.3)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.vo_wait()
        self.wait(0.6)
        self.play(FadeOut(VGroup(series, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= the person and the puzzle =================
        phel = cameo("beard", 0.8).move_to(P(-4.3, 0.75))
        phel_l = VGroup(serif("Thomas Phelippes", 22, INK), note("c. 1556 – 1625 · decipherer for Walsingham", 14)
                        ).arrange(DOWN, buff=0.05).next_to(phel, DOWN, buff=0.15)
        sil_n = note("silhouette stylised, not a likeness", 13).next_to(phel_l, DOWN, buff=0.08)
        place = spaced("England · 1586", 18, SEPIA).move_to(P(1.6, 3.05))
        page_lines = wrap_words(MESSAGE, 30)[:5]
        page_txt = VGroup(*[glyph("".join(KEY.get(c, " ") for c in ln), 26) for ln in page_lines]).arrange(
            DOWN, buff=0.2, aligned_edge=LEFT)
        page = ink_card(page_txt, pad=0.35, rot=-2 * DEGREES).move_to(P(1.8, 0.75))
        page_n = note("symbols invented for this film", 13).next_to(page, DOWN, buff=0.15)
        line("England, 1586. Thomas Phelippes, codebreaker to Elizabeth's spymaster Francis Walsingham, stares at a page of strange symbols.", FadeIn(phel), FadeIn(phel_l), FadeIn(sil_n),
             FadeIn(place), run_time=1.0)
        self.play(FadeIn(page, shift=UP * 0.2), FadeIn(page_n), run_time=1.0)
        self.vo_wait()

        mary = seal("M", 0.75).move_to(P(-4.6, 0.25))
        mary_l = VGroup(serif("Mary, Queen of Scots", 20, INK), note("prisoner in England since 1568", 14)
                        ).arrange(DOWN, buff=0.05).next_to(mary, DOWN, buff=0.18)
        wal = name_card("Walsingham", "Elizabeth's spymaster", 20).move_to(P(1.1, 2.55))
        line("It is a letter for Mary, Queen of Scots. She has been a prisoner in England since 1568.",
             FadeOut(page), FadeOut(page_n), FadeOut(place), FadeOut(sil_n),
             phel.animate.scale(0.5).move_to(P(-0.9, 2.5)), FadeOut(phel_l), run_time=1.0)
        phel_s = serif("Phelippes", 16, INK).next_to(phel, LEFT, buff=0.12)
        self.play(FadeIn(mary, scale=0.8), FadeIn(mary_l), FadeIn(wal), FadeIn(phel_s), run_time=0.9)
        self.vo_wait()

        chart = spaced("Chartley", 15, SEPIA).next_to(mary, UP, buff=0.15)
        bab = name_card("Anthony Babington", None, 20).move_to(P(4.6, 0.25))
        road = DashedLine(P(-3.6, 0.25), P(3.4, 0.25), color=FADED, stroke_width=2, dash_length=0.12)
        bar1 = barrel(0.55).move_to(P(-3.0, 0.25))
        letter1 = Rectangle(width=0.32, height=0.22, fill_color=PAPER, fill_opacity=1, stroke_color=INK,
                            stroke_width=1.2).move_to(mary.get_right() + RIGHT * 0.2)
        line("Her letters travel in and out of Chartley, the house where she is held, hidden in beer barrels.",
             FadeIn(chart), Create(road), FadeIn(bab), run_time=1.0)
        self.play(FadeIn(letter1), run_time=0.4)
        self.play(letter1.animate.move_to(bar1.get_center()).scale(0.5), FadeIn(bar1), run_time=0.9)
        self.remove(letter1)
        self.play(bar1.animate.move_to(P(0.0, 0.25)), run_time=1.4)
        self.vo_wait()

        gif = VGroup(serif("courier: Gilbert Gifford", 17, INK)).next_to(bar1, DOWN, buff=0.3)
        agent = stamp(r"\text{double agent}", size=30).next_to(gif, DOWN, buff=0.2)
        up_arrow = Arrow(P(0, 0.75), wal.get_bottom() + DOWN * 0.05, color=RED_INK, stroke_width=4, buff=0.05,
                         max_tip_length_to_length_ratio=0.2)
        copy = Rectangle(width=0.32, height=0.22, fill_color=PAPER, fill_opacity=1, stroke_color=RED_INK,
                         stroke_width=1.5).move_to(P(0, 0.6))
        line("She believes they are safe. But the courier, Gilbert Gifford, is a double agent. Walsingham sees "
             "everything.", FadeIn(gif), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(agent, scale=1.3), run_time=0.6)
        self.play(GrowArrow(up_arrow), run_time=0.6)
        self.play(copy.animate.move_to(wal.get_bottom() + DOWN * 0.2), run_time=0.8)
        self.play(FadeOut(copy), Indicate(wal, color=RED_INK, scale_factor=1.06), run_time=0.6)
        self.vo_wait()

        plot = VGroup(note("the plot:", 16, RED_INK), serif("kill Elizabeth,", 18, RED_INK),
                      serif("put Mary on the throne", 18, RED_INK)).arrange(DOWN, buff=0.06)
        plot.next_to(bab, DOWN, buff=0.35)
        line("And the letters speak of a plot, led by Anthony Babington, to kill Elizabeth and put Mary on the "
             "throne.", bar1.animate.move_to(P(2.3, 0.25)), run_time=1.4)
        self.play(FadeIn(plot, lag_ratio=0.2), run_time=1.0)
        self.vo_wait()

        story = VGroup(mary, mary_l, chart, road, bar1, gif, agent, up_arrow, bab, plot)
        q = serif("Can he read them?", 40, INK).move_to(P(0.6, 0.2))
        line("To prove it, Phelippes has to read them. That is his puzzle.", FadeOut(story), run_time=0.9)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.8)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(q, phel, phel_s, wal)), run_time=0.7)

        # ================= the cipher and the obvious attack =================
        head = spaced("a substitution cipher", 18, SEPIA).move_to(P(0, 3.05))
        rows = VGroup()
        for chunk in (ALPHA[:13], ALPHA[13:]):
            top = VGroup(*[serif(c, 24, INK) for c in chunk]).arrange(RIGHT, buff=0.42)
            bot = VGroup()
            for c, t in zip(chunk, top):
                bot.add(glyph(KEY[c], 28, RED_INK).next_to(t, DOWN, buff=0.22))
            arrows = VGroup(*[Line(t.get_bottom() + DOWN * 0.03, b.get_top() + UP * 0.03, color=FADED,
                                   stroke_width=1) for t, b in zip(top, bot)])
            rows.add(VGroup(top, arrows, bot))
        rows.arrange(DOWN, buff=0.45).move_to(P(0, 1.35))
        extra = VGroup(
            VGroup(note("symbols for common words", 17, INK), serif("and", 20, INK), glyph("→ ∂", 24, RED_INK)
                   ).arrange(RIGHT, buff=0.2),
            VGroup(note("nulls, meaning nothing", 17, INK), glyph("⊕   ⊗", 24, RED_INK)).arrange(RIGHT, buff=0.25),
        ).arrange(RIGHT, buff=1.0).move_to(P(0, -1.0))
        demo_n = note("simplified; symbols invented for this film", 13).next_to(extra, DOWN, buff=0.18)
        line("Mary's cipher swaps each letter for a symbol, with extra symbols for common words, and nulls that mean nothing.", FadeIn(head), FadeIn(rows[0][0]), FadeIn(rows[1][0]), run_time=0.9)
        self.play(LaggedStart(*[AnimationGroup(Create(rows[i][1][j]), FadeIn(rows[i][2][j]))
                                for i in range(2) for j in range(13)], lag_ratio=0.06), run_time=2.2)
        self.play(FadeIn(extra[0]), run_time=0.6)
        self.play(FadeIn(extra[1]), FadeIn(demo_n), run_time=0.6)
        self.vo_wait()

        big = MathTex(r"26! = 403{,}291{,}461{,}126{,}605{,}635{,}584{,}000{,}000", font_size=40, color=INK)
        big.move_to(P(0, 1.1))
        approx = MathTex(r"\approx 4 \times 10^{26}\ \text{possible keys}", font_size=34, color=RED_INK).next_to(
            big, DOWN, buff=0.35)
        line("The obvious attack is to try every possible swap. But twenty-six letters can be scrambled in about four "
             "hundred million billion billion ways.", FadeOut(VGroup(rows, extra, demo_n)),
             head.animate.become(spaced("the obvious attack: try every key", 18, SEPIA).move_to(P(0, 3.05))),
             run_time=1.0)
        self.play(Write(big), run_time=2.0)
        self.play(FadeIn(approx, shift=UP * 0.1), run_time=0.7)
        self.vo_wait()
        t1 = VGroup(note("a million keys every second:", 20, INK),
                    serif("about 13 trillion years", 26, RED_INK)).arrange(RIGHT, buff=0.25)
        t2 = VGroup(note("the Sun has left:", 20, INK), serif("about 5 billion years", 26, INK)).arrange(RIGHT,
                                                                                                        buff=0.25)
        tt = VGroup(t1, t2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(P(0, -1.3))
        line("Check a million every second, and you would still be checking long after the Sun has burned out.",
             FadeIn(t1), run_time=0.9)
        self.play(FadeIn(t2), run_time=0.7)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(head, big, approx, tt)), run_time=0.7)

        # ================= al-Kindi =================
        tl = NumberLine(x_range=[800, 1650, 100], length=11.0, color=INK, include_numbers=True,
                        decimal_number_config={"num_decimal_places": 0, "color": INK, "group_with_commas": False},
                        font_size=20).move_to(P(0, -0.4))
        k_dot = Dot(tl.n2p(850), radius=0.09, color=RED_INK)
        p_dot = Dot(tl.n2p(1586), radius=0.09, color=BLUE_INK)
        k_lab = VGroup(serif("al-Kindi", 24, RED_INK), note("Baghdad, c. 850", 16)).arrange(DOWN, buff=0.05)
        k_lab.next_to(k_dot, UP, buff=0.35)
        p_lab = VGroup(serif("Phelippes", 22, BLUE_INK), note("1586", 16)).arrange(DOWN, buff=0.05).next_to(
            p_dot, UP, buff=0.35)
        span = BraceBetweenPoints(tl.n2p(850) + DOWN * 0.45, tl.n2p(1586) + DOWN * 0.45, DOWN, color=SEPIA)
        span_l = note("more than 700 years", 17, SEPIA).next_to(span, DOWN, buff=0.08)
        line("The trick that beats it is more than seven hundred years older than Phelippes.", Create(tl),
             run_time=1.0)
        self.play(FadeIn(p_dot), FadeIn(p_lab), FadeIn(k_dot), FadeIn(k_lab), run_time=0.8)
        self.play(GrowFromCenter(span), FadeIn(span_l), run_time=0.8)
        self.vo_wait()
        ms = VGroup(note("A Manuscript on Deciphering Cryptographic Messages", 20, INK),
                    note("the earliest known description of", 16)).arrange(DOWN, buff=0.08).move_to(P(0, 2.55))
        fa = serif("frequency analysis", 40, RED_INK).move_to(P(0, 1.65))
        line("In ninth-century Baghdad, the scholar al-Kindi wrote the earliest known description of it: frequency analysis.", Indicate(k_lab, color=RED_INK), run_time=1.0)
        self.play(FadeIn(ms, shift=DOWN * 0.1), run_time=0.8)
        self.wait(1.4)
        self.play(Write(fa), run_time=1.0)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tl, k_dot, p_dot, k_lab, p_lab, span, span_l, ms)),
                  fa.animate.scale(0.5).move_to(P(0, 3.1)), run_time=0.8)

        # ================= English letter frequencies =================
        vals = [ENGLISH[c] for c in ALPHA]
        e_bars, e_labs, e_axis = bar_chart(list(ALPHA), vals, 0.215, 0.32, 0.44, -2.15, color=SEPIA)
        e_title = note("English text: how often each letter appears (per cent)", 18, INK).move_to(P(0, 2.55))
        line("In any language, some letters turn up far more often than others.", FadeIn(e_title), Create(e_axis),
             FadeIn(e_labs), run_time=0.9)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in e_bars], lag_ratio=0.05), run_time=2.0)
        self.vo_wait()
        hi = {c: e_bars[ALPHA.index(c)] for c in "ETA"}
        e_pc = serif("12.7%  ≈ 1 in 8", 20, RED_INK).next_to(hi["E"], UP, buff=0.1)
        low = VGroup(*[e_bars[ALPHA.index(c)] for c in "JQXZ"])
        low_marks = VGroup(*[Triangle(color=BLUE_INK, fill_color=BLUE_INK, fill_opacity=1, stroke_width=0)
                             .scale(0.08).rotate(PI).next_to(e_labs[ALPHA.index(c)], UP, buff=0.32)
                             for c in "JQXZ"])
        low_l = note("J + Q + X + Z: under 1% together", 17, BLUE_INK).move_to(P(3.6, 0.6))
        line("In English text, E is about one letter in eight. T and A come next. J, Q, X and Z together make less "
             "than one percent.", hi["E"].animate.set_fill(RED_INK), run_time=0.8)
        self.play(FadeIn(e_pc), run_time=0.6)
        self.wait(1.0)
        self.play(hi["T"].animate.set_fill(RED_INK, 0.6), hi["A"].animate.set_fill(RED_INK, 0.6), run_time=0.7)
        self.wait(0.8)
        self.play(FadeIn(low_marks), FadeIn(low_l), run_time=0.8)
        self.vo_wait()
        e_lab = e_labs[ALPHA.index("E")]
        e_glyph = glyph(KEY["E"], 22, RED_INK).move_to(e_lab)
        same = note("same height, new name", 17, RED_INK).next_to(e_pc, UP, buff=0.12)
        line("A swap changes how each letter looks. It does not change how often it appears.", run_time=0.6)
        self.play(Transform(e_lab, e_glyph), run_time=0.9)
        self.play(FadeIn(same), run_time=0.5)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(e_bars, e_labs, e_axis, e_title, e_pc, low_marks, low_l, same)),
                  run_time=0.7)

        # ================= the demonstration =================
        rows_txt = wrap_words(MESSAGE, 46)
        cw, rh = 0.25, 0.38
        grid_cells = []          # (letter, mobject)
        grid = VGroup()
        for r, ln in enumerate(rows_txt):
            x0 = -len(ln) * cw / 2 + cw / 2
            for i, ch in enumerate(ln):
                if ch == " ":
                    continue
                m = glyph(KEY[ch], 22, INK).move_to(P(x0 + i * cw, 2.95 - r * rh))
                grid_cells.append((ch, m, r, i))
                grid.add(m)
        assert len(rows_txt) <= 6 and max(len(x) for x in rows_txt) * cw < 12.2
        msg_n = note(f"{len(LETTERS)} letters, word gaps kept to make the demo quicker", 13).move_to(P(0, 0.66))
        line("So here is a short message, about two hundred letters, enciphered with a secret swap.",
             FadeIn(grid, lag_ratio=0.004), fa.animate.set_opacity(0), run_time=2.0)
        self.play(FadeIn(msg_n), run_time=0.5)
        self.vo_wait()

        counts = [COUNTS[c] for c in RANKED]
        c_bars, c_labs, c_axis = bar_chart([KEY[c] for c in RANKED], counts, 0.045, 0.4, 0.52, -1.95, color=SEPIA,
                                           label_size=20, label_font=GLYPH_FONT)
        c_nums = VGroup(*[mono(str(v), 13, FADED).next_to(b, UP, buff=0.05) for v, b in zip(counts, c_bars)])
        # unsorted first (alphabetical by symbol), then sort
        order0 = sorted(range(len(RANKED)), key=lambda i: KEY[RANKED[i]])
        xs_sorted = [b.get_center()[0] for b in c_bars]
        for pos, i in enumerate(order0):
            dx = xs_sorted[pos] - xs_sorted[i]
            c_bars[i].shift(RIGHT * dx)
            c_labs[i].shift(RIGHT * dx)
            c_nums[i].shift(RIGHT * dx)
        line("Count every symbol. Then sort the counts.", Create(c_axis), FadeIn(c_labs), run_time=0.8)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in c_bars], lag_ratio=0.04), FadeIn(c_nums),
                  run_time=1.4)
        self.play(*[VGroup(c_bars[i], c_labs[i], c_nums[i]).animate.shift(RIGHT * (xs_sorted[i] - c_bars[i].get_center()[0]))
                    for i in range(len(RANKED))], run_time=1.4)
        self.vo_wait()

        def guess(i, text, color=RED_INK):
            return serif(text, 22, color).next_to(c_labs[i], DOWN, buff=0.08)

        gE, gT = guess(0, "E"), guess(1, "T")
        gA = serif("A?", 22, BLUE_INK).next_to(c_nums[2], UP, buff=0.1)
        line("The tallest bar is almost certainly E. The next is probably T.", run_time=0.6)
        self.play(c_bars[0].animate.set_fill(RED_INK), FadeIn(gE), run_time=0.7)
        self.wait(0.6)
        self.play(c_bars[1].animate.set_fill(RED_INK, 0.7), FadeIn(gT), run_time=0.7)
        self.vo_wait()
        wob = note("short message: the ranks wobble", 17, BLUE_INK).move_to(P(3.3, -0.3))
        line("After that, short messages wobble. Every guess must be tested on real words.", FadeIn(gA), run_time=0.8)
        self.play(Wiggle(VGroup(c_bars[2], c_bars[3], c_bars[4], c_bars[5]), scale_value=1.05), FadeIn(wob),
                  run_time=1.2)
        self.vo_wait()

        def reveal(letters, color=RED_INK):
            anims = []
            for ch, m, r, i in grid_cells:
                if ch in letters:
                    anims.append(Transform(m, serif(ch, 22, color).move_to(m.get_center())))
            return anims

        line("Put in E and T.", *reveal("ET"), run_time=1.2)
        # whole-word THE occurrences
        boxes = VGroup()
        for r, ln in enumerate(rows_txt):
            x0 = -len(ln) * cw / 2 + cw / 2
            pos = 0
            for w in ln.split(" "):
                if w == "THE":
                    boxes.add(SurroundingRectangle(VGroup(*[Dot(P(x0 + (pos + j) * cw, 2.95 - r * rh), radius=0.1)
                                                            for j in range(3)]), color=BLUE_INK, buff=0.04,
                                                   stroke_width=2))
                pos += len(w) + 1
        n_the = len(boxes)
        assert n_the == 9
        self.vo_wait()
        line("One three-symbol word, T, something, E, keeps coming back. It must be THE. Now we have H.",
             Create(boxes, lag_ratio=0.15), run_time=1.4)
        self.wait(1.6)
        gH = guess(3, "H")
        self.play(*reveal("H"), FadeIn(gH), FadeOut(gA), FadeOut(wob), run_time=1.0)
        self.vo_wait()
        rest_order = [c for c in RANKED if c not in "ETH"]
        line("Each new letter unlocks more words, like a crossword, until the message reads itself.",
             FadeOut(boxes), run_time=0.6)
        groups = [rest_order[i:i + 4] for i in range(0, len(rest_order), 4)]
        g_rest = VGroup()
        for g in groups:
            gg = VGroup(*[guess(RANKED.index(c), c, INK) for c in g])
            g_rest.add(gg)
            self.play(*reveal(g, INK), FadeIn(gg), run_time=0.7)
        self.vo_wait()
        singh = ink_card(VGroup(note("S. Singh, The Code Book (1999):", 17, INK),
                                serif("Phelippes broke Mary's cipher this way", 22, RED_INK)).arrange(DOWN, buff=0.08),
                         pad=0.22).move_to(P(3.3, -0.3))
        line("According to Simon Singh's The Code Book, this is how Phelippes broke Mary's cipher.",
             FadeIn(singh, shift=UP * 0.1), run_time=0.9)
        self.vo_wait()
        demo_all = VGroup(grid, msg_n, c_bars, c_labs, c_axis, c_nums, gE, gT, gH, g_rest)
        self.play(clear(), FadeOut(demo_all), FadeOut(singh), run_time=0.8)
        self.remove(fa)

        # ================= the gallows letter and the end of the plot =================
        letter_lines = VGroup(*[glyph("".join(KEY.get(c, " ") for c in ln), 18, INK)
                                for ln in wrap_words(MESSAGE[60:200], 24)[:4]]).arrange(DOWN, buff=0.14,
                                                                                         aligned_edge=LEFT)
        mletter = ink_card(letter_lines, pad=0.3).move_to(P(-3.0, 1.55))
        mlab = VGroup(serif("Mary to Babington", 20, INK), note("17 July 1586", 16)).arrange(DOWN, buff=0.04)
        mlab.next_to(mletter, UP, buff=0.12)
        illus = note("letter shown as an illustration", 12).next_to(mletter, DOWN, buff=0.08)
        line("In July 1586, Mary answered Babington. Her letter agreed to the plot.", FadeIn(mletter, shift=UP * 0.1),
             FadeIn(mlab), FadeIn(illus), run_time=1.0)
        self.vo_wait()
        gal = gallows(0.75).next_to(mletter, RIGHT, buff=0.25).align_to(mletter, UP)
        line("When Phelippes deciphered it, he drew a small gallows on the outside.", run_time=0.6)
        self.play(Create(gal), run_time=1.6)
        self.vo_wait()
        ps = ink_card(VGroup(serif("P.S.", 20, RED_INK, italic=True), note("forged, in Mary's cipher:", 14, RED_INK),
                             serif("the names of the six?", 19, INK)).arrange(DOWN, buff=0.05), pad=0.18,
                      rot=3 * DEGREES).next_to(mletter, RIGHT, buff=1.5)
        line("Then a postscript was forged in Mary's cipher, asking Babington for the names of the six men who would "
             "kill the queen.", FadeIn(ps, shift=LEFT * 0.2), run_time=1.0)
        self.vo_wait()

        months = [("Jul", 0), ("Aug", 31), ("Sep", 62), ("Oct", 92), ("Nov", 123), ("Dec", 153), ("Jan", 184),
                  ("Feb", 215)]

        def day(m, d):
            base = dict(months)[m] - 16       # day 0 = 17 July 1586
            return base + d - 1 if m != "Jul" else d - 17

        X0, X1 = -6.0, 6.0
        span_days = day("Feb", 8) + 6

        def tx(dd):
            return X0 + (X1 - X0) * (dd + 3) / (span_days + 3)

        tline = Line(P(X0, -1.35), P(X1, -1.35), color=INK, stroke_width=2)
        ticks = VGroup()
        for m, _ in months:
            x = tx(day(m, 1)) if m != "Jul" else tx(day("Jul", 17))
            ticks.add(Line(P(x, -1.42), P(x, -1.28), color=INK, stroke_width=1.2))
            ticks.add(note(m if m != "Jan" else "Jan 1587", 13, FADED).move_to(P(x, -1.62)))

        def event(dd, text, up=True, color=INK):
            x = tx(dd)
            d = Dot(P(x, -1.35), radius=0.07, color=color)
            lab = serif(text, 15, color)
            lab.move_to(P(x, -0.95 if up else -2.0))
            return VGroup(d, lab)

        ev_letter = event(0, "Mary's letter", up=True, color=RED_INK)
        ev_arrest = event(day("Aug", 3), "Babington's arrest ordered", up=False)
        ev_exec = event(day("Sep", 20), "Babington executed", up=True)
        ev_trial = event(day("Oct", 25), "Mary convicted, Fotheringhay", up=False)
        ev_mary = event(day("Feb", 8), "Mary executed", up=True, color=RED_INK)
        ev_mary[1].shift(LEFT * 0.35)
        line("Babington was arrested in August, and executed in September.", Create(tline), FadeIn(ticks),
             FadeIn(ev_letter), run_time=1.0)
        self.play(FadeIn(ev_arrest), run_time=0.6)
        self.play(FadeIn(ev_exec), run_time=0.6)
        self.vo_wait()
        line("Mary was tried at Fotheringhay in October, found guilty, and executed there on the eighth of February "
             "1587.", FadeIn(ev_trial), run_time=1.0)
        self.wait(1.6)
        self.play(FadeIn(ev_mary), run_time=0.8)
        self.vo_wait()
        debate = note("debated: how far Walsingham's agents steered the plot", 16, BLUE_INK).move_to(P(2.3, 2.95))
        line("Historians still argue over how far Walsingham's agents steered the plot. But the cipher protected no "
             "one.", FadeIn(debate), run_time=0.9)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(mletter, mlab, illus, gal, ps, tline, ticks, ev_letter, ev_arrest, ev_exec,
                                          ev_trial, ev_mary, debate)), run_time=0.8)

        # ================= the lesson =================
        pl_bars, pl_labs, pl_axis = bar_chart(list(ALPHA), [COUNTS.get(c, 0) for c in ALPHA], 0.05, 0.16, 0.21,
                                              0.3, color=SEPIA, label_size=11)
        ci_bars, ci_labs, ci_axis = bar_chart([KEY[c] for c in ALPHA], [COUNTS.get(c, 0) for c in ALPHA], 0.05,
                                              0.16, 0.21, 0.3, color=RED_INK, label_size=12, label_font=GLYPH_FONT)
        left = VGroup(pl_bars, pl_labs, pl_axis).shift(LEFT * 3.3)
        right = VGroup(ci_bars, ci_labs, ci_axis).shift(RIGHT * 3.3)
        lt = note("the message", 17, INK).next_to(left, UP, buff=0.2)
        rt = note("after the swap: the same bars, renamed", 17, RED_INK).next_to(right, UP, buff=0.2)
        moral = serif("A simple swap hides each letter, not the pattern of the language.", 26, INK).move_to(
            P(0, -1.3))
        line("A simple swap hides each letter, but not the pattern of the language.", FadeIn(left), FadeIn(lt), run_time=0.8)
        self.play(TransformFromCopy(left, right), FadeIn(rt), run_time=1.4)
        self.play(FadeIn(moral, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        self.wait(1.2)
        self.play(clear(), FadeOut(VGroup(left, right, lt, rt, moral)), run_time=0.7)

        # ================= 2023 =================
        yr = spaced("2023", 22, SEPIA).move_to(P(0, 3.0))
        names = VGroup(name_card("George Lasry", None, 19), name_card("Norbert Biermann", None, 19),
                       name_card("Satoshi Tomokiyo", None, 19)).arrange(RIGHT, buff=0.4).move_to(P(0, 2.1))
        found = VGroup(serif("57 letters by Mary, 1578 – 1584", 24, RED_INK),
                       note("found among Italian papers in the National Library of France · published in "
                            "Cryptologia", 16)).arrange(DOWN, buff=0.08).move_to(P(0, 1.0))
        line("And Mary's ciphers are still being broken. In 2023, George Lasry, Norbert Biermann and Satoshi Tomokiyo deciphered more than fifty of her lost letters, misfiled in a French library.", FadeIn(yr), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in names], lag_ratio=0.4), run_time=1.8)
        self.wait(1.5)
        self.play(FadeIn(found), run_time=0.8)
        self.vo_wait()
        ax = Axes(x_range=[0, 100, 25], y_range=[0, 1, 0.5], x_length=5.0, y_length=1.9, tips=False,
                  axis_config={"color": INK, "stroke_width": 1.5, "include_ticks": False}).move_to(P(-2.6, -1.3))
        ax_x = note("keys tried", 14).next_to(ax, DOWN, buff=0.08)
        ax_y = note("looks like language", 14).rotate(PI / 2).next_to(ax, LEFT, buff=0.08)
        rng = np.random.default_rng(7)
        ys, y = [], 0.08
        for i in range(101):
            y = min(0.95, y + max(0.0, rng.normal(0.012, 0.02)) * (1 - y) * 1.6)
            ys.append(y)
        hill = VMobject(color=RED_INK, stroke_width=3).set_points_as_corners([ax.c2p(i, v) for i, v in enumerate(ys)])
        hill_n = note("illustration of a hill-climbing search", 13).next_to(ax, UP, buff=0.08)
        split = VGroup(serif("computer: about 30%", 20, RED_INK), serif("by hand: the rest", 20, INK)).arrange(
            DOWN, buff=0.15, aligned_edge=LEFT).move_to(P(3.2, -1.25))
        line("A computer tried key after key, keeping changes that made the text look more like language. The rest they solved by hand.", Create(ax), FadeIn(ax_x), FadeIn(ax_y), FadeIn(hill_n),
             run_time=0.9)
        self.play(Create(hill), run_time=2.4)
        self.play(FadeIn(split[0]), run_time=0.5)
        self.wait(0.6)
        self.play(FadeIn(split[1]), run_time=0.5)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(yr, names, found, ax, ax_x, ax_y, hill, hill_n, split)), run_time=0.7)

        # ================= modern ciphers =================
        m_left_bars, m_left_labs, m_left_axis = bar_chart(list(ALPHA), [COUNTS.get(c, 0) for c in ALPHA], 0.05,
                                                          0.16, 0.21, -1.6, color=SEPIA, label_size=11)
        mleft = VGroup(m_left_bars, m_left_labs, m_left_axis).shift(LEFT * 3.3)
        mean = AES_LEN / 256
        aes_bars = VGroup()
        for b, v in enumerate(AES_COUNTS):
            r = Rectangle(width=0.018, height=v / mean * 1.0, fill_color=BLUE_INK, fill_opacity=0.9, stroke_width=0)
            r.move_to(P(0.7 + b * 0.0215 + 0.009, -1.6 + r.height / 2))
            aes_bars.add(r)
        aes_axis = Line(P(0.6, -1.6), P(6.3, -1.6), color=INK, stroke_width=1.5)
        aes_lab = note("all 256 byte values", 13).next_to(aes_axis, DOWN, buff=0.12)
        mt1 = note("plain English letters", 17, INK).move_to(P(-3.3, 1.35))
        mt2 = note("the same text through AES, counted", 17, BLUE_INK).move_to(P(3.45, 1.35))
        flat = serif("flat: nothing to grab", 22, BLUE_INK).move_to(P(3.45, 0.35))
        line("Modern ciphers make every symbol turn up about equally often. Count them, and you learn almost nothing.", FadeIn(mleft), FadeIn(mt1), run_time=0.9)
        self.play(Create(aes_axis), FadeIn(mt2), LaggedStart(*[GrowFromEdge(r, DOWN) for r in aes_bars],
                                                             lag_ratio=0.004), FadeIn(aes_lab), run_time=1.6)
        self.play(FadeIn(flat), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(mleft, mt1, mt2, aes_bars, aes_axis, aes_lab, flat)), run_time=0.7)

        # ================= try it yourself =================
        tiy = spaced("Try it yourself", 22, RED_INK).move_to(P(0, 2.95))
        steps = VGroup(
            serif("1.  A friend enciphers about 200 letters with a secret swap.", 24, INK),
            serif("2.  Count every symbol and rank them.", 24, INK),
            serif("3.  Guess E and T first.", 24, INK),
            serif("4.  Hunt for THE, then let the words do the rest.", 24, INK),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(P(-0.6, 0.85))
        tally = VGroup(*[VGroup(glyph(KEY[c], 28, INK), mono("|" * (COUNTS[c] // 3), 20, SEPIA)).arrange(
            RIGHT, buff=0.25) for c in RANKED[:4]]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        tally.move_to(P(-0.6, -1.85)).align_to(steps, LEFT)
        tally_n = note("tally, one stroke per 3", 12).next_to(tally, UP, buff=0.08)
        line("Try it yourself. Have a friend encipher about two hundred letters with a secret swap.",
             FadeIn(tiy), FadeIn(steps[0]), run_time=0.9)
        self.vo_wait()
        line("Count the symbols, guess E and T, then hunt for THE, and let the words do the rest.", FadeIn(steps[1]), FadeIn(tally), FadeIn(tally_n), run_time=0.9)
        self.wait(1.2)
        self.play(FadeIn(steps[2]), run_time=0.6)
        self.wait(0.8)
        self.play(FadeIn(steps[3]), run_time=0.6)
        self.vo_wait()
        self.play(clear(), FadeOut(VGroup(tiy, steps, tally, tally_n)), run_time=0.7)

        # ================= close =================
        s2 = seal("M", 0.6).move_to(P(-1.2, 1.4))
        g2 = gallows(1.0).move_to(P(1.2, 1.4))
        last = serif("One queen, one cipher, and a codebreaker who counted.", 32, INK).move_to(P(0, -0.3))
        line("One queen, one cipher, and a codebreaker who counted.", FadeIn(s2), run_time=0.8)
        self.play(Create(g2), FadeIn(last, shift=UP * 0.1), run_time=1.2)
        self.vo_wait()
        self.wait(0.6)
        self.play(clear(), FadeOut(VGroup(s2, g2, last)), run_time=0.8)

        end = VGroup(serif("Science Stories", 40, INK),
                     ornament(2.6),
                     note("story after S. Singh, The Code Book (1999) · sources in the episode notes", 17),
                     note("facts checked against the British Library, NSA (To Catch a Queen), Britannica, Wikipedia, "
                          "History of Information, NPR and Smithsonian", 17),
                     note("silhouette and cipher symbols invented · letter counts and AES histogram computed · Manim · "
                          "synthetic narration", 15)
                     ).arrange(DOWN, buff=0.22).move_to([0, 0.3, 0])
        for m in end:
            if m.width > 12.8:
                m.scale_to_fit_width(12.8)
        self.play(FadeIn(end, lag_ratio=0.15), run_time=1.4)
        self.wait(3.0)
        self.play(FadeOut(end), FadeOut(frame), run_time=1.0)
