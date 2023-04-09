import string
import sys
import fileinput

def vigenere_cipher(key, input_str):
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
   print_type = "prettify"
   block_size = 8

   # Whitespace Options:
   # "literal" (displays & preserves whitespace characters), "ignore" (removes whitespace characters)
   keep_whitespace = "literal"
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
       if (keep_whitespace == "literal"):
           alphabet = string.printable
       elif (keep_whitespace == "ignore"):
           alphabet = ""
           for c in string.printable:
               if c not in string.whitespace:
                   alphabet = alphabet + c
   else:
       print("Failed to produce alphabet! Check cipher options!", file=sys.stderr)
       sys.exit()

   # Produces the enumerated alphabet #
   alpha_dict = dict((j,i) for i,j in enumerate(alphabet))
   # print("Dictionary: ", alpha_dict);

   # Fetches the input file & key # 
   init_plaintext = ""

   try:
       with fileinput.input(files=(input_str)) as f:
           for line in f:
                init_plaintext = init_plaintext + line
   except: 
       print("Not a File! Assuming input is a string.")
       init_plaintext = input_str

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
   
   def print_output(text, output_type):
       output_str = ""
       if (print_type == "preserve" or output_type == "plaintext"):
           print(text)
       elif (print_type == "prettify" and output_type == "cipher"):
           index = 0
           block = ""
           for c in text:
               block = block + c
               index = index + 1
               if (index == block_size):
                   output_str = output_str + block + " "
                   block = ""
                   index = 0
           output_str = output_str + block
       print(output_str)

   pt_to_ciphertext = vigenere_encrypt(key, init_plaintext, alpha_dict)
   ct_to_plaintext = vigenere_decrypt(key, pt_to_ciphertext, alpha_dict)
   
   print("Ciphertext is: ")
   print_output(pt_to_ciphertext, "cipher")
   print("Plaintext is: ")
   print_output(ct_to_plaintext, "plaintext")

if __name__ == "__main__":
    # vigenere_cipher("apple", "?439asdANJ#9fdas)(#$4tfcsdfsfd BEEMOVIE RULES a093njcosd0930j0fsd");
    vigenere_cipher("barrybeebenson??", "beemovie.txt")