"""Builds paper/figure.png from results/n128.json. Run from the repo root."""
import json, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

sys.path.insert(0, "src")
from kakeya import keich

sol = json.load(open("results/n128.json"))
b, area = np.array(sol["intercepts"]), sol["exact_area"]
n, d = 128, 1 / 128
ACCENT, GREY = "#d4552b", "#9aa0a6"


def ell(bb, xs):
    S = np.sort(xs[:, None] * (np.arange(n) / n) + bb, 1)
    L = d * (1 - xs)
    return L + np.minimum(np.diff(S, 1), L[:, None]).sum(1)


plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(1, 3, figsize=(12, 3.5), dpi=220, gridspec_kw={"width_ratios": [1.1, 1.1, 1], "wspace": 0.3})

bb = b - b.min()
ax[0].add_collection(PolyCollection([[(0, bb[i] - d), (0, bb[i]), (1, bb[i] + i / n)] for i in range(n)],
                                    facecolors=[plt.cm.viridis(i / n) for i in range(n)], edgecolors="none", alpha=0.5))
ax[0].autoscale(); ax[0].set_xlim(0, 1)
ax[0].set_title(f"(a) new record: 128 thin triangles,\nunion area {area:.9f}", loc="left")
ax[0].set_xlabel("x"); ax[0].set_ylabel("y")

xs = np.linspace(0, 1, 4001)
ax[1].plot(xs, ell(keich(), xs) / d, color=GREY, lw=1.2, label="Keich (1999), area 0.119207")
ax[1].plot(xs, ell(b, xs) / d, color=ACCENT, lw=1.2, label=f"this work, area {area:.6f}")
ax[1].set_title("(b) cross-section length l(x)\n(area = integral of l over x)", loc="left")
ax[1].set_xlabel("x"); ax[1].set_ylabel("l(x) / delta"); ax[1].legend(frameon=False, fontsize=8)

labels = ["Keich\n1999", "AlphaEvolve\n2025", "GPT-5.4 Pro\n2026", "Dualverse\n2026", "This work\n(Claude)"]
vals = [0.1192072654, 0.1148103258, 0.1091479892, 0.1070666366, area]
ax[2].barh(range(5)[::-1], vals, color=[GREY] * 4 + [ACCENT], height=0.65)
for i, v in enumerate(vals):
    ax[2].text(v + 0.0002, 4 - i, f"{v:.6f}", va="center", fontsize=8, color=ACCENT if i == 4 else "#333")
ax[2].set_yticks(range(5)[::-1]); ax[2].set_yticklabels(labels, fontsize=8)
ax[2].set_xlim(0.100, 0.1235); ax[2].set_xlabel("union area, N=128 (lower is better)")
ax[2].set_title("(c) best known constructions", loc="left")
fig.savefig("paper/figure.png", bbox_inches="tight")
print("wrote paper/figure.png")
