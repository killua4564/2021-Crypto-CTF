from Crypto.Util.number import *

load("coppersmith.sage")
n = 98027132963374134222724984677805364225505454302688777506193468362969111927940238887522916586024601699661401871147674624868439577416387122924526713690754043
c = 42066148309824022259115963832631631482979698275547113127526245628391950322648581438233116362337008919903556068981108710136599590349195987128718867420453399

for p_len in (19, 20):
    for q_len in (19, 20):
        F.<p, q> = PolynomialRing(Zmod(2 * n + 1))
        p, q = p * 10^q_len + q, q * 10^p_len + p
        p, q = p * 10^(p_len+q_len) + q, q * 10^(p_len+q_len) + p
        f = p * q - n
        result = small_roots(f, (2^65, 2^65), m=1, d=3)
        if len(result) > 0:
            p, q = p(*result[0]), q(*result[0])
            if p * q != n:
                continue
            d = inverse_mod(0x10001, (p-1) * (q-1))
            print(long_to_bytes(pow(c, d, n)).decode())
        
