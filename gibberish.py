
import base64
import hashlib
import Crypto
import Crypto.Cipher.AES
import Crypto.Random
import Crypto.Util.Padding

"""
Mimic the Gibberish-AES JS library API. All constants are defaulted for AES-256.

Adapting the script for AES-128 et AES-192 should be relatively straightforward.
"""

def rawEncrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """Return the padded cipher text with the default blocksize of 16."""
    return Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CBC, iv=iv).encrypt(
        Crypto.Util.Padding.pad(plaintext, 16)
    )


def rawDecrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    return Crypto.Util.Padding.unpad(
        Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CBC, iv=iv).decrypt(ciphertext),
        16
    )


def openSSLKey(password: str, salt: bytes):
    salted_password = password.encode('utf-8') + salt
    hash_1 = hashlib.md5(salted_password).digest()
    hash_2 = hashlib.md5(hash_1 + salted_password).digest()
    hash_3 = hashlib.md5(hash_2 + salted_password).digest()
    return (hash_1 +  hash_2, hash_3)


def enc(plaintext: str, password: str):
    salt = Crypto.Random.get_random_bytes(8)
    return base64.b64encode(
        b'Salted__' + salt + rawEncrypt(plaintext.encode('utf-8'), *openSSLKey(password, salt))
    )


def dec(ciphertext: str, password: str):
    ciphertext = base64.b64decode(ciphertext)
    salt = ciphertext[8:16]
    ciphertext = ciphertext[16:]
    return rawDecrypt(ciphertext, *openSSLKey(password, salt))
