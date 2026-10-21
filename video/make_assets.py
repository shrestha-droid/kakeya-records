"""Slide images from results/. Run from repo root."""
import json, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
sys.path.insert(0, "src")
from kakeya import keich
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "axes.spines.top": False, "axes.spines.right": False})
n, d = 128, 1 / 128
b = np.array(json.load(open("results/n128.json"))["intercepts"])


def union(ax, bb, title):
    bb = bb - bb.min()
    ax.add_collection(PolyCollection([[(0, bb[i] - d), (0, bb[i]), (1, bb[i] + i / n)] for i in range(n)],
                      facecolors=[plt.cm.viridis(i / n) for i in range(n)], edgecolors="none", alpha=0.5))
    ax.autoscale(); ax.set_xlim(0, 1); ax.set_title(title); ax.set_xticks([]); ax.set_yticks([])


fig, ax = plt.subplots(1, 2, figsize=(12, 5.2), dpi=160)
union(ax[0], keich(), "Keich (1999): area 0.11921")
union(ax[1], b, f"Claude (2026): area {json.load(open('results/n128.json'))['exact_area']:.6f}")
fig.savefig("video/union.png", bbox_inches="tight", transparent=True)

xs = np.linspace(0, 1, 4001)
def ell(bb):
    S = np.sort(xs[:, None] * (np.arange(n) / n) + bb, 1); L = d * (1 - xs)
    return (L + np.minimum(np.diff(S, 1), L[:, None]).sum(1)) / d
fig, ax = plt.subplots(figsize=(11, 4.8), dpi=160)
ax.plot(xs, ell(keich()), color="#9aa0a6", lw=2.5, label="Keich: flat staircase")
ax.plot(xs, ell(b), color="#d4552b", lw=2.5, label="Claude: three focal points")
for x in (0.174, 0.436, 0.664):
    ax.axvline(x, color="#d4552b", ls=":", lw=1)
ax.set_xlabel("height x"); ax.set_ylabel("slice width  l(x) / δ"); ax.legend(frameon=False)
fig.savefig("video/profile.png", bbox_inches="tight", transparent=True)
print("ok")
