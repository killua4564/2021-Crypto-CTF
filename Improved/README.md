## Improved - medium

* 總感覺這個解法是非預期解
* 題目要你輸入兩個在特定位數以上且不同 m 讓 sig 算出來相同
``` python
def improved(m, params):
    n, f, v = params
    if 1 < m < n**2 - 1:
        e = pow(m, f, n**2)
        u = divmod(e-1, n)[0]
        L = divmod(u*v, n)[1]
    H = hashlib.sha1(str(L).encode('utf-8')).hexdigest()
    return H
```
* 想法是讓不同的 m 有同樣的 e，事情就解決了
* 他是 `pow(m, phi(n), n**2)`，且 `phi(n**2) = n * phi(n)`
* 那我讓 m 的次方項塞入包含 n 的因子就完事了
* 所以送入 `pow(2, n, n**2)` 和 `pow(2, 2*n, n**2)`
* `CCTF{Phillip_N0W_4_pr0b4b1liStiC__aSymM3Tr1C__AlGOrithM!!}`
