## Frozen - mediumn-hard

* 先用 random 的 p, r 生成 U，用尾 32 bits 做成 priv 剩下是 pub
* 把 msg 切成四等份然後對應 priv 相乘模 q 算成 sig
* 那用題目的 example 可以算回 priv，但 q 的選用有可能會小於 priv
* 所以要用 parmas 和 pub 把每個 priv 算回 s 來校正
* 個人覺得沒有中難等級

* `CCTF{Lattice_bA5eD_T3cHn1QuE_70_Br34K_LCG!!}`
