"""<Idea ID> <Working title>, a Science Stories episode.

Render:  manim -qh --frame_rate 30 episodes/<this file>.py <SceneName>
Then:    scripts/finish_video.sh media/videos/<this file>/1080p30/<SceneName>.mp4 out/<Idea ID>.mp4
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
from worlds_of_flow import *  # noqa: E402,F401,F403  palette, NarratedScene, helpers


class ExampleEpisode(NarratedScene):
    def construct(self):
        self.add(*paper_background())   # (paper texture, printed frame)
        title = serif("A story worth telling", size=48)
        self.vo("Every idea in science began with a person who was puzzled.")
        self.play(Write(title), run_time=2)
        self.vo_wait()
        self.wait(1)
