import requests
from multiprocessing import Pool
from multiprocessing import get_context
from functools import partial

def encrypt(message):
    encryptURL="https://aes.cryptohack.org/ecb_oracle/encrypt/"
    if type(message) is bytes:
        r = requests.get(encryptURL+message.hex())
    else: #empty request
        r = requests.get(encryptURL+"")
        print(r.json())
    return r.json()["ciphertext"]


def test_pad(pad,found_bytes,i): #function to test pad
    b = i.to_bytes()
    paddedmessage=pad+found_bytes+bytes(b)
    paddedmessage=paddedmessage[-16:] #make sure to take only 16 relevant bytes to test
    #print(paddedmessage)
    return bytes.fromhex(encrypt(paddedmessage))[:len(paddedmessage)],b
    #return   dict[encrypt(paddedmessage)[:len(paddedmessage)]]=j

'''
Pretty simple implementation. To first get off the ground, fix the first bytes given to the encryption and make a code book mapping
encrypted results to just 1 byte-change. Perform encryption again using the unknown byte and map the ciphertext back to the byte we mapped to
earlier. Not the most efficient, but not terrible. 256*Length-Flag operations at worst. Could make probably 2-3 times more efficient with
using typical character ranges.
'''
pad= b'Z'*15
#found_bytes=bytes()
found_bytes=b''
while b'}' not in found_bytes:
    p=get_context("fork").Pool(16)
    f=partial(test_pad,pad,found_bytes)
    result = p.map(f,range(0,256))
    dict={_:k for (_,k) in result}

    if len(pad)>0:
        check_string=bytes.fromhex(encrypt(pad))
    else:
        check_string=bytes.fromhex(encrypt(b'Z'*16))
    start=0
    pad_range=len(pad)
    found_bytes_pad=min(len(found_bytes)+1,16)
    if len(found_bytes)+1>=16:
        start=(len(found_bytes)+1)-16
        start+=len(pad)
        pad_range=0
    print(start)
    found_bytes += bytes(dict[check_string[start:start+(pad_range+found_bytes_pad)]])
    print(found_bytes)
    if len(pad)>0:
        pad = pad[0:len(pad)-1]
        if len(pad)==0:pad=b'Z'*16