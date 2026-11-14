# I011 · The Most Important Master's Thesis

Book: Jimmy Soni and Rob Goodman, *A Mind at Play: How Claude Shannon Invented the Information Age*
(New York: Simon & Schuster, 2017). Told in our own words.
Field: Engineering. Scene file: `episodes/I011_shannon_switches.py`, scene `ShannonSwitches`.

## Narration

1. Science Stories. The most important master's thesis.
2. 1937. At M.I.T., a twenty-one-year-old graduate student named Claude Shannon spends his days looking after a machine the size of a room.
3. It is Vannevar Bush's differential analyzer: shafts, gears and spinning discs that solve equations by turning.
4. To run it, there was a complicated control circuit full of relays.
5. A relay is just a switch, flipped by an electromagnet. Current flows, or it does not.
6. Wire a few relays together and it is easy to say what happens. Wire a hundred, and the tangle becomes very hard to reason about.
7. Shannon wanted something better: a way to calculate with switches, the way we calculate with numbers.
8. The answer came from an unlikely place. Back at the University of Michigan, he had taken a philosophy class in logic.
9. There he met the algebra of George Boole, from the eighteen-forties and fifties. An algebra not of numbers, but of statements that are either true or false, combined with three words: and, or, not.
10. Shannon's insight was that a switch is a statement. Closed means true. Open means false.
11. Put two switches in a row. The lamp lights only if A is closed and B is closed. That is and.
12. Put them side by side. The lamp lights if A is closed or B is closed. That is or.
13. And a relay whose contact springs open when its coil is energised gives you not.
14. One small detail. In his thesis Shannon actually counted the other way round, with zero for a closed circuit. It is the same algebra, mirrored. Today we use the version you see here.
15. Now the payoff. A circuit becomes an equation, and equations can be simplified.
16. This circuit uses four contacts: A and B, or A and C. But algebra says that is the same as A, and B or C.
17. Same behaviour, one fewer switch. Shannon's thesis did this on far bigger circuits, sometimes cutting the number of parts dramatically.
18. And it works the other way too. Write down the logic you want, and the algebra hands you the circuit.
19. His thesis designed an electric combination lock, and a circuit that adds numbers in binary.
20. Adding two binary digits needs only logic. The sum digit is one when exactly one input is one. The carry is simply A and B.
21. Years later, Shannon said it just happened that no one else was familiar with both those fields at the same time.
22. Every chip in your phone holds billions of tiny switches, and they are still designed with the algebra Shannon joined to circuits in 1937.
23. Try it yourself. Take a battery pack, an L.E.D. with a resistor, and two switches. Wire them in a row and you have an and gate. Wire them side by side and you have or. Then, with two-way switches, build a lock that lights only for your secret combination. Write its equation first, then test it.

## On-screen notes

- Shannon's age: born 30 April 1916 (IEEE Spectrum); the thesis is signed "August 10, 1937", so he was 21 when it was finished. IEEE Spectrum calls him "the 22-year-old student", probably counting from the 1938 publication. The degree itself is dated 1940 on the title page.
- "A complicated control circuit with relays" paraphrases Shannon's own 1987 description quoted by the Bentley Historical Library. The narration avoids giving a number of relays because no source checked states one.
- "Wire a hundred, and the tangle becomes very hard to reason about" is a general framing of why a calculus helps, not a historical claim about how engineers worked.
- The philosophy class: Bentley Historical Library names it "Philosophy 33: Introduction to Logic"; the George Boole 200 site (University College Cork) also says a philosophy class introduced him to Boolean algebra.
- Boole's logic: *The Mathematical Analysis of Logic* (1847) and *The Laws of Thought* (1854), hence "the eighteen-forties and fifties".
- Convention: the thesis uses "hindrance", 0 for a closed circuit and 1 for an open one, with + for series and the product for parallel. The video shows the modern convention (closed = 1, series = AND, parallel = OR) and says so in the narration and on screen.
- The thesis's illustrative examples include "An Electric Combination Lock" and "An Adder to the Base Two" (table of contents). The video's adder is a modern half-adder drawn in gate form for clarity, not Shannon's relay circuit.
- The simplification shown (AB + AC = A(B + C)) is a textbook example chosen for the video, not one of the thesis's figures. "Sometimes cutting the number of parts dramatically" rests on the thesis's own remark "Note the large reduction in the number of elements".
- The quotation in line 21 is reported speech from John Horgan's 1992 IEEE Spectrum interview ("It just happened that no one else was familiar with both those fields at the same time").
- Not used, because not confirmed tonight: Howard Gardner's often-quoted praise of the thesis; the Alfred Noble Prize; a summer at Bell Labs in 1937; the relay count of the analyzer; his birthplace (Petoskey versus Gaylord).
- "Billions of switches" in a phone chip: modern phone processors contain on the order of 10 to 20 billion transistors; the narration says only "billions".
- Silhouettes are stylised, not likenesses. The differential analyzer drawing is schematic.

## Sources

- C. E. Shannon, *A Symbolic Analysis of Relay and Switching Circuits*, MIT thesis (signed 10 August 1937; degree 1940): https://fab.cba.mit.edu/classes/862.16/notes/computation/Shannon-1937.pdf (MIT DSpace record: https://dspace.mit.edu/handle/1721.1/11173)
- Bentley Historical Library, University of Michigan, "The Elegant Philosophy of Ones and Zeros" (2022): https://bentley.umich.edu/news-events/magazine/the-elegant-philosophy-of-ones-and-zeros
- J. Horgan, "Claude Shannon: Tinkerer, Prankster, and Father of Information Theory", IEEE Spectrum (1992, republished 2016): https://spectrum.ieee.org/tech-history/cyberspace/claude-shannon-tinkerer-prankster-and-father-of-information-theory
- George Boole 200, University College Cork, "Boole and engineering": https://georgeboole.com/boole/legacy/engineering
- C. Fedde, "How Claude Shannon's master thesis changed our world", Christian Science Monitor (2016): https://www.csmonitor.com/Technology/2016/0430/How-Claude-Shannon-s-master-thesis-changed-our-world
- Book credited for the story (not consulted directly in this run): J. Soni and R. Goodman, *A Mind at Play* (Simon & Schuster, 2017).
