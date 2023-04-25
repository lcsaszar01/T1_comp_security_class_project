#!/usr/bin/env python3

import sys, subprocess
import Crypto.Cipher
from Crypto.Cipher import AES 
from Crypto.Util import Counter
from Crypto import Random
import secrets
import fileinput 
import codecs

key_bytes = 32

def aes_decrypt(ciphertext, key, digest, nonce):
    plaintext = ciphertext

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try: 
        plaintext = cipher.decrypt_and_verify(ciphertext, digest)
    except:
        print("Error: Wrong key please try again.")
        return -2

    return plaintext

def aes_encrypt(plaintext, key):
    ciphertext = ""
    
    cipher = AES.new(key, AES.MODE_EAX) 
    ciphertext, digest = cipher.encrypt_and_digest(plaintext)
    nonce = cipher.nonce # creation of random nonce value to ensure that it is not reused.

    return [ciphertext, digest, nonce]

def aes_decrypt_text(input_str, key, digest, nonce):
    ciphertext = ""
    try:
        if (len(input_str) == 0):
            print("Error: Cannot process an empty input string!")
            return -1
        else:
            ciphertext = input_str.encode("utf-8")
    except:
        ciphertext = input_str

    try: 
        if (len(key) != 16):
            print("Error: Key must be a 16-byte (character) key!")
            return -2
        else: 
            decrypt_key = key.encode('utf-8')
    except: 
        decrypt_key = key

    return aes_decrypt(ciphertext, decrypt_key, digest, nonce)

    
def aes_encrypt_text(input_str, key):
    encrypt_key = ""
    plaintext = ""
    try:
        if (len(input_str) == 0):
            print("Error: Cannot process an empty input string!")
            return -1
        else:
            plaintext = input_str.encode('utf-8')
    except: 
        plaintext = input_str

    try: 
        if (len(key) != 16):
            print("Error: Key must be a 16-byte (character) key!")
            return -2
        else: 
            encrypt_key = key.encode('utf-8')
    except: 
        encrypt_key = key

    return aes_encrypt(plaintext, encrypt_key)

def aes_encrypt_file(source_file, key_file, digest_file, nonce_file, dest_file):  
    plaintext = ""
    encrypt_key = ""

    try:
        with fileinput.input(files=(source_file)) as f:
            for line in f:
                 plaintext = plaintext + line
    except: 
        print("Error: Invalid Input File Selected!")
        return -1

    try: 
        with fileinput.input(files=(key_file)) as f:
            i = 0
            for line in f:
                if (i == 0):
                    key = line
                    i += 1
                else:
                    print("Too many keys entered! Using first key ", line, " only!")
    except:
        print("Error: Invalid Key File Selected!")
        return -2

    try:
        if (len(plaintext) == 0):
            print("Error: Cannot process an empty input string!")
            return -1
        else:
            plaintext = plaintext.encode('utf-8')
    except: 
        plaintext = plaintext

    try: 
        if (len(key) != 16):
            print("Error: Key must be a 16-byte (character) key!")
            return -2
        else: 
            encrypt_key = key.encode('utf-8')
    except: 
        encrypt_key = key

    ciphertext = aes_encrypt(plaintext, encrypt_key)

    try:
        with open(dest_file, 'w') as f:
            f.write(str(ciphertext[0]))
            f.close()
    except:
        print("Error: Failed to Create File")
        return -3

    try:
        with open(digest_file, 'w') as f:
            f.write(str(ciphertext[1]))
            f.close()
    except:
        print("Error: Failed to Create File")
        return -3

    try:
        with open(nonce_file, 'w') as f:    
            f.write(str(ciphertext[2]))
            f.close()
    except:
        print("Error: Failed to Create File")
        return -3

    return 0

def aes_decrypt_file(source_file, key_file, digest_file, nonce_file, dest_file):
    ciphertext = ""
    digest = ""
    nonce = ""
    decrypt_key = ""

    try:
        with fileinput.input(files=(source_file)) as f:
            for line in f:
                 ciphertext = ciphertext + line
    except: 
        print("Error: Invalid Input File Selected!")
        return -1

    try: 
        with fileinput.input(files=(key_file)) as f:
            i = 0
            for line in f:
                if (i == 0):
                    decrypt_key = line
                    i += 1
                else:
                    print("Too many keys entered! Using first key ", line, " only!")
    except:
        print("Error: Invalid Key File Selected!")
        return -2

    try:
        if (len(ciphertext) == 0):
            print("Error: Cannot process an empty input string!")
            return -1
        else:
            ciphertext = ciphertext.encode('utf-8')
    except: 
        ciphertext = ciphertext

    try: 
        if (len(decrypt_key) != 16):
            print("Error: Key must be a 16-byte (character) key!")
            return -2
        else: 
            decrypt_key = decrypt_key.encode('utf-8')
    except: 
        decrypt_key = decrypt_key


    try:
        with fileinput.input(files=(nonce_file)) as f:
            for line in f:
                 nonce = nonce + line
    except: 
        print("Error: Invalid Input File Selected!")
        return -1

    try:
        with fileinput.input(files=(digest_file)) as f:
            for line in f:
                 digest = digest + line
    except: 
        print("Error: Invalid Input File Selected!")
        return -1

    try:
        if (len(nonce) == 0):
            print("Error: Cannot process an empty input string!")
            return -1
        else:
            nonce = nonce.encode('utf-8')
    except: 
        nonce = nonce

    try: 
        if (len(digest) == 0):
            print("Error: Cannot process an empty input string!")
            return -2
        else: 
            digest = digest.encode('utf-8')
    except: 
        digest = digest

    plaintext = aes_decrypt(ciphertext, decrypt_key, digest, nonce)

    try:
        with open(dest_file, 'w') as f:
            print(ciphertext)
            f.write(str(ciphertext))
            f.close()
    except:
        print("Error: Failed to Create File")
        return -3
    return 0
     
# DEPRECATE FUNCTION ---------------------------------------------------------------------------
def new_func(key, message):
    # Code for the AES encryption
    # ENCRYPT
    default_key = b"More than a hero" #key of bit size 16, means we are using the AES-124 method
    default_message = b"I am Iron Man."
    if(len(key) == 0):
        key = default_key;
    else: 
        key = key.encode("utf-8")

    if(len(message)==0):
        message = default_message;
    else:
        message = message.encode("utf-8")

    print(message)

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

#if __name__ == "__main__":
#    output = new_func("1234567891111111", "1234567891111111")
#    output = aes_encrypt_text("1234567891111111", "1234567891111111")
#    aes_decrypt_text(output[0], "1234567891111111", output[1], output[2])
#    aes_encrypt_file("beemovie.txt", "aesKey.txt", "digest.txt", "nonce.txt", "beeAESencrypt.txt")
#    aes_decrypt_file("beeAESencrypt.txt", "aesKey.txt","digest.txt","nonce.txt", "beeAESdecrypt.txt")
#       print(aes_decrypt_text(output[0], output[1], output[2]))
#       output.decode("utf-8")
