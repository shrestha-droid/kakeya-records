"""Numba kernel for the union area and its (smoothed) gradient. Adjacent x-slices have nearly the
same top ordering, so insertion sort warm-started from the previous slice is ~O(n) per slice."""
import numpy as np
from numba import njit


@njit(cache=True, fastmath=True)
def area_grad_nb(b, xs, w, tau):
    n = b.shape[0]
    order = np.argsort(b)
    t = np.empty(n)
    G = np.zeros(n)
    area = 0.0
    for r in range(xs.shape[0]):
        x = xs[r]
        for i in range(n):
            t[i] = x * i / n + b[i]
        for i in range(1, n):  # insertion sort of `order` by t
            k = order[i]; v = t[k]; j = i - 1
            while j >= 0 and t[order[j]] > v:
                order[j + 1] = order[j]; j -= 1
            order[j + 1] = k
        L = (1.0 - x) / n
        s = L
        wr = w[r]
        for i in range(n - 1):
            g = t[order[i + 1]] - t[order[i]]
            s += g if g < L else L
            if tau > 0:
                z = (L - g) / tau
                dg = 1.0 if z > 30 else (0.0 if z < -30 else 1.0 / (1.0 + np.exp(-z)))
            else:
                dg = 1.0 if g < L else 0.0
            if dg == 0.0:
                continue
            G[order[i + 1]] += wr * dg
            G[order[i]] -= wr * dg
        area += wr * s
    return area, G


@njit(cache=True, fastmath=True)
def area_nb(b, xs, w):
    return area_grad_nb(b, xs, w, 0.0)[0]


def adam_nb(b, xs, w, steps, lr, tau0, power=2.0):
    """Smoothed Adam with tau = tau0*(1-s)^power and linearly decaying lr; returns best seen."""
    return _adam(b.copy(), xs, w, steps, lr, tau0, power)


@njit(cache=True)
def _adam(b, xs, w, steps, lr, tau0, power):
    n = b.shape[0]
    m = np.zeros(n); v = np.zeros(n)
    best_a = area_nb(b, xs, w); best_b = b.copy()
    for t in range(1, steps + 1):
        s = t / steps
        tau = tau0 * (1 - s) ** power
        a, g = area_grad_nb(b, xs, w, tau)
        if tau == 0.0 and a < best_a:
            best_a = a; best_b[:] = b
        m = 0.9 * m + 0.1 * g
        v = 0.999 * v + 0.001 * g * g
        step = lr * (1 - s) + lr * 0.01
        b = b - step * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-12)
        b -= b.mean()
        if t % 25 == 0 or t == steps:
            a0 = area_nb(b, xs, w)
            if a0 < best_a:
                best_a = a0; best_b[:] = b
    return best_a, best_b
