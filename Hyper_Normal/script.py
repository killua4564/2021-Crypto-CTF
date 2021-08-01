import string
from math import gcd
from functools import reduce
from Crypto.Util.number import inverse

p = 8443
arr = eval(open("output.txt", "r").read())

flag = ""
for idx in range(len(arr)):
    for char in string.printable:
        c_char = ord(char) * (idx + 1)
        if all(0 <= row[idx] * inverse(c_char, p) % p <= 126 for row in arr):
            flag += char
            break

print(flag)
