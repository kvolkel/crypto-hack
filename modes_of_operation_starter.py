import requests

challengeURLencrypt="https://aes.cryptohack.org/block_cipher_starter/encrypt_flag/"
challengeURLdecrypt="https://aes.cryptohack.org/block_cipher_starter/decrypt/"
r = requests.get(challengeURLencrypt)

cipher_text = r.json()["ciphertext"]

r = requests.get(challengeURLdecrypt+cipher_text)

plaintext=r.json()["plaintext"]

print(bytes.fromhex(plaintext))
