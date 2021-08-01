from pwn import remote
from Crypto.Cipher import AES

conn = remote("01.cr.yp.toc.tf", 17010)

def menu():
    conn.recvuntil("[Q]uit")

def enc_flag():
    menu()
    conn.sendline("g")
    conn.recvuntil("=")
    return bytes.fromhex(conn.recvuntil("\n").decode())

def enc(ct):
    menu()
    conn.sendline("t")
    conn.recvuntil(": ")
    conn.sendline(ct)
    conn.recvuntil("| enc =")
    mask_enc = conn.recvuntil("\n").decode().strip("\n")
    conn.recvuntil("| key =")
    mask_key = conn.recvuntil("\n").decode().strip("\n")
    return mask_key, mask_enc

mask_key, mask_enc = enc(bytes([0]) * 32)
enc_head, *_, enc_tail = mask_enc.strip().split('*')

mask_key = mask_key.strip("*")
enc_tail = bytes.fromhex(enc_tail[-32:])

for i in range(16**4):
    key = bytes.fromhex(mask_key + hex(i)[2:].zfill(4))
    t_head = AES.new(key, AES.MODE_ECB).decrypt(enc_tail).hex()
    if t_head.startswith(enc_head):
        print("Found key")
        break

iv = AES.new(key, AES.MODE_ECB).decrypt(bytes.fromhex(t_head))

print(AES.new(key, AES.MODE_CBC, iv).decrypt(enc_flag()).decode())
