from pwn import remote
from Crypto.Util.number import *

conn = remote("07.cr.yp.toc.tf", "10101", level="error")

"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+   hi all, all cryptographers know that fast calculation is not easy! +
+   In each stage for given integer m, find number n such that:        +
+   carmichael_lambda(n) = m, e.g. carmichael_lambda(2021) = 966       +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
| send an integer n such that carmichael_lambda(n) = 88: 
 89
| good job, try to solve the next challenge :P
"""

conn.recvuntil(b"|")

def inv_lambda(n):
    for x in divisors(n):
        for y in divisors(n):
            if lcm(x, y) == n and isPrime(x+1) and isPrime(y+1):
                return (x+1)*(y+1)

try:
    while True:
        conn.recvuntil(b" = ")
        n = int(conn.recvuntil(b":").decode().strip(":"))
        conn.sendline(str(inv_lambda(n)).encode())
except EOFError:
    conn.interactive()
