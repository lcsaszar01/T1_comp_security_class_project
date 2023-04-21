#!/usr/bin/env python3

import sys, os, subprocess
from Crypto.Cipher import AES 

def main(key, message):

    #Code for the AES encryption
    
    #ENCRYPT
    default_key = b"More than a hero" #key of bit size 16, means we are using the AES-124 method
    if(len(key) == 0):
        key = default_key;
        
    cipher = AES.new(default_key, AES.MODE_EAX) #
    nonce = cipher.nonce #creation of random nonce value to ensure that it is not reused.
    ciphertext, digest_tag = cipher.encrypt_and_digest(message)
    
    print('The ciphertext is:', ciphertext)
    
    #DECRYPT
    cipher = AES.new(default_key, AES.MODE_EAX, nonce=nonce)
    plaintext=cipher.decrypt(ciphertext)
    
    try:
        cipher.verify(digest_tag)
        print("Message is authentic:", plaintext)
    except ValueError:
        print("Error: Wrong key please try again.")
    
    
key = "";
message = b"its a big bright beautiful tomorrow."
main(key, message)
  
    
    