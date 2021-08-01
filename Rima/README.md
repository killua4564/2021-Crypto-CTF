## Rima - medium-easy (first kill)

* 浪費記憶體的水題
* 把 flag 轉成 bin 然後變成 list
* 做位移加法後依照長度找下一個質數和下下個質數 a 和 b
* 把整個 f 擴張 a 倍和 b 倍變成 g 和 h
* 再依照 len(f) // 4 選下一個質數 c
* 把 g, h 長度加上 c 之後再做位移加總
* 輸出五進制的 g 和 h

* 從 output 拿回來之後暴力破解 c，並符合條件
    * len(g) - c 和 len(h) - c 不是互質，為 f
    * f * next_prime(f) = len(g) - c
    * c = next_prime(f >> 2)

* `CCTF{_how_finD_7h1s_1z_s3cr3T?!}`
