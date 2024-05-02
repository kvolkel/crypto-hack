from random import randint

a = 288260533169915
p = 1007621497415251

#FLAG = b'crypto{????????????????????}'
FLAG = b'crypto'


def encrypt_flag(flag):
    ciphertext = []
    plaintext = ''.join([bin(i)[2:].zfill(8) for i in flag])
    print(plaintext)
    print(bin(FLAG[0])[2:])
    for b in plaintext:
        e = randint(1, p)
        n = pow(a, e, p)
        if b == '1':
            print("1")
            #print(n)
            ciphertext.append(n)
        else:
            print("0")
            n = -n % p
            #print(n)
            ciphertext.append(n)
    return ciphertext



def decrypt(nums):
    bit_string=""
    for n in nums:
        x=pow(n,2,p)
        residue = pow(x,-(p-3)//4,p)
        if residue==n:
            bit_string+="1"
        else:
            bit_string+="0"
    return bit_string


def bitstring_to_bytes(bitstring):
    print(bitstring)
    bs=[]
    for i in range(0,len(bitstring),8):
        bs.append(int(bitstring[i:i+8],2))
    b=bytearray(bs)
    return b


#encrypted_string=encrypt_flag(FLAG)
encrypted_string=[]
with open("adriens_cleaned.txt","r") as f:
    for line in f:
        encrypted_string.append(int(line.strip()))
    
b = decrypt(encrypted_string)
print(bitstring_to_bytes(b))

