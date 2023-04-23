#!/usr/bin/env python3

import sys, subprocess
from Crypto.Cipher import AES 
import secrets

def main(key, message):

    #Code for the AES encryption
    
    #ENCRYPT
    default_key = b"More than a hero" #key of bit size 16, means we are using the AES-124 method
    default_message = b"I am Iron Man."
    if(len(key) == 0):
        key = default_key;
        
    if(len(message)==0):
        message = default_message;
        
    cipher = AES.new(default_key, AES.MODE_EAX) #
    nonce = cipher.nonce #creation of random nonce value to ensure that it is not reused.
    last_nonce = nonce
    if(nonce == last_nonce):
        nonce = cipher.nonce
        
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
        
    
    
#key = "";
#message = b"its a big bright beautiful tomorrow."
#main(key, message)
  
    
    