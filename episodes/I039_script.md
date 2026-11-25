# I039 Secret Keys in Public

Working title kept. Subtitle: *How two strangers can agree a secret while everyone listens.*
Story after S. Singh, *The Code Book* (1999), credited; the book itself was not consulted directly.
Format: plate, 3:44, Kokoro `af_heart`. Field: mathematics (with the Idea's try-it).

## Narration

1. Science Stories. Secret keys in public.
2. Stanford, autumn 1974. Whitfield Diffie, an independent researcher fascinated by codes, visits a professor, Martin Hellman.
3. A half-hour meeting runs all afternoon, and into dinner.
4. Diffie had spent two years travelling to learn all he could about codes.
5. One problem gripped him. Every cipher needs a key, and both sides must share it before they can talk in secret.
6. That meant meeting in person, or trusting a courier with a locked briefcase.
7. On a network, a thousand users would need almost half a million keys.
8. So, the puzzle: can two strangers agree on a secret when every word they send is overheard?
9. Picture it with paint. Alice and Bob agree, in public, on a starting colour.
10. Each stirs in a secret colour and sends the mixture across.
11. Each then adds their own secret to what arrived. Both end with the same shade.
12. Eve sees both mixtures. But mixing is easy, and unmixing is not.
13. Diffie and Hellman needed a mathematical paint. They found it on a clock.
14. Take a clock with twenty-three positions. Start at one and keep multiplying by five, wrapping around past twenty-three.
15. The answers jump around with no obvious pattern. Forward is easy.
16. Backward is hard: told only where you landed, you must find how many steps it took.
17. Now the exchange. In public: clock twenty-three, number five.
18. Alice's secret is six. Five to the sixth, on the clock, is eight. She sends eight.
19. Bob's secret is fifteen. Five to the fifteenth is nineteen. He sends nineteen.
20. Alice raises nineteen to her six. Bob raises eight to his fifteen. Both get two: their shared key.
21. Eve heard five, twenty-three, eight and nineteen. She must run the clock backwards.
22. On this small clock she can try every step. With primes hundreds of digits long, even the best known methods would take ordinary computers far too long.
23. In November 1976 they published it. The paper begins: "We stand today on the brink of a revolution in cryptography."
24. It credits Ralph Merkle, who attacked the problem independently. Hellman later said Merkle's name belongs on it too.
25. In 1997 came a twist. Britain's codebreaking agency, GCHQ, revealed its own people had got there first, in secret.
26. In 1970, James Ellis showed encryption without a shared secret should be possible.
27. In 1973, Clifford Cocks found a working method, close to what became RSA.
28. In 1974, Malcolm Williamson found a key exchange much like Diffie and Hellman's.
29. Ellis died in November 1997, about a month before it was made public.
30. Found twice, but only the open version could be used by everyone.
31. Today, secure web connections agree a fresh key with a descendant of this exchange.
32. In 2016, Diffie and Hellman received the Turing Award.
33. Try it yourself. With a friend, agree out loud on clock twenty-three and the number five, and each pick a secret from one to twenty-two.
34. Raise five to your secret, one step at a time, and swap answers. Then raise what you receive to your secret.
35. If you match, you share a secret you never said.
36. Two strangers, a public line, and a secret that never travelled.

## Decisions

- Person and puzzle: Whitfield Diffie, with the key distribution problem; Hellman as partner. Silhouettes are the kit's stylised cameos (Diffie "beard", Hellman plain), labelled as not likenesses.
- "Autumn 1974 at Stanford", "half-hour meeting ... all afternoon, followed by dinner": ACM Turing Award biography of Hellman (J. Yost). Diffie visited Hellman (ACM Diffie and Hellman bios). Diffie had left Stanford's AI lab to study cryptography independently (Wikipedia: May 1973; ACM: after reading Kahn) and held no university post at the time; narration and screen say "independent researcher".
- "For two years ... travelled": ACM Diffie bio ("frequent travels in 1973 and 1974 to meet with other scientists"); Wikipedia quotes him on "digging up rare manuscripts in libraries, driving around, visiting friends at universities".
- Courier with a locked briefcase: ACM Hellman bio (key carried in "a locked hand-cuffed briefcase").
- 1,000 users need 1000 × 999 / 2 = 499,500 keys for every pair to have its own (computed and asserted in the episode file). This is a modern illustration, labelled.
- Paint mixing is a teaching picture, not something Diffie or Hellman used; labelled as an analogy. Alice, Bob and Eve are later conventions (labelled as names used today).
- Clock arithmetic: 5 is a primitive root mod 23; powers 5^1..5^22 mod 23 = 5, 2, 10, 4, 20, 8, 17, 16, 11, 9, 22, 18, 21, 13, 19, 3, 15, 6, 7, 12, 14, 1 (all computed and asserted). Exchange: 5^6 = 8, 5^15 = 19, 19^6 = 8^15 = 2 (mod 23). The paper's system: Y_i = α^X_i mod q, K_ij = α^(X_i X_j) mod q, security resting on "the apparent difficulty of computing logarithms" mod q (Diffie and Hellman 1976, Section III).
- "Hundreds of digits": a 2048-bit prime has 617 digits (computed). NIST SP 800-57 Part 1 rates 2048-bit finite-field Diffie-Hellman at about 112 bits of security, i.e. roughly 2^112 work with the best known methods; on screen as "about 2^112 steps (NIST estimate)". Narration says "ordinary computers" because large quantum computers would change this; not discussed further.
- Paper: "New Directions in Cryptography", IEEE Transactions on Information Theory, vol. IT-22, no. 6, November 1976, p. 644 (as printed). Opening sentence quoted verbatim from the paper and the ACM bios.
- Merkle: the paper says "Merkle has independently studied the problem of distributing keys over an insecure channel" (Section III). ACM Hellman bio: Hellman later argued the name should include Merkle's. Merkle is called "a young computer scientist" (ACM: Hellman encouraged him to enrol at Stanford in 1976; PhD 1979); where he studied in 1974 is not stated in the sources read, so it is left out.
- GCHQ: Ellis's report "The Possibility of Secure Non-Secret Digital Encryption", January 1970 (Wikipedia, NSA "as early as 1970"); Cocks 1973 (note dated 20 Nov 1973; Wikipedia "technically aligned with ... elements of the RSA algorithm"; Schneier "essentially RSA"), hence "close to what became known as RSA"; Williamson 1974 (NSA, Schneier). Public talk by Cocks on 18 December 1997 (Wikipedia: Cocks and Ellis; GCHQ "a month before the public announcement"); Ellis died 25 November 1997 (GCHQ, Wikipedia). Schneier gives 1 December 1997 for a released document, so the narration says "about a month" and "in 1997" rather than a day.
- "Only the open one could be used by everyone": GCHQ page (at first "only made available for official governmental communications"; "PKC was thought of independently and developed commercially"); Wikipedia Cocks ("no impact on numerous commercial initiatives").
- Secure connections today: TLS 1.3 (RFC 8446) agrees keys with ephemeral Diffie-Hellman over finite fields or elliptic curves ((EC)DHE), or a pre-shared key; hence "a descendant of this exchange".
- Turing Award: the 2015 ACM A.M. Turing Award, announced 1 March 2016 (ACM press release), US$1 million. Narration says "In 2016 ... received", which is when it was announced and presented (11 June 2016 banquet).
- The 300 digits on screen are the start of 2^2047 + 11, a 2048-bit number shown for scale and labelled "not itself a prime".
- Narration trimmed from a 692-word first draft (4:41) to 525 words (3:44) to fit Settings → Format (2 to 4 minutes).
- Pronunciation: "close to what became RSA" checked as /kloʊs/; the kit now also fixes "has to read them" (I037 feedback) and adds Diffie-Hellman, Merkle's and GCHQ.
- Settings lists "Script approved" before rendering, but no idea had that status and NIGHTLY.md and the run prompt ask for one draft video from the Queued list, so this draft was rendered from a Queued idea and is left for review.
- Left out as unconfirmed or disputed: when and where Diffie first had the public-key idea, who of the two thought of the exchange first, the "half an hour" story about Cocks, any claim that NSA had it earlier (only an unverified claim reported by ACM and Schneier).

## Sources

- W. Diffie and M. Hellman, "New Directions in Cryptography", IEEE Trans. Inf. Theory IT-22(6), Nov 1976: https://ee.stanford.edu/~hellman/publications/24.pdf
- ACM A.M. Turing Award, Whitfield Diffie (J. Yost): https://amturing.acm.org/award_recipient/diffie_8371646
- ACM A.M. Turing Award, Martin Hellman (J. Yost): https://amturing.acm.org/award_recipient/hellman_4055781
- ACM press release, 1 March 2016: https://www.acm.org/media-center/2016/march/turing-award-2015
- Wikipedia, Whitfield Diffie: https://en.wikipedia.org/wiki/Whitfield_Diffie
- GCHQ, James Ellis: https://www.gchq.gov.uk/person/james-ellis
- NSA, Clifford Cocks, James Ellis and Malcolm Williamson: https://www.nsa.gov/Press-Room/Digital-Media-Center/Biographies/Biography-View-Page/Article/3006218/clifford-cocks-james-ellis-and-malcolm-williamson
- Wikipedia, James H. Ellis: https://en.wikipedia.org/wiki/James_H._Ellis
- Wikipedia, Clifford Cocks: https://en.wikipedia.org/wiki/Clifford_Cocks
- B. Schneier, "The Secret Story of Non-Secret Encryption" (1998): https://www.schneier.com/essays/archives/1998/04/the_secret_story_of
- NIST SP 800-57 Part 1 Rev. 5 (security strengths): https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- RFC 8446, TLS 1.3: https://www.rfc-editor.org/rfc/rfc8446
- S. Singh, The Code Book (1999), credited for the story; not consulted directly.
