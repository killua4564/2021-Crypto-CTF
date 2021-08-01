from pwn import remote

username = b'n3T4Dm1n'
password = b'P4s5W0rd'

salt_padding = b'\x80' + b'\x00' * 36 + (19 * 8).to_bytes(8, byteorder='little')
pepper_padding = b'\x80' + b'\x00' * 36 + (19 * 8).to_bytes(8, byteorder='big')
left_rotate = lambda n, b: ((n << b) | (n >> (32 - b))) & 0xffffffff

def salt_sig(sig="5f72c4360a2287bc269e0ccba6fc24ba"):
    k = [
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
        0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
        0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
    ]

    r = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
    ]

    sig = bytes.fromhex(sig)
    h0, h1, h2, h3 = (int.from_bytes(sig[idx:idx+4], byteorder='little') for idx in range(0, 16, 4))
    chunk = username + b'\x80' + b'\x00' * 47 + (72 * 8).to_bytes(8, byteorder='little')
    w = [int.from_bytes(chunk[i:i+4], byteorder='little') for i in range(0, len(chunk), 4)]
    a, b, c, d = h0, h1, h2, h3
    for i in range(64):
        if 0 <= i <= 15:
            f = (b & c) | (~b & d)
            g = i
        elif 16 <= i <= 31:
            f = (b & d) | (c & ~d)
            g = (5 * i + 1) % 16
        elif 32 <= i <= 47:
            f = b ^ c ^ d
            g = (3 * i + 5) % 16
        elif 48 <= i <= 63:
            f = c ^ (b | ~d)
            g = (7 * i) % 16
        a, b, c, d = d, (left_rotate((a + f + k[i] + w[g]) & 0xffffffff, r[i]) + b) & 0xffffffff, b, c

    h0 = (h0 + a) & 0xffffffff
    h1 = (h1 + b) & 0xffffffff
    h2 = (h2 + c) & 0xffffffff
    h3 = (h3 + d) & 0xffffffff
    return ''.join(map(lambda x: x.to_bytes(4, byteorder='little').hex(), (h0, h1, h2, h3)))

def pepper_sig(sig="3e0d000a4b0bd712999d730bc331f400221008e0"):
    sig = bytes.fromhex(sig)
    h0, h1, h2, h3, h4 = (int.from_bytes(sig[idx:idx+4], byteorder='big') for idx in range(0, 20, 4))
    chunk = password + salt_sig().encode() + b'\x80' + b'\x00' * 15 + (104 * 8).to_bytes(8, byteorder='big')
    w = [int.from_bytes(chunk[i:i+4], byteorder='big') for i in range(0, len(chunk), 4)]
    for i in range(16, 80):
        w.append(left_rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1))
    a, b, c, d, e = h0, h1, h2, h3, h4
    for i in range(80):
        if 0 <= i <= 19:
            f = (b & c) | (~b & d)
            k = 0x5A827999
        elif 20 <= i <= 39:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif 40 <= i <= 59:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        elif 60 <= i <= 79:
            f = b ^ c ^ d
            k = 0xCA62C1D6
        a, b, c, d, e = (left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff, a, left_rotate(b, 30), c, d
    h0 = (h0 + a) & 0xffffffff
    h1 = (h1 + b) & 0xffffffff
    h2 = (h2 + c) & 0xffffffff
    h3 = (h3 + d) & 0xffffffff
    h4 = (h4 + e) & 0xffffffff
    return ''.join(map(lambda x: x.to_bytes(4, byteorder='big').hex(), (h0, h1, h2, h3, h4)))

conn = remote("02.cr.yp.toc.tf", "28010")
conn.recvuntil("[Q]uit")
conn.sendline("l")
conn.recvuntil(": ")
conn.sendline(f"{(salt_padding + username).hex()},{(pepper_padding + password).hex()}")
conn.recvuntil(": ")
conn.sendline(pepper_sig())
conn.recvuntil(": ")
print(conn.recvuntil("\n").decode().strip("\n"))
