## Salt and Pepper - medium

* 不知道為什麼是解最開心的一題
* 題目給你
    * `USERNAME = b'n3T4Dm1n'`
    * `PASSWORD = b'P4s5W0rd'`
    * `md5(salt).hexdigest() = '5f72c4360a2287bc269e0ccba6fc24ba'`
    * `sha1(pepper).hexdigest() = '3e0d000a4b0bd712999d730bc331f400221008e0'`
    * `len(salt) = len(pepper) = 19`
* 要求輸入 username, password, sig 滿足
    * `USERNAME in username`
    * `PASSWORD in password`
    * `sig = sha1(pepper + password + md5(salt + username).hexdigest()).hexdigest()`
* 自己手作 LEA 蠻輕鬆就過了
* hash 的 python 實作可以參考[這邊](https://github.com/killua4564/SHA-family)

|         | salt | salt_padding | salt_length | USERNAME | padding | length |
| ------- | ---- | ------------ | ----------- | -------- | ------- | ------ |
| Length  |  19  |      37      |      8      |     8    |    48   |    8   |

* chunk 1 = salt + salt_padding + salt_length
* chunk 2 = USERNAME + padding + length
* 題目給的 salt hash 是用 chuck 1(salt_length = 8 * 19) 下去算的
* 所以要在不影響 salt hash 的情況下去串接 USERNAME
    * `username = salt_padding + salt_length + USERNAME)` (salt_length = 8 * 19)
    * 把 salt hash 解開帶回去 md5 main function (h0 ~ h3) 繼續算 chuck 2
    * 且此時的 length 要帶 8 * 72 進去算，然後記得 md5 的 byteorder 是 big 就是

|         | pepper | pepper_padding | pepper_length | PASSWORD | md5_sig | padding | length |
| ------- | ------ | -------------- | ------------- | -------- | ------- | ------- | ------ |
| Length  |   19   |       37       |       8       |     8    |    32   |    16   |    8   |

* chunk 1 = pepper + pepper_padding + pepper_length
* chuck 2 = PASSWORD + md5_sig + padding + length
* 一樣題目給的 pepper hash 是用 chuck 1(pepper_length = 8 * 19) 下去算的
* 所以要在不影響 pepper hash 的情況下去串接 PASSWORD
    * `password = pepper_padding + pepper_length + PASSWORD` (pepper_length = 8 * 19)
    * 把 pepper hash 解開帶回去 sha1 main function (h0 ~ h4) 繼續算 chuck 2
    * 且此時的 length 要帶 8 * 104 進去算，然後記得 w 這個 list 也要跟著 chuck 2 再算一次就是

* 最後 pepper 那邊算出來的 hash 就可以當 sig 帶進去題目了
* `CCTF{Hunters_Killed_82%_More_Wolves_Than_Quota_Allowed_in_Wisconsin}`
