# I022 How a Stone Arch Stands: Hooke's Hanging Chain

Story after J. E. Gordon, *Structures: Or Why Things Don't Fall Down* (1978), credited for the story; the book was
not consulted directly for this draft. Facts checked against the sources listed at the end.

Scene file: `episodes/I022_hooke_arch.py` (scene `HookeArch`).

## Narration

1. Science Stories. How a stone arch stands.
2. London, in the years after the Great Fire of 1666. Robert Hooke is helping to rebuild the city as one of its surveyors.
3. He is also the Royal Society's curator of experiments, the man who has to show something new at every meeting.
4. No confirmed portrait of him survives, so we know his face only in outline.
5. Builders around him face an old puzzle. An arch is just a pile of cut stones, with no glue that can hold them together.
6. So why does it stand? And which shape is best? For centuries, builders had relied on circles and on rules of thumb.
7. In 1671, Hooke told the Royal Society that he had solved the true shape of an arch. But he did not say what it was.
8. Instead, at the end of a book on instruments printed in 1676, he hid the answer as a scramble of letters.
9. It was a way to claim an idea without giving it away. The key was published only after his death.
10. Unscrambled, it is Latin. As hangs the flexible line, so, upside down, will stand the rigid arch.
11. Let's see why. Hang a chain between two pins.
12. A chain cannot push, and it cannot resist bending. All it can do is pull, along its own length.
13. Cut out any piece of it. Its weight pulls down. The chain on either side pulls along the curve. Those three forces must balance.
14. The sideways part of the pull is the same all along the chain. Only the upward part grows, as more weight hangs below.
15. That is why the chain is flat at the bottom and steep near the pins.
16. Now turn it upside down. Every pull becomes a push.
17. Build stones along that curve, and each one is only squeezed, straight along the arch. Nothing tries to pull the joints apart.
18. Stone is very strong when squeezed. That is the arch it wants to be.
19. What is this curve? Galileo had called a hanging chain roughly a parabola. It is close, but not the same.
20. In 1691, Leibniz, Huygens and Johann Bernoulli found the exact answer. We now call it the catenary, from the Latin for chain.
21. But real arches are often circles, and many have stood for centuries. How?
22. In 1697, David Gregory gave the answer. An arch of any other shape stands if a hanging-chain line can fit inside its thickness.
23. Engineers call that path the line of thrust. Here it is for a thick semicircle, from the stones' own weight. It stays inside. The arch stands.
24. Make the same arch thin, and the line has to leave the stones. Where it escapes, the joints open like hinges.
25. With enough hinges, the arch folds, and falls.
26. This idea never went away. In 1748, Giovanni Poleni used a hanging chain to check the cracked dome of Saint Peter's in Rome.
27. Antoni Gaudí designed churches upside down, with models made from strings and little weights.
28. And engineers still check old bridges by asking whether a line of thrust can fit inside the stone.
29. Try it yourself. Hang a light chain against a sheet of card, and trace its curve.
30. Cut the card along the curve and flip it over, to make a temporary support.
31. Stack sugar cubes along it, with a dab of icing in each joint. When it has set, slide the card out.
32. Your arch stands with no support. Press gently on the top, and feel it push back.
33. Then build a semicircle of the same width, press on it the same way, and compare.
34. Hooke hid his answer in a scramble of letters. You can find it again with a piece of string.

## Sources

- R. Hooke, *A Description of Helioscopes, and some other Instruments* (London, 1676; title page dated 1676, some
  modern accounts say 1675): https://distantreader.org/stacks/earlyprint/txt/A44317.txt
- Catenary (history: Hooke 1671 announcement, 1675/76 anagram, solution published 1705 by his executor;
  Galileo's "approximate parabola"; Leibniz, Huygens and Johann Bernoulli 1691; Gregory 1697):
  https://en.wikipedia.org/wiki/Catenary
- BSHM, Scientific Challenges and Encryption of Discoveries in 17th Century Rational Mechanics (anagram letters,
  Latin solution and translation; Hooke 1671; the 1690-91 challenge): https://bshm.ac.uk/node/464
- Newton Excel Bach, Arches, anagrams and plagiarism (Latin text and translation):
  https://newtonexcelbach.com/2010/07/14/arches-anagrams-and-plagiarism/
- Scotland's Oldest Bridges, arches and catenary (Gregory 1697: an arch stands if "within its thickness some
  catenaria is included"): https://scotlandsoldestbridges.co.uk/arches-structure-and-shape.-catenary-bridges.html
- C. Hutton, Mathematical and Philosophical Dictionary (1796), Catenary (Galileo, Jungius, 1691, Gregory 1697):
  https://words.fromoldbooks.org/Hutton-Mathematical-and-Philosophical-Dictionary/c/catenary.html
- University of Michigan, Structures I lecture 8, Catenary arches (Poleni and St Peter's dome, 1748; Gaudí):
  https://structures1.tcaup.umich.edu/lectures/Lec8/314F24_8_CatinaryArches.pdf
- New World Encyclopedia, Robert Hooke (curator of experiments 1662; surveyor after the Great Fire; no authenticated
  portrait survives): https://www.newworldencyclopedia.org/entry/Robert_Hooke
- The Monument, Dr Robert Hooke (Surveyor to the City of London; no known portraits from his lifetime):
  https://www.themonument.org.uk/fr/node/203
- J. E. Gordon, *Structures: Or Why Things Don't Fall Down* (1978), credited for the story; not consulted directly.

## Notes on accuracy

- The 1676 date is the book's title page; some accounts say 1675. Narration says "printed in 1676".
- "The key was published only after his death": Wikipedia says 1705, by his executor (Hooke died 1703).
- The thrust lines are computed for a semicircular arch under its own weight (funicular polygon of the voussoir
  weights, best horizontal thrust), so "thick stays inside, thin escapes" is real for those thicknesses
  (the minimum is about 0.11 of the radius by this simple method; the textbook value is about 0.106). The collapse
  animation is schematic.
- The Poleni line is supported by the Michigan lecture; a magazine account dates the iron hoops fitted to the dome to
  1744, so the narration speaks only of his 1748 check, not the repair dates.
