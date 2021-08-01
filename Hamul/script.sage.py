

# This file was *autogenerated* from the file script.sage
from sage.all_cmdline import *   # import sage library

_sage_const_98027132963374134222724984677805364225505454302688777506193468362969111927940238887522916586024601699661401871147674624868439577416387122924526713690754043 = Integer(98027132963374134222724984677805364225505454302688777506193468362969111927940238887522916586024601699661401871147674624868439577416387122924526713690754043); _sage_const_42066148309824022259115963832631631482979698275547113127526245628391950322648581438233116362337008919903556068981108710136599590349195987128718867420453399 = Integer(42066148309824022259115963832631631482979698275547113127526245628391950322648581438233116362337008919903556068981108710136599590349195987128718867420453399); _sage_const_19 = Integer(19); _sage_const_20 = Integer(20); _sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_10 = Integer(10); _sage_const_65 = Integer(65); _sage_const_3 = Integer(3); _sage_const_0 = Integer(0); _sage_const_0x10001 = Integer(0x10001)
from Crypto.Util.number import *

load("coppersmith.sage")
n = _sage_const_98027132963374134222724984677805364225505454302688777506193468362969111927940238887522916586024601699661401871147674624868439577416387122924526713690754043 
c = _sage_const_42066148309824022259115963832631631482979698275547113127526245628391950322648581438233116362337008919903556068981108710136599590349195987128718867420453399 

for p_len in (_sage_const_19 , _sage_const_20 ):
    for q_len in (_sage_const_19 , _sage_const_20 ):
        F = PolynomialRing(Zmod(_sage_const_2  * n + _sage_const_1 ), names=('p', 'q',)); (p, q,) = F._first_ngens(2)
        p, q = p * _sage_const_10 **q_len + q, q * _sage_const_10 **p_len + p
        p, q = p * _sage_const_10 **(p_len+q_len) + q, q * _sage_const_10 **(p_len+q_len) + p
        f = p * q - n
        result = small_roots(f, (_sage_const_2 **_sage_const_65 , _sage_const_2 **_sage_const_65 ), m=_sage_const_1 , d=_sage_const_3 )
        if len(result) > _sage_const_0 :
            p, q = p(*result[_sage_const_0 ]), q(*result[_sage_const_0 ])
            if p * q != n:
                continue
            d = inverse_mod(_sage_const_0x10001 , (p-_sage_const_1 ) * (q-_sage_const_1 ))
            print(long_to_bytes(pow(c, d, n)).decode())
        

