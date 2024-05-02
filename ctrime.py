import requests
from multiprocessing import Pool
from multiprocessing import get_context
from functools import partial
import imghdr
from PIL import Image
import io
import os

encryptURL="https://aes.cryptohack.org/ctrime/encrypt"

flag=b'crypto{CRIME_571'
test_size=35
#using length oracle to pick out the correct characters
while not b'}' in flag:
    for i in range(128,32,-1):
        candidate=flag[-6:]+i.to_bytes(1)
        print(candidate)
        cipher = requests.get(encryptURL+"/"+candidate.hex()).json()["ciphertext"]
        cipher=bytes.fromhex(cipher)
        print(len(cipher))
        if len(cipher)==test_size:
            flag+=i.to_bytes(1)
            break
    print(flag)
print(flag)