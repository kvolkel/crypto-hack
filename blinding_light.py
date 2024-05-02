#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
from os import urandom
import socket
import json
import re
from pkcs1 import emsa_pkcs1_v15
import random
import sys

ADMIN_TOKEN = b"admin=True"


class Challenge():
    def __init__(self):
        self.before_input = "Watch out for the Blinding Light\n"

    def challenge(self, your_input):
        if 'option' not in your_input:
            return {"error": "You must send an option to this server"}

        elif your_input['option'] == 'get_pubkey':
            return {"N": hex(N), "e": hex(E) }

        elif your_input['option'] == 'sign':
            msg_b = bytes.fromhex(your_input['msg'])
            if ADMIN_TOKEN in msg_b:
                return {"error": "You cannot sign an admin token"}

            msg_i = bytes_to_long(msg_b)
            return {"msg": your_input['msg'], "signature": hex(pow(msg_i, D, N)) }

        elif your_input['option'] == 'verify':
            msg_b = bytes.fromhex(your_input['msg'])
            msg_i = bytes_to_long(msg_b)
            signature = int(your_input['signature'], 16)

            if msg_i < 0 or msg_i > N:
                # prevent attack where user submits admin token plus or minus N
                return {"error": "Invalid msg"}

            verified = pow(signature, E, N)
            if msg_i == verified:
                if long_to_bytes(msg_i) == ADMIN_TOKEN:
                    return {"response": FLAG}
                else:
                    return {"response": "Valid signature"}
            else:
                return {"response": "Invalid signature"}

        else:
            return {"error": "Invalid option"}



#set up connection to the server
try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    port=13376
    host=socket.gethostbyname("socket.cryptohack.org")
except Exception as e:
    print(e)
    exit(0)
print(host)
s.connect((host, port)) 
print(s.recv(1024).decode())


get_pubkey={"option":"get_pubkey"}
s.send(json.dumps(get_pubkey).encode())
signature=json.loads(s.recv(4096).decode())
N=int(signature["N"],16)
e=int(signature["e"],16)
r=getPrime(16)
blind=pow(r,e,N)
admin_i=bytes_to_long(ADMIN_TOKEN)
attack_message=long_to_bytes(blind*admin_i).hex()


sign_dict={
    "option":"sign",
    "msg":attack_message
}

y=json.dumps(sign_dict).encode()
s.send(y)
signature=json.loads(s.recv(4096).decode())["signature"]
signature=int(signature,16)
signature=(signature*pow(r,-1,N))%N




verify_dict={
    "option":"verify",
    "msg":ADMIN_TOKEN.hex(),
    "signature":long_to_bytes(signature).hex()
}

print(verify_dict)

y=json.dumps(verify_dict).encode()
print(len(y))
s.send(y)
print(json.loads(s.recv(1024).decode()))

