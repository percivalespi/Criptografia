# Práctica 2: Algoritmo de Cifrado Vigenère (Español) con clave palabra
"""
    Integrantes
    - Espinoza Matamoros Percival Ulises
    - García Cortés Adolfo de Jesus
    - Lugo Manzano Rodrigo
    - Montiel Juárez Oscar Iván

    Fecha: 1 de septiembre del 2026
"""

# Definición del conjunto de caracteres (universo) para el español
# Sin ñ, solo letras minúsculas sin acentos
A = "abcdefghijklmnopqrstuvwxyz"

def cifrar(mensaje, clave, mostrar_detalle=False):
    """
    Cifra un mensaje usando el algoritmo de Vigenère con clave textual.

    Parámetros:
        mensaje (str): Texto en minúsculas y sin acentos, puede contener espacios.
        clave (str): Palabra clave en minúsculas (solo letras a-z).
        mostrar_detalle (bool): Si es True, imprime la operación para cada letra.

    Retorna:
        str: Mensaje cifrado, manteniendo los espacios.
    """
    mensaje_cifrado = ""
    clave_idx = 0          # índice actual de la clave (solo avanza en letras)
    largo_clave = len(clave)

    for caracter in mensaje:
        if caracter in A:
            # Índice del mensaje
            indice_m = A.index(caracter)
            # Índice de la clave (corrimiento)
            indice_k = A.index(clave[clave_idx % largo_clave])
            # Fórmula de cifrado
            nuevo_indice = (indice_m + indice_k) % len(A)
            letra_cifrada = A[nuevo_indice]

            if mostrar_detalle:
                print(f"'{caracter}' (M={indice_m:2d}) + clave '{clave[clave_idx % largo_clave]}' (K={indice_k:2d}) mod 26 = {nuevo_indice:2d} → '{letra_cifrada}'")

            mensaje_cifrado += letra_cifrada
            clave_idx += 1   # solo avanzamos si ciframos una letra
        else:
            # Espacios se mantienen y NO consumen clave
            mensaje_cifrado += caracter

    return mensaje_cifrado


def descifrar(mensaje_cifrado, clave, mostrar_detalle=False):
    """
    Descifra un mensaje cifrado con Vigenère usando clave textual.

    Parámetros:
        mensaje_cifrado (str): Texto cifrado en minúsculas y sin acentos.
        clave (str): Misma palabra clave usada para cifrar.
        mostrar_detalle (bool): Si es True, imprime la operación para cada letra.

    Retorna:
        str: Mensaje original descifrado.
    """
    mensaje_descifrado = ""
    clave_idx = 0
    largo_clave = len(clave)

    for caracter in mensaje_cifrado:
        if caracter in A:
            indice_c = A.index(caracter)
            indice_k = A.index(clave[clave_idx % largo_clave])
            # Fórmula de descifrado
            nuevo_indice = (indice_c - indice_k) % len(A)
            letra_original = A[nuevo_indice]

            if mostrar_detalle:
                print(f"'{caracter}' (C={indice_c:2d}) - clave '{clave[clave_idx % largo_clave]}' (K={indice_k:2d}) mod 26 = {nuevo_indice:2d} → '{letra_original}'")

            mensaje_descifrado += letra_original
            clave_idx += 1
        else:
            mensaje_descifrado += caracter

    return mensaje_descifrado


if __name__ == "__main__":
    print("\n <><><><><><> Algoritmo de Cifrado Vigenère (Clave Palabra) <><><><><><>\n")

    # Validación del mensaje (solo letras minúsculas y espacios)
    while True:
        mensaje = input("> Ingrese el mensaje a cifrar: ").lower()

        es_valido = True
        for caracter in mensaje:
            if caracter not in A and caracter != " ":
                es_valido = False
                break

        if es_valido and len(mensaje) > 0:
            break
        else:
            print("\n![Error]: Ingrese únicamente letras minúsculas (a-z) y espacios. No se permiten números ni símbolos.\n")

    # Validación de la clave (solo letras minúsculas, sin espacios)
    while True:
        clave = input("> Ingrese la palabra clave (solo letras a-z): ").lower()

        es_valida = True
        for caracter in clave:
            if caracter not in A:
                es_valida = False
                break

        if es_valida and len(clave) > 0:
            break
        else:
            print("\n![Error]: La clave debe contener solo letras minúsculas (a-z), sin espacios ni otros caracteres.\n")

    # Mostrar paso a paso el cifrado
    print("\n--- Cálculo del cifrado (fórmula C = (M + K) mod 26) ---")
    mensaje_cifrado = cifrar(mensaje, clave, mostrar_detalle=True)

    # Mostrar paso a paso el descifrado (opcional, lo activamos)
    print("\n--- Cálculo del descifrado (fórmula M = (C - K) mod 26) ---")
    mensaje_descifrado = descifrar(mensaje_cifrado, clave, mostrar_detalle=True)

    print("\n------------- Resultados -------------\n")
    print("--> Clave utilizada:          ", clave)
    print("--> Mensaje original (m):      ", mensaje)
    print("--> Mensaje cifrado (c):       ", mensaje_cifrado)
    print("--> Mensaje descifrado:        ", mensaje_descifrado)
    print("\n--------------------------------------\n")