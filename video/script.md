# Video script: "Kakeya Records" (target 3:40, hard limit 4:00)

Speak at normal speed; don't speed up the audio. The script is about 480 words, roughly 3.5 minutes at a relaxed pace. Open `video/slides.html` in a browser, go full screen, and press → to advance. Record with QuickTime (File → New Screen Recording) or Zoom, with the microphone on.

---

**[Slide 1: title] (0:00–0:20)**
Hi, I'm Shrestha. This is a solo entry. The organisers asked whether two days is enough for AI to make a real discovery. I wanted to test that directly, so I ran an AI research agent, Claude Code, and directed it at one goal: a verifiable record inside the hackathon. The first record took sixty-three minutes on an eight-gigabyte laptop. I'll show you what was found and how you can check it yourself in one minute.

**[Slide 2: the problem] (0:20–0:55)**
This is the Kakeya needle problem, in a discrete form. Take 128 directions, and for each one place a thin triangle that contains a unit segment in that direction. You can slide each triangle up or down, and you want the union to cover as little area as possible. Keich found the classic construction in 1999. Since then, Google DeepMind's AlphaEvolve, GPT-5.4 Pro on the HorizonMath benchmark, and an agent platform called Dualverse have each pushed the best known area lower. Whether any of these is optimal is an open question.

**[Slide 3: the result] (0:55–1:30)**
Working with the agent, we set new best-known values at every size with a published result. At 128 directions the union area is 0.106962440. That's 6.84% smaller than AlphaEvolve, 2.00% smaller than GPT-5.4 Pro, and below the previous best. We also set records at 32 and 64 directions.

**[Slide 4: how] (1:30–2:30)**
Four ideas made this work on a laptop.
First, an exact reformulation. Every vertical slice of the union is 128 intervals of the same length. So the slice length is that length plus the sum of the gaps between neighbouring intervals, each capped at the interval length. That means no geometry library, and we get an exact gradient.
Second, we smooth those caps with a temperature that we anneal down to zero, and run gradient descent.
Third, a lifting lemma: every triangle is exactly the union of two thinner children. That lets us optimise from 8 directions up to 128.
Fourth, an evolutionary search over populations of local optima, run on a compiled kernel.

**[Slides 5–6: what it found, press → after the first sentence] (2:30–3:05)**
The structure is interesting. Keich's construction keeps every slice about the same width. The optimised one pays for a wider slice at the base, and in return bundles of triangles converge at three focal heights, where the cross-section collapses. It's a different shape of solution, not just a polished version of the old one.

**[Slide 7: trust it] (3:05–3:35)**
Don't take our word for it. Every number passes the benchmark's official validator, and a second verifier we wrote computes the exact rational area of the stored configuration, with no floating point anywhere. The repository has both, plus an interactive marimo notebook.

**[Slide 8: close] (3:35–3:45)**
These are upper bounds, so optimality is still open, and the margin over the previous best is small. But a single agent on a laptop beat AlphaEvolve in seven minutes. Thanks for watching.
