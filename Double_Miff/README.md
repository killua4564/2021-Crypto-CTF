## Double Miff - medium-hard (unsolved)

* 題目說 flag 是 `P`, `Q` 點的 `x` 座標
* `(a, b)` 沒有給，並給定判別式
```python
(a * x * (y**2 - 1) - b * y * (x**2 - 1)) % p == 0
```
* 並且提供兩點相加的公式
```python
x_3 = (x_1 + x_2) * (1 + y_1*y_2) * inverse((1 + x_1*x_2) * (1 - y_1*y_2), p) % p
y_3 = (y_1 + y_2) * (1 + x_1*x_2) * inverse((1 + y_1*y_2) * (1 - x_1*x_2), p) % p
return (x_3, y_3)    
```
* 最後給你三個點 `(P+P, Q+Q, P+Q)`
* 因為 `(P+P)+(Q+Q)=(P+Q)+(P+Q)`，可以用兩種加法算出來的座標值相減取 `gcd` 得到 `p`
* 定義一個 `k` 把 `(a, b)` 比例弄出來
```
a * x * (y**2 - 1) = b * y * (x**2 - 1) mod p
=> k = a/b = y(x^2-1)/x(y^2-1) mod p
=> k * x/(x^2-1) = y/(y^2-1) mod p
```
* 開始對 flag 下手，假設 `(P, Q)` 的值
    * `P+P` 可以表示為
    ```
    pp.x = 2 * p.x * (1 + p.y^2) / (1 + p.x^2) * (1 - p.y^2) mod p
    pp.y = 2 * p.y * (1 + p.x^2) / (1 + p.y^2) * (1 - p.x^2) mod p
    ```
    * 把兩點相乘消掉，帶入 `k` 的等式
    ```
    pp.x * pp.y mod p
    => 4 * p.x * p.y / (1 - p.x^2) * (1 - p.y^2) mod p
    => 4k * (p.x / (p.x^2 - 1))^2 mod p
    => ((p.x^2 - 1) / p.x) ^ 2 = 4k / pp.x * pp.y mod p
    ```
    * 要來開模方了，驗證 `p mod 4 = 3`，則
    ```
    (p.x^2 - 1) / p.x = (4k / pp.x * pp.y) ^ ((p+1)/4) mod p
    ```
    * 令結果為 `l`，那可以用一元二次方程求解
    ```
    l = (p.x^2 - 1) / p.x mod p
    => p.x^2 [+/-] l * p.x - 1 = 0 mod p
    => p.x = [+/-] l [+/-] sqrt(l**2 + 4) / 2 mod p
    ```
    * 對 `Q+Q` 做一樣的事情就好
* `CCTF{D39enEr47E_ECC_4TtaCk!_iN_Huffs?}`