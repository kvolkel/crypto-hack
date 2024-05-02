#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long
from os import urandom
import socket
FLAG = "crypto{???????????????????????????????}"
import json
import requests
from multiprocessing import Pool
from functools import partial
from Crypto.Cipher import ARC4
from multiprocessing import get_context


def send_cmd(ciphertext, nonce):
    if not ciphertext:
        return {"error": "You must specify a ciphertext"}
    if not nonce:
        return {"error": "You must specify a nonce"}

    ciphertext = bytes.fromhex(ciphertext)
    nonce = bytes.fromhex(nonce)

    cipher = ARC4.new(nonce + FLAG.encode())
    cmd = cipher.decrypt(ciphertext)
    if cmd == b"ping":
        return {"msg": "Pong!"}
    else:
        return {"error": f"Unknown command: {cmd.hex()}"}


def KSA(key,iterations=256): #key schedule for some number of iterations
    i=0
    j=0
    S=list(range(0,256))
    for k in range(0,iterations):
        j=(j+S[i]+key[i%len(key)])%256
        S[i],S[j]=S[j],S[i]
        i+=1
    return S,j,i #returned S is S_(i-1) return j is for S_(i-1)

def valid_IV(S_IV,IV_length,B): #Checks to see if an S state is valud given an IV_length and target byte
    if IV_length<=1:
        #print("IV too short")
        return False
    if S_IV[1]>=IV_length:
        #print("S_IV 1 fail {}".format(S_IV))
        return False
    if S_IV[1]+S_IV[S_IV[1]]!=IV_length+B:
        #print("Add fail {}".format(S_IV[1]+S_IV[S_IV[1]]))
        return False
    return True

def get_key_value(S_K_1:list,j_k_1:int,V_K:int,i_k:int): #derive expected key value from returned first byte of keystream
    j_k = S_K_1.index(V_K)
    return (j_k-j_k_1-S_K_1[i_k])%256


def get_IV(target_byte:int):#generate new IV randomly
    IV_SIZE=16
    b = (target_byte+IV_SIZE).to_bytes(1)
    b+=int(255).to_bytes(1)
    return b+urandom(IV_SIZE-2)



def test_IV(flag_bytes,i): #tests IV and gets a sample of keystream and the expected byte
    ciphertext="TEST".encode()
    IV=get_IV(len(flag_bytes))
    S_1,j_1,i=KSA(IV,iterations=len(IV))
    if not valid_IV(S_1,len(IV),len(flag_bytes)): return None
    S_1,j_1,i=KSA(IV+flag_bytes,iterations=len(IV)+len(flag_bytes))
    #result=send_cmd(ciphertext.hex(),IV.hex())
    result=requests.get("https://aes.cryptohack.org/oh_snap/send_cmd/{}/{}".format(ciphertext.hex(),IV.hex())).json()["error"].split(":")[1].strip()
    result=bytes.fromhex(result)[0]^ciphertext[0]
    v=get_key_value(S_1,j_1,result,i)
    return v

if __name__ == '__main__':
    flag_bytes=b'crypto{w1R3d_' #this can be empty if you want, sometimes the sampling messes up and restarting again is fine with a checkpoint
    while b'}' not in flag_bytes:
        results=[]
        results_hist={}
        f=partial(test_IV,flag_bytes)
        p=Pool(16)
        results=p.map(f,range(0,200))
        assert(len(results)>0)
        for _ in results:
            if _ is None: continue 
            results_hist[_]=results_hist.get(_,0)+1
        k,v= sorted(results_hist.items(),key=lambda x: x[1],reverse=True)[0]
        print("=================NEW RESULT===============================")
        print(k,v)
        flag_bytes+=k.to_bytes(1)
        print(flag_bytes)
    exit(0)


