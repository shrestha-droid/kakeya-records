"""Fast exact verifier must equal the reference exact verifier, as rationals."""
import json, sys, time
sys.path.insert(0, "src")
from verify_exact import exact_area as slow
from verify_exact_fast import exact_area as fast

if __name__ == "__main__":
    for f in ("results/n32.json", "results/n128.json"):
        b = json.load(open(f))["intercepts"]
        t = time.time(); a1 = slow(b); t1 = time.time() - t
        t = time.time(); a2, m = fast(b, 6); t2 = time.time() - t
        assert a1 == a2, (f, float(a1), float(a2))
        print(f, "IDENTICAL", f"slow {t1:.0f}s fast {t2:.0f}s", m, flush=True)
