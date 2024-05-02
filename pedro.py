from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from sage.all import *
from Crypto.Util.number import bytes_to_long, inverse,long_to_bytes
import math
import random as rnd
import json
FLAG="This if flag"
import socket
ALICE_N = 22266616657574989868109324252160663470925207690694094953312891282341426880506924648525181014287214350136557941201445475540830225059514652125310445352175047408966028497316806142156338927162621004774769949534239479839334209147097793526879762417526445739552772039876568156469224491682030314994880247983332964121759307658270083947005466578077153185206199759569902810832114058818478518470715726064960617482910172035743003538122402440142861494899725720505181663738931151677884218457824676140190841393217857683627886497104915390385283364971133316672332846071665082777884028170668140862010444247560019193505999704028222347577

ALICE_E = 3
class Challenge():
    def __init__(self):
        self.before_input = "Place your vote. Pedro offers a reward to anyone who votes for him!\n"

    def challenge(self, your_input):
        if 'option' not in your_input:
            return {"error": "You must send an option to this server"}

        elif your_input['option'] == 'vote':
            vote = int(your_input['vote'], 16)
            verified_vote = long_to_bytes(pow(vote, ALICE_E, ALICE_N))

            # remove padding
            vote = verified_vote.split(b'\00')[-1]

            if vote == b'VOTE FOR PEDRO':
                return {"flag": FLAG}
            else:
                return {"error": "You should have voted for Pedro"}

        else:
            return {"error": "Invalid option"}

c=Challenge()
N_bits=ALICE_N.bit_length()
pedro_int = bytes_to_long(b'VOTE FOR PEDRO')
pedro_bits=pedro_int.bit_length()

s=0x01
c=0x01

for i in range(pedro_bits+16):
    c=s**3
    if ((pedro_int>>i)&0x01)==((c>>i)&0x01):continue
    else:
        s^=(0x01<<i)
        #print(s)
print(long_to_bytes(s**3))


#set up connection to the server
try: 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    port=13375
    host=socket.gethostbyname("socket.cryptohack.org")
except Exception as e:
    print(e)
    exit(0)
print(host)
sock.connect((host, port)) 
print(sock.recv(1024).decode())
send_root={"option":"vote","vote":hex(s)}
sock.send(json.dumps(send_root).encode())

flag=sock.recv(100000).decode()

print(flag)