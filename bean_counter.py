import requests
from multiprocessing import Pool
from multiprocessing import get_context
from functools import partial
import imghdr
from PIL import Image
import io
import os

class StepUpCounter(object):
    def __init__(self, step_up=False):
        self.value = os.urandom(16).hex()
        self.step = 1
        self.stup = step_up

    def increment(self):
        if self.stup:
            self.newIV = hex(int(self.value, 16) + self.step)
        else:
            self.newIV = hex(int(self.value, 16) - self.stup)
        self.value = self.newIV[2:len(self.newIV)]
        return bytes.fromhex(self.value.zfill(32))

    def __repr__(self):
        self.increment()
        return self.value
    

def unwind(image_bytes):
    new_bytes=list(image_bytes[0:16])
    for i in range(16,len(image_bytes),16):
        b1=new_bytes[0:16]
        b2=image_bytes[i:i+16]
        new_bytes+=[x^y for x,y in zip(b1,b2)]
    return new_bytes



encryptURL="https://aes.cryptohack.org//bean_counter/encrypt/"

image_bytes = bytes.fromhex(requests.get(encryptURL).json()["encrypted"])

#idea is that the same keystream is used for every 16 bytes, basically each 16 bytes is encrypted through the same one time pad
new_bytes=unwind(image_bytes)
assert(len(new_bytes)==len(image_bytes))
image_bytes=new_bytes
image_bytes[0:16]=list(bytes.fromhex("89504E470D0A1A0A0000000D49484452"))
print(len(image_bytes))

for l in range(100,300):
    for w in range(100,300):
        print(image_bytes[0:16])
        #need to try to guess at the first few set of bytes to try to get the plaintext
        new_bytes=bytes(unwind(image_bytes))
        f=open("out.png","wb+")
        f.write(new_bytes)
        f.close()

        try:
            img = Image.open("out.png")
            img.verify()
            print("Valid image")
            exit()
        except:
            continue
