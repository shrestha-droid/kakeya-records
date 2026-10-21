"""Fill {N32} etc. in templates from results/*.json. Usage (repo root): python paper/fill.py"""
import json
r = {n: json.load(open(f"results/n{n}.json")) for n in (32, 64, 128)}
DV = {32: 0.138596129670274, 64: 0.120900580819172, 128: 0.107066636561635}
a = r[128]["exact_area"]
fmt = lambda n: (f"{r[n]['exact_area']:.6f}" if r[n]["exact_area"] < DV[n] else f"{r[n]['exact_area']:.6f} (not a record)")
pct = lambda old: f"{(old - a) / old * 100:.2f}%"
vals = {"N32": fmt(32), "N64": fmt(64), "N128": f"{a:.9f}", "GAIN_DV": pct(DV[128]), "GAIN_GPT": pct(0.1091479892),
        "GAIN_AE": pct(0.1148103258), "GAIN_K": pct(0.1192072654)}
for src, dst in [("paper/README.template.md", "README.md"), ("paper/summary.template.html", "paper/summary.html"),
                 ("video/script.template.md", "video/script.md"), ("video/slides.template.html", "video/slides.html"), ("paper/index.template.html", "index.html")]:
    try:
        s = open(src).read()
    except FileNotFoundError:
        continue
    for k, v in vals.items():
        s = s.replace("{" + k + "}", v)
    open(dst, "w").write(s)
print(vals)
