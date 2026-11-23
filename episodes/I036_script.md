# I036 Eight Pages from Riemann

Working title: Eight Pages from Riemann. Subtitle: *The hidden music of the prime numbers.*
Story after J. Derbyshire, *Prime Obsession* (2003), credited; front matter, chapters 2, 4, 14 and the epilogue read
in the National Academies Press online edition.
Format: plate, about 3.5 minutes, Kokoro `af_heart`. Field: mathematics. Narration 546 words.

## Narration

1. Science Stories. Eight pages from Riemann.
2. In August 1859, Bernhard Riemann, a mathematician at Göttingen, was made a corresponding member of the Berlin Academy.
3. The custom was to thank the Academy with an original paper. Riemann sent one about prime numbers, the only paper on number theory he ever published.
4. Primes are the numbers with no divisors except one and themselves. Two, three, five, seven, eleven, thirteen.
5. They never run out, but they seem to appear at random. So the question is: how many primes are there below a given number?
6. Count them, and you get a staircase. It climbs one step at every prime, at uneven intervals.
7. The obvious answer had come from Gauss, Riemann's own doctoral supervisor. As a boy of about fifteen, Gauss had counted primes in blocks of a thousand.
8. He noticed that, on average, the primes thin out like one over the logarithm. That gives a smooth curve.
9. The curve follows the staircase well. But a smooth curve can never make sharp steps. It always misses the details.
10. Riemann wanted an exact formula. Not an estimate, but the staircase itself.
11. His key was a function now called the zeta function. Add one, plus one over two to the power s, plus one over three to the power s, and so on forever.
12. Euler had shown that this sum over all whole numbers equals a product over all the primes. So the zeta function secretly knows where the primes are.
13. Riemann's bold step was to let s be a complex number, and to ask where zeta equals zero.
14. Those zeros sit at heights fourteen point one, twenty-one point oh, twenty-five point oh, and on, without end.
15. And here is the magic. Each zero adds a wave to the smooth curve.
16. With one wave, the curve starts to wobble towards the steps. With ten, the steps begin to show. With a hundred, the curve hugs the staircase.
17. The primes, which look random, are a sum of waves, and the zeros of zeta set their pitch.
18. The zeros all seem to sit on one straight line, where the real part is exactly one half.
19. Riemann wrote that it is very probable that all of them do, and that he had set the proof aside after some fleeting, futile attempts.
20. That sentence is the Riemann hypothesis. It is still unproven.
21. If it is true, the waves are as small as they can be, and the primes are as regular as they can possibly be.
22. Computers have checked the first ten trillion zeros. All of them lie on the line.
23. But checking is not proving. The Clay Mathematics Institute offers a million dollars for a proof.
24. Riemann did not live to see any of this. He fell ill with tuberculosis, and died in Italy in 1866, aged thirty-nine.
25. Decades later, Carl Ludwig Siegel studied Riemann's rough notes, and found that he had calculated zeros himself, with a formula he never published.
26. Try it yourself. Write a short program that counts the primes below ten, a hundred, a thousand, a million.
27. Divide each count by x over the natural log of x. Watch the ratio settle towards one, very slowly.
28. Eight pages, one guess, and a question still open after more than a hundred and sixty years.

## Decisions

- "Eight pages": the translators of Siegel's 1932 paper (Barkan and Sklar) call it an "eight-page paper"; Wikipedia
  counts nine. On screen: "about eight printed pages (some count nine)". The title keeps the Idea's wording.
- August 1859 and the custom of thanking the Academy with a paper: Derbyshire ch. 2 ("On August 11 ... 1859 ...
  appointed a corresponding member of the Berlin Academy"; "It was the custom to acknowledge such appointments by
  submitting an original paper"). MacTutor agrees (elected a few days after the Göttingen chair, 30 July 1859).
  The paper's own first sentence thanks the Academy for admitting him "as one of its correspondents" (Wilkins).
- Published in the Monatsberichte, Berlin, November 1859 (Wilkins translation header; Wikipedia).
- "The only paper on number theory he ever published": Wikipedia. Narration says number theory, not "primes".
- Gauss: Riemann's doctoral supervisor (MacTutor, thesis 1851). The boyhood counts: Derbyshire ch. 4 quotes Gauss's
  1849 letter to Encke (work begun "in 1792 or 1793"; tallied primes in blocks of 1,000; "when he was fifteen years
  old"). Narration says "a boy of about fifteen". The block counts shown (168, 135, 127, 120, 119) are computed.
- Gauss's curve is drawn as li(x); density "about 1 / ln x" is the letter's wording ("inversely proportional with the
  logarithm").
- Euler product: Wikipedia (Riemann hypothesis) says Euler proved the series equals the Euler product. Year left out
  (only "the 1730s" confirmed for the series).
- The waves: Riemann's explicit formula in the modern form pi(x) ~ R(x) - sum over zeros of R(x^rho) - 1/ln x +
  arctan(pi/ln x)/pi, with R the Möbius sum of li(x^(1/n)) and li(x^rho) = Ei(rho ln x). Computed with mpmath for the
  first 100 zeros, labelled "in a modern form" on screen. Checked at render time: between x = 6 and 60 the 100-zero
  curve is within 0.32 of the staircase at every half-integer (0.86 with no zeros). Below x = 6 the sum converges
  slowly, so the curves are drawn from x = 3.
- Zero heights 14.13, 21.02, 25.01, 30.42, 32.94, 37.59 from mpmath zetazero, matching Wikipedia.
- "The zeros all seem to sit on one line": not a claim about which zeros Riemann knew.
- Quotation on screen is Wilkins's translation, verbatim: "it is very probable that all roots are real. Certainly one
  would wish for a stricter proof here; I have meanwhile temporarily put aside the search for this after some
  fleeting futile attempts". Noted that his "roots" (of xi(t)) being real means zeros on the line.
- "As regular as they can be": von Koch (1901) showed the hypothesis implies the "best possible" error bound
  (Wikipedia, Riemann hypothesis). Shown as |pi(x) - li(x)| roughly below sqrt(x) ln x, with "≲".
- "Ten trillion zeros": Clay Mathematics Institute ("checked for the first 10,000,000,000,000 solutions").
  US$1 million prize: Wikipedia (Millennium Prize Problems).
- Death: Selasca, Italy, 20 July 1866, aged 39; illness turned to tuberculosis (MacTutor; Derbyshire epilogue gives
  the date).
- Siegel, 1932: found in Riemann's rough notes the formula now called the Riemann-Siegel formula, and that Riemann
  "also calculated some real zeros" with it (Siegel's introduction, tr. Barkan and Sklar; Wikipedia, Riemann-Siegel
  formula). Narration: "calculated zeros himself, with a formula he never published".
- Left out as not confirmed from sources read: the story that his housekeeper burned papers after his death; Riemann's
  personality; the exact count of zeros he computed.
- Mathematics video: the Idea's try-it kept and made concrete (count primes, compare with x / ln x). Values checked:
  4, 25, 168, 78,498; x/ln x 4.3, 21.7, 144.8, 72,382.4; ratios 0.921, 1.151, 1.161, 1.084. The prime number
  theorem (1896) is named on screen as the reason the ratio tends to 1.
- Silhouettes: kit 'beard' cameo for Riemann, 'plain' for Gauss, both stylised.

## Sources

- J. Derbyshire, Prime Obsession (Joseph Henry Press, 2003), online at the National Academies Press: front matter
  https://www.nationalacademies.org/read/10532/chapter/1 ; ch. 2 https://www.nationalacademies.org/read/10532/chapter/4 ;
  ch. 4 https://www.nationalacademies.org/read/10532/chapter/6 ; epilogue https://www.nationalacademies.org/read/10532/chapter/26
- B. Riemann, On the Number of Primes Less Than a Given Magnitude (1859), tr. D. R. Wilkins:
  https://www.claymath.org/wp-content/uploads/2023/04/Wilkins-translation.pdf
- MacTutor, Georg Friedrich Bernhard Riemann: https://mathshistory.st-andrews.ac.uk/Biographies/Riemann/
- Wikipedia, On the Number of Primes Less Than a Given Magnitude:
  https://en.wikipedia.org/wiki/On_the_Number_of_Primes_Less_Than_a_Given_Magnitude
- C. L. Siegel, Über Riemanns Nachlaß zur analytischen Zahlentheorie (1932), tr. E. Barkan and D. Sklar:
  https://arxiv.org/abs/1810.05198
- Wikipedia, Riemann-Siegel formula: https://en.wikipedia.org/wiki/Riemann%E2%80%93Siegel_formula
- Clay Mathematics Institute, The Riemann Hypothesis: https://www.claymath.org/millennium/riemann-hypothesis/
- Wikipedia, Riemann hypothesis: https://en.wikipedia.org/wiki/Riemann_hypothesis
