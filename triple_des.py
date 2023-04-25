# Triple DES
# from tkinter.tix import InputOnly
# from venv import create
# from xmlrpc.client import _binary
import math as math


def print_intArr(label_str, arr_len, arr):
    temp_str = ""
    for c in label_str:
        if (c == '\0'):
            break
        else:
            temp_str = temp_str + c
    print(temp_str)
    print(" = ")
    temp_str = "" 
    i = 0
    for i in range(0,arr_len):
        temp_str = temp_str + str(arr[i])
    print(temp_str)

def print_charArr(label_str, arr_len, arr):
    temp_str = ""
    for c in label_str:
        if (c == '\0'):
            break
        else:
            temp_str = temp_str + c 
    print(temp_str)
    print(" = ")
    temp_str = ""
    for c in arr:
        temp_str = temp_str + c 
    print(temp_str)

S =   [[[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
                      [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
                      [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
                      [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]], 
                     [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
                      [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
                      [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
                      [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]],
                     [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
                      [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
                      [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
                      [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],
                     [[ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
                      [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
                      [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
                      [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],
                     [[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
                      [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
                      [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
                      [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]],
                     [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
                      [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
                      [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
                      [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],
                     [[ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
                      [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
                      [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
                      [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],
                     [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
                      [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
                      [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
                      [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]];
    
P = [   16,  7, 20, 21,
                29, 12, 28, 17,
                 1, 15, 23, 26,
                 5, 18, 31, 10,
                 2,  8, 24, 14,
                32, 27,  3,  9,
                19, 13, 30,  6,
                22, 11,  4, 25];

IP_1 = [40, 8, 48, 16, 56, 24, 64, 32,
                39, 7, 47, 15, 55, 23, 63, 31,
                38, 6, 46, 14, 54, 22, 62, 30,
                37, 5, 45, 13, 53, 21, 61, 29,
                36, 4, 44, 12, 52, 20, 60, 28,
                35, 3, 43, 11, 51, 19, 59, 27,
                34, 2, 42, 10, 50, 18, 58, 26,
                33, 1, 41, 9 , 49, 17, 57, 25];

PC1 = [ 57,49,41,33,25,17,9 ,
                1 ,58,50,42,34,26,18,
                10,2 ,59,51,43,35,27,
                19,11,3 ,60,52,44,36,
                63,55,47,39,31,23,15,
                7 ,62,54,46,38,30,22,
                14,6 ,61,53,45,37,29,
                21,13,5 ,28,20,12,4 ];

Lshift = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1];

PC2 = [ 14,17,11,24,1 ,5 ,
                3 ,28,15,6 ,21,10,
                23,19,12,4 ,26,8 ,
                16,7 ,27,20,13,2 ,
                41,52,31,37,47,55,
                30,40,51,45,33,48,
                44,49,39,56,34,53,
                46,42,50,36,29,32];

IP_Table = [ 58,50,42,34,26,18,10,2,
                    60,52,44,36,28,20,12,4,
                    62,54,46,38,30,22,14,6,
                    64,56,48,40,32,24,16,8,
                    57,49,41,33,25,17,9 ,1,
                    59,51,43,35,27,19,11,3,
                    61,53,45,37,29,21,13,5,
                    63,55,47,39,31,23,15,7];

E_Table = [ 32,1 ,2 ,3 ,4 ,5 ,
                    4 ,5 ,6 ,7 ,8 ,9 ,
                    8 ,9 ,10,11,12,13,
                    12,13,14,15,16,17,
                    16,17,18,19,20,21,
                    20,21,22,23,24,25,
                    24,25,26,27,28,29,
                    28,29,30,31,32,1 ];

def XOR(k, er):
    if (k == er):
        return 0
    else:
        return 1

def charArrToIntArr(arr_char, arr_len):
    arr_int = create_array(arr_len)
    for i in range(0, arr_len):
        if (arr_char[i] == '0'):
            arr_int[i] = 0
        else:
            arr_int[i] = 1
    return arr_int

def intArrToCharArr(arr_int, arr_len):
    arr_char = create_array(arr_len)
    for i in range(0, arr_len):
        if (arr_int[i] == 0):
            arr_char[i] = '0'
        else:
            arr_char[i] = '1'
    return arr_char

def strToBinary(input_str):
    temp = ""
    for k in range(0, 8):
        temp = temp + str(input_str[k])
    binary = ''.join(format(ord(x), '08b') for x in temp)
    return binary

def binaryToString(binary_int): 
    binary = intArrToCharArr(binary_int, 64)
    ascii_str = ""
    arr_len = 64
    char_str = create_array(8)
    # c = 0

    for i in range(0, arr_len, 8):
        j = 0
        for k in range(i, i+8):
            char_str[j] = binary[k]
            j = j + 1

            decimal_value = 0
            base = 1

            for i in range(7, -1, -1):
                if (char_str[i] == '1'):
                    decimal_value = decimal_value + base
                base = base * 2

                ascii_str = ascii_str + chr(decimal_value)
                # c = c + 1

    return ascii_str

def create_matrix(rows, cols):
    new_matrix = []
    for i in range(0,rows):
        new_matrix.append([])
        for c in range(0,cols):
            new_matrix[i].append(0)
    return new_matrix

def create_array(elem): 
    new_arr = [] 
    for i in range(0, elem):
        new_arr.append(0)
    return new_arr

def des_decrypt(m, k0):
    output = []
    K0 = create_array(64)
    M = create_array(64)

    # Copies input into working arrays
    for i in range(0, 64):
        K0[i] = k0[i]
        M[i] = m[i]

    # Left of Message
    Lm = create_array(32)
    for i in range(0, 32):
        Lm[i] = M[i]

    # Right of Message
    Rm = create_array(32)
    for i in range(32, 64):
        Rm[i-32] = M[i]

    # Step 1
    Kplus = create_array(56)
    for i in range(0, 56):
        Kplus[i] = K0[(PC1[i]-1)]

    C = create_matrix(17, 28)
    D = create_matrix(17, 28)

    for i in range(0, 28):
        C[0][i] = Kplus[i]
        D[0][i] = Kplus[i+28]

    for n in range(1, 17):
        if (Lshift[n-1] == 1):
            for i in range(0, 27):
                C[n][i]=C[n-1][i+1]
                D[n][i]=D[n-1][i+1]
            C[n][27] = C[n-1][0]
            D[n][27] = D[n-1][0]
        if (Lshift[n-1] == 2):
            for i in range(0, 26):
                C[n][i]=C[n-1][i+2]
                D[n][i]=D[n-1][i+2]
            C[n][26] = C[n-1][0]
            D[n][26] = D[n-1][0]
            C[n][27] = C[n-1][1]
            D[n][27] = D[n-1][1]

    CD = create_matrix(17, 56)
    for n in range(0, 17):
        for i in range(0, 28):
            CD[n][i] = C[n][i]
            CD[n][i+28] = D[n][i]

    K_en = create_matrix(17, 48)
    K = create_matrix(17, 48)

    for n in range(0, 17):
        for i in range(0, 48):
            K_en[n][i] = CD[n][(PC2[i]-1)]

    for n in range(1, 17):
        for i in range(0, 48):
            K[n][i] = K_en[17-n][i] # keys in reverse order for decryption

    # Step 2
    IP = create_array(64)
    for i in range(0, 64):
        IP[i] = M[(IP_Table[i]-1)]

    L = create_matrix(17, 32)
    for i in range(0, 32):
        L[0][i] = IP[i]

    R = create_matrix(17, 32)
    for i in range(32, 64):
        R[0][i-32] = IP[i]

    E_R = create_matrix(16, 48)
    Kn_xor_ER = create_matrix(16, 48)

    for n in range(1, 17):
        B = create_matrix(8,6)         # 8 groups of 6 bits
        sr = create_matrix(8,2)        # 8 s box row indices --> 2 bits
        sc = create_matrix(8,4)        # 8 s box columb indices --> 4 bits
        sr_ind = create_array(8)       # 8 s box row indices 
        sc_ind = create_array(8)       # 8 s box column indices 
        s_val = create_array(8)        # 8 s box found values
        s_val_bin = create_matrix(8,4) # 8 s box found values --> 4 bits
     
        # L_(n) = R(n-1)
        for i in range(0, 32):
            L[n][i] = R[n-1][i]

        for i in range(0, 48):
            E_R[n-1][i] = R[n-1][E_Table[i]-1]         # R_(n-1) from 32 to 48 bits using E table
            Kn_xor_ER[n-1][i]=XOR(K[n][i],E_R[n-1][i]) # K_(n) XOR E(R_(n-1))

        for k in range(0, 8):
            for c in range(0, 6):
                B[k][c] = Kn_xor_ER[n-1][c+k*6]  # split into 8 groups of 6 bits

            # first and last of each gives row
            sr[k][0] = B[k][0]
            sr[k][1] = B[k][5]
            
            sr_ind[k]= B[k][0]*2 + B[k][5]
            
            # middle 4 give column
            sc[k][0] = B[k][1]
            sc[k][1] = B[k][2]
            sc[k][2] = B[k][3]
            sc[k][3] = B[k][4]
            
            sc_ind[k] = 0;

            c = 0
            for b in range(3,-1,-1):
                sc_ind[k] = sc_ind[k] + (sc[k][b]*pow(2,c))
                c = c + 1
            
            # lookup target value
            s_val[k] = S[k][sr_ind[k]][sc_ind[k]];
            s_val_temp = s_val[k];
            
            # s box found value to 4 bits binary
            for d in range(3,-1,-1):
                s_val_bin[k][d] = s_val_temp % 2;
                s_val_temp = s_val_temp/2;

        sComb = create_array(32)
        a = 0
        while a < 32:
            for k in range(0, 8):
                for d in range(0, 4):
                    sComb[a] = s_val_bin[k][d]
                    a = a + 1

        f = create_array(32)
        for i in range(0, 32):
            f[i] = sComb[(P[i]-1)] # permutation from table P
            R[n][i] = XOR(L[n-1][i],f[i]); # R_(n) = L_(n-1) XOR f(R_(n-1),K_n)

    R16L16 = create_array(64)
    for i in range(0, 32):
        R16L16[i] = R[16][i]
        R16L16[32+i] = L[16][i]
    
    for i in range(0, 64):
        output.append(R16L16[(IP_1[i]-1)])

    return output

def des_encrypt(m, k0):
    output = []
    K0 = create_array(64)
    M = create_array(64)

    # Copies input into working arrays
    for i in range(0, 64):
        K0[i] = k0[i]
        M[i] = m[i]

    # Left of Message
    Lm = create_array(32)
    for i in range(0, 32):
        Lm[i] = M[i]

    # Right of Message
    Rm = create_array(32)
    for i in range(32, 64):
        Rm[i-32] = M[i]

    # Step 1
    Kplus = create_array(56)
    for i in range(0, 56):
        Kplus[i] = K0[(PC1[i]-1)]

    C = create_matrix(17, 28)
    D = create_matrix(17, 28)

    for i in range(0, 28):
        C[0][i] = Kplus[i]
        D[0][i] = Kplus[i+28]

    for n in range(1, 17):
        if (Lshift[n-1] == 1):
            for i in range(0, 27):
                C[n][i]=C[n-1][i+1]
                D[n][i]=D[n-1][i+1]
            C[n][27] = C[n-1][0]
            D[n][27] = D[n-1][0]
        if (Lshift[n-1] == 2):
            for i in range(0, 26):
                C[n][i]=C[n-1][i+2]
                D[n][i]=D[n-1][i+2]
            C[n][26] = C[n-1][0]
            D[n][26] = D[n-1][0]
            C[n][27] = C[n-1][1]
            D[n][27] = D[n-1][1]

    CD = create_matrix(17, 56)
    for n in range(0, 17):
        for i in range(0, 28):
            CD[n][i] = C[n][i]
            CD[n][i+28] = D[n][i]

    K_en = create_matrix(17, 48)
    K = create_matrix(17, 48)

    for n in range(0, 17):
        for i in range(0, 48):
            K_en[n][i] = CD[n][(PC2[i]-1)]

    for n in range(1, 17):
        for i in range(0, 48):
            K[n][i] = K_en[n][i] # keys in reverse order for decryption

    # Step 2
    IP = create_array(64)
    for i in range(0, 64):
        IP[i] = M[(IP_Table[i]-1)]

    L = create_matrix(17, 32)
    for i in range(0, 32):
        L[0][i] = IP[i]

    R = create_matrix(17, 32)
    for i in range(32, 64):
        R[0][i-32] = IP[i]

    E_R = create_matrix(16, 48)
    Kn_xor_ER = create_matrix(16, 48)

    for n in range(1, 17):
        B = create_matrix(8,6)         # 8 groups of 6 bits
        sr = create_matrix(8,2)        # 8 s box row indices --> 2 bits
        sc = create_matrix(8,4)        # 8 s box columb indices --> 4 bits
        sr_ind = create_array(8)       # 8 s box row indices 
        sc_ind = create_array(8)       # 8 s box column indices 
        s_val = create_array(8)        # 8 s box found values
        s_val_bin = create_matrix(8,4) # 8 s box found values --> 4 bits
     
        # L_(n) = R(n-1)
        for i in range(0, 32):
            L[n][i] = R[n-1][i]

        for i in range(0, 48):
            E_R[n-1][i] = R[n-1][E_Table[i]-1]         # R_(n-1) from 32 to 48 bits using E table
            Kn_xor_ER[n-1][i]=XOR(K[n][i],E_R[n-1][i]) # K_(n) XOR E(R_(n-1))

        for k in range(0, 8):
            for c in range(0, 6):
                B[k][c] = Kn_xor_ER[n-1][c+k*6]  # split into 8 groups of 6 bits

            # first and last of each gives row
            sr[k][0] = B[k][0]
            sr[k][1] = B[k][5]
            
            sr_ind[k]= B[k][0]*2 + B[k][5]
            
            # middle 4 give column
            sc[k][0] = B[k][1]
            sc[k][1] = B[k][2]
            sc[k][2] = B[k][3]
            sc[k][3] = B[k][4]
            
            sc_ind[k] = 0;

            c = 0
            for b in range(3,-1,-1):
                sc_ind[k] = sc_ind[k] + (sc[k][b]*pow(2,c))
                c = c + 1
            
            # lookup target value
            s_val[k] = S[k][sr_ind[k]][sc_ind[k]];
            s_val_temp = s_val[k];
            
            # s box found value to 4 bits binary
            for d in range(3,-1,-1):
                s_val_bin[k][d] = s_val_temp % 2;
                s_val_temp = s_val_temp/2;

        sComb = create_array(32)
        a = 0

        while a < 32:
            for k in range(0, 8):
                for d in range(0, 4):
                    sComb[a] = s_val_bin[k][d]
                    a = a + 1
        print(B)
        f = create_array(32)
        for i in range(0, 32):
            f[i] = sComb[(P[i]-1)] # permutation from table P
            R[n][i] = XOR(L[n-1][i],f[i]); # R_(n) = L_(n-1) XOR f(R_(n-1),K_n)

    R16L16 = create_array(64)
    for i in range(0, 32):
        R16L16[i] = R[16][i]
        R16L16[32+i] = L[16][i]
    
    for i in range(0, 64):
        output.append(R16L16[(IP_1[i]-1)])
    return output

def triple_des_decrypt(m, k1, k2, k3):
    output1 = create_array(64)
    output2 = create_array(64)
    output1 = des_decrypt(m, k3)

    output2 = des_encrypt(output1, k2)
    output = des_decrypt(output2, k1)

    return output 

def triple_des_encrypt(m, k1, k2, k3):
    output1 = create_array(64)
    output2 = create_array(64)

    print(m)
    output1 = des_encrypt(m, k3)
    output2 = des_decrypt(output1, k2)
    output = des_encrypt(output2, k1)
    print(output)
    return output 

def triple_des_decrypt_text(input_binary, key1_str, key2_str, key3_str):
    output_str = []
    key1_binary = create_array(64)
    key2_binary = create_array(64)
    key3_binary = create_array(64)

    arr_len = 0
    while (input_binary[arr_len] == 1 or input_binary[arr_len] == 0) and len(input_binary)-1 != arr_len:
        arr_len = arr_len + 1
    key1_binary = strToBinary(key1_str)
    key2_binary = strToBinary(key2_str)
    key3_binary = strToBinary(key3_str)
    
    input_64bit_chunk = create_array(64)
    output_chunk_binary = create_array(64)
    output_chunk_char = create_array(8)
    j = 0
    # c = 0
    
    print(arr_len)
    for i in range(0, arr_len, 64):
        j = 0
        for k in range(i, i+64):
            input_64bit_chunk[j] = input_binary[k]
            j = j + 1
        output_chunk_binary = triple_des_decrypt(input_64bit_chunk, key1_binary, key2_binary, key3_binary)
        output_chunk_char = binaryToString(output_chunk_binary)

        for k in range(0, 8):
            output_str.append(output_chunk_char[k])
            # c = c+1

    return output_str

def triple_des_encrypt_text(input_str, key1_str, key2_str, key3_str):
    output_binary = []
    key1_binary = create_array(64)
    key2_binary = create_array(64)
    key3_binary = create_array(64)

    # takes the first 8 characters of each key and turns them into their 64-bit binary equivalent
    key1_binary = strToBinary(key1_str)
    key2_binary = strToBinary(key2_str)
    key3_binary = strToBinary(key3_str)

    # pads the input str so that its length is a multiple of 64 bits
    num_8char_chunks = len(input_str) / 8
    len_padded = num_8char_chunks * 8
    if (len(input_str) % 8 != 0):
        len_padded = len_padded + 8
  
    input_str_padded = create_array(int(len_padded))
    for i in range(0, int(len_padded)):
        if (i < len(input_str)):
            input_str_padded.append(input_str[i])
        else:
            input_str_padded.append('0')

    input_8char_chunk = []
    input_chunk_binary = []
    output_chunk_binary = [] 
    j = 0
    c = 0

    for p in range(0, int(len_padded), 8):
        j = 0
        for k in range(p, p+8):
            input_8char_chunk.append(input_str_padded[k])
            j = j + 1
        input_chunk_binary = strToBinary(input_8char_chunk)
        output_chunk_binary = triple_des_encrypt(input_chunk_binary, key1_binary, key2_binary, key3_binary)
        
        for k in range(0, 64):
            output_binary.append(output_chunk_binary[k])
            c = c + 1
    return output_binary

if __name__ == "__main__":
    print("TESTING")
    input_str = "tripledestestcomputersecurityfinalproject"
    key1 = "firstkey"
    key2 = "testkey2"
    key3 = "keykeyke"

    input_len = len(input_str)
    encrypted_len = 0

    if (input_len % 8 == 0):
        encrypted_len = input_len * 8
    else: 
        chunks = input_len / 8
        encrypted_len = (chunks + 1) * 64

    encrypted = []
    decrypted = [] 

    # print_charArr("Original", input_len, input_str)
    encrypted = triple_des_encrypt_text(input_str, key1, key2, key3)
    # print_intArr("Encrypted", int(encrypted_len), encrypted)
    decrypted = triple_des_decrypt_text(encrypted, key1, key2, key3)
    print_charArr("Decrypted", int((encrypted_len / 8)), decrypted)
