from ctypes import sizeof
import math
import fileinput

def rsa_encrypt(message, e, n):
    # Convert the message to an integer
    message_int = int.from_bytes(message.encode(encoding='utf-8',errors='strict'), 'big')
    
    # Encrypt the message using RSA
    encrypted_int = pow(message_int, e, n)
   
    # Convert the encrypted message to hexadecimal
    length = len(str(encrypted_int))
    hex_encrypted = bytes.hex((encrypted_int).to_bytes(length-1, "big"))
    return hex_encrypted.lstrip('0')

def rsa_decrypt(hex_encrypted, d, n):
    # Convert the encrypted message from hexadecimal to an integer
    encrypted_int = int.from_bytes(bytes.fromhex(hex_encrypted), "big")
    
    # Decrypt the message using RSA
    decrypted_int = pow(encrypted_int, d, n)
    
    # Convert the decrypted integer to bytes and then to a string
    decrypted_message = decrypted_int.to_bytes(math.ceil(decrypted_int.bit_length() / 8), 'big').decode('utf-8')
    return decrypted_message

def rsa_encrypt_file(source_file, key_file):
  # read in the plaintext file and key file
  plaintext = read_file(source_file)
  if(plaintext == -1):
    return -1
  e, d, n = read_keys(key_file)
  if e==-1 and d==-1 and n==-1: # check for errors
    return -1

  # call rsa_encrypt
  ciphertext = rsa_encrypt(plaintext, e, n)

  # create file with output
  temp = source_file.split('.')
  dest_name = temp[0] + "-encrypted." + temp[1]
  result = create_file(ciphertext, dest_name)
  if(result == -1):
    return -1

def rsa_decrypt_file(source_file, key_file):
  # read in the plaintext file and the key file
  ciphertext = read_file(source_file)
  if(ciphertext == -1):
    return -1
  e, d, n = read_keys(key_file)
  if e==-1 and d==-1 and n==-1: # check for errors
    return -1

  # call rsa_decrypt
  plaintext = rsa_decrypt(ciphertext, d, n)

  # create file with output
  temp = source_file.split('-')
  f_type = temp[1].split('.')
  dest_name = temp[0] + "-decrypted." + f_type[1]
  result = create_file(plaintext, dest_name)
  if(result == -1):
    return -1

def read_file(source_file):
  data = ""
  try:
    with fileinput.input(files=(source_file)) as f:
      for line in f:
        data = data + line
    return data
  except:
    return -1

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
  
  if input_error_check(e, d, n)==False:
    return -1, -1, -1;
  
  return e, d, n;

def input_error_check(e, d, n): # check to see if e, d, and n are valid RSA key pairs
  message = "Hello" # test string
  cipher_int = int.from_bytes(message.encode(encoding='utf-8',errors='strict'), 'big')
  ciphertext = pow(cipher_int, e, n)
  plain_int = pow(ciphertext, d, n)
  return plain_int == cipher_int

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

  # test the keys
  valid = input_error_check(e, d, n)
  print(valid)

  # Test encryption and decryption
  message = 'we are group 2'
  encrypted = rsa_encrypt(message, e, n)
  print(encrypted)
  decrypted = rsa_decrypt(encrypted, d, n)
  print(decrypted)

  # test file encryption and decryption
  key_file = "rsa_keys.txt"
  og_file = "sample.txt"

  f_encrypt = rsa_encrypt_file(og_file, key_file)
  f_decrypt = rsa_decrypt_file("sample-encrypted.txt", key_file)
