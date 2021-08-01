from Crypto.Util.number import *
from gmpy2 import gcd


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

pp = Point(5565164868721370436896101492497307801898270333, 496921328106062528508026412328171886461223562143)
pq = Point(540660810777215925744546848899656347269220877882, 102385886258464739091823423239617164469644309399)
qq = Point(814107817937473043563607662608397956822280643025, 961531436304505096581595159128436662629537620355)

'''
R = pp + qq = pq + pq
R.x = (pp.x + qq.x) * (1 + pp.y * qq.y) / (1 + pp.x * qq.x) * (1 - pp.y * qq.y) mod p
R.x = (pq.x + pq.x) * (1 + pq.y * pq.y) / (1 + pq.x * pq.x) * (1 - pq.y * pq.y) mod p
R.y = (pp.y + qq.y) * (1 + pp.x * qq.x) / (1 + pp.y * qq.y) * (1 - pp.x * qq.x) mod p
R.y = (pq.y + pq.y) * (1 + pq.x * pq.x) / (1 + pq.y * pq.y) * (1 - pq.x * pq.x) mod p
'''

rx1 = (pp.x + qq.x) * (1 + pp.y * qq.y) * (1 + pq.x * pq.x) * (1 - pq.y * pq.y)
rx2 = (pq.x + pq.x) * (1 + pq.y * pq.y) * (1 + pp.x * qq.x) * (1 - pp.y * qq.y)
ry1 = (pp.y + qq.y) * (1 + pp.x * qq.x) * (1 + pq.y * pq.y) * (1 - pq.x * pq.x)
ry2 = (pq.y + pq.y) * (1 + pq.x * pq.x) * (1 + pp.y * qq.y) * (1 - pp.x * qq.x)
 
k = 2
p = gcd(rx1 - rx2, ry1 - ry2)
while not isPrime(p):
    if p % k == 0:
        p //= k
    else:
        k += 1

'''
k = a/b = y(x^2-1)/x(y^2-1) mod p
kx/(x^2-1) = y/(y^2-1) mod p
'''
k = pq.y * (pq.x ** 2 - 1) * inverse(pq.x * (pq.y ** 2 - 1), p) % p

'''
pp.x = 2 * p.x * (1 + p.y^2) / (1 + p.x^2) * (1 - p.y^2) mod p
pp.y = 2 * p.y * (1 + p.x^2) / (1 + p.y^2) * (1 - p.x^2) mod p

pp.x * pp.y mod p
=> 4 * p.x * p.y / (1 - p.x^2) * (1 - p.y^2) mod p
=> 4k * (p.x / (p.x^2 - 1))^2 mod p

((p.x^2 - 1) / p.x) ^ 2 = 4k / pp.x * pp.y mod p

p mod 4 = 3
=> (p.x^2 - 1) / p.x = (4k / pp.x * pp.y) ^ ((p+1)/4) mod p

l = (p.x^2 - 1) / p.x mod p
=> p.x^2 [+/-] l * p.x - 1 = 0 mod p
=> p.x = [+/-] l [+/-] sqrt(l**2 + 4) / 2 mod p

same as q.x
'''

assert p % 4 == 3

def half_flag(point):
    l = pow(4 * k * inverse(point.x * point.y, p), (p + 1) // 4, p)
    D = pow(l ** 2 + 4, (p + 1) // 4, p)
    for b in (l, -l):
        for d in (D, -D):
            flag = long_to_bytes((b + d) * inverse(2, p) % p)
            if flag.startswith(b"CCTF{") or flag.endswith(b"}"):
                return flag.decode()
    return None

print(half_flag(pp) + half_flag(qq))
