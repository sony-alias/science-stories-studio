# I014 · The Transistor's Messy Birth

Book: Jon Gertner, *The Idea Factory: Bell Labs and the Great Age of American Innovation*
(New York: Penguin Press, 2012). Credited for the story; told in our own words. The book itself was not
consulted directly in this run; every fact below was checked against the web sources listed at the end.
Field: Engineering. Scene file: `episodes/I014_transistor_birth.py`, scene `TransistorBirth`.

## Narration

1. Science Stories. The transistor's messy birth.
2. December 1947, at Bell Labs. Walter Brattain takes a razor blade to a strip of gold foil.
3. The foil is glued around the tip of a plastic wedge.
4. One careful cut splits it into two gold contacts, about the width of a sheet of paper apart.
5. A spring presses them onto a slab of germanium.
6. And on December the sixteenth, this crude contraption amplifies a signal, roughly a hundred times.
7. The telephone network ran on vacuum tubes: hot, power-hungry and unreliable.
8. Bell Labs wanted an amplifier made from a solid crystal.
9. The obvious design came from their boss, William Shockley, in 1945.
10. Hold a charged plate near a thin layer of semiconductor, and its electric field should pull in extra electrons, and let more current flow.
11. It did not work as planned.
12. The theorist John Bardeen worked out why: electrons trapped at the crystal's surface were blocking the field, like a crowd jammed in a doorway.
13. The gold wedge was Bardeen and Brattain's way around it.
14. A week later, someone spoke through it for the lab's executives, and was heard, amplified.
15. Shockley called it a magnificent Christmas present.
16. But he later admitted that his elation was balanced by the frustration of not being one of the inventors.
17. He spent New Year's Eve alone in a Chicago hotel, filling about thirty pages of notes.
18. Then, on January the twenty-third, 1948, he found a different design: a sandwich of crystal, with no delicate points.
19. To see how it works, start with a pure crystal of germanium or silicon. Its electrons are locked into bonds, so it barely conducts.
20. Add a trace of phosphorus, and each phosphorus atom brings one spare electron, free to roam. That is N-type.
21. Add boron instead, and each boron atom leaves a gap where an electron is missing.
22. The gap moves like a positive charge. We call it a hole. That is P-type.
23. Shockley's sandwich is N-type, then a very thin slice of P-type, then N-type again.
24. Put a battery across it, and almost nothing flows.
25. The middle layer blocks the electrons.
26. Now feed a tiny current into that middle layer, the base.
27. Electrons pour in from the left.
28. The base is so thin that most of them never meet a hole, and are swept into the far side.
29. So a small current in the base controls a current many times larger, often around a hundred times. That is amplification.
30. Stop the small current, and the big one stops too. That is a switch.
31. Bell Labs announced working junction transistors in 1951, and within a year they beat the best point-contact devices.
32. In 1956 all three shared the Nobel Prize in Physics, though by then they were no longer working together.
33. And here is the twist.
34. By 1960, Mohamed Atalla and Dawon Kahng at Bell Labs had tamed the surface with a thin layer of oxide.
35. Shockley's failed field-effect idea came back to life.
36. Today, over ninety-nine percent of microchips are built from these field-effect transistors.
37. Try it yourself. You need an N P N transistor, a nine-volt battery, an L.E.D., and two one-thousand-ohm resistors.
38. Wire plus through the L.E.D. and a resistor to the collector, and the emitter to minus.
39. Run the base through the other resistor to a bare wire, and put a second bare wire on plus.
40. Touch both wires with one finger.
41. The tiny current through your skin switches on a much larger one, and the L.E.D. lights.
42. If the glow is faint, dampen your fingertip.

## On-screen labels that hedge

- "roughly 100×" for the point-contact gain (CHM: "up to 100 times"; Brattain: "order of magnitude of 100").
- "typical gain ≈ 100; varies by transistor" for the junction transistor.
- The point-contact drawing, the vacuum tube, the field-effect slab and the electron animation are labelled schematic.
- "1959–60" for the MOS transistor: the CHM Silicon Engine page says 1959, the CHM blog says it was described at a conference in 1960.
- Shockley quote attributed: "as quoted in Electronic News, 1972".
- Try-it: "9 V battery only, never mains · keep the resistors in"; part shown as "e.g. 2N3904 or BC547". The 1 kΩ base resistor limits the base current if the two bare wires touch each other directly.

## Sources

- Computer History Museum, "1947: Invention of the Point-Contact Transistor":
  https://www.computerhistory.org/siliconengine/invention-of-the-point-contact-transistor/
- Computer History Museum, "1948: Conception of the Junction Transistor":
  https://www.computerhistory.org/siliconengine/conception-of-the-junction-transistor/
- David Laws, "The Surface State Job", Computer History Museum blog, 2022 (Brattain's notebook, the razor-cut foil,
  the spring, the Dec 23 demonstration, Shockley's 1972 quote via Electronic News):
  https://computerhistory.org/blog/the-surface-state-job/
- PBS, *Transistorized!*: "Shockley's notebook" (New Year's Eve in Chicago, ~30 pages, Jan 23 kitchen table):
  https://www.pbs.org/transistor/background1/events/junctinv.html
- PBS, *Transistorized!*: William Shockley lab page (Jan 23, 1948 notebook; April 1950 NPN demonstration):
  https://www.pbs.org/transistor/science/labpages/labpg9.html
- Computer History Museum, "1951: First Grown-Junction Transistors Fabricated":
  https://www.computerhistory.org/siliconengine/first-grown-junction-transistors-fabricated/
- Computer History Museum, "1960: Metal Oxide Semiconductor (MOS) Transistor Demonstrated":
  https://www.computerhistory.org/siliconengine/metal-oxide-semiconductor-mos-transistor-demonstrated/
- Computer History Museum blog, "13 Sextillion & Counting":
  https://computerhistory.org/blog/13-sextillion-counting-the-long-winding-road-to-the-most-frequently-manufactured-human-artifact-in-history/
- Nobel Prize in Physics 1956, summary and citation: https://www.nobelprize.org/prizes/physics/1956/summary/
- Jon Gertner, *The Idea Factory* (Penguin Press, 2012): credited for the story, not consulted directly.
