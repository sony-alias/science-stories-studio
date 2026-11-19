# I024 1202: The Alarm on the Way to the Moon

Story after David A. Mindell, *Digital Apollo: Human and Machine in Spaceflight* (MIT Press, 2008), credited for
the story; the book was not consulted directly for this draft. Facts checked against the sources listed at the end.

Scene file: `episodes/I024_apollo_1202.py` (scene `Apollo1202`).

## Narration

1. Science Stories. 1202: the alarm on the way to the Moon.
2. The twentieth of July, 1969. Neil Armstrong and Buzz Aldrin are dropping towards the Moon in the lunar module, Eagle.
3. About five minutes into the descent, a warning light comes on. Armstrong: "Program alarm. It's a 1202."
4. He asks Houston for a reading on it. The surface is about seven minutes away.
5. In Mission Control, the question lands on Steve Bales, the guidance officer. He is twenty-six. Abort, or keep going?
6. In a back room sits his support engineer, Jack Garman, a computer specialist. He is twenty-four.
7. Two weeks earlier, they had been here before. On the fifth of July, in a practice landing, the simulation supervisor, Dick Koos, slipped in a 1201 alarm.
8. Bales did not know what it meant, so he called an abort. It was the wrong call. The landing could have gone on.
9. So flight director Gene Kranz had them study every alarm the computer could raise. Garman wrote them all down by hand.
10. For this one, his rule was simple: if it doesn't come back too often, we're fine.
11. Now, for real, Garman says go. Bales calls it: "We're go on that, Flight." And up to Eagle: "We're go on that alarm."
12. But what was the computer complaining about?
13. The guidance computer had to do many jobs at once: work out where they were, steer, throttle the engine, and update the displays.
14. Its scheduler, designed by Hal Laning at M.I.T., gave every job a priority. The most important waiting job always ran first.
15. But every waiting job needed a slot of memory, and there were only a handful of slots.
16. During the landing, a second radar was switched on: the rendezvous radar, there to find the command module if they had to abort.
17. A mismatch in its electrical interface made it send a stream of meaningless signals, and the computer paused to count every one. That ate about thirteen percent of its time.
18. With less time, jobs finished late. New copies arrived before the old ones were done. The slots filled up.
19. When a new job found no free slot, the computer raised alarm 1202. When it ran out of working space, 1201.
20. And then it did something clever. It restarted. It cleared the queue, and rebuilt only the jobs marked as vital, from where they had last saved their place.
21. Less important work simply disappeared. Guidance, steering and the engine carried on.
22. There were five alarms in all: four of them 1202, and one 1201. Each time, the answer from Houston was the same. Go.
23. Then the call: thirty seconds of fuel. Contact light. "Houston, Tranquility Base here. The Eagle has landed."
24. The computer was overloaded, and it landed anyway, because it had been told in advance what mattered most.
25. That idea is everywhere now. Flight computers, car controllers, even your phone, share out their time by priority.
26. Try it yourself. Write a tiny priority scheduler in Python.
27. Give each job a priority and a cost, and give the computer a fixed amount of time every tick.
28. Add a thief that steals thirteen percent, and watch the queue grow.
29. Then add a restart that keeps only the vital jobs, and check whether guidance ever misses a tick.
30. Five alarms, two young engineers who had done their homework, and a computer that knew what to drop.

## On-screen labels and hedges

- Lunar module, DSKY, Mission Control consoles, radar dish: schematic drawings.
- Silhouettes of Bales and Garman are stylised, not likenesses.
- Garman's list on screen is a reconstruction in our own words, not his handwriting.
- Slot boxes: "core sets: 8 (Eyles 2004; another account says 7)". Job names are simplified.
- Queue animation is labelled "illustration, not the real program".
- "about 13%": Eyles's working figure (he gives about 15% at the maximum rate, 13% as the conservative assumption).
- Cause: Eyles calls it an interface/documentation problem (800 Hz phase), other accounts a switch setting; the
  narration says "a mismatch in its electrical interface" and the card notes that accounts differ on blame.
- "Two weeks earlier": the simulation was on 5 July 1969, 15 days before the landing.
- Who ordered the alarm review: Collectspace and Monash Lens both name Kranz; Space.com says Bales asked Garman to
  draw up the sheet. Narration names Kranz for the review and Garman for the list, which fits all three.
- Python on screen is our own example, not Apollo code.

## Sources

- D. Eyles, "Tales from the Lunar Module Guidance Computer", AAS 04-064 (2004):
  https://klabs.org/history/apollo_11_alarms/eyles_2004/eyles_2004_z.htm
- P. Adler, "Apollo 11 Program Alarms", Apollo Lunar Surface Journal:
  https://www.nasa.gov/wp-content/uploads/static/history//alsj/a11/a11.1201-pa.html
- Apollo Expeditions to the Moon (NASA SP-350), ch. 11.4, landing transcript:
  https://www.nasa.gov/wp-content/uploads/static/history/SP-350/ch-11-4.html
- R. Pearlman, Jack Garman obituary, collectSPACE (2016):
  https://www.collectspace.com/news/news-092016b-obituary-jack-garman-apollo11.html
- Space.com, "Apollo 11's Momentous Landing Came Down to One Tough Call" (2019):
  https://www.space.com/apollo-11-guidance-officer-remembers-moon-landing-drama.html
- J. Lattanzio, "Koos control", Monash Lens (2019):
  https://lens.monash.edu/@science/2019/07/17/1375837/koos-control-the-man-who-made-the-apollo-11-moon-landing-possible
- M. Hersch, "Troubleshooting 101 (1201 actually, and 1202 too)", Air & Space / Smithsonian:
  https://www.smithsonianmag.com/air-space-magazine/troubleshooting-101-1201-actually-and-1202-too-111339271/
- D. A. Mindell, Digital Apollo (MIT Press, 2008), credited for the story; not consulted directly.
