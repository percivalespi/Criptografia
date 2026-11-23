/* Proyecto: Algoritmo de Cifrado DES
   Integrantes - Equipo 10:
   Espinoza Matamoros Percival Ulises
   Garcia Cortes Adolfo de Jesus
   Lugo Manzano Rodrigo
   Montiel Juarez Oscar Ivan

*/
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

/* Tablas del estandar DES (las posiciones empiezan en 1) */
static const uint8_t IP[64] = {
    58,50,42,34,26,18,10,2, 60,52,44,36,28,20,12,4,
    62,54,46,38,30,22,14,6, 64,56,48,40,32,24,16,8,
    57,49,41,33,25,17,9,1, 59,51,43,35,27,19,11,3,
    61,53,45,37,29,21,13,5, 63,55,47,39,31,23,15,7
};
static const uint8_t IP_INV[64] = {
    40,8,48,16,56,24,64,32, 39,7,47,15,55,23,63,31,
    38,6,46,14,54,22,62,30, 37,5,45,13,53,21,61,29,
    36,4,44,12,52,20,60,28, 35,3,43,11,51,19,59,27,
    34,2,42,10,50,18,58,26, 33,1,41,9,49,17,57,25
};
static const uint8_t E[48] = {
    32,1,2,3,4,5, 4,5,6,7,8,9, 8,9,10,11,12,13, 12,13,14,15,16,17,
    16,17,18,19,20,21, 20,21,22,23,24,25, 24,25,26,27,28,29, 28,29,30,31,32,1
};
static const uint8_t P[32] = {
    16,7,20,21,29,12,28,17, 1,15,23,26,5,18,31,10,
    2,8,24,14,32,27,3,9, 19,13,30,6,22,11,4,25
};
static const uint8_t PC1[56] = {
    57,49,41,33,25,17,9, 1,58,50,42,34,26,18,
    10,2,59,51,43,35,27, 19,11,3,60,52,44,36,
    63,55,47,39,31,23,15, 7,62,54,46,38,30,
    22,14,6,61,53,45,37,29, 21,13,5,28,20,12,4
};
static const uint8_t PC2[48] = {
    14,17,11,24,1,5,3,28, 15,6,21,10,23,19,12,4,
    26,8,16,7,27,20,13,2, 41,52,31,37,47,55,30,40,
    51,45,33,48,44,49,39,56, 34,53,46,42,50,36,29,32
};
static const uint8_t DESPLAZAMIENTOS[16] = {1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1};
static const uint8_t CAJAS_S[8][4][16] = {
    {{14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7},{0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8},{4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0},{15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13}},
    {{15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10},{3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5},{0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15},{13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9}},
    {{10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8},{13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1},{13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7},{1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12}},
    {{7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15},{13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9},{10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4},{3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14}},
    {{2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9},{14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6},{4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14},{11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3}},
    {{12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11},{10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8},{9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6},{4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13}},
    {{4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1},{13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6},{1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2},{6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12}},
    {{13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7},{1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2},{7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8},{2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11}}
};

/* Reordena los bits de "dato" segun una tabla */
static uint64_t permutar(uint64_t dato, const uint8_t *tabla, int bits_salida, int bits_entrada) {
    uint64_t res = 0;
    for (int i = 0; i < bits_salida; i++)
        res = (res << 1) | ((dato >> (bits_entrada - tabla[i])) & 1u);
    return res;
}

/* Rotacion a la izquierda de un numero de 28 bits */
static uint32_t rotar_28(uint32_t dato, int pasos) {
    return ((dato << pasos) | (dato >> (28 - pasos))) & 0x0fffffffu;
}

/* Crea las 16 llaves de 48 bits (PC-1 quita los bits de paridad) */
static void crear_llaves(uint64_t clave, uint64_t llaves[16]) {
    uint64_t clave56 = permutar(clave, PC1, 56, 64);
    uint32_t c = (uint32_t)(clave56 >> 28);
    uint32_t d = (uint32_t)(clave56 & 0x0fffffffu);
    for (int i = 0; i < 16; i++) {
        c = rotar_28(c, DESPLAZAMIENTOS[i]);
        d = rotar_28(d, DESPLAZAMIENTOS[i]);
        llaves[i] = permutar(((uint64_t)c << 28) | d, PC2, 48, 56);
    }
}

/* Funcion de cada ronda: expansion, XOR con la llave, cajas S y permutacion P */
static uint32_t funcion_ronda(uint32_t der, uint64_t llave) {
    uint64_t xor48 = permutar(der, E, 48, 32) ^ llave;
    uint32_t salida_s = 0;
    for (int i = 0; i < 8; i++) {
        uint8_t seis_bits = (xor48 >> (42 - 6 * i)) & 0x3fu;
        int fila = ((seis_bits & 0x20u) >> 4) | (seis_bits & 1u);
        int col = (seis_bits >> 1) & 0x0fu;
        salida_s = (salida_s << 4) | CAJAS_S[i][fila][col];
    }
    return (uint32_t)permutar(salida_s, P, 32, 32);
}

/* Cifra o descifra un bloque. Para descifrar se usan las llaves al reves */
static uint64_t des_bloque(uint64_t bloque, const uint64_t llaves[16], int descifrar,
                           int mostrar_pasos) {
    uint64_t despues_ip = permutar(bloque, IP, 64, 64);
    uint32_t izq = (uint32_t)(despues_ip >> 32);
    uint32_t der = (uint32_t)despues_ip;
    for (int i = 0; i < 16; i++) {
        uint64_t llave = llaves[descifrar ? 15 - i : i];
        uint32_t nuevo_der = izq ^ funcion_ronda(der, llave);
        izq = der;
        der = nuevo_der;
        if (mostrar_pasos)
            printf("Ronda %2d: K=%012" PRIX64 "  L=%08" PRIX32 "  R=%08" PRIX32 "\n",
                   i + 1, llave, izq, der);
    }
    return permutar(((uint64_t)der << 32) | izq, IP_INV, 64, 64);
}

/* Convierte un texto de 16 caracteres hexadecimales a numero */
static int hex_a_numero(const char *texto, uint64_t *numero) {
    if (strlen(texto) != 16) return 0;
    uint64_t res = 0;
    for (int i = 0; i < 16; i++) {
        char letra = texto[i];
        int valor;
        if (letra >= '0' && letra <= '9') valor = letra - '0';
        else if (letra >= 'a' && letra <= 'f') valor = letra - 'a' + 10;
        else if (letra >= 'A' && letra <= 'F') valor = letra - 'A' + 10;
        else return 0;
        res = (res << 4) | (uint64_t)valor;
    }
    *numero = res;
    return 1;
}

int main(int argc, char *argv[]) {
    char texto_bloque[128], texto_clave[128];
    uint64_t bloque, clave, llaves[16];
    int mostrar_pasos = argc == 1;

    printf("\n Algoritmo de Cifrado DES \n\n");
    if (argc == 3) {
        snprintf(texto_bloque, sizeof texto_bloque, "%s", argv[1]);
        snprintf(texto_clave, sizeof texto_clave, "%s", argv[2]);
    } else if (argc == 1) {
        printf("> Ingrese el bloque de 64 bits (16 digitos hexadecimales): ");
        if (!fgets(texto_bloque, sizeof texto_bloque, stdin)) return 1;
        texto_bloque[strcspn(texto_bloque, "\n")] = '\0';
        printf("> Ingrese la clave de 64 bits (16 digitos hexadecimales): ");
        if (!fgets(texto_clave, sizeof texto_clave, stdin)) return 1;
        texto_clave[strcspn(texto_clave, "\n")] = '\0';
    } else {
        fprintf(stderr, "Uso: %s [BLOQUE_HEX CLAVE_HEX]\n", argv[0]);
        return 1;
    }
    if (!hex_a_numero(texto_bloque, &bloque) ||
        !hex_a_numero(texto_clave, &clave)) {
        fprintf(stderr, "![Error]: El bloque y la clave deben tener exactamente 16 digitos hexadecimales.\n");
        return 1;
    }

    crear_llaves(clave, llaves);
    printf("--- Calculo del cifrado ---\n");
    uint64_t cifrado = des_bloque(bloque, llaves, 0, mostrar_pasos);
    printf("--- Calculo del descifrado ---\n");
    uint64_t descifrado = des_bloque(cifrado, llaves, 1, mostrar_pasos);
    printf("\n------------- Resultados -------------\n\n");
    printf("--> Clave utilizada:    %016" PRIX64 "\n", clave);
    printf("--> Bloque original:    %016" PRIX64 "\n", bloque);
    printf("--> Bloque cifrado:     %016" PRIX64 "\n", cifrado);
    printf("--> Bloque descifrado:  %016" PRIX64 "\n", descifrado);
    printf("\n--------------------------------------\n");
    return descifrado == bloque ? 0 : 1;
}
