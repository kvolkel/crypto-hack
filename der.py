from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from sage.all import *
import base64

f=open("2048b-rsa-example-cert.der","rb")

x = RSA.importKey(f.read())
print(x.n)

