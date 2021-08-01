from base64 import *
import string

ALPHABET = string.printable[:62] + '\\='

F = list(GF(64))

pt = b64encode(b"CCTF")
enc = b"805c9GMYuD5RefTmabUNfS9N9YrkwbAbdZE0df91uCEytcoy9FDSbZ8Ay8jj"

def maptofarm(c):
    return F[ALPHABET.index(c)]

key = maptofarm(chr(enc[0])) / maptofarm(chr(pt[0]))

flag = ""
for i in enc:
    flag += ALPHABET[F.index(maptofarm(chr(i)) / key)]

print(b64decode(flag.encode()).decode())
