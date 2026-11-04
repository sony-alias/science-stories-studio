"""Science Stories style kit, plus the four Worlds of Flow plates built with it.

Worlds of Flow, Plate I: d'Alembert's Paradox.

An archival-style explainer: why ideal-fluid theory predicts zero drag on a
cylinder, and why every real body feels drag anyway.

Render:  manim -pqh worlds_of_flow.py DAlembertParadox
"""
from manim import *
import numpy as np
import hashlib
import os
import re

# =====================================================================
# Narration: offline neural text-to-speech (Kokoro), timed into each scene
# =====================================================================
# Needs:  pip install kokoro-onnx soundfile
# and the two model files from https://github.com/thewh1teagle/kokoro-onnx/releases (model-files-v1.0):
#   kokoro-v1.0.onnx  and  voices-v1.0.bin   in a folder named "kokoro" next to this script
#   (or point the KOKORO_DIR environment variable at them).
# Set NARRATE = False to render silent versions with the original timing.
NARRATE = True
VOICE, VOICE_LANG, VOICE_SPEED = "af_heart", "en-us", 0.95
_HERE = os.path.dirname(os.path.abspath(__file__))
KOKORO_DIR = os.environ.get("KOKORO_DIR") or next(
    (d for d in (os.path.join(_HERE, "kokoro"), os.path.join(_HERE, "..", "kokoro")) if os.path.isdir(d)),
    os.path.join(_HERE, "kokoro"))
VO_CACHE = os.path.join(_HERE, "narration_cache")

# exact pronunciations (IPA) for names the voice would otherwise guess at
PRONOUNCE = {
    "Jean le Rond d'Alembert": "ʒˈɑːn lə ɹˈɔːn dˌælɑːmbˈɛɹ",
    "d'Alembert": "dˌælɑːmbˈɛɹ",
    "D'Alembert": "dˌælɑːmbˈɛɹ",
    "Bernoulli's": "bɚnˈuːliz",
    "Bernoulli": "bɚnˈuːli",
    "Prandtl's": "pɹˈɑːntəlz",
    "Prandtl": "pɹˈɑːntəl",
    "d'Alembert's": "dˌælɑːmbˈɛɹz",
    "Blasius": "blˈɑːziəs",
    "Sommerfeld": "zˈɔmɚfɛlt",
    "Osborne": "ˈɑːzbɔːɹn",
    "Helmholtz's": "hˈɛlmhoʊltsɪz",
    "Helmholtz": "hˈɛlmhoʊlts",
    "Navier-Stokes": "nɑːvjˈeɪ stˈoʊks",
    "Navier": "nɑːvjˈeɪ",
    "Claude-Louis": "klˈoʊd lwˈiː",
    "Kutta": "kˈʊtɑː",
    "Joukowski": "ʒukˈɔfski",
    "Kutta-Joukowski": "kˈʊtɑː ʒukˈɔfski",
    # words spelled the same but said differently by meaning (the voice guesses these wrong)
    "presents a paper": "pɹɪzˈɛnts ɐ pˈeɪpɚ",
    "tears away": "tˈɛɹz ɐwˈeɪ",
    "Close a vortex tube": "klˈoʊz ɐ vˈɔːɹtɛks tˈuːb",
    "laws live on": "lˈɔːz lˈɪv ˌɔn",
    "lives forever": "lˈɪvz fɚɹˈɛvɚ",
}
_kokoro = None

# ---------- language: WOF_LANG=ml renders the Malayalam version ----------
LANG = os.environ.get("WOF_LANG", "en")
ML_FONT = "Noto Sans Malayalam"
ML_VOICE_DIR = os.environ.get("ML_VOICE_DIR", os.path.join(_HERE, "ml_voice"))   # a Piper ml_IN voice folder

ML = {
    # ----- Plate I: on-screen text -----
    "Plate I": "ഫലകം ഒന്ന്",
    "D'Alembert's Paradox": "ഡാലംബേറിന്റെ വിരോധാഭാസം",
    "Why the mathematics said a body in a moving fluid feels no drag":
        "ഒഴുകുന്ന ദ്രവത്തിലെ വസ്തുവിന് പ്രതിരോധമേ ഇല്ലെന്ന് ഗണിതം പറഞ്ഞതെന്തുകൊണ്ട്?",
    "after the history of hydrodynamics in O. Darrigol, Worlds of Flow (Oxford, 2005)":
        "ആധാരം: O. Darrigol, Worlds of Flow (Oxford, 2005) എന്ന ദ്രവഗതിശാസ്ത്ര ചരിത്രഗ്രന്ഥം",
    "Jean le Rond d'Alembert": "ഷാൻ ലെ റോൺ ഡാലംബേർ",
    "Paris · 1752": "പാരീസ് · 1752",
    "Armed with the new calculus of fluids,": "ദ്രവങ്ങളുടെ പുതിയ കലനശാസ്ത്രവുമായി,",
    "d'Alembert asks a deceptively simple question:": "ഡാലംബേർ ലളിതമെന്നു തോന്നുന്ന ഒരു ചോദ്യം ചോദിക്കുന്നു:",
    "“How hard does a flowing fluid push on a body?”": "“ഒഴുകുന്ന ദ്രവം ഒരു വസ്തുവിനെ എത്ര ശക്തിയായി തള്ളും?”",
    "1752 · d'Alembert's essay on fluid resistance": "1752 · ദ്രവപ്രതിരോധത്തെക്കുറിച്ചുള്ള ഡാലംബേറിന്റെ പ്രബന്ധം",
    "The Ideal Fluid": "ആദർശ ദ്രവം",
    "no viscosity, no friction: the fluid of the mathematicians": "ശ്യാനതയില്ല, ഘർഷണമില്ല: ഗണിതജ്ഞരുടെ ദ്രവം",
    "pushes": "തള്ളുന്നു",
    "pulls (suction)": "വലിക്കുന്നു",
    "“… a singular paradox which I leave": "“… ഭാവിയിലെ ജ്യാമിതിജ്ഞർക്ക് വിശദീകരിക്കാൻ",
    "to future geometers to elucidate.”": "ഞാൻ വിട്ടുകൊടുക്കുന്ന ഒരു വിചിത്ര വിരോധാഭാസം.”",
    "Jean le Rond d'Alembert, Opuscules mathématiques, 1768": "ഷാൻ ലെ റോൺ ഡാലംബേർ, Opuscules mathématiques, 1768",
    "Theory": "സിദ്ധാന്തം",
    "the ideal fluid of 1752": "1752-ലെ ആദർശ ദ്രവം",
    "Reality": "യാഥാർത്ഥ്യം",
    "water and air as they actually behave": "വെള്ളവും വായുവും യഥാർത്ഥത്തിൽ പെരുമാറുന്നതുപോലെ",
    "flow breaks away": "ഒഴുക്ക് വേർപെടുന്നു",
    "pressures: typical measurements, drawn qualitatively": "മർദ്ദം: സാധാരണ അളവുകൾ, ഏകദേശരൂപത്തിൽ വരച്ചത്",
    "Ludwig Prandtl": "ലുഡ്‌വിഗ് പ്രാൻഡ്റ്റൽ",
    "Heidelberg · 1904": "ഹൈഡൽബർഗ് · 1904",
    "For a century and a half the paradox stood,": "ഒന്നര നൂറ്റാണ്ട് ഈ വിരോധാഭാസം നിലനിന്നു,",
    "until Prandtl found the culprit:": "ഒടുവിൽ പ്രാൻഡ്റ്റൽ കാരണം കണ്ടെത്തി:",
    "a thin layer of fluid clinging to every surface,": "എല്ലാ പ്രതലങ്ങളിലും പറ്റിപ്പിടിക്കുന്ന ദ്രവത്തിന്റെ നേർത്ത പാളി,",
    "where friction can never be ignored.": "അവിടെ ഘർഷണത്തെ ഒരിക്കലും അവഗണിക്കാനാവില്ല.",
    "1768 · the paradox restated": "1768 · വിരോധാഭാസം വീണ്ടും",
    "1904 · Prandtl's boundary layer": "1904 · പ്രാൻഡ്റ്റലിന്റെ അതിർത്തി പാളി",
    "≈ 150 years": "≈ 150 വർഷം",
    "Next · Plate II · The Boundary Layer": "അടുത്തത് · ഫലകം രണ്ട് · അതിർത്തി പാളി",
    # ----- Plate I: narration (spoken by the voice and shown as subtitles) -----
    "Worlds of Flow. Plate one: d'Alembert's paradox. Why the mathematics once said that a body in a moving fluid feels no drag at all.":
        "വേൾഡ്‌സ് ഓഫ് ഫ്ലോ. ഫലകം ഒന്ന്: ഡാലംബേറിന്റെ വിരോധാഭാസം. ഒഴുകുന്ന ദ്രവത്തിലുള്ള ഒരു വസ്തുവിന് "
        "യാതൊരു പ്രതിരോധവും അനുഭവപ്പെടില്ലെന്ന് ഗണിതശാസ്ത്രം ഒരിക്കൽ പറഞ്ഞത് എന്തുകൊണ്ടാണ്?",
    "Paris, 1752. Armed with the new calculus of fluids, Jean le Rond d'Alembert asks a deceptively simple question: how hard does a flowing fluid push on a body?":
        "പാരീസ്, 1752. ദ്രവങ്ങളുടെ പുതിയ കലനശാസ്ത്രവുമായി, ഷാൻ ലെ റോൺ ഡാലംബേർ ലളിതമെന്നു തോന്നുന്ന "
        "ഒരു ചോദ്യം ചോദിക്കുന്നു: ഒഴുകുന്ന ഒരു ദ്രവം ഒരു വസ്തുവിനെ എത്ര ശക്തിയായി തള്ളും?",
    "Imagine a long cylinder held still in a steady stream of a perfect fluid, one with no friction at all.":
        "ഒട്ടും ഘർഷണമില്ലാത്ത ഒരു സമ്പൂർണ ദ്രവത്തിന്റെ സ്ഥിരമായ ഒഴുക്കിൽ, അനങ്ങാതെ പിടിച്ചുനിർത്തിയ ഒരു നീണ്ട സിലിണ്ടർ സങ്കൽപ്പിക്കുക.",
    "The equations of ideal flow give an exact answer: the streamlines bend smoothly around the body.":
        "ആദർശ പ്രവാഹത്തിന്റെ സമവാക്യങ്ങൾ കൃത്യമായ ഉത്തരം തരുന്നു: ഒഴുക്കുരേഖകൾ വസ്തുവിനു ചുറ്റും സുഗമമായി വളയുന്നു.",
    "Bernoulli's principle tells us that where the fluid speeds up, its pressure drops.":
        "ദ്രവത്തിന്റെ വേഗം കൂടുന്നിടത്ത് അതിന്റെ മർദ്ദം കുറയുമെന്ന് ബെർണൂലിയുടെ തത്വം പറയുന്നു.",
    "But the pressure in front of the cylinder is a perfect mirror of the pressure behind it…":
        "പക്ഷേ സിലിണ്ടറിന്റെ മുന്നിലെ മർദ്ദം, പിന്നിലെ മർദ്ദത്തിന്റെ കൃത്യമായ കണ്ണാടിപ്രതിബിംബമാണ്…",
    "…so every push from the front is cancelled by an equal push from behind. The total drag is exactly zero.":
        "…അതിനാൽ മുന്നിൽ നിന്നുള്ള ഓരോ തള്ളലിനെയും പിന്നിൽ നിന്നുള്ള തുല്യമായ ഒരു തള്ളൽ റദ്ദാക്കുന്നു. "
        "ആകെ പ്രതിരോധം കൃത്യം പൂജ്യം.",
    "D'Alembert could find no error. Sixteen years later he called it a singular paradox, and left it to future geometers to explain.":
        "ഡാലംബേറിന് ഒരു തെറ്റും കണ്ടെത്താനായില്ല. പതിനാറു വർഷം കഴിഞ്ഞ് അദ്ദേഹം ഇതിനെ ഒരു വിചിത്ര "
        "വിരോധാഭാസം എന്നു വിളിച്ചു, വിശദീകരണം ഭാവിയിലെ ജ്യാമിതിജ്ഞർക്കു വിട്ടുകൊടുത്തു.",
    "Yet every river, every ship and every cannonball feels drag.":
        "എന്നിട്ടും ഓരോ നദിയും, ഓരോ കപ്പലും, ഓരോ പീരങ്കിയുണ്ടയും പ്രതിരോധം അനുഭവിക്കുന്നു.",
    "Behind a real body the flow breaks away, leaving a low-pressure wake that holds the body back.":
        "യഥാർത്ഥ വസ്തുവിനു പിന്നിൽ ഒഴുക്ക് വേർപെട്ടുപോകുന്നു; അവിടെ രൂപപ്പെടുന്ന താഴ്ന്ന മർദ്ദമുള്ള "
        "ചുഴിപ്പാത വസ്തുവിനെ പിന്നോട്ടു വലിക്കുന്നു.",
    "For a century and a half the paradox stood, until, in 1904, Ludwig Prandtl found the culprit: a thin layer of fluid clinging to every surface, where friction can never be ignored.":
        "ഒന്നര നൂറ്റാണ്ടോളം ഈ വിരോധാഭാസം നിലനിന്നു. ഒടുവിൽ 1904-ൽ ലുഡ്‌വിഗ് പ്രാൻഡ്റ്റൽ കാരണം കണ്ടെത്തി: "
        "എല്ലാ പ്രതലങ്ങളിലും പറ്റിപ്പിടിക്കുന്ന ദ്രവത്തിന്റെ ഒരു നേർത്ത പാളി, അവിടെ ഘർഷണത്തെ ഒരിക്കലും അവഗണിക്കാനാവില്ല.",
    "Next, in plate two: the boundary layer.": "അടുത്തതായി, ഫലകം രണ്ട്: അതിർത്തി പാളി.",
}


# spoken-only rewrites for the Malayalam voice (the subtitle keeps the written form)
ML_SPOKEN = {"1904-ൽ": "ആയിരത്തി തൊള്ളായിരത്തി നാലിൽ"}


def tr(text):
    """The text in the current language (falls back to English where no translation exists)."""
    return ML.get(text, text) if LANG == "ml" else text


def is_ml(text):
    return any("ഀ" <= ch <= "ൿ" for ch in text)


_ml = None


def _ml_voice():
    global _ml
    if _ml is None:
        import json
        import onnxruntime as ort
        import espeakng_loader
        from phonemizer.backend import EspeakBackend
        from phonemizer.backend.espeak.wrapper import EspeakWrapper
        name = [f for f in os.listdir(ML_VOICE_DIR) if f.endswith(".onnx")][0]
        cfg = json.load(open(os.path.join(ML_VOICE_DIR, name + ".json")))
        EspeakWrapper.set_library(espeakng_loader.get_library_path())
        EspeakWrapper.set_data_path(os.path.join(ML_VOICE_DIR, "espeak-ng-data"))
        be = EspeakBackend(cfg["espeak"]["voice"], preserve_punctuation=True, with_stress=True,
                           punctuation_marks=';:,.!?¡¿—…"«»“”()')
        sess = ort.InferenceSession(os.path.join(ML_VOICE_DIR, name), providers=["CPUExecutionProvider"])
        _ml = (cfg, be, sess, name)
    return _ml


def speak_ml(text, length_scale=1.05):
    """Malayalam narration with a Piper neural voice (espeak-ng phonemes -> VITS). Cached."""
    import numpy as np
    import soundfile as sf
    cfg, be, sess, name = _ml_voice()
    for k, v in ML_SPOKEN.items():
        text = text.replace(k, v)
    ph = be.phonemize([text.replace("…", ", ")], strip=True)[0]
    key = hashlib.sha1(f"ml|{name}|{length_scale}|{ph}".encode()).hexdigest()[:16]
    path = os.path.join(VO_CACHE, f"ml_{key}.wav")
    if not os.path.exists(path):
        os.makedirs(VO_CACHE, exist_ok=True)
        m = cfg["phoneme_id_map"]
        ids = [m["^"][0], m["_"][0]]
        for ch in ph:
            if ch in m:
                ids += [m[ch][0], m["_"][0]]
        ids.append(m["$"][0])
        inf = cfg["inference"]
        x = np.array([ids], dtype=np.int64)
        audio = sess.run(None, {"input": x, "input_lengths": np.array([x.shape[1]], dtype=np.int64),
                                "scales": np.array([inf["noise_scale"], length_scale, inf["noise_w"]],
                                                   dtype=np.float32)})[0].squeeze()
        sf.write(path, audio, cfg["audio"]["sample_rate"])
    info = sf.info(path)
    return path, info.frames / info.samplerate


def _tts():
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(os.path.join(KOKORO_DIR, "kokoro-v1.0.onnx"), os.path.join(KOKORO_DIR, "voices-v1.0.bin"))
    return _kokoro


def _phonemes(text):
    k = _tts()
    keys = sorted(PRONOUNCE, key=len, reverse=True)
    parts = re.split("(" + "|".join(re.escape(x) for x in keys) + ")", text)
    out = []
    for part in parts:
        if not part:
            continue
        if part in PRONOUNCE:
            out.append(PRONOUNCE[part])
        elif part.strip():
            out.append(k.tokenizer.phonemize(part, VOICE_LANG))
    return " ".join(out)


_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _two(n):
    return _ONES[n] if n < 20 else _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])


def say_years(text):
    """Read 1700-1999 the way people say years: 1752 -> seventeen fifty-two, 1904 -> nineteen oh four."""
    def year(m):
        y = int(m.group(0))
        hi, lo = divmod(y, 100)
        tail = "hundred" if lo == 0 else ("oh " + _ONES[lo] if lo < 10 else _two(lo))
        return f"{_two(hi)} {tail}"
    return re.sub(r"\b1[0-9]{3}\b", year, text)


def speak(text):
    """Synthesise one narration line (cached). Returns (wav path, duration in seconds)."""
    import soundfile as sf
    clean = say_years(text.replace("…", "...").replace("“", "").replace("”", "").replace("’", "'")
                      .replace("Γ", "gamma"))
    ph = _phonemes(clean)
    # keyed on the pronunciation, so fixing a word in PRONOUNCE regenerates just the lines that use it
    key = hashlib.sha1(f"{VOICE}|{VOICE_SPEED}|{ph}".encode()).hexdigest()[:16]
    path = os.path.join(VO_CACHE, f"{key}.wav")
    if not os.path.exists(path):
        os.makedirs(VO_CACHE, exist_ok=True)
        audio, sr = _tts().create(ph, voice=VOICE, speed=VOICE_SPEED, is_phonemes=True)
        sf.write(path, audio, sr)
    info = sf.info(path)
    return path, info.frames / info.samplerate


class NarratedScene(Scene):
    """vo(text) starts a narration line now; vo_wait() holds the scene until it has finished."""

    VO_GAP = 0.35

    def vo(self, text):
        self.vo_wait()
        if not NARRATE:
            return
        text = tr(text)
        path, dur = speak_ml(text) if is_ml(text) else speak(text)
        self.add_sound(path)
        self._vo_end = self.renderer.time + dur + self.VO_GAP

    def vo_wait(self):
        rem = getattr(self, "_vo_end", 0.0) - self.renderer.time
        if rem > 0.03:
            self.wait(rem)


def wrap_two(text, width=82):
    """Split a subtitle into one or two balanced lines."""
    if len(text) <= width:
        return [text]
    words = text.split()
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        score = max(len(a), len(b))
        if best is None or score < best[0]:
            best = (score, a, b)
    return [best[1], best[2]]

SERIF = "C059"            # Century Schoolbook-style serif; "Libre Baskerville" or "EB Garamond" also suit
Text.set_default(font=SERIF)

# ---------------- archival palette ----------------
PAPER = "#efe4cc"
PAPER_DARK = "#dccaa6"
INK = "#3b2a1a"
SEPIA = "#8b5a2b"
FADED = "#7a6a55"
RED_INK = "#9b2d20"
BLUE_INK = "#3d5a80"

RNG = np.random.default_rng(1752)


# ---------------- paper, frame, type ----------------
def paper_background():
    vignette = VGroup(*[
        Rectangle(width=14.25 - 2 * 0.07 * i, height=8.05 - 2 * 0.07 * i, stroke_color="#a88a5a",
                  stroke_width=8, stroke_opacity=0.16 * (1 - i / 22) ** 2, fill_opacity=0)
        for i in range(22)
    ])
    grain = VGroup(*[
        Dot([RNG.uniform(-7.1, 7.1), RNG.uniform(-4, 4), 0], radius=RNG.uniform(0.006, 0.018),
            color=INK, fill_opacity=RNG.uniform(0.04, 0.1))
        for _ in range(500)
    ])
    fibres = VGroup()
    for _ in range(45):
        p = np.array([RNG.uniform(-7, 7), RNG.uniform(-3.9, 3.9), 0])
        a = RNG.uniform(0, PI)
        d = np.array([np.cos(a), np.sin(a), 0]) * RNG.uniform(0.15, 0.4)
        fibres.add(ArcBetweenPoints(p, p + d, angle=RNG.uniform(-0.6, 0.6), color=SEPIA,
                                    stroke_width=0.8, stroke_opacity=0.12))
    frame = VGroup(
        Rectangle(width=13.7, height=7.55, color=INK, stroke_width=1.6),
        Rectangle(width=13.5, height=7.35, color=INK, stroke_width=0.7),
    )
    corners = VGroup(*[Square(0.1, fill_color=INK, fill_opacity=1, stroke_width=0).rotate(PI / 4)
                       .move_to([sx * 6.85, sy * 3.775, 0]) for sx in (-1, 1) for sy in (-1, 1)])
    return VGroup(vignette, grain, fibres), VGroup(frame, corners)


def serif(text, size=28, color=INK, italic=False, bold=False):
    text = tr(text)
    if is_ml(text):   # Malayalam has no italics; set it upright in Noto Sans Malayalam, a touch smaller
        return Text(text, font=ML_FONT, font_size=size * 0.86, color=color, weight=BOLD if bold else NORMAL)
    return Text(text, font_size=size, color=color, slant=ITALIC if italic else NORMAL,
                weight=BOLD if bold else NORMAL)


def spaced(text, size=22, color=SEPIA):
    """Letter-spaced small caps, like an old plate heading (Malayalam is set plain: spacing would break its letters)."""
    text = tr(text)
    if is_ml(text):
        return Text(text, font=ML_FONT, font_size=size * 1.0, color=color, weight=MEDIUM)
    return Text("  ".join(text.upper()), font_size=size, color=color)


def ornament(width=3.0, color=SEPIA):
    d = Square(0.12, fill_color=color, fill_opacity=1, stroke_width=0).rotate(PI / 4)
    l = Line(LEFT * width / 2, LEFT * 0.15, color=color, stroke_width=1.5)
    r = Line(RIGHT * 0.15, RIGHT * width / 2, color=color, stroke_width=1.5)
    return VGroup(l, d, r)


def ink_card(mob, pad=0.22, rot=0.0):
    bg = RoundedRectangle(corner_radius=0.06, width=mob.width + 2 * pad, height=mob.height + 2 * pad,
                          fill_color=PAPER, fill_opacity=0.96, stroke_color=INK, stroke_width=1.2)
    inner = RoundedRectangle(corner_radius=0.04, width=mob.width + 2 * pad - 0.1, height=mob.height + 2 * pad - 0.1,
                             stroke_color=INK, stroke_width=0.5, fill_opacity=0)
    card = VGroup(bg, inner, mob.copy().move_to(bg))
    return card.rotate(rot)


def stamp(tex, color=RED_INK, rot=-6 * DEGREES, size=40):
    m = MathTex(tex, font_size=size, color=color)
    box = VGroup(
        RoundedRectangle(corner_radius=0.08, width=m.width + 0.5, height=m.height + 0.4, color=color, stroke_width=3),
        RoundedRectangle(corner_radius=0.06, width=m.width + 0.36, height=m.height + 0.26, color=color, stroke_width=1.2),
    )
    return VGroup(box, m).rotate(rot)


# ---------------- cameo silhouettes (stylised, not likenesses) ----------------
PROFILE = [(-0.45, -1.1), (-0.4, -0.6), (-0.6, -0.2), (-0.62, 0.3), (-0.45, 0.75), (-0.1, 0.95), (0.25, 0.9),
           (0.45, 0.6), (0.5, 0.35), (0.53, 0.24), (0.5, 0.14), (0.69, -0.06), (0.52, -0.13), (0.55, -0.22),
           (0.5, -0.28), (0.54, -0.34), (0.48, -0.42), (0.5, -0.55), (0.3, -0.66), (0.2, -0.76), (0.22, -1.1),
           (0.7, -1.3), (0.92, -1.62), (0.92, -1.75), (-1.0, -1.75), (-0.92, -1.42), (-0.5, -1.15)]


def cameo(kind, scale=0.85):
    oval_out = Ellipse(width=2.5, height=3.2, fill_color=PAPER_DARK, fill_opacity=1, stroke_color=SEPIA, stroke_width=4)
    oval_in = Ellipse(width=2.3, height=3.0, stroke_color=SEPIA, stroke_width=1.2)
    pts = [np.array([x, y, 0]) for x, y in PROFILE]
    head = VMobject(fill_color=INK, fill_opacity=1, stroke_width=0).set_points_smoothly(pts + [pts[0]])
    extras = VGroup()
    if kind == "wig":            # 18th-century powdered wig with side curls and a queue ribbon
        for (x, y, r) in [(-0.5, 0.05, 0.17), (-0.58, 0.32, 0.15), (-0.46, -0.24, 0.16), (-0.25, 0.7, 0.2),
                          (-0.5, 0.58, 0.17), (0.05, 0.86, 0.15)]:
            extras.add(Circle(radius=r, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x, y, 0]))
    elif kind == "beard":        # Victorian: full beard
        extras.add(VMobject(fill_color=INK, fill_opacity=1, stroke_width=0).set_points_smoothly([
            np.array(p) for p in [(0.5, -0.2, 0), (0.62, -0.42, 0), (0.56, -0.72, 0), (0.36, -0.98, 0),
                                  (0.05, -1.0, 0), (-0.1, -0.8, 0), (0.1, -0.45, 0), (0.5, -0.2, 0)]]))
        extras.add(Polygon([0.18, -1.08, 0], [0.5, -1.18, 0], [0.32, -1.34, 0], fill_color=PAPER_DARK,
                           fill_opacity=1, stroke_width=0))
    else:                        # early-1900s: short hair, moustache and collar
        extras.add(Polygon([0.42, -0.16, 0], [0.62, -0.18, 0], [0.6, -0.25, 0], [0.44, -0.24, 0],
                           fill_color=INK, fill_opacity=1, stroke_width=0))
        extras.add(Polygon([0.18, -1.05, 0], [0.5, -1.15, 0], [0.32, -1.32, 0], fill_color=PAPER_DARK,
                           fill_opacity=1, stroke_width=0))
    sil = VGroup(head, extras).scale(0.95).move_to(oval_out.get_center() + DOWN * 0.08)
    return VGroup(oval_out, oval_in, sil).scale(scale)


# ---------------- flow physics ----------------
def potential_velocity(x, y, R, U=1.0):
    """Ideal (inviscid) flow past a cylinder: uniform stream + doublet."""
    r2 = x * x + y * y
    r2 = np.maximum(r2, 1e-6)
    u = U * (1 - R * R * (x * x - y * y) / (r2 * r2))
    v = -U * 2 * R * R * x * y / (r2 * r2)
    return u, v


def streamline(psi0, R, half_w, U=1.0):
    """Points of the streamline psi = psi0 (y > 0), psi = U y (1 - R^2 / r^2)."""
    pts = []
    for x in np.linspace(-half_w, half_w, 160):
        lo = np.sqrt(max(R * R - x * x, 0)) + 1e-4
        hi = 6.0
        f = lambda y: U * y * (1 - R * R / (x * x + y * y)) - psi0
        if f(lo) > 0:
            continue
        for _ in range(50):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
        pts.append(np.array([x, (lo + hi) / 2, 0]))
    return pts


def cp_ideal(theta_front):
    return 1 - 4 * np.sin(theta_front) ** 2


# typical measured pressure on a cylinder in subcritical flow (qualitative)
_CP_TH = np.radians([0, 15, 30, 45, 60, 70, 80, 90, 120, 150, 180])
_CP_VAL = np.array([1.0, 0.75, 0.2, -0.4, -0.95, -1.2, -1.15, -1.1, -1.1, -1.1, -1.1])


def cp_real(theta_front):
    return float(np.interp(theta_front, _CP_TH, _CP_VAL))


def pressure_arrows(center, R, cp_fn, k=0.24, n=20):
    g = VGroup()
    for phi in np.linspace(0, TAU, n, endpoint=False):
        th = abs(PI - phi) if phi <= PI else abs(phi - PI)       # angle from the front stagnation point
        cp = cp_fn(th)
        L = k * abs(cp)
        if L < 0.07:
            continue
        nvec = np.array([np.cos(phi), np.sin(phi), 0])
        if cp > 0:     # pressure pushes on the body
            s, e, col = center + nvec * (R + 0.08 + L), center + nvec * (R + 0.06), RED_INK
        else:          # suction pulls outward
            s, e, col = center + nvec * (R + 0.06), center + nvec * (R + 0.06 + L), BLUE_INK
        g.add(Arrow(s, e, buff=0, color=col, stroke_width=3, tip_length=0.11, max_tip_length_to_length_ratio=0.45))
    return g


def engraved_cylinder(center, R):
    disc = Circle(radius=R, fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=3).move_to(center)
    hatch = VGroup()
    for c in np.arange(-1.4 * R, 1.4 * R, 0.09):
        # chords of the circle along the line x - y = c  (45 degree engraving hatch)
        d = c / np.sqrt(2)
        if abs(d) >= R:
            continue
        h = np.sqrt(R * R - d * d)
        mid = center + np.array([d / np.sqrt(2), -d / np.sqrt(2), 0])
        dirv = np.array([1, 1, 0]) / np.sqrt(2)
        hatch.add(Line(mid - dirv * h * 0.96, mid + dirv * h * 0.96, color=INK, stroke_width=0.8, stroke_opacity=0.55))
    return VGroup(disc, hatch)


class Tracers(VGroup):
    """Ink-dot tracers advected by a velocity field inside a rectangular window."""

    def __init__(self, center, half_w, half_h, R, vel_fn, rate=14, color=SEPIA, x_range=None, **kw):
        super().__init__(**kw)
        self.c, self.hw, self.hh, self.R = np.array(center, dtype=float), half_w, half_h, R
        self.xmin, self.xmax = x_range if x_range is not None else (-half_w, half_w)
        self.vel_fn, self.rate, self.col = vel_fn, rate, color
        self.acc, self.t = 0.0, 0.0
        self.alpha = 1.0
        self.add_updater(lambda m, dt: m.step(dt))

    def prefill(self, n=60, seconds=6.0):
        for _ in range(n):
            self.spawn(x=RNG.uniform(self.xmin, self.xmax))
        for _ in range(int(seconds * 20)):
            self.step(0.05)

    def spawn(self, x=None):
        y = RNG.uniform(-self.hh + 0.05, self.hh - 0.05)
        if abs(y) < 0.04:
            y = 0.06 * np.sign(y + 1e-9)
        x = self.xmin if x is None else x
        if x * x + y * y < (self.R * 1.05) ** 2:
            return
        p = self.c + np.array([x, y, 0])
        d = Line(p, p + RIGHT * 0.05, color=self.col, stroke_width=2.6)
        d.age, d.pos = 0.0, np.array([x, y])
        self.add(d)

    def step(self, dt):
        if dt == 0:
            return
        self.t += dt
        self.acc += self.rate * dt
        while self.acc > 1:
            self.acc -= 1
            self.spawn()
        for d in list(self.submobjects):
            x, y = d.pos
            u1, v1 = self.vel_fn(x, y, self.t)
            u2, v2 = self.vel_fn(x + u1 * dt / 2, y + v1 * dt / 2, self.t)
            x, y = x + u2 * dt, y + v2 * dt
            r = np.hypot(x, y)
            if r < self.R * 1.03:                      # keep tracers outside the body
                x, y = x / r * self.R * 1.03, y / r * self.R * 1.03
            d.age += dt
            if x < self.xmin or x > self.xmax or abs(y) > self.hh or d.age > 16:
                d.set_stroke(opacity=0)  # removed mobjects stay drawn until the current play() ends
                self.remove(d)
                continue
            d.pos = np.array([x, y])
            head = self.c + np.array([x, y, 0])
            vel = np.array([u2, v2, 0])
            sp = np.linalg.norm(vel)
            tail = head - (vel / sp if sp > 1e-6 else RIGHT) * max(0.04, 0.16 * sp)
            d.put_start_and_end_on(tail, head)
            edge = min((self.xmax - x) / 0.4, (x - self.xmin) / 0.4, (self.hh - abs(y)) / 0.2, 1.0)
            d.set_stroke(opacity=max(0.0, edge) * self.alpha)


class Wake:
    """A Karman-like vortex street shed behind a real cylinder (qualitative model)."""

    def __init__(self, R, half_w, strength=1.5, core=0.06, speed=0.72, period=0.85):
        self.R, self.hw = R, half_w
        self.strength, self.core, self.speed, self.period = strength, core, speed, period
        self.vortices, self.clock, self.top = [], 0.0, True

    def step(self, dt):
        self.clock += dt
        if self.clock > self.period:
            self.clock = 0.0
            s = 1 if self.top else -1
            self.vortices.append({"x": self.R * 1.0, "y": s * self.R * 0.55, "G": -self.strength * s, "age": 0.0})
            self.top = not self.top
        for v in self.vortices:
            v["x"] += self.speed * dt
            target = np.sign(v["y"]) * 0.32 * self.R / 0.7
            v["y"] += (target - v["y"]) * 0.9 * dt
            v["age"] += dt
        self.vortices = [v for v in self.vortices if v["x"] < self.hw + 0.5]

    def velocity(self, x, y):
        u, v = potential_velocity(x, y, self.R)
        if x > -0.1 * self.R:                                       # slower fluid in the wake
            u *= 1 - 0.5 * np.exp(-(y / (1.15 * self.R)) ** 2) / (1 + np.exp(-(x - 0.4 * self.R) * 4))
        for vt in self.vortices:
            dx, dy = x - vt["x"], y - vt["y"]
            r2 = dx * dx + dy * dy + 1e-6
            f = vt["G"] / (TAU * r2) * (1 - np.exp(-r2 / self.core))
            u += -f * dy
            v += f * dx
        return u, v


def spiral(center, sign, size=0.22, opacity=1.0):
    t = np.linspace(0, 3 * PI, 60)
    pts = [center + np.array([(0.02 + size * tt / (3 * PI)) * np.cos(sign * tt),
                              (0.02 + size * tt / (3 * PI)) * np.sin(sign * tt), 0]) for tt in t]
    return VMobject(stroke_color=SEPIA, stroke_width=1.6, stroke_opacity=0.55 * opacity).set_points_smoothly(pts)


# =====================================================================
class DAlembertParadox(NarratedScene):
    def construct(self):
        self.camera.background_color = PAPER
        paper, frame = paper_background()
        self.add(paper)
        self.play(FadeIn(frame), run_time=0.8)

        caption = [None]

        def say(text):
            """Show a subtitle and speak it; first waits for the previous line to finish."""
            self.vo(text)
            text = tr(text)
            lines = (wrap_two(text, 62 if is_ml(text) else 82) if NARRATE else [text])
            new = VGroup(*[serif(l, 22 if NARRATE else 24, FADED, italic=True) for l in lines]).arrange(DOWN, buff=0.06)
            if new.width > 12.6:
                new.scale_to_fit_width(12.6)
            new.move_to([0, -3.33 if len(lines) == 1 else -3.2, 0])
            if caption[0] is None:
                anims = [FadeIn(new, shift=UP * 0.1)]
            else:
                anims = [FadeOut(caption[0], shift=UP * 0.1), FadeIn(new, shift=UP * 0.1)]
            caption[0] = new
            return AnimationGroup(*anims)

        def unsay():
            self.vo_wait()
            if caption[0] is None:
                return Wait(0.01)
            old, caption[0] = caption[0], None
            return FadeOut(old)

        # ================= title plate =================
        series = spaced("Worlds of Flow", 22).move_to([0, 1.75, 0])
        plate_no = serif("Plate I", 22, SEPIA, italic=True).next_to(series, DOWN, buff=0.22)
        orn1 = ornament(3.4).next_to(plate_no, DOWN, buff=0.25)
        title = serif("D'Alembert's Paradox", 66).next_to(orn1, DOWN, buff=0.35)
        sub = serif("Why the mathematics said a body in a moving fluid feels no drag", 26, FADED, italic=True)
        sub.next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = serif("after the history of hydrodynamics in O. Darrigol, Worlds of Flow (Oxford, 2005)", 16, FADED,
                       italic=True).move_to([0, -3.2, 0])

        self.vo("Worlds of Flow. Plate one: d'Alembert's paradox. "
                "Why the mathematics once said that a body in a moving fluid feels no drag at all.")
        self.play(FadeIn(series, shift=DOWN * 0.1), FadeIn(plate_no), run_time=0.9)
        self.play(GrowFromCenter(orn1), run_time=0.5)
        self.play(Write(title), run_time=1.6)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.wait(1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, plate_no, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= d'Alembert, 1752 =================
        dal = cameo("wig").move_to([-4.2, 0.55, 0])
        dal_name = serif("Jean le Rond d'Alembert", 24).next_to(dal, DOWN, buff=0.22)
        dal_dates = serif("1717 – 1783", 20, FADED, italic=True).next_to(dal_name, DOWN, buff=0.08)

        place = spaced("Paris · 1752", 20).move_to([1.6, 2.0, 0])
        lines = VGroup(
            serif("Armed with the new calculus of fluids,", 30),
            serif("d'Alembert asks a deceptively simple question:", 30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([1.6, 1.0, 0])
        if lines.width > 8.4:                       # longer translations: keep clear of the cameo
            lines.scale_to_fit_width(8.4).move_to([1.6, 1.0, 0])
        question = serif("“How hard does a flowing fluid push on a body?”", 34, RED_INK, italic=True)
        question.move_to([1.6, -0.25, 0])
        if question.width > 8.4:
            question.scale_to_fit_width(8.4)

        # timeline ribbon (years 1700 to 1950)
        TL_Y = -2.5

        def yx(year):
            return -5.6 + 11.2 * (year - 1700) / 250

        tl_line = Line([yx(1700), TL_Y, 0], [yx(1950), TL_Y, 0], color=INK, stroke_width=1.6)
        tl_ticks = VGroup()
        for yr in range(1700, 1951, 50):
            tl_ticks.add(Line([yx(yr), TL_Y - 0.07, 0], [yx(yr), TL_Y + 0.07, 0], color=INK, stroke_width=1.2))
            tl_ticks.add(serif(str(yr), 15, FADED).move_to([yx(yr), TL_Y - 0.28, 0]))
        timeline = VGroup(tl_line, tl_ticks)

        def tl_mark(year, label, up=True, color=RED_INK):
            dot = Dot([yx(year), TL_Y, 0], radius=0.07, color=color)
            txt = serif(label, 16, color, italic=True)
            txt.next_to(dot, UP if up else DOWN, buff=0.14 if up else 0.42)
            return VGroup(dot, txt)

        m1752 = tl_mark(1752, "1752 · d'Alembert's essay on fluid resistance")

        self.vo("Paris, 1752. Armed with the new calculus of fluids, Jean le Rond d'Alembert "
                "asks a deceptively simple question: how hard does a flowing fluid push on a body?")
        self.play(FadeIn(dal, scale=0.9), run_time=1.0)
        self.play(FadeIn(dal_name, shift=UP * 0.1), FadeIn(dal_dates), FadeIn(place), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in lines], lag_ratio=0.4), run_time=1.4)
        self.play(Write(question), run_time=1.6)
        self.play(Create(tl_line), FadeIn(tl_ticks), run_time=0.9)
        self.play(GrowFromCenter(m1752[0]), FadeIn(m1752[1], shift=UP * 0.1), run_time=0.7)
        self.wait(1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(dal, dal_name, dal_dates, place, lines, question, timeline, m1752)), run_time=0.8)

        # ================= the ideal fluid =================
        head = serif("The Ideal Fluid", 36).move_to([0, 3.22, 0])
        head_sub = serif("no viscosity, no friction: the fluid of the mathematicians", 20, FADED, italic=True)
        head_sub.next_to(head, DOWN, buff=0.08)
        C = np.array([0.0, -0.05, 0])
        R = 1.0
        HW, HH = 6.4, 2.45

        streams = VGroup()
        for psi0 in [0.16, 0.42, 0.78, 1.2, 1.68, 2.2]:
            for s in (1, -1):
                pts = streamline(psi0, R, HW)
                if len(pts) > 3:
                    vm = VMobject().set_points_smoothly([C + np.array([p[0], s * p[1], 0]) for p in pts])
                    streams.add(vm.set_stroke(INK, 1.6, 0.5))
        axis_lines = VGroup(Line(C + LEFT * HW, C + LEFT * R), Line(C + RIGHT * R, C + RIGHT * HW)).set_stroke(INK, 1.6, 0.5)
        cyl = engraved_cylinder(C, R)

        tracers = Tracers(C, HW, HH, R, lambda x, y, t: potential_velocity(x, y, R), rate=13)
        tracers.prefill(70, 7)

        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(head_sub), run_time=0.8)
        self.play(FadeIn(cyl, scale=0.9), say("Imagine a long cylinder held still in a steady stream of a perfect fluid, one with no friction at all."),
                  run_time=0.9)
        self.play(LaggedStart(*[Create(s) for s in streams], lag_ratio=0.05), Create(axis_lines), run_time=2.0)
        self.add(tracers)
        self.bring_to_front(cyl)
        psi_eq = ink_card(MathTex(r"\psi = U\left(r - \frac{R^{2}}{r}\right)\sin\theta", font_size=30, color=INK))
        psi_eq.move_to([4.55, 1.85, 0])
        self.play(FadeIn(psi_eq, shift=DOWN * 0.1),
                  say("The equations of ideal flow give an exact answer: the streamlines bend smoothly around the body."),
                  run_time=0.9)
        self.wait(1.5)

        # pressure from Bernoulli
        cp_eq = ink_card(MathTex(r"C_p = 1 - 4\sin^{2}\theta", font_size=30, color=INK))
        cp_eq.move_to([-4.55, 1.85, 0])
        arrows = pressure_arrows(C, R, cp_ideal, k=0.26)
        legend = VGroup(
            VGroup(Arrow(LEFT * 0.25, RIGHT * 0.25, buff=0, color=RED_INK, stroke_width=3, tip_length=0.1),
                   serif("pushes", 16, RED_INK)).arrange(RIGHT, buff=0.1),
            VGroup(Arrow(LEFT * 0.25, RIGHT * 0.25, buff=0, color=BLUE_INK, stroke_width=3, tip_length=0.1),
                   serif("pulls (suction)", 16, BLUE_INK)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([-4.7, -1.75, 0])
        legend_card = ink_card(legend, pad=0.15).move_to([-4.85, -1.8, 0])
        tracers.alpha = 0.4
        self.play(FadeIn(cp_eq, shift=DOWN * 0.1),
                  say("Bernoulli's principle tells us that where the fluid speeds up, its pressure drops."), run_time=0.9)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.06), FadeIn(legend_card), run_time=2.0)
        self.wait(1.4)

        # symmetry
        mirror = DashedLine(C + UP * 1.9, C + DOWN * 1.9, color=RED_INK, stroke_width=2, dash_length=0.1)
        front = VGroup(*[a for a in arrows if a.get_center()[0] < C[0] - 0.01])
        back = VGroup(*[a for a in arrows if a.get_center()[0] > C[0] + 0.01])
        self.play(Create(mirror), say("But the pressure in front of the cylinder is a perfect mirror of the pressure behind it…"), run_time=1.0)
        self.play(Indicate(front, color=RED_INK, scale_factor=1.08), run_time=0.9)
        self.play(Indicate(back, color=RED_INK, scale_factor=1.08), run_time=0.9)
        drag0 = stamp(r"F_{\text{drag}} = 0").move_to([4.4, -1.55, 0])
        integral = ink_card(MathTex(r"F_{\text{drag}} = -\oint p\,(\hat{n}\cdot\hat{x})\,ds", font_size=26, color=INK),
                            pad=0.15)
        integral.next_to(drag0, UP, buff=0.3)
        self.play(FadeIn(integral), say("…so every push from the front is cancelled by an equal push from behind. The total drag is exactly zero."),
                  run_time=0.9)
        self.play(FadeIn(drag0, scale=1.5), run_time=0.45, rate_func=rate_functions.rush_into)
        self.play(Flash(drag0.get_center(), color=RED_INK, line_length=0.3, flash_radius=1.2, num_lines=14), run_time=0.5)
        self.wait(1.6)

        # the quote (1768)
        veil = Rectangle(width=14.2, height=8, fill_color=PAPER, fill_opacity=0, stroke_width=0)
        self.add(veil)
        q_text = VGroup(
            serif("“… a singular paradox which I leave", 32, INK, italic=True),
            serif("to future geometers to elucidate.”", 32, INK, italic=True),
        ).arrange(DOWN, buff=0.15)
        q_attr = serif("Jean le Rond d'Alembert, Opuscules mathématiques, 1768", 18, FADED)
        q_block = VGroup(q_text, ornament(2.0), q_attr).arrange(DOWN, buff=0.25)
        q_card = ink_card(q_block, pad=0.45, rot=-1.5 * DEGREES).move_to([0, 0.1, 0])
        self.play(veil.animate.set_fill(opacity=0.82), FadeIn(q_card, scale=0.95),
                  say("D'Alembert could find no error. Sixteen years later he called it a singular paradox, "
                      "and left it to future geometers to explain."), run_time=1.0)
        self.wait(2.0)

        # ================= theory vs reality =================
        theory_bits = VGroup(head, head_sub, cyl, streams, axis_lines, psi_eq, cp_eq, arrows, legend_card, mirror,
                             integral, drag0)
        tracers.clear_updaters()
        self.play(FadeOut(q_card), FadeOut(veil), FadeOut(theory_bits), FadeOut(tracers), unsay(), run_time=1.0)
        self.remove(tracers)

        R2, HW2, HH2 = 0.72, 3.05, 2.2
        CL, CR = np.array([-3.45, -0.15, 0]), np.array([3.45, -0.15, 0])

        def panel(center, label, sub_label):
            box = VGroup(Rectangle(width=2 * HW2 + 0.1, height=2 * HH2 + 0.1, color=INK, stroke_width=1.4),
                         Rectangle(width=2 * HW2 - 0.02, height=2 * HH2 - 0.02, color=INK, stroke_width=0.5)).move_to(center)
            t = spaced(label, 18, INK).next_to(box, UP, buff=0.32)
            s = serif(sub_label, 17, FADED, italic=True).next_to(t, DOWN, buff=0.06)
            return box, VGroup(t, s)

        box_l, lab_l = panel(CL, "Theory", "the ideal fluid of 1752")
        box_r, lab_r = panel(CR, "Reality", "water and air as they actually behave")
        cyl_l, cyl_r = engraved_cylinder(CL, R2), engraved_cylinder(CR, R2)

        streams_l = VGroup()
        for psi0 in [0.12, 0.35, 0.7, 1.15, 1.65]:
            for s in (1, -1):
                pts = streamline(psi0, R2, HW2)
                if len(pts) > 3:
                    streams_l.add(VMobject().set_points_smoothly([CL + np.array([p[0], s * p[1], 0]) for p in pts])
                                  .set_stroke(INK, 1.3, 0.4))

        wake = Wake(R2, HW2)
        tr_l = Tracers(CL, HW2, HH2, R2, lambda x, y, t: potential_velocity(x, y, R2), rate=13)
        tr_r = Tracers(CR, HW2, HH2, R2, lambda x, y, t: wake.velocity(x, y), rate=13)
        wake_driver = Mobject()
        wake_driver.add_updater(lambda m, dt: wake.step(dt))
        for _ in range(120):
            wake.step(0.05)
        tr_l.prefill(60, 5)
        tr_r.prefill(60, 5)

        # separating shear layers behind the real cylinder
        sep = VGroup()
        for s in (1, -1):
            a0 = np.radians(100) * s
            p0 = CR + R2 * np.array([np.cos(a0), np.sin(a0), 0])
            sep.add(VMobject().set_points_smoothly([p0, CR + np.array([0.55, s * 0.84, 0]),
                                                    CR + np.array([1.3, s * 0.78, 0]),
                                                    CR + np.array([2.2, s * 0.55, 0])])
                    .set_stroke(SEPIA, 2, 0.8))
        sep = VGroup(*[DashedVMobject(m, num_dashes=18) for m in sep])
        sep_lbl = serif("flow breaks away", 16, SEPIA, italic=True).move_to(CR + np.array([0.15, 1.35, 0]))
        swirls = always_redraw(lambda: VGroup(*[
            spiral(CR + np.array([v["x"], v["y"], 0]), np.sign(v["G"]), 0.2,
                   min(1.0, v["age"] / 0.6) * max(0.0, min(1.0, (HW2 - v["x"]) / 0.6)))
            for v in wake.vortices if v["x"] < HW2 - 0.1
        ]))

        self.play(FadeIn(box_l), FadeIn(box_r), FadeIn(lab_l, shift=DOWN * 0.1), FadeIn(lab_r, shift=DOWN * 0.1),
                  FadeIn(cyl_l), FadeIn(cyl_r), FadeIn(streams_l),
                  say("Yet every river, every ship and every cannonball feels drag."), run_time=1.1)
        self.add(wake_driver, tr_l, tr_r, swirls)
        self.bring_to_front(cyl_l, cyl_r)
        self.play(Create(sep), FadeIn(sep_lbl), run_time=1.0)
        self.wait(3.0)

        arr_l = pressure_arrows(CL, R2, cp_ideal, k=0.2, n=18)
        arr_r = pressure_arrows(CR, R2, cp_real, k=0.2, n=18)
        tr_l.alpha = tr_r.alpha = 0.45
        self.play(LaggedStart(*[GrowArrow(a) for a in arr_l], lag_ratio=0.04),
                  LaggedStart(*[GrowArrow(a) for a in arr_r], lag_ratio=0.04),
                  say("Behind a real body the flow breaks away, leaving a low-pressure wake that holds the body back."),
                  run_time=1.8)
        self.wait(1.0)
        s_l = stamp(r"F_{\text{drag}} = 0", size=32).move_to(CL + np.array([0, -1.62, 0]))
        drag_arrow = Arrow(CR + RIGHT * 0.1 + DOWN * 1.55, CR + RIGHT * 1.75 + DOWN * 1.55, buff=0, color=RED_INK,
                           stroke_width=7, max_tip_length_to_length_ratio=0.2)
        s_r = stamp(r"F_{\text{drag}} > 0", size=32, rot=4 * DEGREES).move_to(CR + np.array([-1.35, -1.62, 0]))
        cp_note = serif("pressures: typical measurements, drawn qualitatively", 13, FADED, italic=True)
        cp_note.next_to(box_r, DOWN, buff=0.06).align_to(box_r, RIGHT)
        self.play(FadeIn(s_l, scale=1.3), run_time=0.5)
        self.play(GrowArrow(drag_arrow), FadeIn(s_r, scale=1.3), FadeIn(cp_note), run_time=0.8)
        self.wait(3.2)

        # ================= the resolution, 1904 =================
        split_bits = VGroup(box_l, box_r, lab_l, lab_r, cyl_l, cyl_r, streams_l, sep, sep_lbl, arr_l, arr_r, s_l, s_r,
                            drag_arrow, cp_note)
        for m in (tr_l, tr_r, wake_driver):
            m.clear_updaters()
        self.play(FadeOut(split_bits), FadeOut(tr_l), FadeOut(tr_r), FadeOut(swirls), unsay(), run_time=1.0)
        self.remove(tr_l, tr_r, swirls, wake_driver)

        pra = cameo("modern").move_to([-4.2, 0.55, 0])
        pra_name = serif("Ludwig Prandtl", 24).next_to(pra, DOWN, buff=0.22)
        pra_dates = serif("1875 – 1953", 20, FADED, italic=True).next_to(pra_name, DOWN, buff=0.08)
        place2 = spaced("Heidelberg · 1904", 20).move_to([1.6, 2.0, 0])
        res = VGroup(
            serif("For a century and a half the paradox stood,", 30),
            serif("until Prandtl found the culprit:", 30),
            serif("a thin layer of fluid clinging to every surface,", 30, RED_INK, italic=True),
            serif("where friction can never be ignored.", 30, RED_INK, italic=True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([1.6, 0.55, 0])
        if res.width > 8.6:
            res.scale_to_fit_width(8.6)

        # raise the timeline a little so its labels clear the closing footer
        TL_Y = -2.0
        tl_line.shift(UP * 0.5)
        tl_ticks.shift(UP * 0.5)
        m1768 = tl_mark(1768, "1768 · the paradox restated", up=False, color=FADED)
        m1904 = tl_mark(1904, "1904 · Prandtl's boundary layer", up=False)
        bridge = ArcBetweenPoints([yx(1752), TL_Y + 0.12, 0], [yx(1904), TL_Y + 0.12, 0], angle=-0.5,
                                  color=SEPIA, stroke_width=1.5)
        bridge_lbl = serif("≈ 150 years", 16, SEPIA, italic=True).next_to(bridge, UP, buff=0.04)
        m1752b = tl_mark(1752, "1752")
        m1752b[1].next_to(m1752b[0], UR, buff=0.06)      # nudge right, clear of the dates above

        self.vo("For a century and a half the paradox stood, until, in 1904, Ludwig Prandtl found the culprit: "
                "a thin layer of fluid clinging to every surface, where friction can never be ignored.")
        self.play(FadeIn(pra, scale=0.9), FadeIn(place2), run_time=0.9)
        self.play(FadeIn(pra_name, shift=UP * 0.1), FadeIn(pra_dates), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in res], lag_ratio=0.45), run_time=2.6)
        self.play(Create(tl_line), FadeIn(tl_ticks), FadeIn(m1752b), FadeIn(m1768), run_time=0.9)
        self.play(GrowFromCenter(m1904[0]), FadeIn(m1904[1], shift=UP * 0.1), Create(bridge), FadeIn(bridge_lbl),
                  run_time=1.2)
        self.wait(1.0)

        nxt = VGroup(ornament(2.4), spaced("Next · Plate II · The Boundary Layer", 18, SEPIA)).arrange(DOWN, buff=0.15)
        nxt.move_to([0, -3.12, 0])
        self.vo("Next, in plate two: the boundary layer.")
        self.play(FadeIn(nxt, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        self.wait(1.5)


# =====================================================================
# Plate II: The Boundary Layer
# Render:  manim -pqh worlds_of_flow.py BoundaryLayerPlate
# =====================================================================

def pohlhausen(eta, lam):
    """Pohlhausen's boundary-layer profile u/U(eta) with pressure-gradient parameter lam.
    lam > 0 favourable, lam = -12 zero wall shear (separation), lam < -12 reversed flow."""
    eta = np.clip(eta, 0, 1)
    F = 2 * eta - 2 * eta ** 3 + eta ** 4
    G = eta * (1 - eta) ** 3 / 6
    return F + lam * G


def hatched_plate(x0, x1, y_top, depth=0.22):
    body = Polygon([x0, y_top, 0], [x1, y_top, 0], [x1, y_top - depth, 0], [x0 + 0.25, y_top - depth, 0],
                   fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=2.5)
    hatch = VGroup()
    for c in np.arange(x0 + 0.05, x1 - 0.05, 0.11):
        a = np.array([c, y_top - depth + 0.02, 0])
        b = a + np.array([depth - 0.04, depth - 0.04, 0])
        if b[0] > x1 - 0.02 or a[0] < x0 + 0.25:
            continue
        hatch.add(Line(a, b, color=INK, stroke_width=0.8, stroke_opacity=0.55))
    return VGroup(body, hatch)


class BoundaryLayerPlate(NarratedScene):
    def construct(self):
        self.camera.background_color = PAPER
        paper, frame = paper_background()
        self.add(paper)
        self.play(FadeIn(frame), run_time=0.8)

        caption = [None]

        def say(text):
            """Show a subtitle and speak it; first waits for the previous line to finish."""
            self.vo(text)
            lines = wrap_two(text) if NARRATE else [text]
            new = VGroup(*[serif(l, 22 if NARRATE else 24, FADED, italic=True) for l in lines]).arrange(DOWN, buff=0.06)
            if new.width > 12.6:
                new.scale_to_fit_width(12.6)
            new.move_to([0, -3.33 if len(lines) == 1 else -3.2, 0])
            if caption[0] is None:
                anims = [FadeIn(new, shift=UP * 0.1)]
            else:
                anims = [FadeOut(caption[0], shift=UP * 0.1), FadeIn(new, shift=UP * 0.1)]
            caption[0] = new
            return AnimationGroup(*anims)

        def unsay():
            self.vo_wait()
            if caption[0] is None:
                return Wait(0.01)
            old, caption[0] = caption[0], None
            return FadeOut(old)

        def header(title, sub):
            h = serif(title, 36).move_to([0, 3.22, 0])
            s = serif(sub, 20, FADED, italic=True).next_to(h, DOWN, buff=0.08)
            return VGroup(h, s)

        # ================= title plate =================
        series = spaced("Worlds of Flow", 22).move_to([0, 1.75, 0])
        plate_no = serif("Plate II", 22, SEPIA, italic=True).next_to(series, DOWN, buff=0.22)
        orn1 = ornament(3.4).next_to(plate_no, DOWN, buff=0.25)
        title = serif("The Boundary Layer", 66).next_to(orn1, DOWN, buff=0.35)
        sub = serif("How a layer thinner than a page resolved a 150-year-old paradox", 26, FADED, italic=True)
        sub.next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = serif("after the history of hydrodynamics in O. Darrigol, Worlds of Flow (Oxford, 2005)", 16, FADED,
                       italic=True).move_to([0, -3.2, 0])
        self.vo("Worlds of Flow. Plate two: the boundary layer. "
                "How a layer thinner than a page resolved a paradox a hundred and fifty years old.")
        self.play(FadeIn(series, shift=DOWN * 0.1), FadeIn(plate_no), run_time=0.9)
        self.play(GrowFromCenter(orn1), run_time=0.5)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.wait(1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, plate_no, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= Heidelberg, 1904 =================
        pra = cameo("modern").move_to([-4.2, 0.55, 0])
        pra_name = serif("Ludwig Prandtl", 24).next_to(pra, DOWN, buff=0.22)
        pra_dates = serif("1875 – 1953", 20, FADED, italic=True).next_to(pra_name, DOWN, buff=0.08)
        place = spaced("Heidelberg · August 1904", 20).move_to([1.6, 2.15, 0])
        intro = VGroup(
            serif("At the International Congress of Mathematicians,", 28),
            serif("a 29-year-old engineering professor", 28),
            serif("presents a paper just eight pages long:", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([1.6, 1.05, 0])
        paper_title = serif("Über Flüssigkeitsbewegung bei sehr kleiner Reibung", 26, RED_INK, italic=True)
        paper_tr = serif("“On fluid motion with very small friction”", 22, FADED, italic=True)
        ptitle = VGroup(paper_title, paper_tr).arrange(DOWN, buff=0.1).move_to([1.6, -0.55, 0])
        if ptitle.width > 8.6:
            ptitle.scale_to_fit_width(8.6)
        self.vo("Heidelberg, August 1904. At the International Congress of Mathematicians, a twenty-nine-year-old "
                "engineering professor, Ludwig Prandtl, presents a paper just eight pages long: "
                "On fluid motion with very small friction.")
        self.play(FadeIn(pra, scale=0.9), FadeIn(place), run_time=0.9)
        self.play(FadeIn(pra_name, shift=UP * 0.1), FadeIn(pra_dates), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in intro], lag_ratio=0.4), run_time=1.6)
        self.play(Write(paper_title), FadeIn(paper_tr), run_time=1.6)
        self.wait(1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(pra, pra_name, pra_dates, place, intro, ptitle)), run_time=0.8)

        # ================= the fluid sticks: no-slip =================
        hdr1 = header("The Fluid Sticks", "Prandtl's starting point: real fluid does not slide along a wall")
        Y_W, X_LE, X_END = -2.0, -5.6, 6.45
        U_SCREEN = 1.6
        plate = hatched_plate(X_LE, X_END, Y_W)
        slip = ValueTracker(0.0)            # 0 = ideal slip, 1 = real no-slip
        grow = ValueTracker(0.0)            # 0 = uniform thin layer, 1 = layer grows with sqrt(x)
        C_D = 2.15 / np.sqrt(X_END - X_LE)

        def delta(x):
            d_grown = C_D * np.sqrt(max(x - X_LE, 1e-4))
            return (1 - grow.get_value()) * 1.45 + grow.get_value() * d_grown

        def plate_vel(xl, yl, t):
            x, y = xl, yl + TR_C[1]
            if x < X_LE:
                return U_SCREEN, 0.0
            eta = (y - Y_W) / max(delta(x), 1e-3)
            f = pohlhausen(eta, 0) if eta < 1 else 1.0
            k = slip.get_value()
            return U_SCREEN * (1 - k + k * f), 0.0

        TOP = 2.45
        TR_C = np.array([0, (Y_W + TOP) / 2, 0])
        tr = Tracers(TR_C, 6.4, (TOP - Y_W) / 2 - 0.02, 0.0, plate_vel, rate=16)
        tr.prefill(70, 5)

        def profile_at(xs, L=1.15, n=11, color=INK):
            def build():
                g = VGroup()
                d = delta(xs)
                k = slip.get_value()
                tips = [np.array([xs, Y_W, 0]) + RIGHT * L * (1 - k)]
                for h in np.linspace(0.12, 2.35, n):
                    eta = h / max(d, 1e-3)
                    u = (1 - k) + k * (pohlhausen(eta, 0) if eta < 1 else 1.0)
                    a = np.array([xs, Y_W + h, 0])
                    tips.append(a + RIGHT * L * u)
                    if L * u > 0.06:
                        g.add(Arrow(a, a + RIGHT * L * u, buff=0, color=color, stroke_width=2.4, tip_length=0.1,
                                    max_tip_length_to_length_ratio=0.35))
                base = Line([xs, Y_W, 0], [xs, Y_W + 2.45, 0], color=INK, stroke_width=1.2, stroke_opacity=0.6)
                env = VMobject(stroke_color=RED_INK, stroke_width=2.4).set_points_smoothly(tips)
                return VGroup(base, g, env)
            return always_redraw(build)

        prof_mid = profile_at(-0.6)
        wall_dot = Dot([-0.6, Y_W, 0], radius=0.06, color=RED_INK)
        noslip_lbl = ink_card(MathTex(r"u = 0 \ \text{at the wall}", font_size=26, color=RED_INK), pad=0.12)
        noslip_lbl.move_to([-2.45, Y_W + 0.42, 0])
        free_lbl = MathTex(r"U", font_size=30, color=INK).move_to([0.95, Y_W + 2.25, 0])

        self.play(FadeIn(hdr1, shift=DOWN * 0.1), FadeIn(plate, shift=UP * 0.1),
                  say("Take the simplest body of all: a thin flat plate in a steady stream."), run_time=1.0)
        self.add(tr)
        self.bring_to_front(plate)
        self.play(FadeIn(prof_mid), FadeIn(free_lbl), run_time=0.8)
        self.wait(1.6)
        self.play(say("In the ideal fluid, the stream would slip past the wall untouched…"), run_time=0.8)
        self.wait(1.2)
        self.play(slip.animate.set_value(1.0), say("…but a real fluid sticks to it. Right at the surface, the speed is exactly zero."),
                  run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
        self.play(GrowFromCenter(wall_dot), FadeIn(noslip_lbl, shift=UP * 0.1), run_time=0.7)
        self.wait(1.8)

        # ================= the layer grows =================
        prof_a, prof_c = profile_at(-3.7, L=1.0, n=10), profile_at(3.3, L=1.0, n=10)
        edge = always_redraw(lambda: DashedVMobject(
            VMobject().set_points_smoothly([np.array([x, Y_W + delta(x), 0])
                                            for x in np.linspace(X_LE + 0.02, X_END - 0.05, 60)])
            .set_stroke(RED_INK, 2.2), num_dashes=46))
        layer_fill = always_redraw(lambda: Polygon(
            *([np.array([x, Y_W + delta(x), 0]) for x in np.linspace(X_LE, X_END, 50)]
              + [np.array([X_END, Y_W, 0]), np.array([X_LE, Y_W, 0])]),
            fill_color=RED_INK, fill_opacity=0.07, stroke_width=0))
        blasius = ink_card(VGroup(MathTex(r"\delta(x) \approx \frac{5.0\,x}{\sqrt{\mathrm{Re}_x}}", font_size=30, color=INK),
                                  serif("Blasius, 1908 · thickness hugely exaggerated", 14, FADED, italic=True)
                                  ).arrange(DOWN, buff=0.1), pad=0.16)
        blasius.move_to([-4.3, 1.65, 0])
        self.play(FadeOut(noslip_lbl), FadeOut(wall_dot), FadeOut(free_lbl), FadeIn(layer_fill), Create(edge),
                  say("Friction spreads this slowness outward, into a thin layer that grows thicker downstream."), run_time=1.2)
        self.play(grow.animate.set_value(1.0), FadeIn(prof_a), FadeIn(prof_c), run_time=2.4,
                  rate_func=rate_functions.ease_in_out_sine)
        self.play(FadeIn(blasius, shift=DOWN * 0.1),
                  say("In 1908, Prandtl's student Blasius worked out exactly how fast it grows."), run_time=0.7)
        self.wait(2.0)

        # ================= Prandtl's split =================
        outer_card = ink_card(VGroup(spaced("Outer flow", 16, INK),
                                     serif("Euler's ideal fluid works perfectly here", 18, FADED, italic=True)
                                     ).arrange(DOWN, buff=0.08), pad=0.16)
        outer_card.move_to([0.4, 1.55, 0])
        inner_card = ink_card(VGroup(spaced("Boundary layer", 13, RED_INK),
                                     serif("thin, slow, and ruled by friction", 16, RED_INK, italic=True)
                                     ).arrange(DOWN, buff=0.08), pad=0.14)
        inner_card.move_to([4.95, 0.88, 0])
        inner_ptr = Arrow(inner_card.get_bottom() + DOWN * 0.02, [5.25, Y_W + 0.75, 0], buff=0, color=RED_INK,
                          stroke_width=2, tip_length=0.12, max_tip_length_to_length_ratio=0.2)
        tr.alpha = 0.55
        self.play(FadeIn(outer_card, shift=DOWN * 0.1), FadeIn(inner_card, shift=UP * 0.1), GrowArrow(inner_ptr),
                  say("Prandtl's insight was to split the flow in two: far from the wall, Euler's ideal fluid works perfectly; "
                      "close to it, a thin layer is ruled by friction."), run_time=1.0)
        self.wait(1.5)

        tr.clear_updaters()
        flat_bits = VGroup(hdr1, plate, prof_mid, prof_a, prof_c, edge, layer_fill, blasius, outer_card, inner_card, inner_ptr)
        self.play(FadeOut(flat_bits), FadeOut(tr), unsay(), run_time=1.0)
        self.remove(tr, prof_mid, prof_a, prof_c, edge, layer_fill)

        # ================= separation on the cylinder =================
        hdr2 = header("Why the Flow Breaks Away", "the same layer, wrapped around d'Alembert's cylinder")
        C = np.array([-3.0, -0.75, 0])
        R = 1.7
        cyl = engraved_cylinder(C, R)

        # thin boundary layer band over the front and top, up to separation at about 82 degrees
        def band(side):
            pts_out, pts_in = [], []
            for th in np.linspace(0, np.radians(82), 40):
                phi = PI - th if side > 0 else PI + th
                n = np.array([np.cos(phi), np.sin(phi), 0])
                thick = 0.04 + 0.12 * (th / np.radians(82)) ** 1.5
                pts_out.append(C + n * (R + thick))
                pts_in.append(C + n * R)
            return Polygon(*pts_out, *reversed(pts_in), fill_color=RED_INK, fill_opacity=0.22, stroke_width=0)

        layer_band = VGroup(band(1), band(-1))

        def wall_profile(th_deg, lam, H=0.6, L=0.46, n=8):
            th = np.radians(th_deg)
            phi = PI - th
            nvec = np.array([np.cos(phi), np.sin(phi), 0])
            tvec = np.array([np.sin(phi), -np.cos(phi), 0])          # along the surface, downstream
            P = C + nvec * R
            g = VGroup(Line(P, P + nvec * (H + 0.08), color=INK, stroke_width=1.1, stroke_opacity=0.6))
            tips = [P]
            for eta in np.linspace(1 / n, 1.0, n):
                u = pohlhausen(eta, lam)
                a = P + nvec * eta * H
                tips.append(a + tvec * u * L)
                if abs(u * L) > 0.035:
                    g.add(Arrow(a, a + tvec * u * L, buff=0, color=INK if u > 0 else BLUE_INK, stroke_width=2.2,
                                tip_length=0.08, max_tip_length_to_length_ratio=0.4))
            g.add(VMobject(stroke_color=RED_INK, stroke_width=2.2).set_points_smoothly(tips))
            return g

        profiles = VGroup(wall_profile(30, 8), wall_profile(58, -3), wall_profile(82, -12), wall_profile(112, -24))
        S_th = np.radians(82)
        S = C + R * np.array([np.cos(PI - S_th), np.sin(PI - S_th), 0])
        S_dot = Dot(S, radius=0.07, color=RED_INK)
        S_n = np.array([np.cos(PI - S_th), np.sin(PI - S_th), 0])
        S_lbl = MathTex("S", font_size=30, color=RED_INK).move_to(S - S_n * 0.3)

        # tracers: ideal flow upstream, separated wake downstream
        wake = Wake(R, 8.0, strength=1.5 * R / 0.7, core=0.06 * (R / 0.7) ** 2, speed=0.72 * R / 0.7 * 0.8, period=1.1)
        for _ in range(140):
            wake.step(0.05)
        tr2 = Tracers(C, 6.0, 2.15, R, lambda x, y, t: wake.velocity(x, y), rate=17, x_range=(-3.35, 9.4))
        tr2.prefill(70, 6)
        wake_driver = Mobject()
        wake_driver.add_updater(lambda m, dt: wake.step(dt))
        swirls = always_redraw(lambda: VGroup(*[
            spiral(C + np.array([v["x"], v["y"], 0]), np.sign(v["G"]), 0.28,
                   min(1.0, v["age"] / 0.6) * max(0.0, min(1.0, (9.3 - v["x"]) / 0.8)))
            for v in wake.vortices
        ]))
        shear = VGroup()
        for s in (1, -1):
            p0 = C + R * np.array([np.cos(PI - S_th), s * np.sin(PI - S_th), 0])
            shear.add(DashedVMobject(VMobject().set_points_smoothly(
                [p0, p0 + np.array([0.7, s * 0.12, 0]), p0 + np.array([1.8, s * 0.02, 0]),
                 p0 + np.array([3.2, -s * 0.25, 0])]).set_stroke(SEPIA, 2.2, 0.85), num_dashes=22))

        notes = VGroup(
            ink_card(VGroup(serif("front: pressure falls", 17, INK),
                            serif("the layer is swept along", 15, FADED, italic=True)).arrange(DOWN, buff=0.05), pad=0.12)
            .move_to([-5.35, 1.95, 0]),
            ink_card(VGroup(serif("rear: pressure rises", 17, INK),
                            serif("slow fluid near the wall stalls, then reverses", 15, FADED, italic=True)
                            ).arrange(DOWN, buff=0.05), pad=0.12).move_to([2.2, 1.95, 0]),
        )
        rev_lbl = serif("backflow", 16, BLUE_INK, italic=True).next_to(profiles[3], RIGHT, buff=0.08).shift(DOWN * 0.15)

        self.play(FadeIn(hdr2, shift=DOWN * 0.1), FadeIn(cyl, scale=0.9),
                  say("Now wrap the layer around d'Alembert's cylinder."), run_time=1.0)
        self.play(FadeIn(layer_band), run_time=0.8)
        self.play(FadeIn(profiles[0]), FadeIn(profiles[1]), FadeIn(notes[0], shift=DOWN * 0.1),
                  say("Over the front, falling pressure keeps the layer moving."), run_time=1.0)
        self.wait(1.6)
        self.play(FadeIn(profiles[2]), FadeIn(notes[1], shift=DOWN * 0.1),
                  say("Past the widest point the pressure climbs again, and the slow layer runs out of momentum…"),
                  run_time=1.0)
        self.play(GrowFromCenter(S_dot), FadeIn(S_lbl), run_time=0.6)
        self.wait(1.2)
        self.play(FadeIn(profiles[3]), FadeIn(rev_lbl),
                  say("…it stops at the point S, then flows backwards, lifting the stream off the surface."), run_time=1.0)
        self.wait(1.8)

        self.add(wake_driver, tr2, swirls)
        self.bring_to_front(cyl, layer_band, profiles, S_dot, S_lbl, rev_lbl)
        self.play(Create(shear), say("The flow tears away into a turbulent wake, and the missing drag appears."),
                  run_time=1.2)
        self.wait(3.6)

        # ================= the resolution =================
        for m in (tr2, wake_driver):
            m.clear_updaters()
        cyl_bits = VGroup(hdr2, cyl, layer_band, profiles, S_dot, S_lbl, rev_lbl, shear, notes)
        self.play(FadeOut(cyl_bits), FadeOut(tr2), FadeOut(swirls), unsay(), run_time=1.0)
        self.remove(tr2, swirls, wake_driver)

        moral = VGroup(
            serif("However small the viscosity,", 36),
            serif("it never truly disappears.", 36, RED_INK, italic=True),
        ).arrange(DOWN, buff=0.18).move_to([0, 1.75, 0])
        limit = MathTex(r"\lim_{\nu \to 0}\,\big(\text{real flow}\big)\;\neq\;\big(\text{ideal flow},\ \nu = 0\big)",
                        font_size=40, color=INK).move_to([0, 0.35, 0])
        limit_note = serif("a “singular” limit: the difference hides in the thin layer at every surface", 20, FADED,
                           italic=True).next_to(limit, DOWN, buff=0.3)

        TL_Y = -1.95

        def yx(year):
            return -5.6 + 11.2 * (year - 1700) / 250

        tl_line = Line([yx(1700), TL_Y, 0], [yx(1950), TL_Y, 0], color=INK, stroke_width=1.6)
        tl_ticks = VGroup()
        for yr in range(1700, 1951, 50):
            tl_ticks.add(Line([yx(yr), TL_Y - 0.07, 0], [yx(yr), TL_Y + 0.07, 0], color=INK, stroke_width=1.2))
            tl_ticks.add(serif(str(yr), 15, FADED).move_to([yx(yr), TL_Y - 0.28, 0]))

        def tl_mark(year, label, color=RED_INK, up=True):
            dot = Dot([yx(year), TL_Y, 0], radius=0.07, color=color)
            txt = serif(label, 16, color, italic=True)
            txt.next_to(dot, UP if up else DOWN, buff=0.14 if up else 0.42)
            return VGroup(dot, txt)

        marks = VGroup(tl_mark(1752, "1752 · the paradox", FADED),
                       tl_mark(1904, "1904 · the boundary layer"),
                       tl_mark(1908, "1908 · Blasius", FADED, up=False))
        marks[1][1].shift(LEFT * 0.6)

        self.vo("However small the viscosity, it never truly disappears. Shrink it towards zero, and the real flow "
                "still does not become the ideal one: the difference hides in a thin layer at every surface.")
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in moral], lag_ratio=0.4), run_time=1.4)
        self.play(Write(limit), run_time=1.6)
        self.play(FadeIn(limit_note), run_time=0.6)
        self.play(Create(tl_line), FadeIn(tl_ticks), LaggedStart(*[FadeIn(m, shift=UP * 0.08) for m in marks],
                                                                 lag_ratio=0.3), run_time=1.4)
        self.wait(1.0)
        nxt = VGroup(ornament(2.4), spaced("Next · Plate III · Reynolds and Turbulence", 18, SEPIA)).arrange(DOWN, buff=0.15)
        nxt.move_to([0, -3.12, 0])
        self.vo("Next, in plate three: Reynolds and turbulence.")
        self.play(FadeIn(nxt, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        self.wait(1.5)


# =====================================================================
# Plate III: Reynolds and Turbulence
# Render:  manim -pqh worlds_of_flow.py ReynoldsTurbulencePlate
# =====================================================================

DYE = "#9b2d20"
WATER_WASH = "#b9cbc6"


class DyeThread(VGroup):
    """Dye released on the axis of a glass tube; laminar, wavering or turbulent depending on Re."""

    def __init__(self, x0, x1, yc, half, speed_fn, turb_fn, **kw):
        super().__init__(**kw)
        self.x0, self.x1, self.yc, self.half = x0, x1, yc, half
        self.speed_fn, self.turb_fn = speed_fn, turb_fn
        self.acc, self.t, self.frozen = 0.0, 0.0, False
        self.add_updater(lambda m, dt: m.step(dt))

    def prefill(self, seconds=4.0):
        for _ in range(int(seconds * 30)):
            self.step(1 / 30)

    def step(self, dt):
        if dt == 0 or self.frozen:
            return
        self.t += dt
        U, T = self.speed_fn(), self.turb_fn()
        self.acc += 34 * U * dt
        while self.acc > 1:
            self.acc -= 1
            d = Dot([self.x0, self.yc, 0], radius=0.032, color=DYE)
            d.p = np.array([self.x0, self.yc + RNG.normal(0, 0.004)])
            d.vy, d.ph, d.mixed = 0.0, RNG.uniform(0, TAU), False
            self.add(d)
        L = self.x1 - self.x0
        xb = self.x1 - L * 0.9 * np.sqrt(T) if T > 0.02 else np.inf      # where the thread breaks up
        for d in list(self.submobjects):
            x, y = d.p
            eta = (y - self.yc) / self.half
            x += U * (1.0 - 0.55 * eta * eta) * dt
            if x > xb or d.mixed:
                d.mixed = True
                d.vy = d.vy * np.exp(-2.5 * dt) + RNG.normal(0, 1) * 7.0 * T * np.sqrt(dt)
                y += (d.vy + 0.9 * T * np.sin(5 * x - 6 * self.t + d.ph)) * dt
            elif T > 0.02:
                frac = (x - self.x0) / max(xb - self.x0, 1e-3)
                y = self.yc + 0.07 * T * frac ** 2 * np.sin(5.5 * x - 8 * self.t)
            if abs(y - self.yc) > self.half:                # bounce off the glass
                y = self.yc + np.sign(y - self.yc) * (2 * self.half - abs(y - self.yc))
                d.vy *= -0.6
            y = float(np.clip(y, self.yc - self.half, self.yc + self.half))
            if x > self.x1:
                d.set_opacity(0)        # Manim keeps drawing removed mobjects until the current play() ends
                self.remove(d)
                continue
            d.p = np.array([x, y])
            d.move_to([x, y, 0])
            d.set_opacity(0.45 if d.mixed else 0.9)


class ReynoldsTurbulencePlate(NarratedScene):
    def construct(self):
        self.camera.background_color = PAPER
        paper, frame = paper_background()
        self.add(paper)
        self.play(FadeIn(frame), run_time=0.8)

        caption = [None]

        def say(text):
            """Show a subtitle and speak it; first waits for the previous line to finish."""
            self.vo(text)
            lines = wrap_two(text) if NARRATE else [text]
            new = VGroup(*[serif(l, 22 if NARRATE else 24, FADED, italic=True) for l in lines]).arrange(DOWN, buff=0.06)
            if new.width > 12.6:
                new.scale_to_fit_width(12.6)
            new.move_to([0, -3.33 if len(lines) == 1 else -3.2, 0])
            if caption[0] is None:
                anims = [FadeIn(new, shift=UP * 0.1)]
            else:
                anims = [FadeOut(caption[0], shift=UP * 0.1), FadeIn(new, shift=UP * 0.1)]
            caption[0] = new
            return AnimationGroup(*anims)

        def unsay():
            self.vo_wait()
            if caption[0] is None:
                return Wait(0.01)
            old, caption[0] = caption[0], None
            return FadeOut(old)

        def header(title, sub):
            h = serif(title, 36).move_to([0, 3.22, 0])
            s = serif(sub, 20, FADED, italic=True).next_to(h, DOWN, buff=0.08)
            return VGroup(h, s)

        # ================= title plate =================
        series = spaced("Worlds of Flow", 22).move_to([0, 1.75, 0])
        plate_no = serif("Plate III", 22, SEPIA, italic=True).next_to(series, DOWN, buff=0.22)
        orn1 = ornament(3.4).next_to(plate_no, DOWN, buff=0.25)
        title = serif("Reynolds and Turbulence", 62).next_to(orn1, DOWN, buff=0.35)
        sub = serif("Why the same water flows smoothly, then suddenly runs wild", 26, FADED, italic=True)
        sub.next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = serif("after the history of hydrodynamics in O. Darrigol, Worlds of Flow (Oxford, 2005)", 16, FADED,
                       italic=True).move_to([0, -3.2, 0])
        self.vo("Worlds of Flow. Plate three: Reynolds and turbulence. "
                "Why the same water flows smoothly, then suddenly runs wild.")
        self.play(FadeIn(series, shift=DOWN * 0.1), FadeIn(plate_no), run_time=0.9)
        self.play(GrowFromCenter(orn1), run_time=0.5)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.wait(1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, plate_no, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= Manchester, 1883 =================
        rey = cameo("beard").move_to([-4.2, 0.55, 0])
        rey_name = serif("Osborne Reynolds", 24).next_to(rey, DOWN, buff=0.22)
        rey_dates = serif("1842 – 1912", 20, FADED, italic=True).next_to(rey_name, DOWN, buff=0.08)
        place = spaced("Manchester · 1883", 20).move_to([1.6, 2.15, 0])
        intro = VGroup(
            serif("At Owens College, an engineering professor", 28),
            serif("puts a glass tube in a tank of water,", 28),
            serif("adds a thread of dye, and asks when the flow is", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([1.6, 1.0, 0])
        words = VGroup(serif("“direct”", 36, INK, italic=True), serif("or", 26, FADED, italic=True),
                       serif("“sinuous”", 36, RED_INK, italic=True)).arrange(RIGHT, buff=0.3).move_to([1.6, -0.45, 0])
        self.vo("Manchester, 1883. At Owens College, the engineering professor Osborne Reynolds puts a glass tube "
                "in a tank of water, adds a thin thread of dye, and asks a simple question: "
                "when is the flow direct, and when is it sinuous?")
        self.play(FadeIn(rey, scale=0.9), FadeIn(place), run_time=0.9)
        self.play(FadeIn(rey_name, shift=UP * 0.1), FadeIn(rey_dates), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in intro], lag_ratio=0.4), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(w, scale=1.15) for w in words], lag_ratio=0.35), run_time=1.2)
        self.wait(1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(rey, rey_name, rey_dates, place, intro, words)), run_time=0.8)

        # ================= the apparatus =================
        hdr = header("The Dye Experiment", "a reconstruction of Reynolds' apparatus, in engraving")
        TX0, TX1, TY, TH = -4.55, 5.75, -0.25, 0.36       # tube: inlet, outlet, axis, inner half-height
        tank = VGroup(
            Rectangle(width=11.9, height=3.0, fill_color=WATER_WASH, fill_opacity=0.35, stroke_color=INK,
                      stroke_width=2.5).move_to([-0.25, -0.15, 0]),
            *[Line([x, 1.27, 0], [x + 0.35, 1.27, 0], color=BLUE_INK, stroke_width=1.2, stroke_opacity=0.5)
              for x in np.arange(-6.0, 5.4, 0.7)],
        )
        glass = VGroup(
            Line([TX0, TY + TH, 0], [6.45, TY + TH, 0], color=INK, stroke_width=2.2),
            Line([TX0, TY - TH, 0], [6.45, TY - TH, 0], color=INK, stroke_width=2.2),
            ArcBetweenPoints([TX0 - 0.45, TY + TH + 0.45, 0], [TX0, TY + TH, 0], angle=-PI / 3, color=INK, stroke_width=2.2),
            ArcBetweenPoints([TX0, TY - TH, 0], [TX0 - 0.45, TY - TH - 0.45, 0], angle=-PI / 3, color=INK, stroke_width=2.2),
        )
        bore = Rectangle(width=6.45 - TX0, height=2 * TH, fill_color=PAPER, fill_opacity=0.35, stroke_width=0)
        bore.move_to([(TX0 + 6.45) / 2, TY, 0])
        flask = VGroup(
            Polygon([-5.65, 2.55, 0], [-4.85, 2.55, 0], [-4.95, 1.75, 0], [-5.55, 1.75, 0],
                    fill_color=DYE, fill_opacity=0.55, stroke_color=INK, stroke_width=2),
            Line([-5.25, 1.75, 0], [-5.25, TY, 0], color=INK, stroke_width=2),
            Line([-5.25, TY, 0], [TX0 - 0.15, TY, 0], color=INK, stroke_width=2),
        )
        valve_c = np.array([6.15, TY, 0])
        speed = ValueTracker(0.0)          # 0 = valve nearly shut, 1 = wide open
        valve_body = VGroup(
            Polygon(valve_c + np.array([-0.2, 0.18, 0]), valve_c + np.array([0.2, -0.18, 0]),
                    valve_c + np.array([0.2, 0.18, 0]), valve_c + np.array([-0.2, -0.18, 0]),
                    fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=2),
        )
        handle = always_redraw(lambda: Line(valve_c + UP * 0.2, valve_c + UP * 0.2 + 0.55 * np.array(
            [np.sin(-0.2 + 1.4 * speed.get_value()), np.cos(-0.2 + 1.4 * speed.get_value()), 0]),
            color=INK, stroke_width=4))
        labels = VGroup(
            serif("dye", 18, DYE, italic=True).next_to(flask[0], RIGHT, buff=0.15),
            serif("glass tube", 18, INK, italic=True).move_to([0.0, TY + TH + 0.3, 0]),
            serif("valve", 18, INK, italic=True).move_to(valve_c + np.array([-0.1, -0.62, 0])),
            serif("tank of still water", 18, FADED, italic=True).move_to([-2.6, -1.35, 0]),
        )

        def Re():
            return 800 + 4200 * speed.get_value()

        def turbulence():
            return float(np.clip((Re() - 2000) / 1800, 0, 1))

        dye = DyeThread(TX0 - 0.1, TX1, TY, TH - 0.03, lambda: 0.75 + 1.6 * speed.get_value(), turbulence)
        dye.prefill(5.0)

        re_lbl = MathTex(r"\mathrm{Re} = \frac{U D}{\nu} \approx", font_size=34, color=INK)
        re_val = Integer(800, font_size=34, color=INK, group_with_commas=True)
        re_val.add_updater(lambda m: m.set_value(int(round(Re() / 10) * 10)))
        readout = VGroup(re_lbl, re_val).arrange(RIGHT, buff=0.15).move_to([-1.6, -2.3, 0])
        re_val.add_updater(lambda m: m.next_to(re_lbl, RIGHT, buff=0.15))
        regimes = VGroup(spaced("laminar · direct", 16, INK), spaced("transitional", 16, SEPIA),
                         spaced("turbulent · sinuous", 16, RED_INK))
        for r in regimes:
            r.move_to([3.4, -2.3, 0])

        def regime_opacity(i):
            rv = Re()
            w = [float(np.clip((2000 - rv) / 200, 0, 1)),
                 float(np.clip(1 - abs(rv - 2700) / 600, 0, 1)),
                 float(np.clip((rv - 3300) / 300, 0, 1))]
            return w[i]

        for i, r in enumerate(regimes):
            r.add_updater(lambda m, i=i: m.set_opacity(regime_opacity(i)))

        self.play(FadeIn(hdr, shift=DOWN * 0.1), FadeIn(tank), run_time=0.8)
        self.play(Create(glass), FadeIn(bore), FadeIn(flask), FadeIn(valve_body), FadeIn(handle), run_time=1.3)
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.2), run_time=1.0)
        self.add(dye)
        self.bring_to_front(glass)
        self.play(FadeIn(readout), FadeIn(regimes),
                  say("With the valve barely open, the dye runs as one straight, unbroken thread."), run_time=1.0)
        self.wait(2.0)
        self.play(speed.animate.set_value(0.42), say("Open the valve a little more, and the thread begins to waver…"),
                  run_time=2.6, rate_func=rate_functions.ease_in_out_sine)
        self.wait(1.4)
        self.play(speed.animate.set_value(1.0),
                  say("…then it suddenly bursts, and the colour floods the whole tube."), run_time=2.4,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(2.6)

        # electric-spark snapshot
        flash = Rectangle(width=14.4, height=8.2, fill_color=WHITE, fill_opacity=0, stroke_width=0)
        self.add(flash)
        dye.frozen = True
        xb = TX1 - (TX1 - TX0) * 0.9
        curls = VGroup(*[spiral(np.array([x, TY + 0.15 * (1 if i % 2 else -1), 0]), 1 if i % 2 else -1, 0.17)
                         .set_stroke(INK, 1.8, 0.8) for i, x in enumerate(np.arange(xb + 0.6, TX1 - 0.2, 0.62))])
        spark_lbl = ink_card(serif("lit by an electric spark, the cloud resolves into curls and eddies", 17, INK,
                                   italic=True), pad=0.12).move_to([1.6, 0.85, 0])
        self.play(flash.animate.set_fill(opacity=0.85), run_time=0.12)
        self.play(flash.animate.set_fill(opacity=0), FadeIn(curls), FadeIn(spark_lbl), run_time=0.6)
        self.play(say("Reynolds froze the motion with an electric spark: the cloud turned out to be a tangle of curls and eddies."), run_time=0.8)
        self.wait(2.6)

        dye.clear_updaters()
        for r in regimes:
            r.clear_updaters()
        re_val.clear_updaters()
        app_bits = VGroup(hdr, tank, glass, bore, flask, valve_body, handle, labels, dye, readout, regimes, curls,
                          spark_lbl)
        self.play(FadeOut(app_bits), unsay(), run_time=1.0)
        self.remove(flash, handle)

        # ================= the number =================
        hdr2 = header("One Number Decides", "not the speed alone, but a balance of inertia against friction")
        big = MathTex(r"\mathrm{Re}", r"=", r"\frac{\rho\,U\,D}{\mu}", r"=", r"\frac{U\,D}{\nu}", font_size=64, color=INK)
        big.move_to([0, 1.55, 0])
        terms = VGroup(
            ink_card(MathTex(r"U \;\;\text{flow speed}", font_size=26, color=INK), pad=0.12),
            ink_card(MathTex(r"D \;\;\text{pipe diameter}", font_size=26, color=INK), pad=0.12),
            ink_card(MathTex(r"\nu \;\;\text{viscosity (stickiness)}", font_size=26, color=INK), pad=0.12),
        ).arrange(RIGHT, buff=0.35).move_to([0, 0.35, 0])
        sommer = serif("named the “Reynolds number” by Arnold Sommerfeld in 1908", 17, FADED, italic=True)
        sommer.next_to(terms, DOWN, buff=0.18)

        # log ruler from bacteria to airliners
        RX0, RX1, RY = -5.9, 5.9, -1.55

        def rx(e):
            return RX0 + (RX1 - RX0) * (e + 5) / 13

        crit = rx(np.log10(2300))
        lam_band = Rectangle(width=crit - RX0, height=0.22, fill_color=BLUE_INK, fill_opacity=0.18, stroke_width=0)
        lam_band.move_to([(RX0 + crit) / 2, RY, 0])
        turb_band = Rectangle(width=RX1 - crit, height=0.22, fill_color=RED_INK, fill_opacity=0.18, stroke_width=0)
        turb_band.move_to([(crit + RX1) / 2, RY, 0])
        ruler = VGroup(Line([RX0, RY, 0], [RX1, RY, 0], color=INK, stroke_width=1.8))
        for e in range(-5, 9):
            ruler.add(Line([rx(e), RY - 0.11, 0], [rx(e), RY + 0.11, 0], color=INK, stroke_width=1.2))
            if e % 2 == 1:
                ruler.add(MathTex(rf"10^{{{e}}}", font_size=20, color=FADED).move_to([rx(e), RY - 0.36, 0]))
        band_lbls = VGroup(spaced("laminar", 14, BLUE_INK).move_to([(RX0 + crit) / 2, RY + 0.32, 0]),
                           spaced("turbulent", 14, RED_INK).move_to([(crit + RX1) / 2, RY + 0.32, 0]))
        crit_mark = VGroup(DashedLine([crit, RY - 0.25, 0], [crit, RY + 0.55, 0], color=RED_INK, stroke_width=2),
                           MathTex(r"\approx 2300", font_size=22, color=RED_INK).move_to([crit, RY + 0.72, 0]))
        examples = [(-5, "swimming bacterium"), (-2, "honey off a spoon"), (6, "a river"), (7.7, "airliner wing")]
        ex_marks = VGroup()
        for e, name in examples:
            lbl = serif(name, 15, INK, italic=True).move_to([rx(e), RY - 0.72, 0])
            lbl.shift(RIGHT * max(0.0, -6.3 - lbl.get_left()[0]) + LEFT * max(0.0, lbl.get_right()[0] - 6.3))
            ex_marks.add(VGroup(Dot([rx(e), RY, 0], radius=0.06, color=INK), lbl))

        self.play(FadeIn(hdr2, shift=DOWN * 0.1), Write(big), say("Reynolds saw that speed alone does not decide. What matters is one number, balancing inertia against friction."),
                  run_time=1.6)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in terms], lag_ratio=0.25), FadeIn(sommer),
                  say("A wider pipe, a faster flow or a thinner fluid all push it up. In 1908, Sommerfeld named it the Reynolds number."), run_time=1.3)
        self.wait(1.6)
        self.play(Create(ruler), FadeIn(lam_band), FadeIn(turb_band), FadeIn(band_lbls), run_time=1.2)
        self.play(FadeIn(crit_mark, shift=DOWN * 0.1),
                  LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in ex_marks], lag_ratio=0.25),
                  say("In a pipe, the switch comes near two thousand three hundred, and nearly everything around us flows far above it."),
                  run_time=1.6)
        self.wait(2.6)
        num_bits = VGroup(hdr2, big, terms, sommer, ruler, lam_band, turb_band, band_lbls, crit_mark, ex_marks)
        self.play(FadeOut(num_bits), unsay(), run_time=0.9)

        # ================= the law of resistance =================
        hdr3 = header("The Law of Resistance", "how hard it is to push water through the pipe")
        O = np.array([-4.6, -2.15, 0])
        W, H = 7.4, 4.3
        axes = VGroup(Arrow(O, O + RIGHT * W, buff=0, color=INK, stroke_width=2, tip_length=0.15),
                      Arrow(O, O + UP * H, buff=0, color=INK, stroke_width=2, tip_length=0.15))
        ax_lbls = VGroup(serif("log  speed", 17, FADED, italic=True).next_to(axes[0], DOWN, buff=0.1).align_to(axes[0], RIGHT),
                         serif("log  pressure drop", 17, FADED, italic=True).rotate(PI / 2).next_to(axes[1], LEFT, buff=0.1))
        xc = 3.3

        def lam_y(x):
            return 0.3 + 0.4 * x

        def tur_y(x):
            return lam_y(xc) + 0.3 + 0.4 * 1.75 * (x - xc)

        lam_line = Line(O + np.array([0.3, lam_y(0.3), 0]), O + np.array([xc, lam_y(xc), 0]), color=BLUE_INK, stroke_width=3)
        tur_line = Line(O + np.array([xc + 0.25, tur_y(xc + 0.25), 0]), O + np.array([6.4, tur_y(6.4), 0]),
                        color=RED_INK, stroke_width=3)
        jump = DashedLine(O + np.array([xc, lam_y(xc), 0]), O + np.array([xc + 0.25, tur_y(xc + 0.25), 0]),
                          color=SEPIA, stroke_width=2)
        pts = VGroup()
        for x in np.linspace(0.5, 6.3, 22):
            if xc - 0.05 < x < xc + 0.3:
                continue
            y = lam_y(x) if x < xc else tur_y(x)
            pts.add(Circle(radius=0.055, color=INK, stroke_width=1.6).move_to(O + np.array([x, y + RNG.normal(0, 0.05), 0])))
        crit_v = DashedLine(O + np.array([xc + 0.12, 0, 0]), O + np.array([xc + 0.12, H - 0.3, 0]), color=SEPIA,
                            stroke_width=1.5)
        crit_t = serif("critical speed", 15, SEPIA, italic=True).next_to(crit_v, UP, buff=0.05)
        lam_t = MathTex(r"\Delta p \propto U", font_size=30, color=BLUE_INK).move_to(O + np.array([1.3, lam_y(1.3) + 0.6, 0]))
        tur_t = MathTex(r"\Delta p \propto U^{1.75}", font_size=30, color=RED_INK).move_to(O + np.array([5.85, 2.75, 0]))
        note = ink_card(VGroup(serif("Below the critical speed, friction", 18, INK),
                               serif("grows with speed. Above it, eddies", 18, INK),
                               serif("make it grow almost with its square.", 18, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.06),
                        pad=0.18).move_to([4.6, 0.55, 0])
        note_tag = serif("slopes drawn to the classic smooth-pipe laws", 13, FADED, italic=True).next_to(note, DOWN, buff=0.1)

        self.play(FadeIn(hdr3, shift=DOWN * 0.1), Create(axes), FadeIn(ax_lbls),
                  say("He also measured how hard the water was to push through the pipe."), run_time=1.2)
        self.play(Create(lam_line), FadeIn(lam_t), LaggedStart(*[FadeIn(p) for p in pts if p.get_x() < O[0] + xc],
                                                                 lag_ratio=0.1),
                  say("Below a critical speed, the resistance simply grows in step with the speed."), run_time=1.4)
        self.play(Create(crit_v), FadeIn(crit_t), Create(jump), run_time=0.8)
        self.play(Create(tur_line), FadeIn(tur_t), LaggedStart(*[FadeIn(p) for p in pts if p.get_x() >= O[0] + xc],
                                                               lag_ratio=0.1),
                  say("Past the critical speed it jumps, and then climbs far more steeply, almost with the square of the speed."), run_time=1.4)
        self.play(FadeIn(note, shift=LEFT * 0.1), FadeIn(note_tag), run_time=0.8)
        self.wait(1.5)
        law_bits = VGroup(hdr3, axes, ax_lbls, lam_line, tur_line, jump, pts, crit_v, crit_t, lam_t, tur_t, note, note_tag)
        self.play(FadeOut(law_bits), unsay(), run_time=0.9)

        # ================= moral + timeline =================
        moral = VGroup(
            serif("Same water, same tube, same equations,", 34),
            serif("yet two utterly different worlds of flow.", 34, RED_INK, italic=True),
        ).arrange(DOWN, buff=0.18).move_to([0, 1.7, 0])
        open_q = serif("Turbulence is still one of the great unsolved problems of classical physics.", 22, FADED,
                       italic=True).move_to([0, 0.55, 0])

        TL_Y = -1.15

        def yx(year):
            return -5.6 + 11.2 * (year - 1700) / 250

        tl_line = Line([yx(1700), TL_Y, 0], [yx(1950), TL_Y, 0], color=INK, stroke_width=1.6)
        tl_ticks = VGroup()
        for yr in range(1700, 1951, 50):
            tl_ticks.add(Line([yx(yr), TL_Y - 0.07, 0], [yx(yr), TL_Y + 0.07, 0], color=INK, stroke_width=1.2))
            tl_ticks.add(serif(str(yr), 15, FADED).move_to([yx(yr), TL_Y - 0.28, 0]))

        def tl_mark(year, label, color=FADED, up=True, dx=0.0):
            dot = Dot([yx(year), TL_Y, 0], radius=0.07, color=color)
            txt = serif(label, 16, color, italic=True)
            txt.next_to(dot, UP if up else DOWN, buff=0.14 if up else 0.42).shift(RIGHT * dx)
            return VGroup(dot, txt)

        marks = VGroup(tl_mark(1752, "1752 · the paradox"),
                       tl_mark(1883, "1883 · Reynolds' dye experiment", RED_INK, dx=-1.4),
                       tl_mark(1904, "1904 · the boundary layer", up=False, dx=0.3),
                       tl_mark(1908, "1908 · “Reynolds number”", up=True, dx=0.95))
        self.vo("Same water, same tube, same equations, yet two utterly different worlds of flow. "
                "More than a century later, turbulence is still one of the great unsolved problems of classical physics.")
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in moral], lag_ratio=0.4), run_time=1.4)
        self.play(FadeIn(open_q), run_time=0.8)
        self.play(Create(tl_line), FadeIn(tl_ticks), LaggedStart(*[FadeIn(m, shift=UP * 0.08) for m in marks],
                                                                 lag_ratio=0.3), run_time=1.6)
        self.wait(1.0)
        nxt = VGroup(ornament(2.4), spaced("Next · Plate IV · Vortices: Helmholtz and Kelvin", 18, SEPIA)).arrange(DOWN, buff=0.15)
        nxt.move_to([0, -3.12, 0])
        if nxt.width > 12.4:
            nxt.scale_to_fit_width(12.4)
        self.vo("Next, in plate four: vortices, with Helmholtz and Kelvin.")
        self.play(FadeIn(nxt, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        self.wait(1.5)


# =====================================================================
# Plate IV: Vortices, Helmholtz and Kelvin
# Render:  manim -pqh worlds_of_flow.py VorticesPlate
# =====================================================================

def vortex_velocity(pts, cores, gammas, core2=0.03):
    """Velocity at pts (N,2) induced by 2D point vortices (smoothed cores)."""
    D = pts[:, None, :] - cores[None, :, :]
    r2 = (D ** 2).sum(-1) + core2
    u = (-D[..., 1] * gammas[None, :] / (TAU * r2)).sum(1)
    v = (D[..., 0] * gammas[None, :] / (TAU * r2)).sum(1)
    return np.stack([u, v], 1)


class VortexSystem:
    """Point vortices moving under each other's induced velocity (RK4)."""

    def __init__(self, cores, gammas, core2=0.004):
        self.P = np.array(cores, dtype=float)
        self.G = np.array(gammas, dtype=float)
        self.core2 = core2
        self.angle = np.zeros(len(self.G))

    def _vel(self, P):
        D = P[:, None, :] - P[None, :, :]
        r2 = (D ** 2).sum(-1) + self.core2
        np.fill_diagonal(r2, np.inf)
        u = (-D[..., 1] * self.G[None, :] / (TAU * r2)).sum(1)
        v = (D[..., 0] * self.G[None, :] / (TAU * r2)).sum(1)
        return np.stack([u, v], 1)

    def step(self, dt, sub=3):
        h = dt / sub
        for _ in range(sub):
            k1 = self._vel(self.P)
            k2 = self._vel(self.P + h / 2 * k1)
            k3 = self._vel(self.P + h / 2 * k2)
            k4 = self._vel(self.P + h * k3)
            self.P = self.P + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        self.angle += np.sign(self.G) * 5.0 * dt


class Smoke(VGroup):
    """A fixed set of smoke dots advected by a velocity field. Dots are never removed (no ghosts)."""

    def __init__(self, xy, colors, vel_fn, x_fade=(-6.6, 6.4), radius=0.03, opacity=0.6, **kw):
        super().__init__(**kw)
        self.xy = np.array(xy, dtype=float)
        self.vel_fn, self.x_fade, self.op = vel_fn, x_fade, opacity
        for p, c in zip(self.xy, colors):
            self.add(Dot([p[0], p[1], 0], radius=radius, color=c, fill_opacity=opacity))
        self.add_updater(lambda m, dt: m.step(dt))

    def step(self, dt):
        if dt == 0:
            return
        k1 = self.vel_fn(self.xy)
        k2 = self.vel_fn(self.xy + dt / 2 * k1)
        self.xy = self.xy + dt * k2
        lo, hi = self.x_fade
        for d, p in zip(self.submobjects, self.xy):
            d.move_to([p[0], p[1], 0])
            fade = float(np.clip(min((hi - p[0]) / 0.5, (p[0] - lo) / 0.5), 0, 1))
            d.set_fill(opacity=self.op * fade)


class Streaks(VGroup):
    """Short ink streaks advected by a vectorised velocity field; recycled in place (no ghosts)."""

    def __init__(self, n, center, half_w, half_h, vel_fn, color=SEPIA, life=(2.5, 5.0), **kw):
        super().__init__(**kw)
        self.c, self.hw, self.hh = np.array(center[:2], dtype=float), half_w, half_h
        self.vel_fn, self.life = vel_fn, life
        self.xy = self._random(n)
        self.age = RNG.uniform(0, life[0], n)
        self.max_age = RNG.uniform(*life, n)
        for _ in range(n):
            self.add(Line(ORIGIN, RIGHT * 0.05, color=color, stroke_width=2.6))
        self.alpha = 1.0
        self.add_updater(lambda m, dt: m.step(dt))
        self.step(1 / 30)

    def _random(self, n):
        return self.c + np.stack([RNG.uniform(-self.hw, self.hw, n), RNG.uniform(-self.hh, self.hh, n)], 1)

    def step(self, dt):
        if dt == 0:
            return
        k1 = self.vel_fn(self.xy)
        k2 = self.vel_fn(self.xy + dt / 2 * k1)
        self.xy = self.xy + dt * k2
        self.age += dt
        rel = self.xy - self.c
        dead = (self.age > self.max_age) | (np.abs(rel[:, 0]) > self.hw) | (np.abs(rel[:, 1]) > self.hh)
        if dead.any():
            self.xy[dead] = self._random(int(dead.sum()))
            self.age[dead] = 0.0
        vel = self.vel_fn(self.xy)
        for i, line in enumerate(self.submobjects):
            p = np.array([self.xy[i, 0], self.xy[i, 1], 0])
            v = np.array([vel[i, 0], vel[i, 1], 0])
            sp = np.linalg.norm(v)
            tail = p - (v / sp if sp > 1e-6 else RIGHT) * float(np.clip(0.12 * sp, 0.03, 0.28))
            line.put_start_and_end_on(tail, p)
            a = self.age[i]
            fade = min(a / 0.4, (self.max_age[i] - a) / 0.4, 1.0)
            line.set_stroke(opacity=max(0.0, fade) * self.alpha)


def knot_mobject(fn, center, scale, frac=1.0, n=420, ink=INK, width=7, gap=0.13):
    """Draw a knot from a 3D parametric curve. Wherever a strand passes under another, a short
    gap is cut in it, as in a hand-drawn knot diagram."""
    ts = np.linspace(0, TAU, n, endpoint=False)
    pts = np.array([fn(t) for t in ts])
    nxt = np.roll(pts, -1, axis=0)
    mid = (pts + nxt) / 2
    xy = mid[:, :2] * scale
    z = mid[:, 2]
    d = np.linalg.norm(xy[:, None, :] - xy[None, :, :], axis=-1)
    idx = np.arange(n)
    sep = np.abs(idx[:, None] - idx[None, :])
    sep = np.minimum(sep, n - sep)
    drawn = idx < max(2, int(n * frac))
    under = ((d < gap) & (sep > 12) & (z[None, :] > z[:, None]) & drawn[None, :]).any(1)
    keep = ~under & drawn
    c = np.array(center, dtype=float)
    g = VGroup()
    run = []
    order = list(range(n))
    start = next((i for i in order if not keep[i]), None)
    if start is not None:                      # walk the loop from a gap, so runs never wrap
        order = order[start:] + order[:start]
    for i in order + [None]:
        if i is not None and keep[i]:
            run.append(i)
            continue
        if len(run) >= 2:
            ptsr = [c + scale * np.array([pts[j][0], pts[j][1], 0]) for j in run]
            j = (run[-1] + 1) % n
            ptsr.append(c + scale * np.array([pts[j][0], pts[j][1], 0]))
            g.add(VMobject(stroke_color=ink, stroke_width=width).set_points_smoothly(ptsr))
        run = []
    if start is None:                          # no crossings at all (the unknot)
        ptsr = [c + scale * np.array([p_[0], p_[1], 0]) for p_ in pts[: max(2, int(n * frac))]]
        if frac >= 1:
            ptsr.append(ptsr[0])
        g.add(VMobject(stroke_color=ink, stroke_width=width).set_points_smoothly(ptsr))
    return g


def torus_knot(p, q):
    return lambda t: np.array([(np.cos(q * t) + 2) * np.cos(p * t), (np.cos(q * t) + 2) * np.sin(p * t), -np.sin(q * t)])


def figure_eight(t):
    """Figure-eight knot (after Paul Bourke's parametrisation), scaled to roughly unit size."""
    x = 10 * (np.cos(t) + np.cos(3 * t)) + np.cos(2 * t) + np.cos(4 * t)
    y = 6 * np.sin(t) + 10 * np.sin(3 * t)
    z = 4 * np.sin(3 * t) * np.sin(2.5 * t) + 4 * np.sin(4 * t) - 2 * np.sin(6 * t)
    return np.array([x, y, z]) / 7.3


def unknot(t):
    return np.array([2.6 * np.cos(t), 2.6 * np.sin(t), 0.0])


def perspective_ring(center, w=1.3, h=3.3, t=0.38, color=SEPIA, fill=PAPER_DARK):
    outer = Ellipse(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=2.2)
    inner = Ellipse(width=w - 2 * t * 0.9, height=h - 2 * t, fill_color=PAPER, fill_opacity=1, stroke_color=INK,
                    stroke_width=1.6)
    hatch = VGroup()
    for k in range(26):
        a = TAU * k / 26
        p_out = np.array([w / 2 * np.cos(a), h / 2 * np.sin(a), 0])
        p_in = np.array([(w / 2 - t * 0.9) * np.cos(a), (h / 2 - t) * np.sin(a), 0])
        hatch.add(Line(p_in * 0.98 + p_out * 0.02, p_out * 0.96 + p_in * 0.04, color=INK, stroke_width=0.8,
                       stroke_opacity=0.5))
    return VGroup(outer, hatch, inner).move_to(center)


def swirl_arrow(center, radius=0.32, ccw=True, color=RED_INK):
    start = -PI * 0.15 if ccw else PI * 1.15
    ang = PI * 1.55 if ccw else -PI * 1.55
    arc = Arc(radius=radius, start_angle=start, angle=ang, arc_center=center, color=color, stroke_width=3)
    arc.add_tip(tip_length=0.12)
    return arc


def core_glyph(center, sign, angle=0.0, size=0.22, color=INK):
    return spiral(np.array(center), sign, size).set_stroke(color, 2.0, 0.9).rotate(angle, about_point=np.array(center))


class VorticesPlate(NarratedScene):
    def construct(self):
        self.camera.background_color = PAPER
        paper, frame = paper_background()
        self.add(paper)
        self.play(FadeIn(frame), run_time=0.8)

        caption = [None]

        def say(text):
            """Show a subtitle and speak it; first waits for the previous line to finish."""
            self.vo(text)
            lines = wrap_two(text) if NARRATE else [text]
            new = VGroup(*[serif(l, 22 if NARRATE else 24, FADED, italic=True) for l in lines]).arrange(DOWN, buff=0.06)
            if new.width > 12.6:
                new.scale_to_fit_width(12.6)
            new.move_to([0, -3.33 if len(lines) == 1 else -3.2, 0])
            if caption[0] is None:
                anims = [FadeIn(new, shift=UP * 0.1)]
            else:
                anims = [FadeOut(caption[0], shift=UP * 0.1), FadeIn(new, shift=UP * 0.1)]
            caption[0] = new
            return AnimationGroup(*anims)

        def unsay():
            self.vo_wait()
            if caption[0] is None:
                return Wait(0.01)
            old, caption[0] = caption[0], None
            return FadeOut(old)

        def header(title, sub):
            h = serif(title, 36).move_to([0, 3.22, 0])
            s = serif(sub, 20, FADED, italic=True).next_to(h, DOWN, buff=0.08)
            return VGroup(h, s)

        # ================= title plate =================
        series = spaced("Worlds of Flow", 22).move_to([0, 1.75, 0])
        plate_no = serif("Plate IV", 22, SEPIA, italic=True).next_to(series, DOWN, buff=0.22)
        orn1 = ornament(3.4).next_to(plate_no, DOWN, buff=0.25)
        title = serif("Vortices", 66).next_to(orn1, DOWN, buff=0.35)
        sub = serif("Helmholtz, Kelvin, and the dream of atoms made of whirlpools", 26, FADED, italic=True)
        sub.next_to(title, DOWN, buff=0.3)
        orn2 = ornament(2.2).next_to(sub, DOWN, buff=0.35)
        credit = serif("after the history of hydrodynamics in O. Darrigol, Worlds of Flow (Oxford, 2005)", 16, FADED,
                       italic=True).move_to([0, -3.2, 0])
        self.vo("Worlds of Flow. Plate four: vortices. "
                "Helmholtz, Kelvin, and the dream of atoms made of whirlpools.")
        self.play(FadeIn(series, shift=DOWN * 0.1), FadeIn(plate_no), run_time=0.9)
        self.play(GrowFromCenter(orn1), run_time=0.5)
        self.play(Write(title), run_time=1.3)
        self.play(FadeIn(sub, shift=UP * 0.1), GrowFromCenter(orn2), FadeIn(credit), run_time=1.0)
        self.wait(1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(series, plate_no, orn1, title, sub, orn2, credit)), run_time=0.8)

        # ================= Bonn, 1858 =================
        hel = cameo("modern").move_to([-4.2, 0.55, 0])
        hel_name = serif("Hermann von Helmholtz", 24).next_to(hel, DOWN, buff=0.22)
        hel_dates = serif("1821 – 1894", 20, FADED, italic=True).next_to(hel_name, DOWN, buff=0.08)
        place = spaced("Bonn · 1858", 20).move_to([1.6, 2.15, 0])
        intro = VGroup(
            serif("Theorists had mostly studied flows with", 28),
            serif("no spin at all. Helmholtz, a physician turned", 28),
            serif("physicist, asked what the spinning part does:", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([1.6, 1.0, 0])
        ptitle = VGroup(
            serif("Über Integrale der hydrodynamischen Gleichungen,", 23, RED_INK, italic=True),
            serif("welche den Wirbelbewegungen entsprechen", 23, RED_INK, italic=True),
            serif("“On the integrals of the hydrodynamic equations", 17, FADED, italic=True),
            serif("that correspond to vortex motions”", 17, FADED, italic=True),
        ).arrange(DOWN, buff=0.08).move_to([1.7, -0.75, 0])
        if ptitle.width > 8.2:
            ptitle.scale_to_fit_width(8.2)
        self.vo("Bonn, 1858. Theorists had mostly studied flows with no spin at all. "
                "Hermann von Helmholtz, a physician turned physicist, asked what the spinning part of a flow actually does, "
                "in a paper on the integrals of the hydrodynamic equations that correspond to vortex motions.")
        self.play(FadeIn(hel, scale=0.9), FadeIn(place), run_time=0.9)
        self.play(FadeIn(hel_name, shift=UP * 0.1), FadeIn(hel_dates), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in intro], lag_ratio=0.4), run_time=1.6)
        self.play(Write(ptitle[:2]), FadeIn(ptitle[2:]), run_time=1.8)
        self.wait(1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(hel, hel_name, hel_dates, place, intro, ptitle)), run_time=0.8)

        # ================= a single vortex + Helmholtz's laws =================
        hdr = header("Helmholtz's Vortex Laws", "what a whirl does in a perfect, frictionless fluid")
        VC = np.array([-3.6, -0.15, 0])
        GAM = 4.0
        core = np.array([VC[:2]])

        def single_field(xy):
            return vortex_velocity(xy, core, np.array([GAM]), core2=0.06)

        streaks = Streaks(150, VC, 2.6, 2.35, single_field, life=(2.0, 4.0))
        glyph_angle = ValueTracker(0.0)
        glyph_angle.add_updater(lambda m, dt: m.increment_value(2.2 * dt))
        glyph = always_redraw(lambda: core_glyph(VC, 1, glyph_angle.get_value(), 0.26))
        loop = DashedVMobject(Circle(radius=1.35, color=RED_INK, stroke_width=2.4).move_to(VC), num_dashes=36)
        loop_tips = VGroup(*[Triangle(fill_color=RED_INK, fill_opacity=1, stroke_width=0).scale(0.08)
                             .rotate(a + PI / 2 + PI / 6).move_to(VC + 1.35 * np.array([np.cos(a), np.sin(a), 0]))
                             for a in (PI / 4, 5 * PI / 4)])
        circ = ink_card(MathTex(r"\Gamma = \oint \mathbf{v}\cdot d\mathbf{l}", font_size=30, color=RED_INK), pad=0.12)
        circ.move_to(VC + np.array([0, -1.95, 0]))
        circ_lbl = serif("circulation: the strength of the whirl", 15, FADED, italic=True).next_to(circ, UP, buff=0.06)
        circ_lbl.move_to(VC + np.array([0, 1.95, 0]))

        laws = VGroup()
        for num, line1, line2 in [
            ("I", "Vortex lines move with the fluid,", "as if dyed into it"),
            ("II", "A vortex tube keeps the same", "strength Γ, forever"),
            ("III", "It can never simply end: it closes", "into a ring, or reaches a wall"),
        ]:
            numeral = serif(num, 28, RED_INK, bold=True)
            body = VGroup(serif(line1, 21, INK), serif(line2, 21, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            row = VGroup(numeral, body).arrange(RIGHT, buff=0.3, aligned_edge=UP)
            numeral.align_to(body, UP)
            laws.add(row)
        laws.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([2.75, 0.05, 0])
        for row in laws:
            row[0].set_x(laws.get_left()[0] + 0.25)

        immortal = stamp(r"\text{no friction} \;\Rightarrow\; \text{vortices are immortal}", size=30, rot=-3 * DEGREES)
        immortal.move_to([2.75, -2.25, 0])

        self.play(FadeIn(hdr, shift=DOWN * 0.1),
                  say("A vortex is fluid spinning around a line, like water round a plughole."), run_time=0.9)
        self.add(streaks, glyph_angle, glyph)
        self.play(FadeIn(streaks), FadeIn(glyph), run_time=0.8)
        self.wait(1.4)
        self.play(Create(loop), FadeIn(loop_tips), FadeIn(circ), FadeIn(circ_lbl),
                  say("Its strength is the circulation Γ: the swirl measured around any loop enclosing it."),
                  run_time=1.2)
        self.wait(1.6)
        for i, line in enumerate(["Helmholtz proved three laws. Vortex lines are carried along with the fluid…",
                                  "…a vortex tube's strength never changes…",
                                  "…and a vortex can never just stop in mid-fluid."]):
            self.play(FadeIn(laws[i], shift=LEFT * 0.15), say(line), run_time=0.9)
            self.wait(0.8)
        self.play(FadeIn(immortal, scale=1.4), say("Without friction, nothing can create a vortex or destroy one."),
                  run_time=0.7)
        self.wait(2.0)

        streaks.clear_updaters()
        glyph_angle.clear_updaters()
        self.play(FadeOut(VGroup(hdr, streaks, glyph, loop, loop_tips, circ, circ_lbl, laws, immortal)), unsay(),
                  run_time=0.9)
        self.remove(streaks, glyph, glyph_angle)

        # ================= the vortex ring =================
        hdr2 = header("The Vortex Ring", "a vortex tube closed on itself: a smoke ring")
        RC = np.array([-3.7, -0.15, 0])
        ring = perspective_ring(RC)
        axis = DashedLine(RC + LEFT * 1.6, RC + RIGHT * 1.9, color=FADED, stroke_width=1.5, dash_length=0.08)
        top_c, bot_c = RC + UP * 1.46, RC + DOWN * 1.46
        spins = VGroup(swirl_arrow(top_c, 0.36, ccw=True), swirl_arrow(bot_c, 0.36, ccw=False))
        go = Arrow(RC + RIGHT * 1.0, RC + RIGHT * 2.3, buff=0, color=RED_INK, stroke_width=5,
                   max_tip_length_to_length_ratio=0.25)
        go_lbl = serif("it carries itself forward", 17, RED_INK, italic=True).next_to(go, DOWN, buff=0.12)
        go_lbl.shift(RIGHT * max(0.0, ring.get_right()[0] + 0.15 - go_lbl.get_left()[0]))

        XC = np.array([3.4, -0.15, 0])
        cut_title = spaced("Cross-section", 16, INK).move_to(XC + UP * 2.2)
        cut_sub = serif("slice the ring through its axis", 15, FADED, italic=True).next_to(cut_title, DOWN, buff=0.05)
        cores2 = VGroup(core_glyph(XC + UP * 0.8, 1, 0, 0.3), core_glyph(XC + DOWN * 0.8, -1, 0, 0.3))
        jet = VGroup(*[Arrow(XC + LEFT * 0.7 + UP * dy, XC + RIGHT * 0.9 + UP * dy, buff=0, color=BLUE_INK,
                             stroke_width=3, max_tip_length_to_length_ratio=0.18) for dy in (-0.25, 0, 0.25)])
        back = VGroup(*[CurvedArrow(XC + RIGHT * 0.6 + UP * s * 1.15, XC + LEFT * 0.6 + UP * s * 1.15,
                                    angle=s * 0.9, color=FADED, stroke_width=2, tip_length=0.12) for s in (1, -1)])
        cut_note = serif("two opposite whirls push the fluid between them, and themselves, forward", 15, FADED,
                         italic=True).move_to(XC + DOWN * 1.95)
        if cut_note.width > 6.0:
            cut_note.scale_to_fit_width(6.0)

        self.play(FadeIn(hdr2, shift=DOWN * 0.1), FadeIn(ring, scale=0.9), Create(axis),
                  say("Close a vortex tube on itself and you get a ring, the shape of every smoke ring."), run_time=1.1)
        self.play(Create(spins), run_time=0.9)
        self.play(GrowArrow(go), FadeIn(go_lbl), say("The fluid whirls around the ring, and the ring glides along its axis."),
                  run_time=0.9)
        self.wait(1.2)
        self.play(FadeIn(cut_title), FadeIn(cut_sub), FadeIn(cores2, scale=0.6), run_time=0.8)
        self.play(LaggedStart(*[GrowArrow(j) for j in jet], lag_ratio=0.2), Create(back), FadeIn(cut_note),
                  say("Cut through it, and the ring becomes a pair of opposite whirls."), run_time=1.2)
        self.wait(2.0)
        self.play(FadeOut(VGroup(hdr2, ring, axis, spins, go, go_lbl, cut_title, cut_sub, cores2, jet, back, cut_note)),
                  unsay(), run_time=0.9)

        # ================= leapfrog =================
        hdr3 = header("Leapfrog", "two rings on one axis, computed from the vortex equations")
        a, s0, G = 0.7, 0.6, 3.4
        x_start = -5.6
        sysv = VortexSystem([[x_start, a], [x_start, -a], [x_start + s0, a], [x_start + s0, -a]], [G, -G, G, -G])
        cols = [RED_INK, RED_INK, BLUE_INK, BLUE_INK]
        seeds, seed_cols = [], []
        for i, (cx, cy) in enumerate(sysv.P):
            for _ in range(75):
                r = abs(RNG.normal(0, 0.1))
                th = RNG.uniform(0, TAU)
                seeds.append([cx + r * np.cos(th), cy + r * np.sin(th)])
                seed_cols.append(cols[i])
        smoke = Smoke(seeds, seed_cols, lambda xy: vortex_velocity(xy, sysv.P, sysv.G, core2=0.035),
                      x_fade=(-6.7, 6.3), radius=0.028, opacity=0.55)
        driver = Mobject()
        driver.add_updater(lambda m, dt: sysv.step(dt) if dt > 0 else None)
        glyphs = always_redraw(lambda: VGroup(*[
            core_glyph([p[0], p[1], 0], np.sign(g), ang, 0.17, color=col)
            .set_stroke(opacity=0.9 * float(np.clip((6.3 - p[0]) / 0.5, 0, 1)))
            for p, g, ang, col in zip(sysv.P, sysv.G, sysv.angle, cols)]))
        axis2 = DashedLine([-6.6, 0, 0], [6.5, 0, 0], color=FADED, stroke_width=1.2, dash_length=0.1)
        key = VGroup(
            VGroup(Dot(radius=0.07, color=RED_INK), serif("ring A", 16, RED_INK, italic=True)).arrange(RIGHT, buff=0.1),
            VGroup(Dot(radius=0.07, color=BLUE_INK), serif("ring B", 16, BLUE_INK, italic=True)).arrange(RIGHT, buff=0.1),
        ).arrange(RIGHT, buff=0.4).move_to([4.9, 2.42, 0])
        sim_note = serif("each ring seen in cross-section, as a pair of whirls", 14, FADED, italic=True)
        sim_note.move_to([-4.3, 2.42, 0])

        self.play(FadeIn(hdr3, shift=DOWN * 0.1), Create(axis2), FadeIn(key), FadeIn(sim_note),
                  say("Now send two rings along the same axis, one just behind the other."), run_time=1.0)
        self.add(driver, smoke, glyphs)
        self.play(FadeIn(smoke), FadeIn(glyphs), run_time=0.6)
        self.wait(2.0)
        self.play(say("The front ring's whirl squeezes the rear ring: it shrinks, speeds up, and slips straight through…"),
                  run_time=0.8)
        self.wait(3.0)
        self.play(say("…then the roles swap. The rings play leapfrog, again and again."), run_time=0.8)
        self.wait(3.5)

        for m in (driver, smoke):
            m.clear_updaters()
        self.play(FadeOut(VGroup(hdr3, axis2, key, sim_note, smoke, glyphs)), unsay(), run_time=0.9)
        self.remove(driver, smoke, glyphs)

        # ================= Edinburgh, 1867 =================
        kel = cameo("beard").move_to([-4.2, 0.55, 0])
        kel_name = serif("William Thomson, Lord Kelvin", 22).next_to(kel, DOWN, buff=0.22)
        kel_dates = serif("1824 – 1907", 20, FADED, italic=True).next_to(kel_name, DOWN, buff=0.08)
        place2 = spaced("Edinburgh · 1867", 20).move_to([1.6, 2.15, 0])
        k_intro = VGroup(
            serif("His friend Peter Guthrie Tait builds a box", 28),
            serif("that fires smoke rings. Kelvin watches them", 28),
            serif("collide, quiver and bounce away, unbroken.", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([1.6, 1.0, 0])

        # Tait's box
        BX = np.array([0.2, -1.25, 0])
        box = VGroup(
            Rectangle(width=1.6, height=1.25, fill_color=PAPER_DARK, fill_opacity=1, stroke_color=INK, stroke_width=2.2),
            Polygon([-0.8, 0.625, 0], [-0.5, 0.85, 0], [1.1, 0.85, 0], [0.8, 0.625, 0], fill_color=PAPER_DARK,
                    fill_opacity=1, stroke_color=INK, stroke_width=1.8),
            Polygon([0.8, 0.625, 0], [1.1, 0.85, 0], [1.1, -0.4, 0], [0.8, -0.625, 0], fill_color="#cbb68f",
                    fill_opacity=1, stroke_color=INK, stroke_width=1.8),
        ).move_to(BX)
        hole_c = box[2].get_center() + np.array([0.0, 0.05, 0])
        hole = Ellipse(width=0.16, height=0.5, fill_color=INK, fill_opacity=0.85, stroke_width=0).move_to(hole_c)
        box_lbl = serif("Tait's smoke box", 15, FADED, italic=True).next_to(box, DOWN, buff=0.12)

        self.vo("Edinburgh, 1867. William Thomson, later Lord Kelvin, watches his friend Peter Guthrie Tait "
                "fire smoke rings from a box. The rings collide, quiver and bounce away, never breaking apart.")
        self.play(FadeIn(kel, scale=0.9), FadeIn(place2), run_time=0.9)
        self.play(FadeIn(kel_name, shift=UP * 0.1), FadeIn(kel_dates), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in k_intro], lag_ratio=0.4), run_time=1.6)
        self.play(FadeIn(box, shift=UP * 0.1), FadeIn(hole), FadeIn(box_lbl), run_time=0.7)
        for k in range(3):
            puff = VGroup(Ellipse(width=0.22, height=0.56, color=SEPIA, stroke_width=11, stroke_opacity=0.75),
                          Ellipse(width=0.12, height=0.38, color=PAPER_DARK, stroke_width=3, stroke_opacity=0.9)
                          ).move_to(hole_c)
            self.add(puff)
            self.play(box.animate(rate_func=there_and_back).shift(RIGHT * 0.06),
                      puff.animate(rate_func=linear).shift(RIGHT * 4.8).scale(1.7).set_opacity(0),
                      run_time=1.6 if k < 2 else 2.0)
            self.remove(puff)
        idea = serif("What if every atom is a vortex ring in the ether?", 30, RED_INK, italic=True)
        idea.move_to([1.6, -0.15, 0])
        self.vo("And Kelvin has a bold idea: what if every atom is a vortex ring in the ether?")
        self.play(FadeOut(box), FadeOut(hole), FadeOut(box_lbl), Write(idea), run_time=1.4)
        self.wait(1.0)
        self.vo_wait()
        self.play(FadeOut(VGroup(kel, kel_name, kel_dates, place2, k_intro, idea)), run_time=0.8)

        # ================= vortex atoms =================
        hdr4 = header("Vortex Atoms", "Kelvin's proposal: matter made of knotted whirls in the ether")
        knot_specs = [(unknot, "a simple ring"), (torus_knot(2, 3), "three crossings"), (figure_eight, "four crossings")]
        xs = [-4.2, 0.0, 4.2]
        names = [r"0_1", r"3_1", r"4_1"]
        knots = VGroup()
        self.play(FadeIn(hdr4, shift=DOWN * 0.1),
                  say("Helmholtz's laws made such rings indestructible, exactly what atoms seemed to need."), run_time=1.0)
        for (fn, desc), x, nm in zip(knot_specs, xs, names):
            frac = ValueTracker(0.02)
            sc = 0.47 if fn is figure_eight else 0.4
            live = always_redraw(lambda fn=fn, x=x, frac=frac, sc=sc: knot_mobject(fn, [x, 0.55, 0], sc, frac.get_value()))
            self.add(live)
            self.play(frac.animate.set_value(1.0), run_time=1.6, rate_func=rate_functions.ease_in_out_sine)
            live.clear_updaters()
            final = knot_mobject(fn, [x, 0.55, 0], sc, 1.0)
            self.remove(live)
            self.add(final)
            lbl = VGroup(MathTex(nm, font_size=30, color=INK), serif(desc, 16, FADED, italic=True)).arrange(DOWN, buff=0.06)
            lbl.move_to([x, -1.05, 0])
            self.play(FadeIn(lbl, shift=UP * 0.1), run_time=0.4)
            knots.add(VGroup(final, lbl))
        props = ink_card(VGroup(
            serif("indestructible, by Helmholtz's laws  ·  able to vibrate, giving spectral lines", 17, INK),
            serif("each kind of knot, perhaps, a different chemical element", 17, RED_INK, italic=True),
        ).arrange(DOWN, buff=0.08), pad=0.18).move_to([0, -2.15, 0])
        self.play(FadeIn(props, shift=UP * 0.1),
                  say("Different knots might be different elements, so Tait set out to list every knot there is."),
                  run_time=0.9)
        self.wait(2.6)
        self.play(FadeOut(VGroup(hdr4, knots, props)), unsay(), run_time=0.9)

        # ================= the dream fades, knot theory is born =================
        hdr5 = header("A Beautiful Failure", "the ether vanished, and the vortex atom with it")
        table_bg = RoundedRectangle(corner_radius=0.08, width=9.6, height=3.0, fill_color=PAPER, fill_opacity=0.96,
                                    stroke_color=INK, stroke_width=1.4).move_to([0, 0.35, 0])
        table_in = RoundedRectangle(corner_radius=0.06, width=9.45, height=2.85, stroke_color=INK, stroke_width=0.5)
        table_in.move_to(table_bg)
        tab_title = spaced("Tait's table of knots", 15, SEPIA).move_to([0, 1.6, 0])
        entries = [(torus_knot(2, 3), r"3_1"), (figure_eight, r"4_1"), (torus_knot(2, 5), r"5_1"),
                   (lambda t: torus_knot(3, 4)(t) * np.array([1, 1, 1]), r"8_{19}")]
        cells = VGroup()
        for i, (fn, nm) in enumerate(entries):
            x = -3.45 + 2.3 * i
            k = knot_mobject(fn, [x, 0.3, 0], 0.32 if fn is figure_eight else 0.27, 1.0, width=4.5, gap=0.1)
            cells.add(VGroup(k, MathTex(nm, font_size=26, color=INK).move_to([x, -0.75, 0])))
        legacy = VGroup(
            serif("Tait's lists outlived the theory that inspired them:", 24),
            serif("they became the first chapter of modern knot theory.", 24, RED_INK, italic=True),
        ).arrange(DOWN, buff=0.1).move_to([0, -1.7, 0])
        self.play(FadeIn(hdr5, shift=DOWN * 0.1), FadeIn(table_bg), FadeIn(table_in), FadeIn(tab_title),
                  say("By the early 1900s the ether was gone, and the vortex atom with it."), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in cells], lag_ratio=0.25), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in legacy], lag_ratio=0.35),
                  say("But Helmholtz's laws live on in every smoke ring, tornado and wingtip vortex."), run_time=1.2)
        self.wait(2.6)
        self.play(FadeOut(VGroup(hdr5, table_bg, table_in, tab_title, cells, legacy)), unsay(), run_time=0.9)

        # ================= moral + timeline =================
        moral = VGroup(
            serif("In a perfect fluid, a vortex lives forever.", 34),
            serif("Kelvin hoped that matter would too.", 34, RED_INK, italic=True),
        ).arrange(DOWN, buff=0.18).move_to([0, 1.55, 0])

        TL_Y = -0.9

        def yx(year):
            return -5.6 + 11.2 * (year - 1700) / 250

        tl_line = Line([yx(1700), TL_Y, 0], [yx(1950), TL_Y, 0], color=INK, stroke_width=1.6)
        tl_ticks = VGroup()
        for yr in range(1700, 1951, 50):
            tl_ticks.add(Line([yx(yr), TL_Y - 0.07, 0], [yx(yr), TL_Y + 0.07, 0], color=INK, stroke_width=1.2))
            tl_ticks.add(serif(str(yr), 15, FADED).move_to([yx(yr), TL_Y - 0.28, 0]))

        def tl_mark(year, label, color=FADED, up=True, dx=0.0):
            dot = Dot([yx(year), TL_Y, 0], radius=0.07, color=color)
            txt = serif(label, 16, color, italic=True)
            txt.next_to(dot, UP if up else DOWN, buff=0.14 if up else 0.42).shift(RIGHT * dx)
            return VGroup(dot, txt)

        marks = VGroup(tl_mark(1752, "1752 · the paradox"),
                       tl_mark(1858, "1858 · Helmholtz's vortex laws", RED_INK, dx=-1.35),
                       tl_mark(1867, "1867 · Kelvin's vortex atoms", RED_INK, up=False),
                       tl_mark(1877, "1877 · Tait's knot tables", FADED, dx=1.3))
        self.vo("In a perfect fluid, a vortex lives forever. Kelvin hoped that matter would too.")
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in moral], lag_ratio=0.4), run_time=1.4)
        self.play(Create(tl_line), FadeIn(tl_ticks), LaggedStart(*[FadeIn(m, shift=UP * 0.08) for m in marks],
                                                                 lag_ratio=0.3), run_time=1.6)
        self.wait(2.0)
        nxt = VGroup(ornament(2.4), spaced("Next · Plate V · Circulation and Lift", 18, SEPIA)).arrange(DOWN, buff=0.15)
        nxt.move_to([0, -3.12, 0])
        self.vo("Next, in plate five: circulation and lift.")
        self.play(FadeIn(nxt, shift=UP * 0.1), run_time=0.8)
        self.vo_wait()
        self.wait(1.5)


# =====================================================================
# Episode bookends: opening series card and end card
# Render:  manim -pqh worlds_of_flow.py SeriesIntro   /   SeriesOutro
# =====================================================================

class SeriesIntro(NarratedScene):
    def construct(self):
        self.camera.background_color = PAPER
        paper, frame = paper_background()
        self.add(paper)
        self.play(FadeIn(frame), run_time=0.8)

        title = serif("Worlds of Flow", 72).move_to([0, 2.05, 0])
        orn = ornament(4.0).next_to(title, DOWN, buff=0.3)
        sub = serif("four plates from the history of hydrodynamics", 26, FADED, italic=True).next_to(orn, DOWN, buff=0.3)
        self.vo("Worlds of Flow: four plates from the history of hydrodynamics. How, over a century and a half, "
                "mathematicians and engineers learned how water and air really move.")
        self.play(Write(title), run_time=1.6)
        self.play(GrowFromCenter(orn), FadeIn(sub, shift=UP * 0.1), run_time=0.9)

        plates = [("I", "D'Alembert's Paradox", "1752"), ("II", "The Boundary Layer", "1904"),
                  ("III", "Reynolds and Turbulence", "1883"), ("IV", "Vortices", "1858 – 1867")]
        rows = VGroup()
        for num, name, year in plates:
            n = serif(num, 26, RED_INK, bold=True)
            t = serif(name, 28, INK)
            y = serif(year, 20, FADED, italic=True)
            rows.add(VGroup(n, t, y))
        for r in rows:
            r[0].move_to([-3.2, 0, 0])
            r[1].next_to(r[0], RIGHT, buff=0.5).set_x(r[1].width / 2 - 2.55)
            r[2].next_to(r[1], RIGHT, buff=0.4)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to([0, -1.3, 0])
        for r in rows:
            r[0].set_x(-3.2)
            r[1].shift(RIGHT * (-2.55 - r[1].get_left()[0]))
            r[2].next_to(r[1], RIGHT, buff=0.4)
        self.wait(0.6)
        self.vo("Plate one: d'Alembert's paradox. Two: the boundary layer. "
                "Three: Reynolds and turbulence. And four: vortices.")
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.15), run_time=0.7)
            self.wait(0.75)
        credit = serif("after the history of hydrodynamics in O. Darrigol, Worlds of Flow (Oxford, 2005)", 16, FADED,
                       italic=True).move_to([0, -3.2, 0])
        self.play(FadeIn(credit), run_time=0.6)
        self.vo_wait()
        self.wait(0.8)
        self.play(FadeOut(VGroup(title, orn, sub, rows, credit)), run_time=0.9)


class SeriesOutro(NarratedScene):
    def construct(self):
        self.camera.background_color = PAPER
        paper, frame = paper_background()
        self.add(paper, frame)
        thanks = serif("Thank you for watching", 54).move_to([0, 1.1, 0])
        orn = ornament(3.4).next_to(thanks, DOWN, buff=0.35)
        lines = VGroup(
            serif("Worlds of Flow · Plates I – IV", 24, SEPIA, italic=True),
            serif("history after Olivier Darrigol, Worlds of Flow: A History of Hydrodynamics", 18, FADED, italic=True),
            serif("from the Bernoullis to Prandtl (Oxford University Press, 2005)", 18, FADED, italic=True),
            serif("animated with Manim · narration by a synthetic voice", 16, FADED, italic=True),
        ).arrange(DOWN, buff=0.14).next_to(orn, DOWN, buff=0.45)
        self.vo("Thank you for watching.")
        self.play(FadeIn(thanks, shift=UP * 0.1), GrowFromCenter(orn), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.08) for l in lines], lag_ratio=0.25), run_time=1.4)
        self.vo_wait()
        self.wait(2.5)
        self.play(FadeOut(VGroup(thanks, orn, lines, frame)), run_time=1.2)
        self.wait(0.4)
