"""Exact rational area of the union of the 128 thin triangles. Usage: verify_exact.py solution.json

Every float intercept is converted to the exact binary rational it denotes, so the result is
the exact area of exactly the configuration in the file (no rounding anywhere).
Union length l(x) is continuous and piecewise linear with breakpoints only where two of the
256 edge lines cross, so the trapezoid rule over all crossings is exact.
"""
import json, sys
from fractions import Fraction as F


def union_len(tops, L):
    tops = sorted(tops)
    return L + sum(min(b - a, L) for a, b in zip(tops, tops[1:]))


def exact_area(bs):
    n = len(bs)
    d = F(1, n)
    b = [F(v) for v in bs]
    lines = [(F(i, n), b[i]) for i in range(n)] + [(F(i, n) + d, b[i] - d) for i in range(n)]
    xs = {F(0), F(1)}
    for j in range(len(lines)):
        sj, cj = lines[j]
        for k in range(j + 1, len(lines)):
            sk, ck = lines[k]
            if sj != sk:
                x = (ck - cj) / (sj - sk)
                if 0 < x < 1:
                    xs.add(x)
    xs = sorted(xs)

    def ell(x):
        return union_len([F(i, n) * x + b[i] for i in range(n)], d * (1 - x))

    area, px, pl = F(0), xs[0], ell(xs[0])
    for x in xs[1:]:
        l = ell(x)
        area += (pl + l) * (x - px) / 2
        px, pl = x, l
    return area


if __name__ == "__main__":
    sol = json.load(open(sys.argv[1]))
    a = exact_area(sol["intercepts"])
    print(f"exact area = {float(a):.15f}  (rational with {len(str(a.denominator))}-digit denominator)")
