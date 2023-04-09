import fileinput

def vigenere_cipher():
   print("Enter a key")
   key = list(input())
   print(key)

   print("Enter your filename")
   filename = input()
   plaintext = fileinput.input(files=(filename))
   print(plaintext)

if __name__ == "__main__":
    vigenere_cipher();