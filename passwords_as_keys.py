import requests
import hashlib
from Crypto.Cipher import AES



def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}


encryptURL="https://aes.cryptohack.org/passwords_as_keys/encrypt_flag/"
decryptURL="https://aes.cryptohack.org/passwords_as_keys/decrypt/"


encrypted_text = requests.get(encryptURL).json()["ciphertext"]
print(encrypted_text)

with open("data/words.txt","r") as words:
    for line in words:
        word=line.strip()
        word_hash=hashlib.md5(word.encode()).digest()
        word_hash=word_hash.hex()
        print("Trying {}".format(word_hash))
        #decrypt_result=requests.get(decryptURL+encrypted_text+"/"+word_hash)
        decrypt_result=decrypt(encrypted_text,word_hash)
        #print(decrypt_result.text)
        if b'crypto' in bytes.fromhex(decrypt_result["plaintext"]):
            print(bytes.fromhex(decrypt_result["plaintext"]))
            break
