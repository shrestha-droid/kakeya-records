"""Pick the best island solution for each n, verify exactly (and with the official validator
for n=128), and save to certified/. Usage: certify.py"""
import glob, json, os, subprocess, sys, time
import numpy as np
from kakeya import official
from verify_exact import exact_area
PREV = {32: 0.138596129670274, 64: 0.120900580819172, 128: 0.107066636561635,
        256: 0.10683227734375}  # n=256: no published optimised value; Keich's construction
os.makedirs("certified", exist_ok=True)
for n in (32, 64, 128, 256):
    fs = glob.glob(f"pool{n}/isl*.json")
    if not fs: continue
    f = min(fs, key=lambda f: json.load(open(f))["grid_area"])
    b = [float(v) for v in json.load(open(f))["intercepts"]]
    ex = float(exact_area(b))
    off = official(b).metrics["area"] if n == 128 else None
    out = f"certified/n{n}.json"
    old = json.load(open(out))["exact_area"] if os.path.exists(out) else 1.0
    tag = "RECORD" if ex < PREV[n] else "not yet"
    print(f"n={n}: exact={ex:.12f} official={off} prev_best={PREV[n]:.12f} {tag}")
    if ex < old:
        json.dump({"n": n, "intercepts": b, "exact_area": ex, "official_validator_area": off,
                   "previous_best": PREV[n], "certified_at": time.strftime("%Y-%m-%d %H:%M %Z")},
                  open(out, "w"), indent=1)
