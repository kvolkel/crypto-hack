import requests
from multiprocessing import Pool
from multiprocessing import get_context
from functools import partial
import imghdr
from PIL import Image
import io
import os

encryptURL="https://aes.cryptohack.org/lazy_cbc/encrypt/"
decryptURL="https://aes.cryptohack.org/lazy_cbc/receive/"
flagURL="https://aes.cryptohack.org/lazy_cbc/get_flag/"

plaintext=b'A'*16
x=[0]*16
encrypted_plaintext=bytes.fromhex(requests.get(encryptURL+"/"+plaintext.hex()).json()['ciphertext'])
dummycipher_text=bytes(x)+encrypted_plaintext
IV_xor_plaintext=bytes.fromhex(requests.get(decryptURL+"/"+dummycipher_text.hex()).json()["error"].split("Invalid plaintext: ")[1])
print(IV_xor_plaintext)

IV_mix = IV_xor_plaintext[16:]
key=[x^y for x,y in zip(IV_mix,plaintext)]

print(bytes.fromhex(requests.get(flagURL+"/"+bytes(key).hex()).json()["plaintext"]))
