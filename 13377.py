#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long, long_to_bytes
import base64
import codecs
import random
from pwn import * # pip install pwntools
import json

FLAG = "crypto{????????????????????}"
ENCODINGS = [
    "base64",
    "hex",
    "rot13",
    "bigint",
    "utf-8",
]


class Challenge():
    def __init__(self):
        self.challenge_words = ""
        self.stage = 0

    def create_level(self):
        self.stage += 1
        self.challenge_words = "_".join(random.choices(WORDS, k=3))
        encoding = random.choice(ENCODINGS)

        if encoding == "base64":
            encoded = base64.b64encode(self.challenge_words.encode()).decode() # wow so encode
        elif encoding == "hex":
            encoded = self.challenge_words.encode().hex()
        elif encoding == "rot13":
            encoded = codecs.encode(self.challenge_words, 'rot_13')
        elif encoding == "bigint":
            encoded = hex(bytes_to_long(self.challenge_words.encode()))
        elif encoding == "utf-8":
            encoded = [ord(b) for b in self.challenge_words]

        return {"type": encoding, "encoded": encoded}

    #
    # This challenge function is called on your input, which must be JSON
    # encoded
    #
    def challenge(self, your_input):
        if self.stage == 0:
            return self.create_level()
        elif self.stage == 100:
            self.exit = True
            return {"flag": FLAG}

        if self.challenge_words == your_input["decoded"]:
            return self.create_level()

        return {"error": "Decoding fail"}





r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


received = json_recv()

while True:
    encoded_string=received["encoded"]
    t = received["type"]
    print(t)
    send_dict={}
    if t=="base64":
        send_dict["decoded"]=base64.b64decode(encoded_string).decode()
    elif t=="hex":
        send_dict["decoded"]=bytes.fromhex(encoded_string).decode()
    elif t=="bigint":
        send_dict["decoded"]=long_to_bytes(int(encoded_string,16)).decode()
    elif t=="utf-8":
        send_dict["decoded"]="".join([chr(_) for _ in encoded_string])
    elif t=="rot13":
        send_dict["decoded"]=codecs.decode(encoded_string,"rot_13")
    json_send(send_dict)
    received=json_recv()
    if "flag" in received:
        print(received["flag"])
        break