"""Island memetic search on the numba kernel, with migration through pool/.
Usage: memetic2.py SEED MINUTES N"""
import glob, json, os, sys, time
import numpy as np
from kakeya import keich, grid
from fast import adam_nb, area_nb

seed, minutes, n = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
rng = np.random.default_rng(seed)
xs, w = grid(1000)
P = 14
os.makedirs(f"pool{n}", exist_ok=True)
S = 128 / n  # scale hyper-parameters with n


def refine(b, steps=None):
    return adam_nb(b, xs, w, steps or int(rng.integers(1500, 4000)), 10 ** rng.uniform(-3.4, -2.6) * S,
                   10 ** rng.uniform(-3.6, -2.4) * S, rng.choice([1.0, 2.0, 3.0]))


def load_pool():
    out = []
    for f in glob.glob(f"pool{n}/*.json"):
        try:
            out.append(np.array(json.load(open(f))["intercepts"]))
        except Exception:
            pass
    return out


pop = [refine(b, 500) for b in load_pool()]
while len(pop) < P:
    pop.append(refine(keich(int(np.log2(n))) * rng.uniform(0.7, 1.3) + rng.normal(0, 0.01 * S, n)))
pop.sort(key=lambda t: t[0]); pop = pop[:P]
log = open(f"m2log_{n}_{seed}.txt", "a")
print(f"init best {pop[0][0]:.9f}", file=log, flush=True)
t0 = time.time(); gen = 0; best_seen = pop[0][0]; ops = {}
while time.time() - t0 < minutes * 60:
    gen += 1
    i = min(rng.integers(0, P, 2)); b = pop[i][1].copy()
    r = rng.random()
    if r < 0.25:
        op = "noise"; b += rng.normal(0, 10 ** rng.uniform(-3.5, -2) * S, n)
    elif r < 0.45:
        op = "xover"; o = pop[rng.integers(0, P)][1]; k = 2 ** rng.integers(2, int(np.log2(n))); s = rng.integers(0, n // k) * k
        b[s:s + k] = o[s:s + k] - o[s:s + k].mean() + b[s:s + k].mean()
    elif r < 0.65:
        op = "shift"; k = int(rng.integers(1, n // 2)); s = rng.integers(0, n - k + 1)
        b[s:s + k] += 10 ** rng.uniform(-3.5, -1.8) * S * rng.choice([-1, 1])
    elif r < 0.8:
        op = "reset"; k = int(rng.integers(2, 17)); s = rng.integers(0, n - k + 1)
        b[s:s + k] = np.linspace(b[s], b[s + k - 1], k) + rng.normal(0, 0.003 * S, k)
    else:
        op = "tilt"; k = int(rng.integers(4, n // 2)); s = rng.integers(0, n - k + 1)
        b[s:s + k] += np.linspace(0, 1, k) * 10 ** rng.uniform(-3.5, -2) * S * rng.choice([-1, 1])
    a, c = refine(b)
    if a < pop[-1][0] and all(abs(a - q[0]) > 1e-9 for q in pop):
        pop[-1] = (a, c); pop.sort(key=lambda t: t[0])
        ops[op] = ops.get(op, 0) + 1
    if pop[0][0] < best_seen - 1e-10:
        best_seen = pop[0][0]
        print(f"{time.time()-t0:6.0f}s gen{gen} best={best_seen:.10f} ops={ops}", file=log, flush=True)
        json.dump({"intercepts": pop[0][1].tolist(), "grid_area": best_seen}, open(f"pool{n}/isl{seed}.json", "w"))
    if gen % 40 == 0:  # migration: pull the best other island's solution
        others = load_pool()
        if others:
            cand = min(others, key=lambda v: area_nb(v, xs, w))
            a = area_nb(cand, xs, w)
            if a < pop[-1][0] and all(abs(a - q[0]) > 1e-9 for q in pop):
                pop[-1] = (a, cand); pop.sort(key=lambda t: t[0])
