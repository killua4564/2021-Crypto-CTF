## Onlude - medium

* 線性代數期末考題 (x
* 把 flag 轉成 matrix 我們就不多提，反正求出 A 就對了
* 題目
```
R, S = random_matrix
S = L * U

E = L^(-1) * S * (A + R)
a = L * U * L
b = L^(-1) * S^2 * L
c = R^(-1) * S^8
```
* 過程
```
b * a^(-1) = L^(-1) * S  (S = L * U = U * L)
a * b^(-1) * E = A + R   (上式^(-1) * E)

a * b * a^(-1) = S^2     (define ss)
c * ss^(-4) = R^(-1)

a * b^(-1) * E - c * ss^(-4) = A  (solve)
```
* `CCTF{LU__D3c0mpO517Ion__4L90?}`
