import string
import sys
import fileinput

def vigenere_cipher():
   ############## OPTIONS FOR VIGENERE CIPHER ##############
   # Type of alphabet:
   # "standard" (letters-only), "alphanum" (letters+numbers), "all" (ASCII)
   alpha_type = "alphanum"

   # Conversion type (for letters-only option):
   # "lower" (all lowercase), "upper" (all uppercase), "default" (no conversion)
   convert_type = "default"

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
   alpha_dict = dict((j,i) for i,j in enumerate(alphabet, start=1))
   print(alpha_dict);

   # Fetches the input file & key #
      
   # print("Enter a key")
   # key = list(input())
   # print(key)

   # print("Enter your filename")
   # filename = input()
   # plaintext = fileinput.input(files=(filename))
   # print(plaintext)

   # Some Input --> Plaintext (string) Conversions

   # TESTING USING ONLY STRING #
   key = "apple"
   init_plaintext = "?439asdANJ#9fdas)(#$4tfcsdfsfd BEEMOVIE RULES a093njcosd0930j0fsd"
   
   print("Initial Key: " + key)
   print("Initial Plaintex: " + init_plaintext)

  

   # Begin Encryption Function
   def vigenere_encrypt(key, plaintext, dictionary):
       cipher_result = ""
       
       for c in plaintext:
           if c not in dictionary.keys():
               if (compliant_type == "remove"):
                    # Do nothing (ignore the character)
                    cipher_result = cipher_result
               elif (compliant_type == "ignore"):
                    # Keep character in cipher_result
                    cipher_result = cipher_result + c
               else: 
                    print("Failed to check non-compliance! Check cipher options!", file=sys.stderr)
                    sys.exit()
           else:
               cipher_result = cipher_result + c

       return cipher_result
   # Conversion: Key_enum + Plaintext_enum - 1
   # E.g. a=1, b=2, if key_enum=1, pt_enum=2, then conv=1+2-1=2 (cipher=2=b)
   # Begin Decryption Function

   def vigenere_decrypt(key, ciphertext):
       print("Do more stuff")
       return "dud"
   
   pt_to_ciphertext = vigenere_encrypt(key, init_plaintext, alpha_dict)
   # ct_to_plaintext = vigenere_decrypt(key, pt_to_ciphertext)

   print("Ciphertext is: " + pt_to_ciphertext)
   # print("Plaintext is: " + ct_to_plaintext)

if __name__ == "__main__":
    vigenere_cipher();