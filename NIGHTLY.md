# Nightly run

Each night a scheduled run makes **one** draft video from the queue and logs it. The run has no one to ask,
so it decides, writes down what it decided, and leaves the final judgement to the review in the Sheet.

Sheet: `1e1RsozK5NgMf9qCgiLtKh4qZOM34GDP90v3wwQlfvgI` (tabs: Overview, Ideas, Books, Log, Settings,
Style Notes). Repository: `sony-alias/science-stories-studio`.

## 1. Prepare

1. Clone the repository and run `bash scripts/setup.sh`. It must end with `ready`. Commit as
   `sony-alias <sony-alias@users.noreply.github.com>`; GitHub refuses pushes that show a private email.
   Read **Settings** too.
2. Read **Style Notes** in full, including *Lessons from your feedback*. These rules win over this file.
3. Read the **Log**. For every row with a verdict of *Revise* or *Reject* and feedback that is not yet
   reflected in Style Notes, add a short lesson under *Lessons from your feedback*.
4. If any *Revise* row exists that has not been redone (no later Log row for the same Idea ID), redo
   that idea tonight instead of a new one, applying the feedback.

## 2. Pick the idea

From **Ideas**, take the row with Status *Queued*, the lowest Priority number, then the lowest Idea ID.
Set its Status to *In production*. Read its Book row in **Books** for the human story behind it.

## 3. Research

- Find at least three reliable sources: the book itself where possible, a primary paper or archive, and an
  encyclopedia or university page. Note each URL.
- Check every date, name, number and quotation against a source. Do not invent quotations. If something
  cannot be confirmed, leave it out or say plainly that it is uncertain.

## 4. Write the script

- Length as set in **Settings → Format** (currently 2 to 4 minutes, roughly 300 to 550 words of narration).
- Shape: a person and a puzzle in the first 20 seconds; the failed or obvious answer; the idea built up
  visually, one step at a time; the payoff; why it matters now; for engineering, one *Try it yourself*
  step a student can do with cheap materials (from the Idea's "Try it yourself" column).
- Spoken English, short sentences, no jargon without a picture. One idea per line of narration.
- Save the script as `episodes/<IdeaID>_script.md` with the sources at the end.

## 5. Build the scenes

- Create `episodes/<IdeaID>_<short_name>.py` from `episodes/TEMPLATE.py`. Use the kit's look
  (`paper_background`, `serif`, `ink_card`, `cameo`, sepia and red ink) unless Style Notes say otherwise.
- Use `self.vo(...)` for every narration line, then the animations that go with it. Show the actual
  mechanism, not decoration. Prefer real equations and real data when they help.
- Add `PRONOUNCE` entries for any names or heteronyms in the script.
- Kit lessons: a mobject removed in the middle of `play()` stays drawn until the end of that `play()`, so
  set its opacity to 0 first, or recycle mobjects. Check every text for overlap and for staying inside the
  frame.

## 6. Check before the full render

1. Render at low quality: `manim -ql --frame_rate 30 episodes/<file>.py <Scene>`.
2. Take a still every 5 seconds with ffmpeg and look at every one of them. Fix overlaps, clipped text,
   empty stretches, and anything that disagrees with the narration. Repeat until clean.
3. Read the script once more against the sources.

## 7. Render and finish

1. `manim -qh --frame_rate 30 episodes/<file>.py <Scene>`
2. `scripts/finish_video.sh <rendered>.mp4 out/<IdeaID>_<short_name>.mp4`
3. Make a thumbnail still (`out/<IdeaID>_thumb.png`) from the strongest frame.
4. Commit the episode file, script, any kit changes, and push to `main`.

## 8. Store the video

1. `scripts/store_video.sh <IdeaID>-<YYYYMMDD> out/<IdeaID>_<short_name>.mp4 out/<IdeaID>_thumb.png`
   It puts the files on their own branch, `video/<IdeaID>-<YYYYMMDD>`, and prints a link for each file.
   GitHub releases cannot be made from a session, which is why videos live on branches.
2. Keep each call under about 50 MB. If the video is bigger, re-encode it first:
   `ffmpeg -i in.mp4 -c:v libx264 -preset veryfast -crf 23 -c:a copy -movflags +faststart out.mp4`
3. If storing fails, also attach the video and thumbnail to the run's own conversation, and say so in
   *Run notes*.

## 9. Log it

Append one row to **Log**: Date (today, IST), Idea ID, leave Title (it is a formula), Status
*Draft ready* (or *Failed check* if the video could not pass step 6), Length (m:ss), Video link, Script link
(the file on GitHub), Sources (URLs separated by new lines), Self-check notes (what was checked, anything
still doubtful), leave the review columns empty, Run notes (decisions taken, problems hit).

Set the Idea's Status to *Draft ready* (or back to *Queued* with a note if it failed).

## 10. Never

- Never upload to YouTube or Instagram. Publishing is done by hand after review.
- Never delete or rewrite earlier Log rows, review columns or the owner's feedback.
- Never present an uncertain fact as certain.
