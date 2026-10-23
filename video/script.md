# Video script: Kakeya Records

**Target:** about 3:45. **Hard limit:** 4:00. Speak at your normal pace and don't speed up the audio.

## Before you hit record
1. Open the slides in your browser and go full screen (press F). Use → or Space to go forward and ← to go back.
2. Open a second browser tab at **shrestha-droid.github.io/kakeya-records**.
3. Open Terminal and paste this command, but **don't press Enter yet**:
   ```
   cd ~/kakeya-records && git pull -q && python3 src/verify_official.py results/n128.json
   ```
4. Start recording: Cmd+Shift+5 → Record Entire Screen → Options → Microphone: MacBook mic.

---

### Slide 1: title (0:00–0:20)
Hi, I'm Shrestha, and this is a solo entry. The organisers asked whether two days is enough for AI to make a real discovery. I wanted to test that directly. So I ran an AI research agent, Claude Code, and directed it at one goal: a verifiable record inside the hackathon. The first record took sixty-three minutes, on an eight-gigabyte laptop.

### Slide 2: the problem (0:20–0:55)
This is the Kakeya needle problem, in a discrete form. Take 128 directions. For each one, place a thin triangle that contains a line segment pointing that way. You can slide each triangle up or down, and the goal is to make the union cover as little area as possible.
Keich found the classic construction in 1999. Since then, Google DeepMind's AlphaEvolve, GPT-5.4 Pro, and an agent platform called Dualverse have each pushed the best known area lower. Nobody knows what the optimum is.

### Slide 3: the result (0:55–1:30)
Working with the agent, we set new best-known values at every size that has a published result. At 128 directions, the area is 0.106909327. That's 6.88% smaller than AlphaEvolve, 2.05% smaller than GPT-5.4 Pro, and below the previous best. We also set records at 32 and 64 directions. And at 256, 512 and 1024 directions, where nobody had published an optimised result, we produced the first ones, each about ten percent below Keich's classic construction.

### Slide 4: how (1:30–2:20)
Four ideas made this possible on a laptop.
**One:** an exact formula. Every vertical slice of the union is 128 intervals of the same length. So the slice width is that length plus the gaps between neighbouring intervals, each capped at the interval length. No geometry library, and we get an exact gradient.
**Two:** we smooth those caps, then slowly sharpen them back while running gradient descent.
**Three:** a lifting trick. Every triangle is exactly two thinner triangles glued together, so we solve 8 directions first and refine all the way up to 128.
**Four:** an evolutionary search over many good solutions at once, running on compiled code.

### Slide 5 → Slide 6: what it found (2:20–2:45)
*(Slide 5)* Here's the old construction next to ours.
*(Press → for slide 6)* Keich's construction keeps every slice about the same width. Ours pays for a wider base, and in return the triangles bunch up at three focal heights, where the cross-section collapses.

### Slide 7 → live demo (2:45–3:30)
*(Slide 7)* You don't have to take my word for it.
*(Switch to the project-page tab and scroll once)* This is the live project page: the code, the certified solutions, and an interactive notebook.
*(Switch to Terminal and press Enter. It finishes in about a second.)* This is the benchmark's own official validator checking our solution live. It's valid, and the area is below the previous best. A second checker in the repository recomputes it with exact fractions, no rounding at all.

### Slide 8: close (3:30–3:45)
*(Switch back to the slides and press →)* These are upper bounds, so the true optimum is still open, and our margin over the very latest result is small. But one person directing an AI agent on a laptop beat AlphaEvolve in seven minutes. Thanks for watching.

---

## If you run long
Cut the second paragraph of slide 2 (the history), since slide 3 covers it. That saves about 15 seconds.

## The numbers, in case you're asked
| Directions | Previous best | Ours |
|---|---|---|
| 32 | 0.138596 | 0.138432 |
| 64 | 0.120901 | 0.120839 |
| 128 | 0.107067 | 0.106909327 |
| 256 | none published (Keich 0.106832) | 0.095951 |
| 512 | none published (Keich 0.096732) | 0.087041 |
| 1024 | none published (Keich 0.088343) | 0.079662 |
