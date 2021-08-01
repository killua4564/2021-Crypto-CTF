from math import gcd
from pwn import remote
from functools import reduce
from Crypto.Util.number import *
from factordb.factordb import FactorDB


conn = remote("07.cr.yp.toc.tf", "18010")

def get_prime(nbit=160):
    k = 1
    start = 1 << nbit
    result = []
    while True:
        if isPrime(k * start + 1):
            result.append(k * start + 1)
            if len(result) == 3:
                return result
        k += 1

def lcm(a, b):
    return a * b // gcd(a, b)

p, q, r = get_prime()
phi1, phi2, phi3 = (p-1)*(q-1), (p-1)*(r-1), (q-1)*(r-1)

factor = FactorDB(lcm(lcm(phi1, phi2), phi3) + 1)
factor.connect()
*e, d = factor.get_factor_list()
e = reduce(lambda x, y: x * y, e)

conn.recvuntil("[Q]uit")
conn.sendline("s")
conn.recvuntil(": ")
conn.sendline(f"{p},{q}")
conn.recvuntil(": ")
conn.sendline(f"{p},{r}")
conn.recvuntil(": ")
conn.sendline(f"{q},{r}")
conn.recvuntil(": ")
conn.sendline(f"{e},{d}")
conn.recvuntil("\n")

conn.recvuntil(": ")
print(conn.recvuntil("\n").decode().strip("\n"))
