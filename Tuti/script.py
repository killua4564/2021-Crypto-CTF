from Crypto.Util.number import *
from gmpy2 import isqrt

# (x+1)**2 * (y-1)**2 = 4k
# (x+1)(y-1) = 2 * sqrt(k)
k = int("bfdc32162934ad6a054b4b3db8578674e27a165113f8ed018cbe91124fbd63144ab6923d107eee2bc0712fcbdb50d96fdf04dd1ba1b69cb1efe71af7ca08ddc7cc2d3dfb9080ae56861d952e8d5ec0ba0d3dfdf2d12764", 16)

# 2 * isqrt(k) = 2^2 · 3 · 11^2 · 19 · 47 · 71 · 3449 · 11953 · 5485619 · 2035395403834744453 · 17258104558019725087 · 1357459302115148222329561139218955500171643099

n = 2 * int(isqrt(k))
E = [(2, 2), (3, 1), (11, 2), (19, 1), (47, 1), (71, 1), (3449, 1), (11953, 1), (5485619, 1), (2035395403834744453, 1), (17258104558019725087, 1), (1357459302115148222329561139218955500171643099, 1)]


def f(total=1, idx=0):
    if idx == len(E):
        yield total
        return
    for i in range(E[idx][1]+1):
        yield from f(total * E[idx][0] ** i, idx+1)

for m in f():
    if long_to_bytes(m).startswith(b"CCTF"):
        print((long_to_bytes(m-1) + long_to_bytes(n // m + 1)).decode())


