import string
from pwn import remote
from functools import reduce


conn = remote("01.cr.yp.toc.tf", "27010")

xor = lambda *args: bytes(reduce(lambda x, y: x ^ y, items) for items in zip(*args))

def enc_flag():
    conn.recvuntil("[Q]uit")
    conn.sendline("g")
    conn.recvuntil(" = ")
    return bytes.fromhex(conn.recvuntil("\n").decode().strip("\n"))

def enc(pt):
    conn.recvuntil("[Q]uit")
    conn.sendline("t")
    conn.recvuntil(": ")
    conn.sendline(pt)
    conn.recvuntil(" = ")
    return bytes.fromhex(conn.recvuntil("\n").decode().strip("\n"))


pt = "A" * (15 + 16 * 4)
enc_list = []
for _ in range(100):
    r = xor(enc(pt)[16:], ("\n"+pt).encode())
    for idx in range(0, len(r), 16):
        enc_list.append(r[idx:idx+16])
print("Get Encs")

flag = ""
flag_enc = enc_flag()
for idx in range(0, len(flag_enc), 16):
    enc_t = flag_enc[idx:idx+16]
    for enc in enc_list:
        flag_t = xor(enc, enc_t)
        if all(c in string.printable.encode() for c in flag_t):
            flag += flag_t.decode().strip("\n")
            print(flag)
            break
print(flag)
