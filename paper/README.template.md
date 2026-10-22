# Kakeya Records: new best-known thin-triangle Kakeya constructions found by an AI agent

**Shrestha Pandey · 4th Open Scientific Intelligence Hackathon, 21–22 Oct 2026 · solo entry**

I set out to answer the hackathon's own question: can one person directing an AI research agent reach a real, verifiable discovery within the event? I ran Claude Code (Claude Opus 5.5) on an 8 GB M1 laptop as my research agent. It picked an open problem from the [HorizonMath](https://github.com/ewang26/HorizonMath) benchmark and, **63 minutes after starting**, found a construction that beats every published value for the *thin-triangle Kakeya problem*. The previous published values came from Keich (1999), Google DeepMind's AlphaEvolve (2025), GPT-5.4 Pro (HorizonMath, 2026) and Dualverse Station (2026). Each record below is checked twice: by the benchmark's official validator, and by an independent verifier that uses **exact rational arithmetic**.

![figure](paper/figure.png)

## The problem

Fix N slopes a_i = i/N and δ = 1/N. Each slope gets a thin triangle with a vertical base [b_i − δ, b_i] at x = 0 and its apex at (1, a_i + b_i). You choose the intercepts b_i, and the goal is to **minimise the area of the union**. This is a discretised Kakeya needle problem: the union contains a unit segment in every one of the N directions. Keich (1999) showed the area can shrink like 1/log N, and finding the best finite N constructions is open. N = 128 is HorizonMath problem `keich_thin_triangles_128`.

## Results (union area; lower is better)

| N | Keich 1999 | AlphaEvolve 2025 | GPT-5.4 Pro 2026 | Dualverse 2026 (previous best) | **This work** |
|---|---|---|---|---|---|
| 32 | 0.154590 | 0.141647 | – | 0.138596 | **{N32}** |
| 64 | 0.134694 | 0.121735 | – | 0.120901 | **{N64}** |
| 128 | 0.119207 | 0.114810 | 0.109148 | 0.107067 | **{N128}** |
| 256 | 0.106832 | – | – | none published | **{N256}** (first optimised value) |
| 512 | 0.096732 | – | – | none published | **{N512}** (first optimised value) |
| 1024 | 0.088343 | – | – | none published | **{N1024}** (first optimised value) |

At N = 128 the new construction is {GAIN_DV} below the previous best, {GAIN_GPT} below GPT-5.4 Pro, {GAIN_AE} below AlphaEvolve and {GAIN_K} below Keich. The intercepts are in [`results/`](results/). Each file stores the float64 intercepts and the **exact** area of exactly that configuration.

## Verify it yourself (about 1 minute)

```bash
git clone https://github.com/ewang26/HorizonMath
python -c "import json,sys; sys.path.insert(0,'HorizonMath'); from validators.keich_thin_triangles_128 import validate; print(validate({'intercepts': json.load(open('results/n128.json'))['intercepts']}))"
python src/verify_exact.py results/n128.json        # exact rational arithmetic, any N (reference)
python src/verify_exact_fast.py results/n1024.json  # same exact result in integer arithmetic, parallel; tests/ checks they agree
```

To explore it interactively, run `marimo edit notebook.py`. The notebook has a cross-section slider, the l(x) profile, the comparison table and a live run of the official validator.

## How it was found

1. **Exact reformulation.** Every vertical slice of the union is N intervals of the *same* length L(x) = δ(1 − x). The slice length is therefore exactly L + Σ_k min(g_k, L), where g_k are the gaps between consecutive sorted interval tops. That gives the area and an exact subgradient in O(N log N) per slice, with no polygon clipping.
2. **Smoothed descent.** We replace min(g, L) with a soft-min whose temperature τ is annealed to 0, and run Adam on the 128 intercepts. A single run takes about 10 s and gives 0.1084 from the Keich start, which already beats AlphaEvolve and GPT-5.4 Pro.
3. **Coarse-to-fine lifting.** A triangle at resolution N is *exactly* the union of its two children at resolution 2N, using intercepts b and b − 1/(2N). So the best area can only go down along dyadic refinement. We optimise at N = 8, 16, …, 128, keeping a beam of the best configurations at each level.
4. **Memetic islands.** Populations of locally optimal configurations are mutated in five ways: Gaussian noise, dyadic-block crossover, block shifts, block tilts and block resets. Each child is re-descended. Islands share their best configurations through a pool. Two choices made this cheap: a Numba kernel, and an insertion sort warm-started from the previous slice, since neighbouring slices are nearly sorted already.
5. **Certification.** The best configuration goes through the official HorizonMath validator and through `src/verify_exact.py`. The second one converts every float to the exact binary rational it denotes, collects all 32,640 pairwise crossings of the 256 edge lines (the breakpoints of the piecewise-linear l(x)), and integrates exactly with Python `Fraction`s.

## What the agent noticed

- **Mirror symmetry.** The problem is invariant under b_i ↦ δ − b_{N−1−i}, a reflection combined with a shear. Optimal configurations are *not* symmetric, and forcing symmetry did not help.
- **Focusing, not flattening.** Keich's construction has an almost flat, staircase cross-section profile. The optimised configurations instead accept a much wider slice at x = 0 (27δ against 18δ). In return, bundles of triangles converge at three *focal heights*, x ≈ 0.17, 0.44 and 0.66, where the slice shrinks to about 10–12δ (panel b).
- **Discretisation.** The midpoint rule on 1000 slices agrees with the exact area to about 3e-7, so the search ran on the cheap estimate and only finalists were certified exactly.

## Timeline (IST, 21–22 Oct 2026)

| time | event |
|---|---|
| 23:02 | Agent starts, sets up the environment and surveys the 113 HorizonMath problems |
| 23:09 | First optimiser run gives 0.108390, beating AlphaEvolve and GPT-5.4 Pro |
| 23:20 | Literature check finds Dualverse's 0.107067, which becomes the new target |
| 23:38 | Coarse-to-fine lifting reaches 0.10735 |
| 23:55 | Numba kernel gives about 4× the throughput, and the memetic islands start |
| **00:05** | **0.1070334 certified: new record for N = 128** |
| 00:20 | 0.1069676 for N = 128; 0.1384322 for N = 32 (record) |
| 00:27 | 0.1208867 for N = 64 (record): new best at every N with a published value |

## Roles

- **Shrestha Pandey: project lead.** Entered solo, set the goal (a verifiable record inside the hackathon window, aimed at winning), directed the agent throughout, pushed it to keep going past the first win to beat the strongest prior value and to cover every published size, reviewed and approved what was published, and prepared and presented the submission.
- **Claude Code (Claude Opus 5.5): research agent.** Surveyed the benchmark and chose the problem, derived the formulation, wrote the search and verification code, and ran the experiments.

## Honest caveats

- These are upper bounds from explicit constructions. Nobody knows how far they are from optimal.
- The previous best at every N is a 2026 web notebook from Dualverse Station, not a peer-reviewed paper. We compare against it because it is the strongest value we could find.
- The N = 128 margin over that value is small ({GAIN_DV}). The margins over AlphaEvolve and GPT-5.4 Pro are large.

## Repository

- `src/kakeya.py`: problem definition, NumPy reference kernel, Keich construction, official-validator hook.
- `src/fast.py`: Numba area/gradient kernel and annealed Adam.
- `src/multiscale.py`, `src/memetic2.py`: the coarse-to-fine beam search and the island search.
- `src/verify_exact.py`, `src/certify.py`: exact certification.
- `notebook.py`: interactive marimo certificate.
- `paper/`: figure and one-page summary.
- `video/`: the four-minute talk script and slides.

## References

U. Keich, *On L^p bounds for Kakeya maximal functions and the Minkowski dimension in R²*, Bull. LMS (1999) · A. Novikov et al., *AlphaEvolve* (2025) · B. Georgiev, J. Gómez-Serrano, T. Tao, A. Z. Wagner, *Mathematical exploration and discovery at scale* (2025) · E. Y. Wang et al., *HorizonMath* (arXiv:2603.15617, 2026) · Dualverse Station, *Discretized Kakeya Needle* (2026).
