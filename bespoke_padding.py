#!/usr/bin/env python3
import socket
from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
import random as rnd
import json 
from sage.all import *

FLAG = b'crypto{???????????????????????????}'


class Challenge():
    def __init__(self):
        self.before_input = "Come back as much as you want! You'll never get my flag.\n"
        self.p = getPrime(1024)
        self.q = getPrime(1024)
        self.N = self.p * self.q
        self.e = 11

    def pad(self, flag):
        m = bytes_to_long(flag)
        a = rnd.randint(2, self.N)
        b = rnd.randint(2, self.N)
        return (a, b), a*m+b

    def encrypt(self, flag):
        pad_var, pad_msg = self.pad(flag)
        encrypted = (pow(pad_msg, self.e, self.N), self.N)
        return pad_var, encrypted

    def challenge(self, your_input):
        if not 'option' in your_input:
            return {"error": "You must send an option to this server"}

        elif your_input['option'] == 'get_flag':
            pad_var, encrypted = self.encrypt(FLAG)
            return {"encrypted_flag": encrypted[0], "modulus": encrypted[1], "padding": pad_var}

        else:
            return {"error": "Invalid option"}

local_challenge=Challenge()
def get_challenge(local,s=None):
    get_pubkey={"option":"get_flag"}
    if local:
        return local_challenge.challenge(get_pubkey)
    else:
        try:
            s.send(json.dumps(get_pubkey).encode())
            j=s.recv(100000).decode()
            encryption_info=json.loads(j)
        except:
            exit(1)
        return encryption_info



#set up connection to the server
try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    port=13386
    host=socket.gethostbyname("socket.cryptohack.org")
except Exception as e:
    print(e)
    exit(0)
print(host)
s.connect((host, port)) 
print(s.recv(1024).decode())



moduli=[]
ciphers=[]
linear=[]
constant=[]
#need to get a number of cipher texts that are the message we are looking for padded
while len(constant)<11:
    encryption_info=get_challenge(False,s)
    N=encryption_info["modulus"]
    linear_factor=encryption_info["padding"][0]
    constant_term=encryption_info["padding"][1]
    encrypted_flag=encryption_info["encrypted_flag"]
    moduli.append(N)
    ciphers.append(encrypted_flag)
    linear.append(linear_factor)
    constant.append(constant_term)
for i in moduli: assert i==moduli[0]
R =  PolynomialRing(Integers(moduli[0]),'x')
x=R.gen()
e=11
polys=[]
scaled_ciphers=[]
for cipher,linear,constant in zip(ciphers,linear,constant):
    p = (linear*x+constant)**e
    s = p.coefficients()[0]
    p = (p-s)
    print(p.list())
    polys.append(p.list()[1:])
    scaled_ciphers.append(((cipher-s)%moduli[0]))

assert len(scaled_ciphers)==len(polys)
assert len(scaled_ciphers)==11

Matrix_Ring = Integers(moduli[0])

coefficient_matrix=Matrix(Matrix_Ring,polys)

c_matrix=vector(Matrix_Ring,scaled_ciphers)

M_vector=coefficient_matrix.solve_right(c_matrix)

print(long_to_bytes(int(M_vector[0])))
