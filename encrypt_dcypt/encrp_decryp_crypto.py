import Crypto.Random
from Crypto.Cipher import AES
import hashlib

# salt size in bytes
SALT_SIZE = 4
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 2
# the size multiple required for AES
AES_MULTIPLE = 16

def generate_key(password, salt, iterations):
    assert iterations > 0
    key = password + salt
    print("generate_key : "+key)
    for i in range(iterations):
        key = hashlib.sha256(key.encode()).hexdigest()
    print("generate_key : "+key)
    return key

def pad_text(text, multiple):
    extra_bytes = len(text) % multiple
    padding_size = multiple - extra_bytes
    padding = chr(padding_size) * padding_size
    padded_text = text + padding
    print("pad_text : "+padded_text)
    return padded_text

def unpad_text(padded_text):
    padding_size = ord(padded_text[-1])
    text = padded_text[:-padding_size]
    return text

def encrypt(plaintext, password):
    salt = Crypto.Random.get_random_bytes(SALT_SIZE)
    key = generate_key(password, str(salt), NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_CBC)
    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    print("encrypt : "+ciphertext_with_salt)
    return ciphertext_with_salt

def decrypt(ciphertext, password):
    salt = ciphertext[0:SALT_SIZE]
    ciphertext_sans_salt = ciphertext[SALT_SIZE:]
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = cipher.decrypt(ciphertext_sans_salt)
    plaintext = unpad_text(padded_plaintext)
    return plaintext

encrypt("key","sravani")