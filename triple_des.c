#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>
#include <string.h>

void print_intArr(char label_str[], int len, int arr[]){
    int i = 0;
    while (label_str[i]!='\0'){
        printf("%c", label_str[i]);
        i++;
    }
    printf(" = ");
    for (i=0; i<len; i++){
        printf("%d", arr[i]);
    }
    printf("\n");
}

void print_charArr(char label_str[], int len, char arr[]){
    int i = 0;
    while (label_str[i]!='\0'){
        printf("%c", label_str[i]);
        i++;
    }
    printf(" = ");
    for (i=0; i<len; i++){
        printf("%c", arr[i]);
    }
    printf("\n");
}

int S[8][4][16] =   {{{14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7},
                      { 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8},
                      { 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0},
                      {15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13}},
                      
                     {{15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10},
                      { 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5},
                      { 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15},
                      {13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9}},

                     {{10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8},
                      {13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1},
                      {13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7},
                      { 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12}},
                     {{ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15},
                      {13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9},
                      {10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4},
                      { 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14}},
                     {{ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9},
                      {14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6},
                      { 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14},
                      {11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3}},
                     {{12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11},
                      {10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8},
                      { 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6},
                      { 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13}},
                     {{ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1},
                      {13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6},
                      { 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2},
                      { 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12}},
                     {{13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7},
                      { 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2},
                      { 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8},
                      { 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11}}};
    
int P[32] = {   16,  7, 20, 21,
                29, 12, 28, 17,
                 1, 15, 23, 26,
                 5, 18, 31, 10,
                 2,  8, 24, 14,
                32, 27,  3,  9,
                19, 13, 30,  6,
                22, 11,  4, 25};

int IP_1[64] = {40, 8, 48, 16, 56, 24, 64, 32,
                39, 7, 47, 15, 55, 23, 63, 31,
                38, 6, 46, 14, 54, 22, 62, 30,
                37, 5, 45, 13, 53, 21, 61, 29,
                36, 4, 44, 12, 52, 20, 60, 28,
                35, 3, 43, 11, 51, 19, 59, 27,
                34, 2, 42, 10, 50, 18, 58, 26,
                33, 1, 41, 9 , 49, 17, 57, 25};

int PC1[56] = { 57,49,41,33,25,17,9 ,
                1 ,58,50,42,34,26,18,
                10,2 ,59,51,43,35,27,
                19,11,3 ,60,52,44,36,
                63,55,47,39,31,23,15,
                7 ,62,54,46,38,30,22,
                14,6 ,61,53,45,37,29,
                21,13,5 ,28,20,12,4 };

int Lshift[16] = {1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1};

int PC2[48] = { 14,17,11,24,1 ,5 ,
                3 ,28,15,6 ,21,10,
                23,19,12,4 ,26,8 ,
                16,7 ,27,20,13,2 ,
                41,52,31,37,47,55,
                30,40,51,45,33,48,
                44,49,39,56,34,53,
                46,42,50,36,29,32};

int IP_Table[64] ={ 58,50,42,34,26,18,10,2,
                    60,52,44,36,28,20,12,4,
                    62,54,46,38,30,22,14,6,
                    64,56,48,40,32,24,16,8,
                    57,49,41,33,25,17,9 ,1,
                    59,51,43,35,27,19,11,3,
                    61,53,45,37,29,21,13,5,
                    63,55,47,39,31,23,15,7};
                    
int E_table[48] = { 32,1 ,2 ,3 ,4 ,5 ,
                    4 ,5 ,6 ,7 ,8 ,9 ,
                    8 ,9 ,10,11,12,13,
                    12,13,14,15,16,17,
                    16,17,18,19,20,21,
                    20,21,22,23,24,25,
                    24,25,26,27,28,29,
                    28,29,30,31,32,1 };
    
int xor(int k, int er){
    if (k==er){
        return 0;
    } else {
        return 1;
    }
}

void charArrToIntArr(char arr_char[], int *arr_int, int len){
    for (int i = 0; i<len; i++){
        if (arr_char[i] == '0') { arr_int[i] = 0; } else { arr_int[i] = 1; }
    }
}

void intArrToCharArr(int arr_int[], char *arr_char, int len){
    for (int i = 0; i<len; i++){
        if (arr_int[i] == 0) { arr_char[i] = '0'; } else { arr_char[i] = '1'; }
    }
}

void strToBinary(char str[8], int *binary){
    int c = 0;
    for (int k = 0; k<8; k++){
        for(int i = 7; i >= 0; i--){
            binary[c] = ( unsigned int )( ( str[k] & (1 << i) ) ? 1 : 0);
            c++;
        }
    }
}

void binaryToStr(int binary_int[64], char *ascii_str){
    char binary[64];
    intArrToCharArr(binary_int, binary,64);
    int len = 64;
    int c = 0;
    char char_str[8];
    int decimal_value;
    int base;
    
    for (int i = 0; i<len; i+=8){
        int j = 0;
        for (int k = i; k<i+8; k++){
            char_str[j] = binary[k];
            j++;
        }

        decimal_value = 0;
        base = 1;
        for (int i = 7; i>=0; i--){
            if (char_str[i]=='1'){
                decimal_value+=base;
            }
            base = base*2;
        }

        ascii_str[c] = (char)decimal_value;
        c++;
    }
}

void des_decrypt(int m[64], int k0[64], int *output){

    int K0[64];
    int M[64];

    // copies input into working arrays
    for (int i = 0; i<64; i++){
        K0[i] = k0[i];
        M[i] = m[i];
    }
    
    // left of message
    int Lm[32];
    for(int i = 0; i<32; i++){
        Lm[i] = M[i];
    }
    
    // right of message
    int Rm[32];
    for(int i = 32; i<64; i++){
        Rm[i-32] = M[i];
    }
    
    //STEP 1    
    int Kplus[56];
    for (int i = 0; i<56; i++){
        Kplus[i] = K0[(PC1[i]-1)];
    }
    
    int C[17][28];
    int D[17][28];
    
    for(int i = 0; i<28; i++){
        C[0][i] = Kplus[i];
        D[0][i] = Kplus[i+28];
    }
    
    for (int n = 1; n<17; n++){
        if (Lshift[n-1]==1){
            for (int i = 0; i<27; i++){
                C[n][i]=C[n-1][i+1];
                D[n][i]=D[n-1][i+1];
            }
            C[n][27] = C[n-1][0];
            D[n][27] = D[n-1][0];
        }
        if (Lshift[n-1]==2){
            for (int i = 0; i<26; i++){
                C[n][i]=C[n-1][i+2];
                D[n][i]=D[n-1][i+2];
            }
            C[n][26] = C[n-1][0];
            D[n][26] = D[n-1][0];
            C[n][27] = C[n-1][1];
            D[n][27] = D[n-1][1];
        }
        
    }
    
    int CD[17][56];
    for (int n = 0; n<17; n++){
        for (int i = 0; i<28; i++){
            CD[n][i] = C[n][i];
            CD[n][i+28] = D[n][i];
        }
    }
    
    
    int K_en[17][48];
    int K[17][48];
    
    for (int n = 0; n<17; n++){
        for (int i = 0; i<48; i++){
            K_en[n][i] = CD[n][(PC2[i]-1)];
        }
    }
    
    for(int n = 1; n<17; n++){
        for (int i = 0; i<48; i++){
            K[n][i] = K_en[17-n][i]; // keys in reverse order for decryption
        }
    }
    
    //STEP 2
    int IP[64];
    for(int i = 0; i<64; i++){
        IP[i] = M[IP_Table[i]-1];
    }
    
    int L[17][32];
    for(int i = 0; i<32; i++){
        L[0][i] = IP[i];
    }
    
    int R[17][32];
    for(int i = 32; i<64; i++){
        R[0][i-32] = IP[i];
    }
    
    int E_R[16][48];
    int Kn_xor_ER[16][48];

    
    for(int n = 1; n<17; n++){
        int B[8][6];        // 8 groups of 6 bits
        int sr[8][2];       // 8 s box row indices --> 2 bits
        int sc[8][4];       // 8 s box columb indices --> 4 bits
        int sr_ind[8];      // 8 s box row indices 
        int sc_ind[8];      // 8 s box column indices 
        int s_val[8];       // 8 s box found values
        int s_val_bin[8][4];// 8 s box found values --> 4 bits
        
        //L_(n) = R(n-1)
        for(int i = 0; i<32; i++){
            L[n][i] = R[n-1][i];
        }
        
        for(int i = 0; i<48; i++){
            E_R[n-1][i] = R[n-1][E_table[i]-1]; //R_(n-1) from 32 to 48 bits using E table
            Kn_xor_ER[n-1][i]=xor(K[n][i],E_R[n-1][i]); //K_(n) XOR E(R_(n-1))
        }
    
        for(int k = 0; k<8; k++){
            for (int c = 0; c<6; c++){
                B[k][c] = Kn_xor_ER[n-1][c+k*6]; // split into 8 groups of 6 bits
            }
        
            // first and last of each gives row
            sr[k][0] = B[k][0];
            sr[k][1] = B[k][5];
            
            sr_ind[k]= B[k][0]*2 + B[k][5];
            
            // middle 4 give column
            sc[k][0] = B[k][1];
            sc[k][1] = B[k][2];
            sc[k][2] = B[k][3];
            sc[k][3] = B[k][4];
            
            
            sc_ind[k] = 0;
            int c = 0;
            for (int b = 3; b>=0; b--){
                sc_ind[k] = sc_ind[k] + (sc[k][b]*pow(2,c));
                c++;
            }
            
            // lookup target value
            s_val[k] = S[k][sr_ind[k]][sc_ind[k]];
            int s_val_temp = s_val[k];
            
            // s box found value to 4 bits binary
            for (int d = 3; d>=0; d--){
                s_val_bin[k][d] = s_val_temp % 2;
                s_val_temp = s_val_temp/2;
            }
            
        }
        
        // combine 8 chunks of 4 bits into one 32 bit chuk
        int sComb[32];
        int a = 0;
        while(a<32){
            for (int k = 0; k<8; k++){
                for (int d = 0; d<4; d++){
                    sComb[a] = s_val_bin[k][d];
                    a++;
                }
            }
        }
        
        int f[32];
        for (int i = 0; i<32; i++){
            f[i] = sComb[P[i]-1]; // permuation from table P 
            R[n][i] = xor(L[n-1][i],f[i]); // R_(n) = L_(n-1) XOR f(R_(n-1),K_n)
        }
    }
    
    int R16L16[64];
    for (int i = 0; i<32; i++){
        R16L16[i] = R[16][i];
        R16L16[32+i] = L[16][i];
    }
    
    for (int i = 0; i<64; i++){
        output[i] = R16L16[IP_1[i]-1];
    }
    
}

void des_encrypt(int m[64], int k0[64], int *output){

    int K0[64];
    int M[64];

    for (int i = 0; i<64; i++){
        K0[i] = k0[i];
        M[i] = m[i];
    }
    
    int Lm[32];
    for(int i = 0; i<32; i++){
        Lm[i] = M[i];
    }
    
    int Rm[32];
    for(int i = 32; i<64; i++){
        Rm[i-32] = M[i];
    }
    
    //STEP 1    
    int Kplus[56];
    for (int i = 0; i<56; i++){
        Kplus[i] = K0[(PC1[i]-1)];
    }
    
    int C[17][28];
    int D[17][28];
    
    for(int i = 0; i<28; i++){
        C[0][i] = Kplus[i];
        D[0][i] = Kplus[i+28];
    }
    
    for (int n = 1; n<17; n++){
        if (Lshift[n-1]==1){
            for (int i = 0; i<27; i++){
                C[n][i]=C[n-1][i+1];
                D[n][i]=D[n-1][i+1];
            }
            C[n][27] = C[n-1][0];
            D[n][27] = D[n-1][0];
        }
        if (Lshift[n-1]==2){
            for (int i = 0; i<26; i++){
                C[n][i]=C[n-1][i+2];
                D[n][i]=D[n-1][i+2];
            }
            C[n][26] = C[n-1][0];
            D[n][26] = D[n-1][0];
            C[n][27] = C[n-1][1];
            D[n][27] = D[n-1][1];
        }
        
    }
    
    int CD[17][56];
    for (int n = 0; n<17; n++){
        for (int i = 0; i<28; i++){
            CD[n][i] = C[n][i];
            CD[n][i+28] = D[n][i];
        }
    }
    
    
    int K_en[17][48];
    int K[17][48];
    
    for (int n = 0; n<17; n++){
        for (int i = 0; i<48; i++){
            K_en[n][i] = CD[n][(PC2[i]-1)];
        }
    }
    
    for(int n = 1; n<17; n++){
        for (int i = 0; i<48; i++){
            K[n][i] = K_en[n][i];
        }
    }
    
    //STEP 2
    int IP[64];
    for(int i = 0; i<64; i++){
        IP[i] = M[IP_Table[i]-1];
    }
    
    int L[17][32];
    for(int i = 0; i<32; i++){
        L[0][i] = IP[i];
    }
    
    int R[17][32];
    for(int i = 32; i<64; i++){
        R[0][i-32] = IP[i];
    }
    
    int E_R[16][48];
    int Kn_xor_ER[16][48];

    
    for(int n = 1; n<17; n++){
        int B[8][6];        // 8 groups of 6 bits
        int sr[8][2];       // 8 s box row indices --> 2 bits
        int sc[8][4];       // 8 s box columb indices --> 4 bits
        int sr_ind[8];      // 8 s box row indices 
        int sc_ind[8];      // 8 s box column indices 
        int s_val[8];       // 8 s box found values
        int s_val_bin[8][4];// 8 s box found values --> 4 bits
        
        //L_(n) = R(n-1)
        for(int i = 0; i<32; i++){
            L[n][i] = R[n-1][i];
        }
        
        for(int i = 0; i<48; i++){
            E_R[n-1][i] = R[n-1][E_table[i]-1]; //R_(n-1) from 32 to 48 bits using E table
            Kn_xor_ER[n-1][i]=xor(K[n][i],E_R[n-1][i]); //K_(n) XOR E(R_(n-1))
        }
    
        for(int k = 0; k<8; k++){
            for (int c = 0; c<6; c++){
                B[k][c] = Kn_xor_ER[n-1][c+k*6]; // split into 8 groups of 6 bits
            }
        
            // first and last of each gives row
            sr[k][0] = B[k][0];
            sr[k][1] = B[k][5];
            
            sr_ind[k]= B[k][0]*2 + B[k][5];
            
            // middle 4 give column
            sc[k][0] = B[k][1];
            sc[k][1] = B[k][2];
            sc[k][2] = B[k][3];
            sc[k][3] = B[k][4];
            
            
            sc_ind[k] = 0;
            int c = 0;
            for (int b = 3; b>=0; b--){
                sc_ind[k] = sc_ind[k] + (sc[k][b]*pow(2,c));
                c++;
            }
            
            // lookup target value
            s_val[k] = S[k][sr_ind[k]][sc_ind[k]];
            int s_val_temp = s_val[k];
            
            // s box found value to 4 bits binary
            for (int d = 3; d>=0; d--){
                s_val_bin[k][d] = s_val_temp % 2;
                s_val_temp = s_val_temp/2;
            }
            
        }
        
        // combine 8 chunks of 4 bits into one 32 bit chuk
        int sComb[32];
        int a = 0;
        while(a<32){
            for (int k = 0; k<8; k++){
                for (int d = 0; d<4; d++){
                    sComb[a] = s_val_bin[k][d];
                    a++;
                }
            }
        }
        
        int f[32];
        for (int i = 0; i<32; i++){
            f[i] = sComb[P[i]-1]; // permuation from table P 
            R[n][i] = xor(L[n-1][i],f[i]); // R_(n) = L_(n-1) XOR f(R_(n-1),K_n)
        }
    }
    
    int R16L16[64];
    for (int i = 0; i<32; i++){
        R16L16[i] = R[16][i];
        R16L16[32+i] = L[16][i];
    }
    
    for (int i = 0; i<64; i++){
        output[i] = R16L16[IP_1[i]-1];
    }
    
}

void triple_des_decrypt(int m[64], int k1[64], int k2[64], int k3[64], int *output){
    int output1[64];
    int output2[64];

    des_decrypt(m, k3, output1);
    des_encrypt(output1, k2, output2);
    des_decrypt(output2, k1, output);
}

void triple_des_encrypt(int m[64], int k1[64], int k2[64], int k3[64], int *output){
    int output1[64];
    int output2[64];

    des_encrypt(m, k1, output1);
    des_decrypt(output1, k2, output2);
    des_encrypt(output2, k3, output);
}

void triple_des_decrypt_text(int input_binary[], char key1_str[], char key2_str[], char key3_str[], char *output_str){
    int key1_binary[64];
    int key2_binary[64];
    int key3_binary[64];

    int len = 0;
    while (input_binary[len]==1 || input_binary[len]==0){
        len++;
    }

    // takes first 8 characters of each key and turns them into their 64-bit binary equivalent
    strToBinary(key1_str, key1_binary);
    strToBinary(key2_str, key2_binary);
    strToBinary(key3_str, key3_binary);

    int input_64bit_chunk[64];
    int output_chunk_binary[64];
    char output_chunk_char[8];
    int j;
    int c=0;
    for (int i = 0; i<len; i+=64){
        j = 0;
        for (int k = i; k<i+64; k++){
            input_64bit_chunk[j] = input_binary[k];
            j++;
        }
        triple_des_decrypt(input_64bit_chunk, key1_binary, key2_binary, key3_binary, output_chunk_binary);
        binaryToStr(output_chunk_binary,output_chunk_char);
        
        for (int k = 0; k<8; k++){
            output_str[c] = output_chunk_char[k];
            c++;
        }
    }
}

void triple_des_encrypt_text(char input_str[], char key1_str[], char key2_str[], char key3_str[], int *output_binary){
    int key1_binary[64];
    int key2_binary[64];
    int key3_binary[64];

    // takes first 8 characters of each key and turns them into their 64-bit binary equivalent
    strToBinary(key1_str, key1_binary);
    strToBinary(key2_str, key2_binary);
    strToBinary(key3_str, key3_binary);

    // pads the input str so that its length is a multiple of 64 bits
    int num_8char_chunks = strlen(input_str)/8;
    int len_padded = num_8char_chunks*8;
    if (strlen(input_str)%8 != 0){
        len_padded+=8;
    }
    
    char input_str_padded[len_padded];
    for (int i = 0; i<len_padded; i++){
        if (i<strlen(input_str)){ input_str_padded[i] = input_str[i]; } else { input_str_padded[i] = '0'; }
    }

    char input_8char_chunk[8];
    int input_chunk_binary[64];
    int output_chunk_binary[64];
    int j;
    int c=0;

    for (int p = 0; p<len_padded; p+=8){
        j = 0;
        for (int k = p; k<p+8; k++){
            input_8char_chunk[j] = input_str_padded[k];
            j++;
        }
        strToBinary(input_8char_chunk, input_chunk_binary);
        triple_des_encrypt(input_chunk_binary, key1_binary, key2_binary, key3_binary, output_chunk_binary);
        
        for (int k = 0; k<64; k++){
            output_binary[c] = output_chunk_binary[k];
            c++;
        }

    }
}

void triple_des_encrypt_file(char source_file[], char key_file[], char *dest_file){
    FILE *source_fptr;
    FILE *key_fptr;
    FILE *dest_fptr;

    source_fptr = fopen(source_file, "r");
    key_fptr = fopen(key_file, "r");
    dest_fptr = fopen(dest_file, "w");

    char key1[8];
    char key2[8];
    char key3[8];
    char key_buff[100];
    char source_buff[3000];
    int output_buff_ints[3000*8];
    char output_buff[3000*8];

    if (source_fptr == NULL || key_fptr == NULL || dest_fptr == NULL){
        if (source_fptr == NULL){ 
            printf("Not able to open source file.\n");
        } 
        if (key_fptr == NULL){
            printf("Not able to open key file.\n");
        } 
        if (dest_fptr == NULL){
            printf("Not able to open destination file.\n");
        }
        exit(1);
    } else {
        fgets(key_buff, 100, key_fptr);
        for (int i = 0; i<8; i++){key1[i] = key_buff[i];}
        fgets(key_buff, 100, key_fptr);
        for (int i = 0; i<8; i++){key2[i] = key_buff[i];}
        fgets(key_buff, 100, key_fptr);
        for (int i = 0; i<8; i++){key3[i] = key_buff[i];}
        fgets(source_buff, 3000, source_fptr);
        triple_des_encrypt_text(source_buff, key1, key2, key3, output_buff_ints);
        intArrToCharArr(output_buff_ints, output_buff,3000*8);
        if(fprintf(dest_fptr, "%s", output_buff)){ printf("Success!\n");} else { printf("Something went wrong...\n");}
    }

    fclose(source_fptr);
    fclose(key_fptr);
    fclose(dest_fptr);
}

void triple_des_decrypt_file(char source_file[], char key_file[], char *dest_file){
    FILE *source_fptr;
    FILE *key_fptr;
    FILE *dest_fptr;

    source_fptr = fopen(source_file, "r");
    key_fptr = fopen(key_file, "r");
    dest_fptr = fopen(dest_file, "w");

    char key1[8];
    char key2[8];
    char key3[8];
    char key_buff[100];
    char source_buff_chars[3000*8];
    int source_buff [3000*8];
    char output_buff[3000];

    if (source_fptr == NULL || key_fptr == NULL || dest_fptr == NULL){
        if (source_fptr == NULL){ 
            printf("Not able to open source file.\n");
        } 
        if (key_fptr == NULL){
            printf("Not able to open key file.\n");
        } 
        if (dest_fptr == NULL){
            printf("Not able to open destination file.\n");
        }
        exit(1);
    } else {
        fgets(key_buff, 100, key_fptr);
        for (int i = 0; i<8; i++){key1[i] = key_buff[i];}
        fgets(key_buff, 100, key_fptr);
        for (int i = 0; i<8; i++){key2[i] = key_buff[i];}
        fgets(key_buff, 100, key_fptr);
        for (int i = 0; i<8; i++){key3[i] = key_buff[i];}
        fgets(source_buff_chars, 3000*8, source_fptr);
        charArrToIntArr(source_buff_chars, source_buff,3000*8);
        triple_des_decrypt_text(source_buff, key1, key2, key3, output_buff);
        if(fprintf(dest_fptr, "%s", output_buff)){ printf("Success!\n");} else { printf("Something went wrong...\n");}
    }

    fclose(source_fptr);
    fclose(key_fptr);
    fclose(dest_fptr);
}

int main()
{  
    printf("\n******** Text Mode ********\n");
    // input will come from user via GUI
    
    char input[300] = "tripledestestcomputersecurityfinalproject";
    char key1[8] = "firstkey";
    char key2[8] = "testkey2";
    char key3[8] = "keykeyke";

    int input_len = strlen(input);
    int encrypted_len;
    if (input_len%8 == 0) { 
        encrypted_len = input_len*8; 
    } else { 
        int chunks = input_len/8;
        encrypted_len = (chunks+1)*64; 
    }
    
    int encrypted[encrypted_len];
    char decrypted[encrypted_len/8];

    print_charArr("Original", input_len, input);
    triple_des_encrypt_text(input,key1,key2,key3,encrypted);
    print_intArr("Encrypted", encrypted_len, encrypted);
    triple_des_decrypt_text(encrypted,key1,key2,key3,decrypted);
    print_charArr("Decrypted", (encrypted_len/8), decrypted);

    printf("\n******** File Mode ********\n");

    triple_des_encrypt_file("source_test1.txt", "key_test1.txt", "encrypted_test1.txt");
    triple_des_decrypt_file("encrypted_test1.txt", "key_test1.txt", "decrypted_test1.txt");    
}