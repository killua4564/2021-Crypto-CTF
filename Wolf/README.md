## Wolf

* AES.MODE_GCM 沒使用 auth 部分，所以是 AES.MODE_CTR
* CTR: `ciphertext = enc(counter + nonce, key) xor plaintext`
* 所以只要拿夠多的 `enc(counter + nonce, key)` 就可以湊出 flag
* 題目隨意加密的地方會放 `length = 17` 的 `msg_header` 來擾民，所以在算 `enc_list` 的時候要把 plaintext 前面加上 `\n`
* `CCTF{____w0lveS____c4n____be____dan9er0uS____t0____p3oplE____!!!!!!}`
