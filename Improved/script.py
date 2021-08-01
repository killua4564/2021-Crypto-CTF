from pwn import remote

conn = remote("05.cr.yp.toc.tf", "14010")

def params():
    conn.recvuntil("[Q]uit")
    conn.sendline("g")
    conn.recvuntil("(")
    return conn.recvuntil(")").decode().strip(")").split(",")

def report(a, b):
    conn.recvuntil("[Q]uit")
    conn.sendline("r")
    conn.recvuntil(": ")
    conn.sendline(f"{a},{b}")
    conn.recvuntil(": ")
    print(conn.recvuntil("\n").decode().strip("\n"))

n, f, v = list(map(int, params()))
report(pow(2, n, n**2), pow(2, 2*n, n**2))
