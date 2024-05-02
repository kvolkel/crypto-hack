#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long
from os import urandom
import socket
FLAG = "crypto{???????????????????????????????}"
import json

class CFB8:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        IV = urandom(16)
        cipher = AES.new(self.key, AES.MODE_ECB)
        ct = b''
        state = IV
        for i in range(len(plaintext)):
            b = cipher.encrypt(state)[0]
            c = b ^ plaintext[i]
            ct += bytes([c])
            state = state[1:] + bytes([c])
        return IV + ct

    def decrypt(self, ciphertext):
        IV = ciphertext[:16]
        ct = ciphertext[16:]
        cipher = AES.new(self.key, AES.MODE_ECB)
        pt = b''
        state = IV
        for i in range(len(ct)):
            b = cipher.encrypt(state)[0]
            c = b ^ ct[i]
            pt += bytes([c])
            state = state[1:] + bytes([ct[i]])
        return pt


class Challenge():
    def __init__(self):
        self.before_input = "Please authenticate to this Domain Controller to proceed\n"
        self.password = urandom(20)
        self.password_length = len(self.password)
        self.cipher = CFB8(urandom(16))

    def challenge(self, your_input):
        if your_input['option'] == 'authenticate':
            if 'password' not in your_input:
                return {'msg': 'No password provided.'}
            your_password = your_input['password']
            if your_password.encode() == self.password:
                self.exit = True
                return {'msg': 'Welcome admin, flag: ' + FLAG}
            else:
                return {'msg': 'Wrong password.'}

        if your_input['option'] == 'reset_connection':
            self.cipher = CFB8(urandom(16))
            return {'msg': 'Connection has been reset.'}

        if your_input['option'] == 'reset_password':
            if 'token' not in your_input:
                return {'msg': 'No token provided.'}
            token_ct = bytes.fromhex(your_input['token'])
            if len(token_ct) < 28:
                return {'msg': 'New password should be at least 8-characters long.'}

            token = self.cipher.decrypt(token_ct)
            new_password = token[:-4]
            self.password_length = bytes_to_long(token[-4:])
            print("reset")
            self.password = new_password[:self.password_length]
            print(self.password)
            return {'msg': 'Password has been correctly reset.'}




#set up connection to the server
try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    port=13399
    host=socket.gethostbyname("socket.cryptohack.org")
except Exception as e:
    print(e)
    exit(0)
print(host)
s.connect((host, port)) 
print(s.recv(1024).decode())


for i in range(0,256):
    print(i)
    token=bytes([i]*28).hex()
    reset={"option":'reset_password',"token":token}
    s.send(json.dumps(reset).encode())
    print(s.recv(1024).decode())
    x={"option":"authenticate",'password':""}
    s.send(json.dumps(x).encode())
    print(print(s.recv(1024).decode()))
exit(0)


