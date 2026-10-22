"""Pick the best island solution for each n, compute its exact area, check n=128 with the official
validator too, and keep the best certified solution per n in certified/. Usage: certify.py"""
import glob, json, os, time
from kakeya import official
from verify_exact_fast import exact_area

# Best previously published value per n: Dualverse Station (2026) for 32-128. Nothing optimised is
# published beyond 128, so there the comparison is Keich's construction (exact areas).
PREV = {32: 0.138596129670274, 64: 0.120900580819172, 128: 0.107066636561635,
        256: 0.10683190822601318, 512: 0.09673193943353345, 1024: 0.08834310054779054}

if __name__ == "__main__":
    os.makedirs("certified", exist_ok=True)
    for n in PREV:
        fs = glob.glob(f"pool{n}/isl*.json")
        if not fs:
            continue
        f = min(fs, key=lambda f: json.load(open(f))["grid_area"])
        b = [float(v) for v in json.load(open(f))["intercepts"]]
        out = f"certified/n{n}.json"
        old = json.load(open(out))["exact_area"] if os.path.exists(out) else 1.0
        if json.load(open(f))["grid_area"] > old + 1e-6:  # clearly worse than what we hold
            print(f"n={n}: kept {old:.12f}")
            continue
        ex = float(exact_area(b)[0])
        off = official(b).metrics["area"] if n == 128 else None
        print(f"n={n}: exact={ex:.12f} official={off} prev={PREV[n]:.12f} {'BEATS' if ex < PREV[n] else 'not yet'}", flush=True)
        if ex < old:
            json.dump({"n": n, "intercepts": b, "exact_area": ex, "official_validator_area": off,
                       "previous_best": PREV[n], "certified_at": time.strftime("%Y-%m-%d %H:%M %Z")},
                      open(out, "w"), indent=1)
