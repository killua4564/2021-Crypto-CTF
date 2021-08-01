## Triplet - medium (unsolved)

* 題目要求輸入三對不同的 (p, q) 和一對 (e, d)
* 然後要 e * d 分別模三對的 phi 皆等於 1
* 那構造 e * d = lcm(phi1, phi2, phi3) + 1 即可
* 所以先算出來 e * d 後丟入 factordb 分成 e, d (比賽時沒想到這步)
* 但這樣有個前提是 e * d 是要可分解的，所以選質數方面使用梅森質數(p=2^k+1)會比較快且方便
* `CCTF{7HrE3_b4Bie5_c4rRi3d_dUr1nG_0Ne_pr39naNcY_Ar3_triplets}`
