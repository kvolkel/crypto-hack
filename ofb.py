import requests
from multiprocessing import Pool
from multiprocessing import get_context
from functools import partial


encryptURL="https://aes.cryptohack.org/symmetry/encrypt_flag/"

queryURL="https://aes.cryptohack.org/symmetry/encrypt/"

encrypted_flag = requests.get(encryptURL).json()["ciphertext"]

encrypted_flag_bytes = bytes.fromhex(encrypted_flag)


flag=bytes()
IV =encrypted_flag_bytes[0:16]
block_iter=1
while b"}" not in flag:
    encrypted_flag=encrypted_flag_bytes[16*block_iter:16*block_iter+16]
    dummy_bytes= bytes(16).hex()
    keystream_IV = bytes.fromhex(requests.get(queryURL+"/"+dummy_bytes+"/"+IV.hex()).json()["ciphertext"])
    flag+=bytes([x^y for x,y in zip(encrypted_flag,keystream_IV)])
    IV=keystream_IV
    block_iter+=1
print(bytes(flag))



