## Hyper Normal - medium-easy

* 一直誤會題目意思的水題QQ
* 他先把 flag 乘上 hyper 係數之後每個字分到相應不同的 list
* 然後把每個 list 乘上不同的 seed
* 最後再把每個 list 相對應的位置加總起來
* 所以有沒有分 list 其實一點都不重要
* 最後面的 `random.shuffle(transpose(W))` 也只是幌子
* transpose 是重新指派一個 list in list 跟原本 W 的 addr 根本沒關
``` python
def encrypt(msg):
    l = len(msg)
    hyper = [ord(m)*(i+1) for (m, i) in zip(list(msg), range(l))]
    V, W = [], []
    for i in range(l):
        v = [0]*i + [hyper[i]] + [0]*(l - i - 1)
        V.append(v)
    random.shuffle(V)
    for _ in range(l):
        R, v = [random.randint(0, 126) for _ in range(l)], [0]*l
        for j in range(l):
            v = vsum(v, sprod(R[j], V[j]))
        W.append(v)
    random.shuffle(transpose(W))
    return W
```
* 所以只要每個字遍例 string.printable 然後反算回來每個 case 的 seed 都是合理的，機率上來說都只會有唯一值
* O(100n) 很快就有答案
* `CCTF{H0w_f1Nd_th3_4lL_3I9EnV4Lu35_iN_FiN173_Fi3lD5!???}`
