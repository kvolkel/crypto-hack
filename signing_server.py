#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, long_to_bytes
from os import urandom
import socket
FLAG = "crypto{???????????????????????????????}"
import json

class Challenge():
    def __init__(self):
        self.before_input = "Welcome to my signing server. You can get_pubkey, get_secret, or sign.\n"

    def challenge(self, your_input):
        if not 'option' in your_input:
            return {"error": "You must send an option to this server"}

        elif your_input['option'] == 'get_pubkey':
            return {"N": hex(N), "e": hex(E) }

        elif your_input['option'] == 'get_secret':
            secret = bytes_to_long(SECRET_MESSAGE)
            return {"secret": hex(pow(secret, E, N)) }

        elif your_input['option'] == 'sign':
            msg = int(your_input['msg'], 16)
            return {"signature": hex(pow(msg, D, N)) }

        else:
            return {"error": "Invalid option"}


#set up connection to the server
try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    port=13374
    host=socket.gethostbyname("socket.cryptohack.org")
except Exception as e:
    print(e)
    exit(0)
print(host)
s.connect((host, port)) 
print(s.recv(1024).decode())


get_pubkey={"option":"get_pubkey"}
s.send(json.dumps(get_pubkey).encode())
pkey=json.loads(s.recv(1024).decode())
N=int(pkey["N"],16)
e=int(pkey["e"],16)
plaintext=int(0x02).to_bytes(1).hex()
s.send(json.dumps({"option":"get_secret"}).encode())
secret=json.loads(s.recv(1024).decode())["secret"]
print(secret)
s.send(json.dumps({"option":"sign",'msg':secret}).encode())
print(long_to_bytes(int(json.loads(s.recv(1024).decode())["signature"],16)))


