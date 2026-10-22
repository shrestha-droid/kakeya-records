"""Exact union area, fast: same maths as verify_exact.py, but in plain integers and in parallel.

Every float64 intercept is a dyadic rational B_i / 2^K. Scaling y by n*2^K makes all 2N edge
lines integer lines S*x + C. At a breakpoint x = P/Q every edge value times Q is the integer
S*P + C*Q, so the slice length times (n*2^K*Q) is an exact integer U(P/Q). The area is the
exact trapezoid sum over all breakpoints, accumulated as one Fraction at the end of each chunk.
Usage: verify_exact_fast.py solution.json [workers]"""
import json, sys
from fractions import Fraction as F
from math import gcd
from multiprocessing import Pool

_S = _C = None
_n = _K2 = 0


def _init(S, C, n, K2):
    global _S, _C, _n, _K2
    _S, _C, _n, _K2 = S, C, n, K2


def _U(PQ):
    """Exact slice length at x=P/Q, times n*2^K*Q, as an integer."""
    P, Q = PQ
    tops = sorted(_S[i] * P + _C[i] * Q for i in range(_n))
    L = _K2 * (Q - P)  # delta*(1-x) scaled: 2^K*(Q-P)
    u = L
    for a, b in zip(tops, tops[1:]):
        g = b - a
        u += g if g < L else L
    return u


def _chunk(pts):
    """Sum of trapezoids over consecutive breakpoints pts[0..m] (exact Fraction)."""
    tot = F(0)
    prev = None
    for P, Q in pts:
        l = F(_U((P, Q)), Q)
        if prev is not None:
            (pP, pQ), pl = prev
            tot += (pl + l) * (F(P, Q) - F(pP, pQ)) / 2
        prev = ((P, Q), l)
    return tot


def exact_area(bs, workers=8):
    n = len(bs)
    assert n & (n - 1) == 0, "n must be a power of two"
    rats = [F(v) for v in bs]
    K = max(r.denominator.bit_length() - 1 for r in rats)
    K2 = 1 << K
    Bi = [r.numerator * (K2 // r.denominator) for r in rats]  # b_i = Bi / 2^K exactly
    # y scaled by n*2^K: top_i = i*2^K*x + n*Bi, bottom_i = (i+1)*2^K*x + n*Bi - 2^K
    S = [i * K2 for i in range(n)]
    C = [n * Bi[i] for i in range(n)]
    lines = list(zip(S, C)) + [((i + 1) * K2, n * Bi[i] - K2) for i in range(n)]
    xs = {(0, 1), (1, 1)}
    for j in range(len(lines)):
        sj, cj = lines[j]
        for k in range(j + 1, len(lines)):
            sk, ck = lines[k]
            if sj == sk:
                continue
            P, Q = ck - cj, sj - sk
            if Q < 0:
                P, Q = -P, -Q
            if 0 < P < Q:
                g = gcd(P, Q)
                xs.add((P // g, Q // g))
    xs = sorted(xs, key=lambda t: F(t[0], t[1]))
    m = len(xs)
    step = max(1, m // (workers * 8))
    chunks = [xs[i:min(i + step + 1, m)] for i in range(0, m - 1, step)]  # overlap by one point
    with Pool(workers, initializer=_init, initargs=(S, C, n, K2)) as pool:
        parts = pool.map(_chunk, chunks)
    # slice length was scaled by n*2^K; undo it
    return sum(parts, F(0)) / (n * K2), m


if __name__ == "__main__":
    sol = json.load(open(sys.argv[1]))
    a, m = exact_area(sol["intercepts"], int(sys.argv[2]) if len(sys.argv) > 2 else 8)
    print(f"exact area = {float(a):.15f}  ({m} breakpoints, rational with {len(str(a.denominator))}-digit denominator)")
