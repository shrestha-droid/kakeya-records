"""Score an N=128 solution with HorizonMath's official validator (needs ./HorizonMath).
Usage: python src/verify_official.py results/n128.json"""
import json, sys
sys.path.insert(0, "HorizonMath")
from validators.keich_thin_triangles_128 import validate
r = validate({"intercepts": json.load(open(sys.argv[1]))["intercepts"]})
print(f"official HorizonMath validator: valid={r.valid}  union area={r.metrics['area']:.12f}")
print(f"previous best (Dualverse 2026):                   0.107066636562")
