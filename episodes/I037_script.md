# I037 The Cipher That Cost a Queen Her Head

Working title kept. Subtitle: *How counting letters broke a secret code.*
Story after S. Singh, *The Code Book* (1999), credited; the book itself was not consulted directly.
Format: plate, about 3.5 minutes, Kokoro `af_heart`. Field: mathematics (with the Idea's try-it).

## Narration

1. Science Stories. The cipher that cost a queen her head.
2. England, 1586. Thomas Phelippes, codebreaker to Elizabeth's spymaster Francis Walsingham, stares at a page of strange symbols.
3. It is a letter for Mary, Queen of Scots. She has been a prisoner in England since 1568.
4. Her letters travel in and out of Chartley, the house where she is held, hidden in beer barrels.
5. She believes they are safe. But the courier, Gilbert Gifford, is a double agent. Walsingham sees everything.
6. And the letters speak of a plot, led by Anthony Babington, to kill Elizabeth and put Mary on the throne.
7. To prove it, Phelippes has to read them. That is his puzzle.
8. Mary's cipher swaps each letter for a symbol, with extra symbols for common words, and nulls that mean nothing.
9. The obvious attack is to try every possible swap. But twenty-six letters can be scrambled in about four hundred million billion billion ways.
10. Check a million every second, and you would still be checking long after the Sun has burned out.
11. The trick that beats it is more than seven hundred years older than Phelippes.
12. In ninth-century Baghdad, the scholar al-Kindi wrote the earliest known description of it: frequency analysis.
13. In any language, some letters turn up far more often than others.
14. In English text, E is about one letter in eight. T and A come next. J, Q, X and Z together make less than one percent.
15. A swap changes how each letter looks. It does not change how often it appears.
16. So here is a short message, about two hundred letters, enciphered with a secret swap.
17. Count every symbol. Then sort the counts.
18. The tallest bar is almost certainly E. The next is probably T.
19. After that, short messages wobble. Every guess must be tested on real words.
20. Put in E and T. One three-symbol word, T, something, E, keeps coming back. It must be THE. Now we have H.
21. Each new letter unlocks more words, like a crossword, until the message reads itself.
22. According to Simon Singh's The Code Book, this is how Phelippes broke Mary's cipher.
23. In July 1586, Mary answered Babington. Her letter agreed to the plot.
24. When Phelippes deciphered it, he drew a small gallows on the outside.
25. Then a postscript was forged in Mary's cipher, asking Babington for the names of the six men who would kill the queen.
26. Babington was arrested in August, and executed in September.
27. Mary was tried at Fotheringhay in October, found guilty, and executed there on the eighth of February 1587.
28. Historians still argue over how far Walsingham's agents steered the plot. But the cipher protected no one.
29. A simple swap hides each letter, but not the pattern of the language.
30. And Mary's ciphers are still being broken. In 2023, George Lasry, Norbert Biermann and Satoshi Tomokiyo deciphered more than fifty of her lost letters, misfiled in a French library.
31. A computer tried key after key, keeping changes that made the text look more like language. The rest they solved by hand.
32. Modern ciphers make every symbol turn up about equally often. Count them, and you learn almost nothing.
33. Try it yourself. Have a friend encipher about two hundred letters with a secret swap.
34. Count the symbols, guess E and T, then hunt for THE, and let the words do the rest.
35. One queen, one cipher, and a codebreaker who counted.

## Decisions

- The person at the centre is Phelippes, the codebreaker, with Mary's letters as his puzzle. Silhouette: the kit's stylised 'beard' cameo (Wikipedia quotes Mary describing him as yellow-bearded); Mary is shown as a crowned seal, not a figure.
- "Codebreaker to Walsingham": BL calls him Walsingham's cryptographer, NSA his chief cryptanalyst.
- Prisoner since 1568: NSA (fled Scotland 1568) and Wikipedia, Execution of Mary (crossed the Solway 16 May 1568).
- Chartley and beer barrels: BL (Chartley Hall; letters hidden in beer barrels), Britannica excerpt (beer barrel), NSA (cork tube in a beer or wine cask). The Burton brewer is left out (rests on one historian per Wikipedia).
- Gifford as double agent and courier: NSA. "Walsingham sees everything": Wikipedia (Walsingham arranged for the letters to be smuggled; they were deciphered and read by him).
- The plot's aim: Singh (assassinate Elizabeth I and put Mary on the throne).
- Cipher description: NSA ("single substitution ... with additional substitutions for repeating words, common syllables, nulls"). Exact symbol counts are not given; the symbols on screen are invented for the demo and labelled.
- 26! = 403,291,461,126,605,635,584,000,000, about 4 × 10^26 ("four hundred million billion billion"). At 10^6 per second that is about 1.3 × 10^13 years; the Sun has roughly 5 billion years left. The 26-letter swap is a simplification of Mary's cipher (labelled).
- al-Kindi: Baghdad, c. 850 (History of Information), "earliest known" description (Singh article: A Manuscript on Deciphering Cryptographic Messages). 1586 − 850 ≈ 736, hence "more than seven hundred years". Narration says "ninth century".
- English letter frequencies: Emory table (E 12.702 %, T 9.056 %, A 8.167 %; J+Q+X+Z = 0.472 %); Singh's article gives E 12.7 % and J, Q, X, Z under 1 % combined. "About one letter in eight" = 12.5 %.
- Demo message is our own 209-letter text, enciphered with a random swap (seed fixed in the episode file). Its real counts: E 42, T 26, R 19, H 17 ... so the third bar is R, not A, which is why the narration warns that ranks wobble. A check on a 27,700-letter English text found E on top in only about 63 % of random 200-letter windows, so "almost certainly" refers to this message's very tall E bar (42 vs 26) rather than a general rule; the try-it says "guess E and T first", then test words.
- "According to Simon Singh's The Code Book": the method is attributed, since BL and NSA say only that Phelippes deciphered the letters; Singh's article says he "used frequencies to crack the plotters' cipher".
- Mary's letter of 17 July 1586 (BL). "Agreed to the plot": NSA (complicity "in her own words"); BL calls it the letter that sealed her fate. Historians' debate is stated in line 28 (NSA: agents provocateurs; "some question remains concerning her guilt").
- Gallows: BL ("Phelippes drew a gallows on the address leaf"), NSA ("on the outside of the copy he sent to Walsingham"); narration says "on the outside", which fits both.
- Postscript: BL (Walsingham had a postscript added asking Babington to name the six); NSA says Phelippes forged it in cipher. Narration uses the passive "a postscript was forged".
- Babington: arrest ordered 3 August, executed 20 September 1586 (BL). Manner of execution not narrated.
- Mary: taken to Fotheringhay 25 Sept, tried in October, convicted 25 October, executed 8 February 1587 at Fotheringhay (Wikipedia, Execution of Mary; NSA gives 8 Feb 1587).
- 2023 letters: Lasry, Biermann, Tomokiyo; 57 letters (Smithsonian; NPR "more than 55"), so narration says "more than fifty"; 1578–1584; found in the Bibliothèque nationale de France catalogued among Italian papers; mostly to Castelnau; Cryptologia, February 2023; hill-climbing computer search recovered about 30 %, rest by hand (Smithsonian). The score curve on screen is a labelled illustration.
- Modern-cipher histogram: real AES-128-CTR output (fixed demo key) of the demo text repeated 300 times, counted by byte value, beside the plaintext's letter counts. Shown as "AES, counted".
- Left out as not confirmed from sources read: the nomenclator's exact number of symbols, where Phelippes worked, Babington's age, the Burton brewer, how many conspirators were executed, al-Kindi's exact dates.

## Sources

- British Library, A. Bryson, "The Gallows Letter" (2022): https://www.bl.uk/stories/blogs/posts/the-gallows-letter
- NSA, Crypto Almanac 50th, "To Catch a Queen": https://www.nsa.gov/Portals/70/documents/news-features/declassified-documents/crypto-almanac-50th/to-catch-a-queen.pdf
- Wikipedia, Thomas Phelippes: https://en.wikipedia.org/wiki/Thomas_Phelippes
- Wikipedia, Execution of Mary, Queen of Scots: https://en.wikipedia.org/wiki/Execution_of_Mary,_Queen_of_Scots
- Britannica, Babington Plot: https://www.britannica.com/topic/Babington-Plot
- S. Singh, "Arab Code Breakers": https://simonsingh.net/media/articles/maths-and-science/arab-code-breakers
- History of Information, al-Kindi's treatise: https://www.historyofinformation.com/detail.php?entryid=3605
- Emory, Letter frequencies in English: https://math.oxford.emory.edu/site/math125/englishLetterFreqs/
- NPR (2023), Mary's cipher letters: https://www.npr.org/2023/02/10/1155701113/mary-queen-of-scots-ciphers-prison-letters
- Smithsonian (2023), lost letters deciphered: https://www.smithsonianmag.com/history/codebreakers-discoverand-decipherlong-lost-letters-by-mary-queen-of-scots-180981613/
- S. Singh, The Code Book (1999), credited for the story; not consulted directly.
