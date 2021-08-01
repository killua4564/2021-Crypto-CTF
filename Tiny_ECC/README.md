## Tiny ECC - medium (unsolved)

* 看一陣子還沒懂的 [writeup](https://github.com/r00tstici/writeups/tree/master/cryptoCTF_2021/tiny_ecc#deal-with-singular-curve)
* 題目
    * 要求輸入 ECC 的 `a, b, p`，其中 p 要求是強質數
    * 用 `(a, b, p)` 和 `(a, b, 2p+1)` 生出 ECC `Ep, Eq`
    * 並在對應的 GF 下產兩個隨機點 `P, Q`，給定 `kP, lQ` 問 DLP `(k, l)`
* 想法
    * 找到 p 後讓 `a = b = p * (2p+1)`，因為 `a * b != 0`
    * 這樣兩個 curve 都是 `y^2 = x^3` 就會變成 `singular curve`
    * 然後如果 `|ECC(Fq)| = q`，則可以把 curve 上的點 mapping 到對應的 `GF(q)`
    * `y^2 = x^3` 對應的 mapping 方程是 `x/y` [ref](./Singular.md)
    * 所以只要做 `map(kP)/map(P)` 和 `map(lQ)/map(Q)` 就可以輕鬆解出 `(k, l)` 了
* `CCTF{ECC_With_Special_Prime5}`
