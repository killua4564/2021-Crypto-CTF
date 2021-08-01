## Hamul - medium-easy (unsolved)

* 參考 maple3142 大大寫的 [writeup](https://blog.maple3142.net/2021/08/01/cryptoctf-2021-writeups/)
* 首先依據題目可以推出 `p, q` 長度落在 `19 ~ 20`，所以
```
P = p * 10^q_len + q
Q = q * 10^p_len + q
PP = P * 10^Q_len + Q
QQ = Q * 10^P_len + P
```
* 所以最後會化成一個 `f(p, q)` 的多項式
* 那依照 n 去生成 `Zmod` 再用 `coppersmith` 解出 `small_roots` 即可
* 因為 sage 的 `small_roots` 不支援 `Multivariate Polynomial Ring`
* 所以其中使用了這個擴展 [small_roots](https://github.com/defund/coppersmith/blob/master/coppersmith.sage)
* 問過大大裡面的參數 m, d 全靠經驗，我也是慢慢試才試出來的
* `CCTF{wH3Re_0Ur_Br41N_Iz_5uP3R_4CtIVe_bY_RSA!!}`
