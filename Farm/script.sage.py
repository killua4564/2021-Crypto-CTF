

# This file was *autogenerated* from the file script.sage
from sage.all_cmdline import *   # import sage library

_sage_const_62 = Integer(62); _sage_const_64 = Integer(64); _sage_const_0 = Integer(0)
from base64 import *
import string

ALPHABET = string.printable[:_sage_const_62 ] + '\\='

F = list(GF(_sage_const_64 ))

pt = b64encode(b"CCTF")
enc = b"805c9GMYuD5RefTmabUNfS9N9YrkwbAbdZE0df91uCEytcoy9FDSbZ8Ay8jj"

def maptofarm(c):
    return F[ALPHABET.index(c)]

key = maptofarm(chr(enc[_sage_const_0 ])) / maptofarm(chr(pt[_sage_const_0 ]))

flag = ""
for i in enc:
    flag += ALPHABET[F.index(maptofarm(chr(i)) / key)]

print(b64decode(flag.encode()).decode())
