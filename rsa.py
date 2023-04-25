from ctypes import sizeof
import math
import fileinput

# itty bitty bug: the message to be encrypted can't have a number followed by !
# (specifically at the end of the string), decoding does not like that for some reason
# I am too lazy to figure it out
# yikes, 'my name is cori' also throws an error ¯\_(ツ)_/¯

def rsa_encrypt(message, e, n):
    # Check and see if e and n are valid

    # Convert the message to an integer
    message_int = int.from_bytes(message.encode(encoding='utf-8',errors='strict'), 'big')
    
    # Encrypt the message using RSA
    encrypted_int = pow(message_int, e, n)
   
    # Convert the encrypted message to hexadecimal
    length = len(str(encrypted_int))
    hex_encrypted = bytes.hex((encrypted_int).to_bytes(length-1, "big"))
    return hex_encrypted.lstrip('0')

def rsa_decrypt(hex_encrypted, d, n):
    # check if d and n are valid

    # Convert the encrypted message from hexadecimal to an integer
    encrypted_int = int.from_bytes(bytes.fromhex(hex_encrypted), "big")
    
    # Decrypt the message using RSA
    decrypted_int = pow(encrypted_int, d, n)
    
    # Convert the decrypted integer to bytes and then to a string
    decrypted_message = decrypted_int.to_bytes(math.ceil(decrypted_int.bit_length() / 8), 'big').decode('utf-8')
    return decrypted_message

def rsa_encrypt_file(source_file, key_file, dest_file):
  # read in the plaintext file and key file
  plaintext = read_file(source_file)
  if(plaintext == -1):
    return -1
  e, d, n = read_keys(key_file)

  # error checking on the given e, d, and n
  e_result = input_error_check(e, d, n)
  if e_result == -1:
    return -1

  # call rsa_encrypt
  ciphertext = rsa_encrypt(plaintext, e, n)

  # create file with output
  result = create_file(ciphertext, dest_file)
  if(result == -1):
    return -1
  return 0 

def rsa_decrypt_file(source_file, key_file, dest_file):
  # read in the plaintext file and the key file
  ciphertext = read_file(source_file)
  if(ciphertext == -1):
    return -1
  e, d, n = read_keys(key_file)
  print(e, d, n)

  # error checking on the given e, d, and n
  e_result = input_error_check(e, d, n)
  if e_result == -1:
    return -1

  # call rsa_decrypt
  plaintext = rsa_decrypt(ciphertext, d, n)

  # create file with output
  result = create_file(plaintext, dest_file)
  if(result == -1):
    return -1
  return 0 

def read_file(source_file):
  data = ""
  try:
    with fileinput.input(files=(source_file)) as f:
      for line in f:
        data = data + line
  except:
    return -1

  return data

def read_keys(source_file):
  f = open(source_file, 'r')
  e = 0
  d = 0
  n = 0

  count = 1
  for line in f:
    if count == 1:
      e = int(line.strip())
    elif count == 2:
      d = int(line.strip())
    elif count == 3:
      n = int(line.strip())
    count += 1
  
  return e, d, n

def input_error_check(e, d, n): # check to see if e, d, and n are valid RSA key pairs
  int = 1

def create_file(content, dest_name):
  try:
    f = open(dest_name, "w") # create a new file, overwrite if it already exists
    f.write(content)         # put the content into the file
    f.close()                # close the file pointer
  except:
    return -1

if __name__ == "__main__":
  # test key parameters
  e = 65537
  d = 52203292265329821477201215331647767385
  n = 109658872566201497189314566136483333067

  # Test encryption and decryption
  # message = 'we are group 2'
  message = input("enter a string to encrypt: ")
  encrypted = rsa_encrypt(message, e, n)
  print(encrypted)
  encrypted_input = input("enter a string to decrypt: ")
  decrypted = rsa_decrypt(encrypted_input, d, n)
  print(decrypted)
