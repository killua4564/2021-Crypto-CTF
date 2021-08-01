from pwn import remote
from Crypto.Util.number import *


conn = remote("07.cr.yp.toc.tf", "31010")


def params():
    conn.sendlineafter("[Q]uit", "e")
    conn.recvuntil(" = ")
    p = int(conn.recvuntil("\n").decode().strip("\n"))
    conn.recvuntil(" = ")
    u = int(conn.recvuntil("\n").decode().strip("\n"))
    conn.recvuntil(" = ")
    v = int(conn.recvuntil("\n").decode().strip("\n"))
    conn.recvuntil(" = ")
    w = int(conn.recvuntil("\n").decode().strip("\n"))
    return (p, u, v, w)

def enc_flag():
    conn.sendlineafter("[Q]uit", "s")
    conn.recvuntil(" = ")
    return list(map(int, conn.recvuntil("\n").decode().strip("\n").split(", ")))

def encrypt(m):
    conn.sendlineafter("[Q]uit", "t")
    conn.sendlineafter(": ", long_to_bytes(m))
    conn.recvuntil(" = ")
    return list(map(int, conn.recvuntil("\n").decode().strip("\n").split(", ")))

'''
w = pow(u, x, p)
v = pow(u, r1, p) 
---
ca = pow(u, r2, p)
cb = pow(v, s, p) = pow(u, r1 * s, p)
cc = m * pow(w, r2+s, p) = m * pow(u, x * r2, p) * pow(u, x * s, p)
---
decrypt
cc * pow(ca, -x, p) * pow(cb, x / r1, p) % p
'''

p, u, v, w = params()
ca, cb, cc = enc_flag()

Z = Zmod(p) # p-1 smooth

r = discrete_log(Z(ca), Z(u))
s = discrete_log(Z(cb), Z(v))
flag = Z(cc) / (Z(w) ** (r + s))
print(long_to_bytes(flag).decode())

x = discrete_log(Z(w), Z(u))
r1 = discrete_log(Z(v), Z(u))
flag = Z(cc) / Z(ca) ** x / Z(cb) ** (x * inverse_mod(r1, p-1))
print(long_to_bytes(flag).decode())
