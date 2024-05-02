#!/usr/bin/env python3

from os import urandom


FLAG = b'crypto{?????????????????????????????}'


def bytes_to_words(b):
    return [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)] #good

def rotate(x, n):
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff) #good

def inv_rotate(x,n):
    return ((x << 32-n) & 0xffffffff) | ((x >> n) & 0xffffffff) #good

def word(x):
    return x % (2 ** 32) #good

def words_to_bytes(w):
    return b''.join([i.to_bytes(4, 'little') for i in w]) #good

def xor(a, b):
    return b''.join([bytes([x ^ y]) for x, y in zip(a, b)]) #good


class ChaCha20:
    def __init__(self):
        self._state = []

    def _inner_block(self, state):
        #column rounds
        self._quarter_round(state, 0, 4, 8, 12) #good
        self._quarter_round(state, 1, 5, 9, 13) #good
        self._quarter_round(state, 2, 6, 10, 14) #good
        self._quarter_round(state, 3, 7, 11, 15) #good
        #diagonal rounds
        self._quarter_round(state, 0, 5, 10, 15) #good
        self._quarter_round(state, 1, 6, 11, 12) #good
        self._quarter_round(state, 2, 7, 8, 13) #good
        self._quarter_round(state, 3, 4, 9, 14) #good

    def _inv_inner_block(self,state):
        #back track through the rounds 
        self._inv_quarter_round(state, 3, 4, 9, 14) #good
        self._inv_quarter_round(state, 2, 7, 8, 13) #good
        self._inv_quarter_round(state, 1, 6, 11, 12) #good
        self._inv_quarter_round(state, 0, 5, 10, 15) #good
        self._inv_quarter_round(state, 3, 7, 11, 15) #good
        self._inv_quarter_round(state, 2, 6, 10, 14) #good
        self._inv_quarter_round(state, 1, 5, 9, 13) #good
        self._inv_quarter_round(state, 0, 4, 8, 12) #good

    def _quarter_round(self, x, a, b, c, d):
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 16) #good
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 12) #good
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 8)  #good
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 7)  #good
    
    def _inv_quarter_round(self,x,a,b,c,d):
       x[b] = inv_rotate(x[b], 7);  x[b] ^= x[c];  x[c] = word(x[c] - x[d])
       x[d] = inv_rotate(x[d], 8);  x[d] ^= x[a];  x[a] = word(x[a] - x[b])   
       x[b] = inv_rotate(x[b], 12); x[b] ^= x[c];  x[c] = word(x[c] - x[d])
       x[d] = inv_rotate(x[d], 16); x[d] ^= x[a];  x[a] = word(x[a] - x[b])


    def _setup_state(self, key, iv):
        self._state = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]#good
        self._state.extend(bytes_to_words(key))#good
        self._state.append(self._counter)#good
        self._state.extend(bytes_to_words(iv)) #good
    def decrypt(self, c, key, iv):
        return self.encrypt(c, key, iv) #good

    def encrypt(self, m, key, iv):
        c = b''
        self._counter = 1 #good, counter resets for message
        for i in range(0, len(m), 64): #iterate
            self._setup_state(key, iv)
            for j in range(10):
                self._inner_block(self._state)
            #state isn't added?============
            c += xor(m[i:i+64], words_to_bytes(self._state)) #state is 64 bytes, this is fine
            self._counter += 1 #counter increment for next block
        
        return c
    def decrypt_state(self,state:bytes):
        state_words=bytes_to_words(state)
        for i in range(10):
            self._inv_inner_block(state_words)
        return words_to_bytes(state_words)

if __name__ == '__main__':
    msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'
    iv1 = bytes.fromhex('e42758d6d218013ea63e3c49')
    iv2 = bytes.fromhex('a99f9a7d097daabd2aa2a235')
    msg_enc = bytes.fromhex('f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c211ef5a52628094f09a30fc692cb25647f')
    msg_keystream=xor(msg_enc,msg)
    flag_enc = bytes.fromhex('b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0fe622b32732')
    c = ChaCha20()
    key=c.decrypt_state(msg_keystream[0:64])[16:48]
    msg_dec=c.decrypt(msg_enc,key,iv1)
    print(msg_dec)
    flag_dec=c.decrypt(flag_enc,key,iv2)
    print(f"iv1 = '{iv1.hex()}'")
    print(f"iv2 = '{iv2.hex()}'")
    print(f"msg_enc = '{msg_enc.hex()}'")
    print(f"flag_enc = '{flag_dec.decode()}'")
    print("message xor flag = {}".format(xor(msg,FLAG).hex()))
    print("E(message) xor E(flag) = {}".format(xor(msg_enc,flag_enc).hex()))
