from Crypto.Util.number import long_to_bytes, inverse
from functools import reduce
from gmpy2 import gcd, isqrt
from pwn import remote


conn = remote("04.cr.yp.toc.tf", "38010")


def encrypt(m):
    conn.recvuntil("[Q]uit")
    conn.sendline("e")
    conn.recvuntil(": ")
    conn.sendline(str(m))
    conn.recvuntil(" = ")
    return int(conn.recvuntil("\n").decode().strip("\n"))

def decrypt(c):
    conn.recvuntil("[Q]uit")
    conn.sendline("d")
    conn.recvuntil(": ")
    conn.sendline(str(c))
    conn.recvuntil(" = ")
    return int(conn.recvuntil("\n").decode().strip("\n"))

def enc_flag():
    conn.recvuntil("[Q]uit")
    conn.sendline("s")
    conn.recvuntil(" = ")
    return int(conn.recvuntil("\n").decode().strip("\n"))

'''
p % 4 = q % 4 = 3
m ** 2 % p**2*q = c

c ** (p+1)/4 % p
=> m ** (p+1)/2 % p**2*q % p
=> m ** (2/2) % p
=> m

p**2*q = gcd(m ** 2 - encrypt(m))
p = gcd(decrypt(c)**2 - c)
'''

pubkey = reduce(gcd, ((2**i)**2 - encrypt(2**i) for i in range(2000, 2004)))
privkey = reduce(gcd, (decrypt(2**i)**2 - 2**i for i in range(1991, 2015, 2)))

assert pubkey > 1 and privkey > 1
assert isqrt(privkey) ** 2 == privkey

p = isqrt(privkey)
q = pubkey // (p**2)
assert p ** 2 * q == pubkey

d = inverse(0x10001, (p-1)*(q-1))
print(long_to_bytes(pow(enc_flag(), d, p*q)).decode())
