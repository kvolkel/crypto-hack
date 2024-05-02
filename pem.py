from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from sage.all import *


with open("/Users/kevinvolkel/Documents/crypto/privacy_enhanced_mail.pem") as f:
    x=RSA.importKey(f.read())
    print(x.d)

