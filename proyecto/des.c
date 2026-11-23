/* Proyecto: Algoritmo de Cifrado DES
   Integrantes - Equipo 10:
   Espinoza Matamoros Percival Ulises
   Garcia Cortes Adolfo de Jesus
   Lugo Manzano Rodrigo
   Montiel Juarez Oscar Ivan

   Un bloque y una clave se escriben con 16 digitos hexadecimales.
   DES se incluye con fines academicos; no se recomienda para datos nuevos.
*/
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

/* Tablas de posiciones de bits del estandar DES (numeradas desde 1). */
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
static const uint8_t GIROS[16] = {1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1};
static const uint8_t S[8][4][16] = {
    {{14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7},{0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8},{4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0},{15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13}},
    {{15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10},{3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5},{0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15},{13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9}},
    {{10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8},{13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1},{13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7},{1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12}},
    {{7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15},{13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9},{10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4},{3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14}},
    {{2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9},{14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6},{4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14},{11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3}},
    {{12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11},{10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8},{9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6},{4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13}},
    {{4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1},{13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6},{1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2},{6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12}},
    {{13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7},{1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2},{7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8},{2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11}}
};

/* Selecciona bits en el orden de la tabla, del mas significativo al menos significativo. */
static uint64_t permutar(uint64_t valor, const uint8_t *tabla, int salida, int entrada) {
    uint64_t resultado = 0;
    for (int i = 0; i < salida; i++)
        resultado = (resultado << 1) | ((valor >> (entrada - tabla[i])) & 1u);
    return resultado;
}

static uint32_t girar_28(uint32_t valor, int pasos) {
    return ((valor << pasos) | (valor >> (28 - pasos))) & 0x0fffffffu;
}

/* Genera las 16 subclaves de 48 bits. PC-1 descarta los bits de paridad. */
static void generar_subclaves(uint64_t clave, uint64_t subclaves[16]) {
    uint64_t reducida = permutar(clave, PC1, 56, 64);
    uint32_t c = (uint32_t)(reducida >> 28);
    uint32_t d = (uint32_t)(reducida & 0x0fffffffu);
    for (int i = 0; i < 16; i++) {
        c = girar_28(c, GIROS[i]);
        d = girar_28(d, GIROS[i]);
        subclaves[i] = permutar(((uint64_t)c << 28) | d, PC2, 48, 56);
    }
}

/* Expansion E, XOR con la subclave, cajas S y permutacion P. */
static uint32_t funcion_f(uint32_t derecha, uint64_t subclave) {
    uint64_t mezcla = permutar(derecha, E, 48, 32) ^ subclave;
    uint32_t sustitucion = 0;
    for (int i = 0; i < 8; i++) {
        uint8_t grupo = (mezcla >> (42 - 6 * i)) & 0x3fu;
        int fila = ((grupo & 0x20u) >> 4) | (grupo & 1u);
        int columna = (grupo >> 1) & 0x0fu;
        sustitucion = (sustitucion << 4) | S[i][fila][columna];
    }
    return (uint32_t)permutar(sustitucion, P, 32, 32);
}

/* Descifrar solo invierte el orden de las subclaves. */
static uint64_t procesar(uint64_t bloque, const uint64_t subclaves[16], int descifrar,
                         int mostrar_detalle) {
    uint64_t inicial = permutar(bloque, IP, 64, 64);
    uint32_t izquierda = (uint32_t)(inicial >> 32);
    uint32_t derecha = (uint32_t)inicial;
    for (int i = 0; i < 16; i++) {
        uint64_t subclave = subclaves[descifrar ? 15 - i : i];
        uint32_t siguiente = izquierda ^ funcion_f(derecha, subclave);
        izquierda = derecha;
        derecha = siguiente;
        if (mostrar_detalle)
            printf("Ronda %2d: K=%012" PRIX64 "  L=%08" PRIX32 "  R=%08" PRIX32 "\n",
                   i + 1, subclave, izquierda, derecha);
    }
    return permutar(((uint64_t)derecha << 32) | izquierda, IP_INV, 64, 64);
}

static int leer_hexadecimal(const char *texto, uint64_t *valor) {
    if (strlen(texto) != 16) return 0;
    uint64_t resultado = 0;
    for (int i = 0; i < 16; i++) {
        char c = texto[i];
        int digito;
        if (c >= '0' && c <= '9') digito = c - '0';
        else if (c >= 'a' && c <= 'f') digito = c - 'a' + 10;
        else if (c >= 'A' && c <= 'F') digito = c - 'A' + 10;
        else return 0;
        resultado = (resultado << 4) | (uint64_t)digito;
    }
    *valor = resultado;
    return 1;
}

int main(int argc, char *argv[]) {
    char texto_bloque[128], texto_clave[128];
    uint64_t bloque, clave, subclaves[16];
    int detalle = argc == 1;

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
    if (!leer_hexadecimal(texto_bloque, &bloque) ||
        !leer_hexadecimal(texto_clave, &clave)) {
        fprintf(stderr, "![Error]: El bloque y la clave deben tener exactamente 16 digitos hexadecimales.\n");
        return 1;
    }

    generar_subclaves(clave, subclaves);
    printf("--- Calculo del cifrado ---\n");
    uint64_t cifrado = procesar(bloque, subclaves, 0, detalle);
    printf("--- Calculo del descifrado ---\n");
    uint64_t recuperado = procesar(cifrado, subclaves, 1, detalle);
    printf("\n------------- Resultados -------------\n\n");
    printf("--> Clave utilizada:    %016" PRIX64 "\n", clave);
    printf("--> Bloque original:    %016" PRIX64 "\n", bloque);
    printf("--> Bloque cifrado:     %016" PRIX64 "\n", cifrado);
    printf("--> Bloque descifrado:  %016" PRIX64 "\n", recuperado);
    printf("\n--------------------------------------\n");
    return recuperado == bloque ? 0 : 1;
}
