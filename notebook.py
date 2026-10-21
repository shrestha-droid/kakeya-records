import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    return PolyCollection, json, mo, np, plt


@app.cell
def _(mo):
    mo.md(r"""
    # Thin-triangle Kakeya, N = 128: an interactive certificate

    For each slope $a_i = i/128$ we place a thin triangle with vertical base
    $[b_i-\delta, b_i]$ at $x=0$ and apex $(1, a_i + b_i)$, where $\delta = 1/128$. The score is
    the area of the union, and **lower is better**. This is HorizonMath problem
    `keich_thin_triangles_128`.

    Every vertical cross-section of the union is 128 intervals of equal length
    $L(x)=\delta(1-x)$. Its length is therefore $L + \sum_k \min(g_k, L)$, where $g_k$ are the
    gaps between consecutive sorted tops. Our optimiser descends this quantity directly.
    """)
    return


@app.cell
def _(json, np):
    sol = json.load(open("results/n128.json"))
    b = np.array(sol["intercepts"])
    n, d = 128, 1 / 128

    def profile(bb, xs):
        T = xs[:, None] * (np.arange(n) / n) + bb
        S = np.sort(T, 1)
        L = d * (1 - xs)
        return L + np.minimum(np.diff(S, 1), L[:, None]).sum(1)

    def keich(m=7):
        k = np.arange(2**m)
        out = np.zeros(2**m)
        for i in range(1, m + 1):
            out += ((1 - i) / m) * ((k >> (m - i)) & 1) * 2.0**-i
        return out

    return b, d, keich, n, profile


@app.cell
def _(mo):
    x_slider = mo.ui.slider(0.0, 0.99, step=0.01, value=0.25, label="cross-section at x")
    x_slider
    return (x_slider,)


@app.cell
def _(PolyCollection, b, d, keich, mo, n, np, plt, profile, x_slider):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    bb = b - b.min()
    tris = [[(0, bb[i] - d), (0, bb[i]), (1, bb[i] + i / n)] for i in range(n)]
    axes[0].add_collection(PolyCollection(tris, facecolors=[plt.cm.viridis(i / n) for i in range(n)], alpha=0.5))
    axes[0].autoscale()
    axes[0].axvline(x_slider.value, color="k", lw=1)
    axes[0].set_title("union of 128 thin triangles")
    xs = np.linspace(0, 1, 2001)
    axes[1].plot(xs, profile(keich(), xs), label="Keich (1999)", color="#9aa0a6")
    axes[1].plot(xs, profile(b, xs), label="this work", color="#d4552b")
    axes[1].axvline(x_slider.value, color="k", lw=1)
    axes[1].set_title("cross-section length l(x); area = integral")
    axes[1].legend()
    mo.mpl.interactive(fig)
    return


@app.cell
def _(b, keich, mo, np, profile):
    xm = (np.arange(200000) + 0.5) / 200000
    ours = profile(b, xm).mean()
    mo.md(f"""
    | construction | union area |
    |---|---|
    | Keich (1999) | {profile(keich(), xm).mean():.9f} |
    | AlphaEvolve (2025) | 0.114810326 |
    | GPT-5.4 Pro, HorizonMath (2026) | 0.109147989 |
    | Dualverse Station (2026) | 0.107066637 |
    | **this work** (midpoint rule, 200k nodes) | **{ours:.9f}** |
    """)
    return


@app.cell
def _(b, mo):
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path("HorizonMath").resolve()))
    try:
        from validators.keich_thin_triangles_128 import validate
        r = validate({"intercepts": [float(v) for v in b]})
        out = mo.md(f"**Official HorizonMath validator:** valid={r.valid}, area = `{r.metrics.get('area'):.15f}`")
    except ImportError:
        out = mo.md("Clone `ewang26/HorizonMath` next to this notebook to run the official validator.")
    out
    return


if __name__ == "__main__":
    app.run()
