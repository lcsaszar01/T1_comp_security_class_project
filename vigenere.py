import string
import sys
import fileinput

def vigenere_cipher():
   ############## OPTIONS FOR VIGENERE CIPHER ##############
   # Type of alphabet:
   # "standard" (letters-only), "alphanum" (letters+numbers), "all" (ASCII)
   alpha_type = "all"

   # Conversion type (for letters-only option):
   # "lower" (all lowercase), "upper" (all uppercase), "default" (no conversion)
   convert_type = "upper"

   # Non-compliant Character Settings:
   # "ignore" (keep non-compliant characters), "remove" (remove characters)
   compliant_type = "remove"

   # Print Output:
   # "preserve" (print out exactly as input), "prettify" (print in blocks of 8-characters)
   print_type = "preserve"

   # Print Output (whitespaces):
   # "show" (prints out whitespace characters), "literal" (print out exact characters)
   print_whitespace = "show"
   # END OPTIONS ####################

   # Choose an alphabet #
   if (alpha_type == "standard"):
       if (convert_type == "upper"):
           alphabet = string.ascii_uppercase
       elif (convert_type == "lower"):
           alphabet = string.ascii_lowercase
       elif (convert_type == "default"):
           alphabet = string.ascii_lowercase + string.ascii_uppercase
       else:
           print("Failed to produce alphabet! Check cipher options!", file=sys.stderr)
           sys.exit()
   elif (alpha_type == "alphanum"):
       alphabet = string.ascii_letters + string.digits
   elif (alpha_type == "all"):
       alphabet = string.printable
   else:
       print("Failed to produce alphabet! Check cipher options!", file=sys.stderr)
       sys.exit()

   # Produces the enumerated alphabet #
   alpha_dict = dict((j,i) for i,j in enumerate(alphabet))
   print(alpha_dict);

   # Fetches the input file & key # 
      
   # print("Enter a key")
   # key = list(input())
   # print(key)

   # print("Enter your filename")
   # filename = input()
   # plaintext = fileinput.input(files=(filename))
   # print(plaintext)



   # TESTING USING ONLY STRING #
   key = "apple"
   init_plaintext = "?439asdANJ#9fdas)(#$4tfcsdfsfd BEEMOVIE RULES a093njcosd0930j0fsd"

   # Some Input --> Plaintext (string) Conversions #
   # Checks if input is standard vigenere cipher
   if (alpha_type == "standard" and convert_type == "upper"):
       init_plaintext = init_plaintext.upper()
       key = key.upper()
   elif (alpha_type == "standard" and convert_type == "lower"):
       init_plaintext = init_plaintext.lower()
       key = key.lower()

   # Checks initial input 
   print("Initial Key: " + key)
   print("Initial Plaintext: " + init_plaintext)

   # Begin Encryption Function
   def vigenere_encrypt(key, plaintext, dictionary):
       encrypt_result = ""
       max_enum = max(dictionary.values())
       pt_enum = 0 
       key_enum = 0
       key_index = 0

       # Error Case: Invalid Key
       for k in key:
           if k not in alpha_dict.keys():
                print("Key inside encryption function is invalid!", file=sys.stderr)
                sys.exit()
       # Error Case: Invalid Plaintext

       # Error Case: Invalid Dictionary

       print("Value of key is: ", key[key_enum])
       print("Max Dictionary Value: ", max(dictionary.values()))
       
       for c in plaintext:
           if c not in dictionary.keys():
               if (compliant_type == "remove"):
                    # Do nothing (ignore the character)
                    encrypt_result = encrypt_result
               elif (compliant_type == "ignore"):
                    # Keep character in cipher_result
                    encrypt_result = encrypt_result + c
               else: 
                    print("Failed to check non-compliance! Check cipher options!", file=sys.stderr)
                    sys.exit()
           else:
               pt_enum = dictionary[c]
               key_enum = dictionary[key[key_index]]

               cipher_c = (pt_enum + key_enum) % max_enum
               encrypt_result = encrypt_result + list(dictionary.keys())[list(dictionary.values()).index(cipher_c)]
               
               key_index = key_index + 1
               if (key_index >= len(key)):
                   key_index = 0
                            
       return encrypt_result
   
   # Begin Decryption Function
   def vigenere_decrypt(key, ciphertext, dictionary):
       decrypt_result = ""
       max_enum = max(dictionary.values())
       ct_enum = 0 
       key_enum = 0
       key_index = 0

       # TODO: Error checking

       for c in ciphertext:
           if c not in dictionary.keys():
               if (compliant_type == "remove"):
                    # Do nothing (ignore the character)
                    decrypt_result = decrypt_result
               elif (compliant_type == "ignore"):
                    # Keep character in cipher_result
                    decrypt_result = decrypt_result + c
               else: 
                    print("Failed to check non-compliance! Check cipher options!", file=sys.stderr)
                    sys.exit()
           else:
               ct_enum = dictionary[c]
               key_enum = dictionary[key[key_index]]

               plain_c = (ct_enum - key_enum) % max_enum
               decrypt_result = decrypt_result + list(dictionary.keys())[list(dictionary.values()).index(plain_c)]
               
               key_index = key_index + 1
               if (key_index >= len(key)):
                   key_index = 0
             
       return decrypt_result
   
   pt_to_ciphertext = vigenere_encrypt(key, init_plaintext, alpha_dict)
   ct_to_plaintext = vigenere_decrypt(key, pt_to_ciphertext, alpha_dict)

   print("Ciphertext is: " + pt_to_ciphertext)
   print("Plaintext is: " + ct_to_plaintext)

if __name__ == "__main__":
    vigenere_cipher();