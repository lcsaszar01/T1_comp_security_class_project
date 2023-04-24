import string
import sys
import fileinput

####### ALL OPTIONS #######
# Type of alphabet: options[0]
# options[0]: "standard" (letters-only), "alphanum" (letters+numbers), "all" (ASCII)

# Conversion type (for letters-only option): options[1]
# options[1]: "lower" (all lowercase), "upper" (all uppercase), "default" (no conversion)

# Non-compliant Character Settings: options[2]
# options[2]: "ignore" (keep non-compliant characters), "remove" (remove characters)

# Print Output: options[3], options[4]
# options[3]: "preserve" (print out exactly as input), "prettify" (print in blocks of 8-characters)
# options[4]: 0-64 bit-size blocks

# Whitespace Options: options[5]
# options[5]: "literal" (displays & preserves whitespace characters), "ignore" (removes whitespace characters)

###### ERROR CODES ########
# -1: Invalid Input (Ciphertext/Plaintext Input)
# -2: Invalid Key
# -3: Other Error (Writing, Reading, etc.)
# -4: Bad Option Selection

def make_alphabet(options):
   alphabet = ""

   # Choose an alphabet #
   if (options[0] == "standard"):
       if (options[1] == "upper"):
           alphabet = string.ascii_uppercase
       elif (options[1] == "lower"):
           alphabet = string.ascii_lowercase
       elif (options[1] == "default"):
           alphabet = string.ascii_lowercase + string.ascii_uppercase
       else:
           print("Failed to produce alphabet! Check cipher options!", file=sys.stderr)
           sys.exit()
   elif (options[0] == "alphanum"):
       alphabet = string.ascii_letters + string.digits
   elif (options[0] == "all"):
       if (options[5] == "literal"):
           alphabet = string.printable
       elif (options[5] == "ignore"):
           alphabet = ""
           for c in string.printable:
               if c not in string.whitespace:
                   alphabet = alphabet + c
   else:
       print("Failed to produce alphabet! Check cipher options!", file=sys.stderr)
       return -4

   return alphabet

def modify_key(input_key, options):
    # Some Input --> Plaintext (string) Conversions #
    # Checks if input is standard vigenere cipher
    if (options[0] == "standard" and options[1] == "upper"):
        input_key = input_key.upper()
    elif (options[0] == "standard" and options[1] == "lower"):
        input_key = input_key.lower()
    return input_key

def modify_plaintext(input_str, options):
    # Some Input --> Plaintext (string) Conversions #
    # Checks if input is standard vigenere cipher
    if (options[0] == "standard" and options[1] == "upper"):
        input_str = input_str.upper()
    elif (options[0] == "standard" and options[1] == "lower"):
        input_str = input_str.lower()
    return input_str

def vigenere_encrypt(key, plaintext, dictionary, options):
    encrypt_result = ""
    max_enum = max(dictionary.values())
    pt_enum = 0 
    key_enum = 0
    key_index = 0

    # Error Case: Invalid Key
    for k in key:
        if k not in dictionary.keys():
             print("Key inside encryption function is invalid!", file=sys.stderr)
             return -2

    for c in plaintext:
        if c not in dictionary.keys():
            if (options[2] == "remove"):
                 # Do nothing (ignore the character)
                 encrypt_result = encrypt_result
            elif (options[2] == "ignore"):
                 # Keep character in cipher_result
                 encrypt_result = encrypt_result + c
            else: 
                 print("Failed to check non-compliance! Check cipher options!", file=sys.stderr)
                 return -4
        else:
            pt_enum = dictionary[c]
            key_enum = dictionary[key[key_index]]
 
            cipher_c = (pt_enum + key_enum) % max_enum
            encrypt_result = encrypt_result + list(dictionary.keys())[list(dictionary.values()).index(cipher_c)]
               
            key_index = key_index + 1
            if (key_index >= len(key)):
                key_index = 0
                  
    return encrypt_result

def vigenere_decrypt(key, ciphertext, dictionary, options):
    decrypt_result = ""
    max_enum = max(dictionary.values())
    ct_enum = 0 
    key_enum = 0
    key_index = 0

    # Error Case: Invalid Key
    for k in key:
        if k not in dictionary.keys():
             print("Key inside encryption function is invalid!", file=sys.stderr)
             return -2

    for c in ciphertext:
        if c not in dictionary.keys():
            if (options[2] == "remove"):
                 # Do nothing (ignore the character)
                 decrypt_result = decrypt_result
            elif (options[2] == "ignore"):
                 # Keep character in cipher_result
                 decrypt_result = decrypt_result + c
            else: 
                 print("Failed to check non-compliance! Check cipher options!", file=sys.stderr)
                 return -4
        else:
            ct_enum = dictionary[c]
            key_enum = dictionary[key[key_index]]

            plain_c = (ct_enum - key_enum) % max_enum
            decrypt_result = decrypt_result + list(dictionary.keys())[list(dictionary.values()).index(plain_c)]
               
            key_index = key_index + 1
            if (key_index >= len(key)):
                key_index = 0
             
    return decrypt_result

def vigenere_cipher_encrypt_file(source_file, key_file, dest_file, options):
    alphabet = make_alphabet(options)

    # Produces the enumerated alphabet #
    alpha_dict = dict((j,i) for i,j in enumerate(alphabet))

    # Fetches the input file & key # 
    plaintext = ""
    key = ""
    ciphertext = ""

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

    ciphertext = vigenere_encrypt(key, plaintext, alpha_dict, options)

    try: 
        with open(dest_file, "w") as f:
            output_str = ""
            if (options[3] == "preserve"):
                f.writelines(ciphertext)
            elif (options[3] == "prettify"):
                index = 0
                block = ""
                for c in ciphertext:
                    block = block + c
                    index = index + 1
                    if (index == options[4]):
                        output_str = output_str + block + " \n"
                        block = ""
                        index = 0
                        f.write(output_str)
                        output_str = ""
            f.close()
    except:
        print("Error: Failed to Create File")
        return -3

    return 0

def vigenere_cipher_decrypt_file(source_file, key_file, dest_file, options):
    alphabet = make_alphabet(options)

    # Produces the enumerated alphabet #
    alpha_dict = dict((j,i) for i,j in enumerate(alphabet))

    # Fetches the input file & key # 
    ciphertext = ""
    key = ""
    plaintext = ""

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
                    key = line
                    i += 1
                else:
                    print("Too many keys entered! Using first key ", line, " only!")
    except:
        print("Error: Invalid Key File Selected!")
        return -2

    plaintext = vigenere_decrypt(key, ciphertext, alpha_dict, options)

    try: 
        with open(dest_file, "w") as f:
            output_str = ""
            if (options[3] == "preserve"):
                f.writelines(plaintext)
            elif (options[3] == "prettify"):
                index = 0
                block = ""
                for c in plaintext:
                    block = block + c
                    index = index + 1
                    if (index == options[4]):
                        output_str = output_str + block + " \n"
                        block = ""
                        index = 0
                        f.write(output_str)
                        output_str = ""
            f.close()
    except:
        print("Error: Failed to Create File")
        return -3

    return 0

def vigenere_cipher_encrypt_text(source_str, key_str, options):
    # Makes proper alphabet based on provided options
    alphabet = make_alphabet(options)

    # Produces the enumerated alphabet
    alpha_dict = dict((j,i) for i,j in enumerate(alphabet))

    # Produces the corresponding ciphertext 
    ciphertext = vigenere_encrypt(key_str, source_str, alpha_dict, options)

    return ciphertext

def vigenere_cipher_decrypt_text(source_str, key_str, options):
    # Makes proper alphabet based on provided options
    alphabet = make_alphabet(options)

    # Produces the enumerated alphabet
    alpha_dict = dict((j,i) for i,j in enumerate(alphabet))

    # Produces the corresponding plaintext 
    plaintext = vigenere_decrypt(key_str, source_str, alpha_dict, options)

    return plaintext