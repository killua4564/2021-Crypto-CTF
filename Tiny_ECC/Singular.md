# Singular

We have this challenge:

```
Alice and Bob calculated a shared key on the elliptic curve 

y^2 = x^3 + 330762886318172394930696774593722907073441522749x^2 + 6688528763308432271990130594743714957884433976x + 759214505060964991648440027744756938681220132782 

p = 785482254973602570424508065997142892171538672071 
G = (1, 68596750097555148647236998220450053605331891340)

(Alice's public key) P = d1 * G = (453762742842106273626661098428675073042272925939, 680431771406393872682158079307720147623468587944) 
(Bob's poblic key) Q = d2 * G = (353016783569351064519522488538358652176885848450, 287096710721721383077746502546881354857243084036) 


They have calculated K = d1 * d2 * G. They have taken K's x coordinate in decimal and took sha256 of it and used it for AES ECB to encrypt the flag.

Here is the encrypted flag: 480fd106c9a637d22fddd814965742236eb314c1b8fb68e70a7c7445ff04476082f8b9026c49d27110ba41b95e9f51dc
```



OK, so it looks like we need to solve a discrete logarithm problem on this particular instance of an elliptic curve. 

Let's do some sanity checks first:

```
sage: p = 785482254973602570424508065997142892171538672071
sage: is_prime(p)
True
```

OK, so the ground field is $`GF(p)`$ for a prime $`p`$.

Let's try to build the curve to play with it. We use the long form of the Weierstrass equation
```math
y^2 + a_1 xy + a_3y = x^3 + a_2 x^2 + a_4 x + a_6
```
to initialize Sage's EllipticCurve object

```
sage: a1 = 0
sage: a3 = 0
sage: a2 = 330762886318172394930696774593722907073441522749
sage: a4 = 6688528763308432271990130594743714957884433976
sage: a6 = 759214505060964991648440027744756938681220132782
sage: EE = EllipticCurve(GF(p), [a1,a2,a3,a4,a6])

```

However, we get the following error

```
---------------------------------------------------------------------------
ArithmeticError                           Traceback (most recent call last)
<ipython-input-49-9bc6af2c1a74> in <module>()
----> 1 EE = EllipticCurve(GF(p), [a1,a2,a3,a4,a6])

sage/structure/factory.pyx in sage.structure.factory.UniqueFactory.__call__ (build/cythonized/sage/structure/factory.c:1894)()

sage/structure/factory.pyx in sage.structure.factory.UniqueFactory.get_object (build/cythonized/sage/structure/factory.c:2278)()

/usr/lib/python2.7/dist-packages/sage/schemes/elliptic_curves/constructor.pyc in create_object(self, version, key, **kwds)
    457         elif is_FiniteField(R) or (is_IntegerModRing(R) and R.characteristic().is_prime()):
    458             from .ell_finite_field import EllipticCurve_finite_field
--> 459             return EllipticCurve_finite_field(R, x)
    460         elif R in _Fields:
    461             from .ell_field import EllipticCurve_field

/usr/lib/python2.7/dist-packages/sage/schemes/elliptic_curves/ell_generic.pyc in __init__(self, K, ainvs)
    149         self.__ainvs = tuple(K(a) for a in ainvs)
    150         if self.discriminant() == 0:
--> 151             raise ArithmeticError("invariants " + str(ainvs) + " define a singular curve")
    152         PP = projective_space.ProjectiveSpace(2, K, names='xyz');
    153         x, y, z = PP.coordinate_ring().gens()

ArithmeticError: invariants (0, 330762886318172394930696774593722907073441522749, 0, 6688528763308432271990130594743714957884433976, 759214505060964991648440027744756938681220132782) define a singular curve
```

Looks like the curve is singular and Sagemath seems to be not happy working with these. Let's double check this and compute the discriminant following the formulae from http://mathworld.wolfram.com/EllipticDiscriminant.html

```
sage: b2 = a1^2 + 4*a2
sage: b4 = 2*a4 + a1*a3
sage: b6 = a3^2 + 4*a6
sage: b8 = a1^2*a6 + 4*a2*a6 - a1*a3*a4 + a2*a3^2 - a4^2
sage: Di = -b2^2*b8 - 8*b4^3 - 27*b6^2 + 9*b2*b4*b6
sage: Di % p
0
```

Indeed, our curve has discriminant equal to zero (mod p).

This actually is a pretty good news since both the name of the challenge and the path forward are clearer now.

There is a reason why singular curves are not used for any cryptographic applications. Turns out that on these curves the group of non-singular points is isomorphic to other groups where DLP is easier.

I have used hints from [this great answer](https://crypto.stackexchange.com/questions/61302/how-to-solve-this-ecdlp) by Samuel Neves and recommended chapter 2 of an excellent book "Elliptic Curves: Number Theory and Cryptography".

Section 2.10 of the book deals with the case when the singularity point is at (0,0). We have to transform the coordinates to move our singularity point there. But first, we need to find it. 

A singular point has partial derivatives vanishing, so we first need to compute
```math
\frac{df}{dx} = 3x^2 + 2a_2x + a_4
```
and
```math
\frac{df}{dy} = 2y
```
Clearly, to have these two values equal to zero, we have $`y' = 0`$ but we also need to solve the quadratic equation $`3x^2 + 2a_2x + a_4 = 0`$. Let's compute the determinant:

```
sage: det = GF(p)(4*a2^2 - 4*3*a4)
sage: det
0
```

Nice, since $`\Delta=0`$, we have one solution
```math
x' = \frac{-2a_2}{2\cdot 3} = - \frac{a_2}{3} \enspace .
```

```
sage: xx = - GF(p)(a2)*GF(p)(3)^-1
sage: xx
413400541209677581972773119133520959089878607131
```



Let's see how the curve will look like after the translation $` (x,y) \to (x-x', y-0) `$.

```
sage: P.<x> = GF(p)[]
sage: f = x^3 + a2*x^2 + a4*x + a6
sage: f_ = f.subs(x = x+xx)
sage: f_
x^3
```

OK, so we have the case of $`y^2 = x^3`$. Singular point of this curve is at $`(0,0)`$ and if we leave it out as Section 2.10 of the book suggests, the rest of the points constitutes a group called $`E_{ns}(GF_p)`$ .

Now, the crucial result we will use is Theorem 2.30 from the book:

> Let $`E`$ be the curve $`y^2 = x^3`$ and let $`E_{ns}(K)`$ be the nonsingular points on this curve with coordinates in field K, including point at infinity $`\infty = (0:1:0)`$. The map
> ```math
> E_{ns}(K) \to K \quad (x,y)\mapsto \frac{x}{y}, \quad \infty\mapsto 0
> ```
> is a group isomorphism between $`E_{ns}(K)`$ and $`K`$ regarded as an additive group.

Great! So we can use this isomorphism to map points from $`E_{ns}`$ to elements of the group $`(GF_p, +)`$. Note that we talk about the **additive** group of the finite field and in this group discrete logarithm problem is easy  since it boils down to division (i.e. multiplication by the inverse element). This is because if we have
```math
q = g + g + g + \dots + g
```
we have
```math
q\cdot g^{-1} = 1 + 1 + \dots + 1
```
so slightly abusing the distinction between prime field elements and integers we can write $`dlog_g(q) = q\cdot g^{-1}`$.

our plan is to take both one of the public values of Alice (P) or Bob (Q) and compute its discrete log by transferring the problem via the above isomorphism. 

Let's transform the original points to the curve $`E_{ns}`$ first:

```
sage: G_ = (GF(p)(G[0] - xx), GF(p)(G[1]))
sage: P_ = (GF(p)(P[0] - xx), GF(p)(P[1]))
sage: Q_ = (GF(p)(Q[0] - xx), GF(p)(Q[1]))
```

and then map it to the group  $`(GP_p, +)`$ 

```
sage: mapG = G_[0]*(G_[1]^-1)
sage: mapP = P_[0]*(P_[1]^-1)
sage: mapQ = Q_[0]*(Q_[1]^-1)
```

Now we can compute the discrete logs (in fact one value would be enough, but we want to double check our computations)

```
sage: d1 = mapP*(mapG^-1)
sage: d1
733677047520440525642834723493438680490143125031
sage: d2 = mapQ*(mapG^-1)
sage: d2
763634997366397729521910551455953865027020672657
```



Once we have the discrete logarithms $`d_1`$ and $`d_2`$ we can compute the common point.

Since both Sagemath and Magma complain about working with singular curves, I tried GP/Pari hoping I won't need to implement point arithmetic myself.

```
? p = 785482254973602570424508065997142892171538672071
%1 = 785482254973602570424508065997142892171538672071
? a1 = Mod(0,p)
%2 = Mod(0, 785482254973602570424508065997142892171538672071)
? a3 = Mod(0,p)
%3 = Mod(0, 785482254973602570424508065997142892171538672071)
? a2 = Mod(330762886318172394930696774593722907073441522749,p)
%4 = Mod(330762886318172394930696774593722907073441522749, 785482254973602570424508065997142892171538672071)
? a4 = Mod(6688528763308432271990130594743714957884433976,p)
%5 = Mod(6688528763308432271990130594743714957884433976, 785482254973602570424508065997142892171538672071)
? a6 = Mod(759214505060964991648440027744756938681220132782,p)
%6 = Mod(759214505060964991648440027744756938681220132782, 785482254973602570424508065997142892171538672071)
? E = ellinit([a1,a2,a3,a4,a5])
%7 = [Mod(0, 785482254973602570424508065997142892171538672071), Mod(330762886318172394930696774593722907073441522749, 785482254973602570424508065997142892171538672071), Mod(0, 785482254973602570424508065997142892171538672071), Mod(6688528763308432271990130594743714957884433976, 785482254973602570424508065997142892171538672071), a5, Mod(537569290299087009298279032377748736122227418925, 785482254973602570424508065997142892171538672071), Mod(13377057526616864543980261189487429915768867952, 785482254973602570424508065997142892171538672071), 4*a5, Mod(537569290299087009298279032377748736122227418925, 785482254973602570424508065997142892171538672071)*a5 + Mod(312900959865375580233147003426906342366729916787, 785482254973602570424508065997142892171538672071), Mod(0, 785482254973602570424508065997142892171538672071), -864*a5 + Mod(83649469715606479787948863855680057339403544363, 785482254973602570424508065997142892171538672071), -432*a5^2 + Mod(83649469715606479787948863855680057339403544363, 785482254973602570424508065997142892171538672071)*a5 + Mod(632635017901057450618923677383624244296949916122, 785482254973602570424508065997142892171538672071), Mod(0, 785482254973602570424508065997142892171538672071), Vecsmall([0]), [Vecsmall([128, 0])], [0, 0, 0, 0]]

```

Looks like GP/Pari does not complain yet. 

Let's try to use it to compute our shared secret as $`d_1 \cdot Q`$  and $`d_2 \cdot P`$.

```
? P = [Mod(453762742842106273626661098428675073042272925939,p), Mod(680431771406393872682158079307720147623468587944,p)]
%11 = [Mod(453762742842106273626661098428675073042272925939, 785482254973602570424508065997142892171538672071), Mod(680431771406393872682158079307720147623468587944, 785482254973602570424508065997142892171538672071)]
? Q = [Mod(353016783569351064519522488538358652176885848450,p), Mod(287096710721721383077746502546881354857243084036,p)]
%12 = [Mod(353016783569351064519522488538358652176885848450, 785482254973602570424508065997142892171538672071), Mod(287096710721721383077746502546881354857243084036, 785482254973602570424508065997142892171538672071)]
? ellpow(E, P, 763634997366397729521910551455953865027020672657)
%13 = [Mod(165140565353247266256196454126511228757085857653, 785482254973602570424508065997142892171538672071), Mod(231669028154545692129434024805430410636820018050, 785482254973602570424508065997142892171538672071)]
? ellpow(E, Q, 733677047520440525642834723493438680490143125031)
%14 = [Mod(165140565353247266256196454126511228757085857653, 785482254973602570424508065997142892171538672071), Mod(231669028154545692129434024805430410636820018050, 785482254973602570424508065997142892171538672071)]
```

Hurray! In both cases we get the same point $`(165140565353247266256196454126511228757085857653, 231669028154545692129434024805430410636820018050)`$ so we can hope this is our right solution. 

Taking the $`x`$ coordinate and using it to derive the symmetric decryption using the script

```python

from hashlib import sha256
from Crypto.Cipher import AES
from binascii import *

xcoord = '165140565353247266256196454126511228757085857653'
ciphertext = unhexlify('480fd106c9a637d22fddd814965742236eb314c1b8fb68e70a7c7445ff04476082f8b9026c49d27110ba41b95e9f51dc')

key = sha256(xcoord).digest()
cipher = AES.new(key, AES.MODE_ECB)
plain = cipher.decrypt(ciphertext)
print(plain)
```

we get some garbage characters and the flag

```
hackim19{w0ah_math_i5_quite_fun_a57f8e21}
```

It was a very good challenge, I enjoyed it a lot.