"""Thin-triangle Kakeya (HorizonMath keich_thin_triangles_128): minimise union area.

Cross-section at x: 128 intervals of equal length L(x)=delta*(1-x) with tops t_i(x)=a_i x+b_i.
Union length = L + sum_k min(gap_k, L) over consecutive sorted tops -> cheap, vectorised,
with an exact subgradient. Final scores always come from the official validator.
"""
import json, sys, time
import numpy as np

N = 128


def keich(n=7):
    k = np.arange(2**n)
    b = np.zeros(2**n)
    for i in range(1, n + 1):
        eps = (k >> (n - i)) & 1  # i-th binary digit of k/2^n
        b += ((1 - i) / n) * eps * 2.0**-i
    return b


def grid(m):
    xs = (np.arange(m) + 0.5) / m  # midpoint rule
    return xs, np.full(m, 1.0 / m)


def area_grad(b, xs, w, tau=0.0):
    n = len(b)
    T = xs[:, None] * (np.arange(n) / n)[None, :] + b[None, :]
    idx = np.argsort(T, axis=1)
    S = np.take_along_axis(T, idx, axis=1)
    g = np.diff(S, axis=1)
    L = ((1 - xs) / n)[:, None]
    if tau > 0:  # smooth min(g, L) = -tau*log(exp(-g/tau)+exp(-L/tau)); area reported unsmoothed
        e = np.exp(-np.abs(g - L) / tau)
        dg = np.where(g < L, 1.0, e) / (1.0 + e)  # d/dg of the smooth min
    else:
        dg = (g < L).astype(float)
    area = float(w @ (L[:, 0] + np.minimum(g, L).sum(1)))
    dg = dg * w[:, None]
    D = np.zeros_like(T)
    D[:, 1:] += dg
    D[:, :-1] -= dg
    G = np.empty_like(T)
    np.put_along_axis(G, idx, D, axis=1)
    return area, G.sum(0)


def adam(b, xs, w, steps, lr, tau_sched=None, seed=0):
    m = np.zeros_like(b); v = np.zeros_like(b)
    best = (area_grad(b, xs, w)[0], b.copy())
    for t in range(1, steps + 1):
        tau = tau_sched(t / steps) if tau_sched else 0.0
        a, g = area_grad(b, xs, w, tau)
        m = 0.9 * m + 0.1 * g; v = 0.999 * v + 0.001 * g * g
        step = lr * (1 - t / steps) + lr * 0.01
        b = b - step * (m / (1 - 0.9**t)) / (np.sqrt(v / (1 - 0.999**t)) + 1e-12)
        b -= b.mean()
        if t % 50 == 0 or t == steps:
            a0 = area_grad(b, xs, w)[0]
            if a0 < best[0]:
                best = (a0, b.copy())
    return best


def official(b):
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "HorizonMath"))
    from validators.keich_thin_triangles_128 import validate
    r = validate({"intercepts": [float(x) for x in b]})
    return r


if __name__ == "__main__":
    xs, w = grid(4000)
    b0 = keich()
    print("keich grid area", area_grad(b0, xs, w)[0])
