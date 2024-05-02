from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from sage.all import *


key_array=[]
cipher_array=[]

for i in range(1,51):
    with open("keys_and_messages/{}.pem".format(i)) as f:
        key_array.append(RSA.importKey(f.read()))
    with open("keys_and_messages/{}.ciphertext".format(i)) as f:
        cipher_array.append(bytes.fromhex(f.read()))


key_pairs=[]

for i_index,i in enumerate(key_array):
    for j_index,j in enumerate(key_array):
        if i==j: continue
        if gcd(i.n,j.n)!=1:
            key_pairs.append((i_index,j_index))

for i,j in key_pairs:
    shared_prime=gcd(key_array[i].n,key_array[j].n)
    i_prime = key_array[i].n//shared_prime
    j_prime = key_array[j].n//shared_prime
    i_d = pow(key_array[i].e,-1,lcm((i_prime-1),(shared_prime-1)))
    j_d = pow(key_array[j].e,-1,lcm((j_prime-1),(shared_prime-1)))
    i_private_key=RSA.construct((key_array[i].n,
                                 key_array[i].e,
                                 int(i_d),
                                 int(shared_prime),
                                 int(i_prime)),True)
    
    cipher_i = PKCS1_OAEP.new(i_private_key)
    print(cipher_i.decrypt(cipher_array[i]))
