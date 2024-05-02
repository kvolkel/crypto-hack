import requests
from multiprocessing import Pool
from multiprocessing import get_context
from functools import partial


cookieURL="https://aes.cryptohack.org/flipping_cookie/get_cookie/"

cookie=requests.get(cookieURL)

cookie=cookie.json()["cookie"]

cookie=bytes.fromhex(cookie)

IV=cookie[:16]
cookiecipher=cookie[16:]

beginningbytes=b'admin=False;expi'
endbytes=b'admin=True;;expi'
newIV=bytes([x^y^z for x,y,z in zip(IV,beginningbytes,endbytes)])

sendURL="https://aes.cryptohack.org/flipping_cookie/check_admin/"


sendcookie=requests.get(sendURL+"/"+cookiecipher.hex()+"/"+newIV.hex())

print(sendcookie.text)