## RSAphantine - medium-hard (unsolved)

* 題目給你
```python
a = 2*z**5 - x**3 + y*z
b = x**4 + y**5 + x*y*z
c = y**6 + 2*z**5 + z*y

p = nextPrime(x**2 + z**2 + y**2 << 76)
q = nextPrime(z**2 + y**3 - y*x*z ^ 67)
```
* 把 `c-a` 之後只剩下 `x**3 + y**6` 可以分解成 `(x + y**2)(x**2 - x*y**2 + y**4)` (比賽的時候看很久居然忘記要拆項==)
* 於是把 `c-a` 丟 `factordb` 因數分解後用 `sage` 的 `solve` 把 `(x, y, z)` 還原回來，進而產出 `(p, q)` 就結束了
```python
x = var("x")
assume(x, "integer")
sol = solve(x^2 - x*(ca1-x) + (ca1-x)**2 == ca2, x)
```
* p.s. 記得在 `sage` 裡面要把 `python` 的 `xor` 換成 `^^`
* `CCTF{y0Ur_jO8_C4l13D_Diophantine_An4LySI5!}`