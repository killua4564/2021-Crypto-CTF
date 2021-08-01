## Maid - medium (unsolved)

* 兩個質數 `p mod 4 = 3`，`pubkey = p ** 2 * q, privkey = p`
* 加密是 `pow(m, 2, pubkey)`
* 解密沒有給，但感覺就跟 `pow(c, (p+1)/4, p)` 脫不了關係
* flag 加密是正常的 RSA，所以還是要把 `(p, q)` leak 出來
* 可以任意的加解密，所以構造
```python
pubkey = gcd(m**2 - encrypt(m))
privkey = gcd(decrypt(c)**2 - c)
```
* 兩者一樣意思但解出來東西不同
* 後來官方賽後給的解密函數
```python
def decrypt(c, privkey):
    m_p = pow(c, (privkey + 1) // 4, privkey)
    i = (c - pow(m_p, 2)) // privkey
    j = i * inverse(2*m_p, privkey) % privkey
    m = m_p + j * privkey
    if 2*m < privkey**2:
        return m
    else:
        return privkey**2 - m
```
* 才發現 `decrypt` 那邊要避免 `c` 本身的次方項為偶數
* 然後解出來的不是 `p` 而是 `p**2`
* `CCTF{___Ra8!N_H_Cryp70_5YsT3M___} `
