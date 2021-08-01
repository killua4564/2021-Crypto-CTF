## Keybase - easy

* AES.CBC_MODE
* 給你任意輸入 32 bytes 加密的機會，然後回傳
    * 沒有後面兩個 bytes 的 key 
    * 第一個 block 幾乎都 mask 的 enc
* 那想辦法知道明文和對應的密文，就可以自己用 ECB 去暴力破解 key O(256^2)
* 礙於 iv 是未知的情況下，送入 `\x00 * 32` 可以不影響 iv 每次的迭代加密
* 這樣就可以試 decrypt(block 2, key).startswith(block 1 head)
* 測出來機率上就是原本得 key 了，也能順便還原 block 1
* 此時 `iv = decrypt(block 1, key)`
* 開心算回 flag 吧
* `CCTF{h0W_R3cOVER_7He_5eCrET_1V?}`