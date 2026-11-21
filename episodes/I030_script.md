# I030 Seven Years in Secret

Working title in Ideas: *Seven Years in the Attic*. Used title: **Seven Years in Secret**. Subtitle: *Andrew Wiles and the bridge to Fermat.*
Story after S. Singh, *Fermat's Enigma* (1997), credited; not consulted directly.
Format: plate, about 4 minutes, Kokoro `af_heart`. Field: mathematics.

## Narration

1. Science Stories. Seven years in secret.
2. Cambridge, England, 1963. A ten-year-old boy is browsing the maths shelf of his local library.
3. His name is Andrew Wiles, and he has found a book about a single problem.
4. Take whole numbers x, y and z. With squares there are plenty of answers. Three squared plus four squared is five squared.
5. But with cubes, or any higher power, no one had ever found a single answer.
6. Around 1637, Pierre de Fermat wrote in the margin of an ancient book, the Arithmetica, that none exist.
7. And he added: I have discovered a truly remarkable proof, which this margin is too small to contain.
8. Historians now doubt he really had one. For more than three centuries, no one could find a proof.
9. Wiles later said: I knew from that moment that I would never let it go.
10. One summer evening in 1986, at a friend's house, Wiles, now a mathematician, heard some news.
11. Ken Ribet had proved that Fermat's problem was tied to another puzzle, the Taniyama–Shimura conjecture. Wiles said he was electrified.
12. Suppose Fermat was wrong, and some numbers a, b and c did work.
13. Gerhard Frey, building on earlier work, showed how to turn them into an elliptic curve with very strange properties.
14. Ribet proved that such a curve could not be what mathematicians call modular.
15. But Taniyama and Shimura had guessed, in the 1950s and 60s, that every elliptic curve is modular.
16. So prove their guess, at least for curves like Frey's, and the numbers a, b and c cannot exist.
17. No one knew where to begin. Wiles set almost everything else aside, and told almost no one but his wife.
18. It took him seven years.
19. He compared it to a dark mansion: months stumbling in one room, until you find the light switch.
20. So what does modular mean? Take this elliptic curve: y squared plus y equals x cubed minus x squared.
21. Now count on a clock. Modulo five there are only five numbers, so test every pair.
22. Four pairs work. Five minus four is one.
23. Modulo seven, nine pairs work. Seven minus nine is minus two.
24. Now a series built from a product with deep symmetry: a modular form.
25. Multiply it out, and read off the numbers.
26. In front of q to the fifth: one. In front of q to the seventh: minus two.
27. The same numbers. Prime after prime, they keep matching.
28. That is what modular means: the curve's counts are secretly the coefficients of a modular form. Taniyama and Shimura guessed every elliptic curve has such a twin.
29. In June 1993, back in Cambridge, Wiles gave three lectures without saying where they were going.
30. At the end of the last one, on the 23rd of June, he wrote Fermat's Last Theorem on the board. The room broke into applause.
31. But later that year, as the proof was checked, a gap turned up in one crucial step.
32. Wiles worked for another year to repair it, helped by Richard Taylor.
33. On the 19th of September 1994, close to giving up, he took one last look, and saw how to make it work.
34. The proof appeared in 1995, in two papers that filled an issue of the Annals of Mathematics.
35. By 2001, others had carried the bridge across to every elliptic curve.
36. Try it yourself. Write a short program that counts the pairs that work, modulo each prime.
37. Subtract each count from its prime, compare with the series, then try bigger primes.
38. A problem a ten-year-old could understand, and a promise kept three decades later.

## Decisions

- Ideas row calls it *Seven Years in the Attic*; none of the sources read tonight mention an attic (NOVA has Wiles say only "my study"), so the title and narration say "in secret".
- One core idea: what "modular" means, shown with an exact example: the curve y^2 + y = x^3 - x^2 (LMFDB 11.a3, conductor 11) and the modular form q * prod (1-q^n)^2 (1-q^{11n})^2 (LMFDB 11.2.a.a). Point counts were computed in the episode file and checked against the q-expansion for all primes up to 53 (they agree, including p = 11).
- "Counts" are affine solution pairs (x, y) mod p; then a_p = p - count. (The full count with the point at infinity is p + 1 - a_p.)
- Frey curve shown in its usual form y^2 = x(x - a^p)(x + b^p). Hellegouarch's earlier work is acknowledged as "building on earlier work".
- Narration trimmed from a 4:30 first cut (dropped the 1670 publication line, now shown only as a timeline tick; dropped a general claim that the bridge 'carries much of modern number theory').
- Pronunciations added to the kit: Fermat, Arithmetica, Taniyama, Shimura, Gerhard Frey, 'a, b and c'. Ribet left to the voice's default (his own pronunciation not confirmed).
- The 1993 gap: told without naming the referee on screen (Wikipedia: Katz's questions as referee led Wiles to it; IMU: "a referee").

## Sources

- MacTutor, Andrew John Wiles: https://mathshistory.st-andrews.ac.uk/Biographies/Wiles/
- IMU / Abel Prize 2016 biography: https://www.mathunion.org/fileadmin/IMU/Prizes/Abel/2016/Abelprize_2016_Wiles_bio.pdf
- Britannica, Andrew Wiles: https://www.britannica.com/biography/Andrew-Wiles
- NOVA interview, "Andrew Wiles on Solving Fermat" (2000): https://www.pbs.org/wgbh/nova/article/andrew-wiles-fermat/
- Wikipedia, Wiles's proof of Fermat's Last Theorem: https://en.wikipedia.org/wiki/Wiles%27s_proof_of_Fermat%27s_Last_Theorem
- Wikipedia, Frey curve: https://en.wikipedia.org/wiki/Frey_curve ; Ribet's theorem: https://en.wikipedia.org/wiki/Ribet%27s_theorem
- MacTutor, Pierre de Fermat: https://mathshistory.st-andrews.ac.uk/Biographies/Fermat
- History of Information, "Did Fermat Prove his Last Theorem?": https://www.historyofinformation.com/detail.php?id=3074
- LMFDB, elliptic curve 11.a3 and modular form 11.2.a.a: https://www.lmfdb.org/EllipticCurve/Q/11/a/3
- A. Wiles, Modular elliptic curves and Fermat's Last Theorem, Ann. of Math. 141 (1995) 443-551; R. Taylor and A. Wiles, Ring-theoretic properties of certain Hecke algebras, ibid. 553-572 (cited via Wikipedia and Britannica; not opened).
- S. Singh, *Fermat's Enigma* (1997), credited for the story; not consulted directly.
