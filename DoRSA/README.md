## DoRSA - hard (unsolved)

* 從題目可知
```
n1 = p * r
n2 = q * s

p = u * v + 1
q = u * y + 1
r = x * y + 1
s = k * v + 1  (k = e * d // phi)
```
* `(n1, n2)` 非常相近，所以考慮 `Wiener Attack`
```
n2   q * s   (u * y + 1)(k * v + 1)   u * y * k * v   k
-- = ----- = ---------------------- ≈ ------------- = -
n1   p * r   (u * v + 1)(x * y + 1)   u * y * x * v   x
```
* 相除丟進 `sage` 內建的 `continued_fraction` 拿分子分母
```python
cf = continued_fraction(n2 / n1)

for idx in range(1, len(cf)):
    k = cf.numerator(idx)
    x = cf.denominator(idx)
```
* 那只要用 `(k, x)` 想辦法求出來 `phi` 就結束了
    * 把 `k` 用上
    ```
    e * d = 1 mod phi
    => e * d = k * phi + 1
    => k * phi + 1 = 0 mod e
    => phi = -1/k mod e
    ```
    * 把 `x` 用上
    ```
    n = (u * v + 1) * (x * y + 1)
    => phi = u * v * x * y
    => phi = 0 mod x
    ```
    * 最後來個約束條件
    ```
    |n1 - phi| = |p * r - (p-1) * (r-1)| = p + r - 1 <= 2^513
    ```
* 用 `CRT` 把 `phi` 擠出來
```python
phi = crt(inverse_mod(-k, e), 0, e, x)
# phi % e = inverse_mod(-k, e)
# phi % x = 0
lcm = e * x // GCD(e, x)
    phi += (n1 - phi - 2**513) // lcm * lcm
    while phi < n1:
        phi += lcm
        if GCD(e, phi) > 1:
            continue
```
* 之後算出 `d` 用 `(n1, enc1)` 把 flag 還原就好
* `CCTF{__Lattice-Based_atT4cK_on_RSA_V4R1aN75!!!}`
