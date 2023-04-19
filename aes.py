#!/python/usr/bin python3

import sys, os, subprocess, pkg_resources
from cryptography.hazmat.primitives.ciphers.aead import AESOCB3

def main(input_data):

    #Code for the AES 256bit encryption
    try:
        data_message=input_data
    except: 
        data_message = b"It's kind of fun to do the impossible. - Walt Disney."
    aad = b"authenicated but unencrypted data."
    key = AESOCB3.generate_key(bit_length=256)
    aesocb = AESOCB3(key)
    nonce = os.urandom(15)
    encrypted_message = aesocb.encrypt(nonce,data_message,aad)
    return aesocb.decrypt(nonce, encrypted_message, aad)
    