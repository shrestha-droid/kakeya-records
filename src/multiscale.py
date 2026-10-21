"""Coarse-to-fine: optimise n slopes, lift to 2n by splitting each triangle in two
(child offset d), re-optimise; beam of the best few at each scale."""
import numpy as np, sys, time
from kakeya import *
rng=np.random.default_rng(int(sys.argv[1])); xs,w=grid(1000)
beam=[(0,np.zeros(4))]
n=4
while n<128:
    n*=2; cand=[]
    for _,b in beam:
        for rep in range(int(sys.argv[2])):
            d=rng.uniform(-1.5,0.5)/n
            b2=np.repeat(b,2); b2[1::2]+=d; b2+=rng.normal(0,0.1/n,n)
            tau0=10**rng.uniform(-3,-2)*128/n
            steps=1500 if n<128 else 3000
            cand.append(adam(b2,xs,w,steps,10**rng.uniform(-3.3,-2.6)*128/n,lambda s:tau0*(1-s)**2))
    cand.sort(key=lambda t:t[0]); beam=cand[:int(sys.argv[3])]
    print(n,[round(c[0],6) for c in cand[:5]],flush=True)
np.save(f"ms_{sys.argv[1]}.npy",beam[0][1])
