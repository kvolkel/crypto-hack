import requests
from multiprocessing import Pool
from multiprocessing import get_context
from functools import partial
import imghdr
from PIL import Image
import io
import os
import itertools

GATHER=False
encryptURL="https://aes.cryptohack.org/stream_consciousness/encrypt/"

def xor(x1,y1):
    return b''.join([bytes([x^y]) for x,y in zip(x1,y1)])

if GATHER: #gather messages from the set 
    ciphers=set()
    for i in range(300):
        print(i)
        ciphers.add(requests.get(encryptURL).json()["ciphertext"])
        print("Ciphers len {}".format(len(ciphers)))
    with open("stream_of_consc.txt","w+") as f: #store messages so we don't need to keep getting them from the website
        for c in ciphers:
            f.write(c+"\n")
else:
    ciphers=[]
    with open("stream_of_consc.txt","r") as f:
        for l in f:
            ciphers.append(l.strip())
    ciphers.sort(key=lambda x: len(x))
    ciphers=[bytes.fromhex(_) for _ in ciphers]
    tester=b'crypto{'
    baseline=ciphers[12]
    for c_index,c in enumerate(ciphers):
        if c==baseline: continue
        b1 = c[:len(tester)]
        b2 = baseline[:len(tester)]
        b_xor = b''.join([bytes([x^y]) for x,y in zip(b1,b2)])
        assert(len(b_xor)==len(tester))
        print(c_index)
        #print(len(c))
        #print(baseline.hex())
        #print(c.hex())
        #print(b_xor)
        print( b''.join([bytes([x^y]) for x,y in zip(b_xor,tester)]))
    FLAG_INDEX=4
    flag_cipher=ciphers[FLAG_INDEX]
    build_flag=tester
    flag_xor_messages=[]
    for c in ciphers:
        flag_xor_messages.append(
            b''.join([bytes([x^y]) for x,y in zip(c,flag_cipher)])
        )
    #make a game out of determining the flag
    #MAIN IDEA: Look at incremental plaintexts of messages, figure out an extension and see if the resulting key makes sense across all messages and continue
    while b'}' not in build_flag:
        os.system("clear")
        print("These are the current messages for FLAG: {}".format(build_flag))
        for c_index,c in enumerate(flag_xor_messages):
            print("Index: {}".format(c_index))
            print(xor(c,build_flag))
        index=int(input("Choose message to extend: "))
        message=xor(flag_xor_messages[index],build_flag)
        new_chars=input("Enter characters to extend onto message ")
        new_chars=new_chars.encode()
        new_message=message+new_chars
        print("Your new message is {}".format(new_message))
        new_key=xor(flag_xor_messages[index],new_message)
        print("The new key is {}".format(new_key))
        print("These are the new messages")
        for c_index,c in enumerate(flag_xor_messages):
            print("Index: {}".format(c_index))
            print(xor(c,new_key))
        keep=input("Do you want to keep this key (y/n)")
        if keep=="y":
            build_flag=new_key
        elif keep=="n":
            continue
        else:
            assert(0)

    