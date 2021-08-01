from pwn import remote
from gmpy2 import next_prime
from Crypto.Util.number import *


conn = remote("03.cr.yp.toc.tf", "25010")

def get_params():
    conn.recvuntil("[Q]uit")
    conn.sendline("s")
    conn.recvuntil(" = ")
    p = int(conn.recvuntil("\n").decode())
    conn.recvuntil(" = ")
    r = int(conn.recvuntil("\n").decode())
    return (p, r)

def get_public():
    conn.recvuntil("[Q]uit")
    conn.sendline("p")
    conn.recvuntil("[")
    return list(map(int, conn.recvuntil("]").decode().strip("]").split(", ")))

def get_example():
    conn.recvuntil("[Q]uit")
    conn.sendline("e")
    conn.recvuntil("\"")
    randstr = conn.recvuntil("\"").decode().strip("\"")
    conn.recvuntil("[")
    return randstr, list(map(int, conn.recvuntil("]").decode().strip("]").split(", ")))

p, r = get_params()
pubkey = get_public()
randstr, sign = get_example()
M = [
    bytes_to_long(randstr[4*i:4*(i+1)].encode())
    for i in range(len(randstr) // 4)
]
q = int(next_prime(max(M)))
privkey = [sig * inverse(m, q) % q for m, sig in zip(M, sign)]
inv_r = inverse(r, p)
s_list = (
    (pubkey[0] + privkey[0]) * inv_r % p,
    (pubkey[0] + privkey[0] + q) * inv_r % p
)
key = True
for idx in range(1, len(privkey)):
    ts = (pubkey[idx] + privkey[idx]) * pow(inv_r, idx+1, p) % p
    if ts not in s_list:
        privkey[idx] += q
    elif key:
        key = False
        if ts == s_list[1]:
            privkey[0] += q

conn.recvuntil("[Q]uit")
conn.sendline("f")
conn.recvuntil(": ")

randmsg = conn.recvuntil("\n").decode().strip("\n")
MM = [
    bytes_to_long(randmsg[4*i:4*(i+1)].encode())
    for i in range(len(randmsg) // 4)
]
qq = int(next_prime(max(MM)))

conn.sendline(",".join(
    map(str, (mm * priv % qq for mm, priv in zip(MM, privkey)))
))
conn.recvuntil("'")
print(conn.recvuntil("'").decode().strip("'"))
