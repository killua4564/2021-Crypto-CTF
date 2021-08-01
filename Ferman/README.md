## Ferman - medium (unsolved)

* 比賽的時候我好像想太多了，直接丟 sage 去 solve 就有解了
* 看到有 [writeup](https://blog.maple3142.net/2021/08/01/cryptoctf-2021-writeups/) 用 [Brahmagupta–Fibonacci identity](https://en.wikipedia.org/wiki/Brahmagupta%E2%80%93Fibonacci_identity) 解，以後有機會可以應用一下
```python
p, q = var("p, q")
assume(p, "integer")
assume(q, "integer")
sol = solve((p - 1003) ** 2 + (q - 48) ** 2 == k, p, q)

for p, q in sol:
    if p > 0 and q > 0:
        p, q = int(p), int(q)
        if isPrime(p) and isPrime(q):
            d = inverse_mod(0x10001, (p-1)*(q-1))
            print(long_to_bytes(pow(c, d, p*q)).decode())
```
* `CCTF{Congrats_Y0u_5OLv3d_x**2+y**2=z**7}`