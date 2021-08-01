from pwn import remote
from Crypto.Util.number import *

conn = remote("01.cr.yp.toc.tf", "29010")

p = 286838999562166707375553799215992552311
a = b = p * (2 * p + 1)

conn.recvuntil("[Q]uit")
conn.sendline("c")
conn.recvuntil(": ")
conn.sendline(f"{p}")

conn.recvuntil("[Q]uit")
conn.sendline("a")
conn.recvuntil(": ")
conn.sendline(f"{a},{b}")

conn.recvuntil("[Q]uit")
conn.sendline("s")
conn.recvuntil(": ")
conn.recvuntil("(")
P = list(map(int, conn.recvuntil(")").decode().strip(")").split(",")))
conn.recvuntil("(")
kP = list(map(int, conn.recvuntil(")").decode().strip(")").split(",")))
conn.recvuntil("(")
Q = list(map(int, conn.recvuntil(")").decode().strip(")").split(",")))
conn.recvuntil("(")
lQ = list(map(int, conn.recvuntil(")").decode().strip(")").split(",")))

map_p = P[0] * inverse(P[1], p) % p
map_kp = kP[0] * inverse(kP[1], p) % p

map_q = Q[0] * inverse(Q[1], 2 * p + 1) % (2 * p + 1)
map_lq = lQ[0] * inverse(lQ[1], 2 * p + 1) % (2 * p + 1)

k = map_kp * inverse(map_p, p) % p
l = map_lq * inverse(map_q, 2 * p + 1) % (2 * p + 1)

conn.recvuntil(": ")
conn.sendline(f"{k},{l}")

conn.recvuntil(": ")
print(conn.recvuntil("\n").decode().strip("\n"))
