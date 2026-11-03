# Science Stories Studio

Story-led explainer videos on engineering, mathematics, physics and complex systems, in the spirit of
Veritasium and 3Blue1Brown. Every video follows a person, not just an idea, and engineering videos end with
something the viewer can build or try.

The planning lives in the Google Sheet **Science Stories: Nightly Video Pipeline**
(`1e1RsozK5NgMf9qCgiLtKh4qZOM34GDP90v3wwQlfvgI`): the books, the queue of ideas, the nightly log and the
style notes learned from review. A scheduled run makes one draft video each night and logs it there.
Publishing to YouTube and Instagram is done by hand after review.

## Layout

| Path | What it is |
|---|---|
| `kit/worlds_of_flow.py` | The style kit: engraved paper look, narrated scenes (`NarratedScene.vo`), offline voice, pronunciation fixes, flow and vortex helpers. Also holds the four *Worlds of Flow* plates and the series intro and outro. |
| `episodes/` | One file per new video. Start from `episodes/TEMPLATE.py`. |
| `scripts/setup.sh` | Installs Manim, LaTeX, the Kokoro voice and checks narration works. |
| `scripts/finish_video.sh` | Brings a rendered video to YouTube loudness (-16 LUFS). |
| `scripts/make_episode.py` | Joins several narrated parts with crossfades and exact audio sync. |
| `NIGHTLY.md` | The step-by-step procedure each nightly run follows. |

## Quick start

```bash
bash scripts/setup.sh
manim -qh --frame_rate 30 kit/worlds_of_flow.py DAlembertParadox
scripts/finish_video.sh media/videos/worlds_of_flow/1080p30/DAlembertParadox.mp4 out/plate1.mp4
```

## Narration

`self.vo("text")` speaks a line with the Kokoro voice `af_heart` and holds the scene until the line ends,
so the picture follows the voice. Lines are cached by their phonemes, so changing a word regenerates only
that line. When a word is said wrongly, add it to `PRONOUNCE` in the kit, as IPA. For words spelt the same
but said differently ("lives", "tears", "close", "presents") add the whole phrase, not the single word.
Years from 1700 to 1999 are read the way people say them.

## Rendered videos

Videos are not committed. Finished drafts go to this repository's Releases, one release per video, and the
link goes in the Log tab of the Sheet.
