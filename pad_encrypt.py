#"""""
#!/usr/bin/env sage
from sage.all import *
from Crypto.Util.number import bytes_to_long, long_to_bytes

FLAG = b"crypto{???????????????????????????????????}"


n = 95341235345618011251857577682324351171197688101180707030749869409235726634345899397258784261937590128088284421816891826202978052640992678267974129629670862991769812330793126662251062120518795878693122854189330426777286315442926939843468730196970939951374889986320771714519309125434348512571864406646232154103
e = 3
c = 63476139027102349822147098087901756023488558030079225358836870725611623045683759473454129221778690683914555720975250395929721681009556415292257804239149809875424000027362678341633901036035522299395660255954384685936351041718040558055860508481512479599089561391846007771856837130233678763953257086620228436828


print(n.bit_length())
print(len(FLAG)*8)
top_bytes=b"crypto"
top_byte_exponent=len(FLAG)-1
top_bytes_int=0
top_byte_ints_array=[]
#construct an offset we can use in order to move a portion of the message cubed under N so we can take a cube-root over the integers
#at face value, the message is too large after being cubed to fitting in one iteration of N, so we can't directly take a cube root like 
#in a previous challenge.
for i,b in enumerate(top_bytes):
    top_bytes_int+=int(b)*pow(256,top_byte_exponent-i)
    top_byte_ints_array.append(int(b)*pow(256,top_byte_exponent-i))

for i in range(57,58):
    r = pow(256,int(-e*(i)),n)
    M3=(r*c)%n
    M3=(M3-pow(top_bytes_int,e))%n
    M3=M3+pow(top_bytes_int,e)
    try:
        print(long_to_bytes(Integer(M3).nth_root(3)))
    except:
        continue 

    

 