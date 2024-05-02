#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, long_to_bytes
from os import urandom
import socket
import json
import re
from pkcs1 import emsa_pkcs1_v15
import random
import sys
sys.set_int_max_str_digits(10000000)
def find_largest_k(nk,target_bit_length=0):
    k=2
    while nk%k==0 and (nk//k).bit_length()>target_bit_length:
        if nk%(k*2)!=0: break
        k*=2
    return k


class Challenge():
    def __init__(self):
        self.before_input = "This server validates domain ownership with RSA signatures. Present your message and public key, and if the signature matches ours, you must own the domain.\n"

    def challenge(self, your_input):
        if not 'option' in your_input:
            return {"error": "You must send an option to this server"}

        elif your_input['option'] == 'get_signature':
            return {
                "N": hex(N),
                "e": hex(E),
                "signature": hex(SIGNATURE)
            }

        elif your_input['option'] == 'verify':
            msg = your_input['msg']
            n = int(your_input['N'], 16)
            e = int(your_input['e'], 16)

            digest = emsa_pkcs1_v15.encode(msg.encode(), 256)
            calculated_digest = pow(SIGNATURE, e, n)

            if bytes_to_long(digest) == calculated_digest:
                r = re.match(r'^I am Mallory.*own CryptoHack.org$', msg)
                if r:
                    return {"msg": f"Congratulations, here's a secret: {FLAG}"}
                else:
                    return {"msg": f"Ownership verified."}
            else:
                return {"error": "Invalid signature"}

        else:
            return {"error": "Invalid option"}




#set up connection to the server
try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    port=13391
    host=socket.gethostbyname("socket.cryptohack.org")
except Exception as e:
    print(e)
    exit(0)
print(host)
s.connect((host, port)) 
print(s.recv(1024).decode())


get_pubkey={"option":"get_signature"}
s.send(json.dumps(get_pubkey).encode())
signature=json.loads(s.recv(4096).decode())
N=int(signature["N"],16)
e=int(signature["e"],16)
sig =int(signature["signature"],16)
sig_int=pow(sig,e,N)


message=b'I am Mallory own CryptoHack.org'
message_digest= emsa_pkcs1_v15.encode(message, 256)
print(message_digest)
print("Signature Bit length {}".format(sig_int.bit_length()))
nk=1
e_prime=1
digest_int=bytes_to_long(message_digest)
print("Digest bit length {}".format(digest_int.bit_length()))
print(sig_int)
print(digest_int)
while True:
    nk = pow(sig,e_prime)-digest_int
    if nk%2==0:
        l = find_largest_k(nk,target_bit_length=0)
        #if (nk//l).bit_length()<=4096 and (nk//l).bit_length()>=2048: break
        print("Found {} ".format(l))
        break

n_prime=nk//l

print("N prime bit length {}".format(n_prime.bit_length()))

print((pow(sig,e_prime,n_prime)) == digest_int)

#send e prime, n prime with new message 
print(len(long_to_bytes(n_prime).hex()))
attack_dict={
    "option":"verify",
    "N":long_to_bytes(n_prime).hex(),
    "e":long_to_bytes(e_prime).hex(),
    "msg":message.decode()
}

print(attack_dict)
i=0
y=json.dumps(attack_dict).encode()
x=y[i:i+500]
s.send(y)
print(json.loads(s.recv(1024).decode()))


