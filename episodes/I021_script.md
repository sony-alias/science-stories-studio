# I021 Why Cracks Grow: Griffith's Glass

Story after J. E. Gordon, *Structures: Or Why Things Don't Fall Down* (1978), credited for the story; the book was
not consulted directly for this draft. Facts checked against the sources listed at the end.

Scene file: `episodes/I021_griffith_cracks.py` (scene `GriffithCracks`).

## Narration

1. Science Stories. Why cracks grow.
2. Farnborough, England, around 1920. A young engineer named Alan Arnold Griffith is breaking glass on purpose.
3. He works at the Royal Aircraft Establishment, where engineers need to know exactly how strong their materials are.
4. Glass is a perfect test. It does not bend out of shape, or flow, before it breaks. It simply snaps.
5. And glass holds a puzzle. Work out the force needed to pull its atoms apart, and you expect a strength of roughly ten thousand megapascals.
6. Pull on an ordinary piece of glass, and it breaks at around a hundred. A hundred times weaker than theory, or worse.
7. The obvious answer is that the theory is wrong. Griffith suspected the glass.
8. He drew glass into fibres, thinner and thinner. The thinner the fibre, the stronger it was, creeping up towards the theoretical strength.
9. Why should size matter? Griffith's answer: real glass is full of tiny cracks. A thin fibre has less room for a bad one.
10. A few years earlier, the engineer Charles Inglis had worked out what a hole does to the stress in a plate.
11. Picture the force passing through a stretched plate as lines. A hole makes them crowd around its edges.
12. For an elliptical hole, the stress at its tip is multiplied by one, plus twice its length over its width.
13. Now make the hole a crack, long and razor thin, and that factor becomes enormous. At the tip, the stress can reach the theoretical strength, even under a modest load.
14. But that raises a new puzzle. By this rule, every sharp crack should run at almost any load. They don't. So what decides?
15. Griffith's leap was to stop thinking about force, and start thinking about energy.
16. A stretched plate stores energy, like a spring. A crack lets the material around it relax, and releases some of that energy.
17. The energy released grows with the square of the crack's length.
18. But a crack has a cost. It makes two new surfaces, and breaking bonds takes energy. That cost grows only in step with the length.
19. Add them up. For a short crack the cost wins, and the crack stays put. Past a critical length, the release wins, and the crack runs on its own.
20. Out of this balance comes Griffith's rule: the breaking stress falls with the square root of the crack's length.
21. He tested it. He made cracks of known length in glass bulbs and tubes, and broke them. Stress times the square root of crack length came out nearly constant.
22. The paper appeared in 1921. At first it was seen as a rule for brittle things like glass. Decades later, others extended it to metals, and fracture mechanics was born.
23. Today, aircraft are designed on the assumption that small cracks are already there. Engineers work out how long a crack can safely grow, and inspect before it gets there.
24. Griffith himself went on to design jet engines at Rolls-Royce. But his glass taught a deeper lesson: strength depends not only on what a material is made of, but on its flaws.
25. Try it yourself. Take a strip of paper and pull it from both ends. It is surprisingly hard to break.
26. Now snip a small notch in one edge, and pull again. It tears easily, and the tear starts at the notch.
27. Next, find a crack in an old plastic lid. With an adult's help, drill a small hole right at the crack's tip.
28. The round hole blunts the sharp tip, so the stress no longer piles up there, and the crack stops growing. Engineers call it a stop hole.
   On screen during line 28: "safety glasses on · clamp the plastic · an adult runs the drill".
29. A crack is a lever on a material's atoms. Griffith taught engineers to count the energy, and respect the flaw.

## Notes on accuracy

- Griffith born 13 June 1893, died 13 October 1963 (Wikipedia; Grace's Guide). Joined the Royal Aircraft Factory as a
  trainee in 1915, its Physics and Instrument Department in 1916, soon renamed the Royal Aircraft Establishment
  (Wikipedia; Grace's Guide).
- Paper: "The Phenomena of Rupture and Flow in Solids", Phil. Trans. R. Soc. A 221, 163–198, dated 1921 (Wikipedia
  reference, Britannica, Greatpapers, Royal Society blog); some authors date it 1920 (iMechanica; Grace's Guide text).
  Narration therefore says "around 1920" for the experiments and "appeared in 1921" for the paper.
- Theoretical strength of glass about 10,000 MPa vs bulk glass about 100 MPa (Wikipedia, Fracture mechanics; modern
  round figures, shown as such on screen). Grace's Guide and Wikipedia's biography say materials could fail at
  "1,000 times less" than the predicted value, so the narration says "a hundred times weaker than theory, or worse".
- Fibres: strength rises as diameter falls, tending towards the theoretical strength (Grace's Guide; Wikipedia,
  Fracture mechanics; Kendall et al. via arXiv 2411.10672 fit Griffith's fibre data). The fibre curve on screen is
  labelled schematic; Griffith's own fibre numbers were not read tonight and are not shown.
- Inglis: elliptical-hole solution (Sethna, Cornell, gives 1913; Britannica gives 1914), so narration says "a few
  years earlier". sigma_tip = sigma(1 + 2a/b) is the standard Inglis result. Lines of force are drawn as an
  illustration (potential-flow analogy), labelled so.
- Energy balance: released strain energy vs surface energy of two new surfaces (Royal Society blog; Britannica;
  Wikipedia: released energy grows with the square of crack length). Formula shown in its modern plane-stress form
  sigma_f = sqrt(2 E gamma / (pi a)) for a crack of length 2a, labelled "modern form".
- Bulbs and tubes with cracks of known length (arXiv 2411.10672); stress times root crack length nearly constant
  (Wikipedia, Fracture mechanics). Points on screen are an illustration, not Griffith's data.
- At first regarded as important only for very brittle solids such as glass; later extended (Britannica: Irwin;
  Wikipedia: Irwin, Rivlin and Thomas in the 1950s).
- Rolls-Royce from 1939; designed the AJ.65 (Avon) (Wikipedia; Grace's Guide). 1926 turbine paper (Wikipedia).
- "Aircraft are designed on the assumption that small cracks are already there" is the general damage-tolerance
  approach, stated as a general claim.
- Griffith's cameo is a stylised silhouette, not a likeness.

## Sources

- https://royalsociety.org/blog/2015/04/phenomena-of-rupture-and-flow-in-solids
- https://en.wikipedia.org/wiki/Alan_Arnold_Griffith
- https://gracesguide.co.uk/Alan_Arnold_Griffith
- https://en.wikipedia.org/wiki/Fracture_mechanics
- https://www.britannica.com/science/mechanics-of-solids/Stress-concentrations-and-fracture
- https://sethna.lassp.cornell.edu/SimScience/cracks/advanced/history1.html
- https://greatpapers.substack.com/p/the-flaws-the-limit
- https://arxiv.org/html/2411.10672 (Section 2 and Fig. 2, on Griffith's bulbs, tubes and fibres)
- https://imechanica.org/node/7470 (on the 1920/1921 dating)
- A. A. Griffith, "The Phenomena of Rupture and Flow in Solids", Phil. Trans. R. Soc. A 221 (1921) 163–198,
  doi:10.1098/rsta.1921.0006 (cited; full text could not be opened from this run)
- J. E. Gordon, *Structures: Or Why Things Don't Fall Down* (1978), credited for the story; not consulted directly
