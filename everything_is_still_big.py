from Crypto.Util.number import getPrime, bytes_to_long, inverse
from random import getrandbits
from math import gcd

FLAG = b"crypto{?????????????????????????????????????}"

m = bytes_to_long(FLAG)

def get_huge_RSA():
    p = getPrime(1024) #this is ok
    q = getPrime(1024) #this is ok
    N = p*q #ok
    phi = (p-1)*(q-1) #ok
    while True:
        d = getrandbits(512) #uses rand bits, Mersenne Twister algorithm, but we don't know seed, or the actual bits to use
        if (3*d)**4 > N and gcd(d,phi) == 1: 
            e = inverse(d, phi)
            break
    return N,e,d


N, e, d = get_huge_RSA()
c = pow(m, e, N)

print(f'N = {hex(N)}')
print(f'e = {hex(e)}')
print(f'c = {hex(c)}')
print(f'd = {hex(d)}')

print(N.bit_length())
