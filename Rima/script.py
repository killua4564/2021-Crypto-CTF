from Crypto.Util.number import long_to_bytes
from math import gcd
from gmpy2 import next_prime

g = int.from_bytes(open("g.enc", "rb").read(), "big")
h = int.from_bytes(open("h.enc", "rb").read(), "big")

g_list = []
h_list = []
for num, arr in ((g, g_list), (h, h_list)):
    while num > 0:
        arr.append(num % 5)
        num //= 5
    arr.reverse()

g_len = len(g_list)
h_len = len(h_list)

c = 0
while True:
    f = gcd(g_len - c, h_len - c)
    if f > 1 and f * next_prime(f) + c == g_len and next_prime(f >> 2) == c:
        print(f"Found c={c} f={f}")
        break
    c += 1

for arr in (g_list, h_list):
    for i in range(len(arr) - c - 1, -1, -1):
        arr[i] -= arr[i+c]
    for _ in range(c):
        del arr[0]

assert g_list[:f] == h_list[:f]

f_list = g_list[:f]
for i in range(len(f_list)-2, -1, -1):
    f_list[i] -= f_list[i+1]
del f_list[0]

print(long_to_bytes(int("".join(map(str, f_list)), 2)).decode())
