# I032 Archimedes Traps Pi

Working title: Archimedes Traps Pi. Subtitle: *How to pin down a number you can never measure.*
Story after W. Dunham, *Journey Through Genius* (1990), credited; not consulted directly.
Format: plate, about 3 to 3.5 minutes, Kokoro `af_heart`. Field: mathematics.

## Narration

1. Science Stories. Archimedes traps pi.
2. Syracuse, Sicily, in the third century BCE. Archimedes puzzles over a question that sounds almost childish.
3. How far is it around a circle?
4. Every circle goes around a little more than three times its width. That ratio is the number we now call pi.
5. But the edge of a circle is curved, and a ruler is straight. You cannot lay a straight ruler along a curve.
6. The obvious answer is to measure. Wrap a string around a wheel, then stretch it out.
7. You get about three and a bit. But a measurement is only as good as your string.
8. Archimedes wanted something no string could give him. A proof.
9. His idea was this. If you cannot measure the curve, trap it, between shapes made only of straight lines.
10. Draw a hexagon inside the circle. Each of its six sides is exactly as long as the radius.
11. So its perimeter is six radii, which is three diameters. The circle bulges outside it, so pi must be more than three.
12. Now draw a hexagon outside the circle. Its perimeter works out to about three point four six diameters. So pi must be less than that.
13. Pi is caught between three and three point four six. A loose cage.
14. So Archimedes doubled the sides. Twelve sides. Now pi is trapped between about three point one one and three point two two.
15. Twenty-four sides. Forty-eight. Ninety-six.
16. With each doubling, the polygons hug the circle more closely, and the gap between them shrinks to about a quarter.
17. And Archimedes had no decimals. Every step was done in whole numbers and fractions, by hand.
18. Even the square root of three had to be pinned between two fractions. He never said how he found them.
19. At ninety-six sides he stopped. His result: pi is less than three and one seventh, and more than three and ten seventy-firsts.
20. In decimals, between three point one four oh eight and three point one four two nine. Right to two decimal places, and proven.
21. But the real gift was the method. Archimedes showed how to get as close as you like, and to know exactly how close you are.
22. An upper bound and a lower bound, squeezing in on the truth. That idea is still used across mathematics and computing.
23. In 212 BCE, Roman forces captured Syracuse, and Archimedes was killed by a Roman soldier.
24. Plutarch gives three versions. In one, Archimedes was so absorbed in a problem on a diagram that he would not leave it.
25. The famous words, do not disturb my circles, come from later retellings. No one knows what he said.
26. Try it yourself. In a spreadsheet, start with the hexagon. Inside, three. Outside, two root three.
27. To double the sides: new outside is two times inside times outside, over inside plus outside.
28. New inside is the square root of new outside times old inside.
29. Four rows give Archimedes' ninety-six sides. Twenty rows trap pi to ten decimal places.
30. A curve no ruler could measure, two cages of straight lines, and a number trapped over two thousand years ago.

## Decisions

- Archimedes' dates shown as "c. 287 to 212 BCE": MacTutor gives 287 and 212 BC; the birth year rests on a later report, so it carries "c.".
- The symbol pi and the name are not attributed to Archimedes; the narration says "the number we now call pi". On screen the ratio is called "distance around ÷ width".
- The string measurement is an illustration of the obvious approach, not a claim about what Archimedes did. PBS NOVA calls his value the first theoretical rather than measured calculation.
- Order follows Measurement of a Circle, Proposition 3 as reconstructed by B. Rosenberg: he starts from the hexagon, bisects four times to 96 sides, circumscribed polygon first, then inscribed.
- Intermediate values (12, 24, 48 sides) are computed exactly (n·sin(π/n), n·tan(π/n)) in modern decimals and labelled as such; Archimedes' own working used fractions slightly inside these.
- The √3 fractions 265/153 and 1351/780 are shown on screen, not read aloud.
- The 96-gon ratios shown, 6336 / 2017¼ and 14688 / 4673½, are from Rosenberg's reconstruction (14688 = 96 × 153 is implied there, not written).
- "No decimals": PBS NOVA (decimals came hundreds of years later) and Feldman (he used fractions).
- Plutarch's three versions are from the Dryden translation of the Life of Marcellus (Livius). "Do not disturb my circles" is labelled a later form: Wikipedia notes Plutarch does not have it, and the only ancient form is Valerius Maximus's "noli, obsecro, istum disturbare".
- "Gap shrinks to about a quarter": computed, ratios 0.236, 0.247, 0.249, 0.250.
- Left out as not confirmed from sources read: Proposition 1 (circle area as a triangle), whether the surviving text is damaged, Ludolph van Ceulen and later polygon records, the inventor of the symbol pi.
- Mathematics video: the Idea's try-it kept (spreadsheet with the harmonic-mean / geometric-mean doubling rule). Values checked in Python ("two root three" means 2·√3): 96 sides 3.1410319509 / 3.1427145996; 20 doublings (6,291,456 sides) agree with pi to 10 decimals.

## Sources

- MacTutor, Archimedes of Syracuse (dates, father Phidias, killed 212 BC at the capture of Syracuse, 96-sided polygons, bounds 3 10/71 and 3 1/7, Plutarch's three versions): https://mathshistory.st-andrews.ac.uk/Biographies/Archimedes/
- B. Rosenberg, Archimedes and Pi (2003), reconstruction of Measurement of a Circle Prop. 3 (hexagon start, bisections to 96, 265/153 and 1351/780, 4673½ and 2017¼): https://www.cs.miami.edu/home/burt/manuscripts/archimedes/meas_circle.pdf
- J. Feldman, Archimedes' (Approximate) Computation of π, UBC (inscribed and circumscribed perimeters, √3 bounds, fractions not decimals): https://personal.math.ubc.ca/~feldman/m120/archimedesPi.pdf
- PBS NOVA, Approximating Pi (hexagon doubled to 96, 3.1408 to 3.1429, first theoretical rather than measured calculation, no decimals): https://www.pbs.org/wgbh/nova/physics/approximating-pi.html
- Plutarch, Life of Marcellus, on the death of Archimedes (Livius): https://livius.org/sources/content/plutarch/plutarchs-marcellus/the-death-of-archimedes
- Wikipedia, Noli turbare circulos meos! (phrase not in Plutarch; Valerius Maximus's form): https://en.wikipedia.org/wiki/Noli_turbare_circulos_meos!
- W. Dunham, Journey Through Genius (1990), chapter on Archimedes, credited for the story; not consulted directly.
