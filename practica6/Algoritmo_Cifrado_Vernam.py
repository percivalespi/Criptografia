# Práctica 6: Algoritmo de Cifrado Vernam
"""
    Integrantes
    - Espinoza Matamoros Percival Ulises
    - García Cortés Adolfo de Jesus
    - Lugo Manzano Rodrigo
    - Montiel Juárez Oscar Iván
"""

import random

# Definición del alfabeto (universo)
A = "abcdefghijklmnopqrstuvwxyz"


def a_bits(numero):
    #Convierte un número (0-31) a una cadena de 5 bits.
    return format(numero, "05b")


def xor_bits(bits1, bits2):
    #XOR bit a bit: bits iguales -> 0, bits distintos -> 1.
    resultado = ""
    for b1, b2 in zip(bits1, bits2):
        resultado += "0" if b1 == b2 else "1"
    return resultado


def generar_clave(largo):
    #Genera una clave aleatoria de letras con la misma longitud que el mensaje.
    return "".join(random.choice(A) for _ in range(largo))


# Función de cifrado
def cifrar(mensaje, clave, mostrar_detalle=False):
    
    #Vernam: C = M xor K (bit a bit, 5 bits por letra).
    #Retorna una lista de cadenas de 5 bits, porque el resultado puede ser
    #un valor entre 26 y 31 que ya no corresponde a una letra.

    texto = mensaje.replace(" ", "")
    criptograma = []

    for i, caracter in enumerate(texto):
        bits_m = a_bits(A.index(caracter))
        bits_k = a_bits(A.index(clave[i]))
        bits_c = xor_bits(bits_m, bits_k)
        decimal = int(bits_c, 2)

        if mostrar_detalle:
            nota = f"'{A[decimal]}'" if decimal < 26 else "(no es letra)"
            print(f"'{caracter}' {bits_m} xor '{clave[i]}' {bits_k} = {bits_c} ({decimal:2d}) {nota}")

        criptograma.append(bits_c)

    return criptograma


# Función de descifrado
def descifrar(criptograma, clave, mostrar_detalle=False):

    # M = C xor K (porque K xor K = 0).
    
    mensaje = ""

    for i, bits_c in enumerate(criptograma):
        bits_k = a_bits(A.index(clave[i]))
        bits_m = xor_bits(bits_c, bits_k)
        decimal = int(bits_m, 2)
        letra = A[decimal]

        if mostrar_detalle:
            print(f"{bits_c} xor '{clave[i]}' {bits_k} = {bits_m} ({decimal:2d}) -> '{letra}'")

        mensaje += letra

    return mensaje


if __name__ == "__main__":
    print("\n  Algoritmo de Cifrado Vernam \n")

    # Validación del mensaje (solo letras minúsculas y espacios)
    while True:
        mensaje = input("> Ingrese el mensaje a cifrar: ").lower()

        es_valido = True
        for caracter in mensaje:
            if caracter not in A and caracter != " ":
                es_valido = False
                break

        if es_valido and mensaje.replace(" ", "") != "":
            break
        else:
            print("\n![Error]: Ingrese únicamente letras minúsculas (a-z) y espacios. No se permiten números ni símbolos.\n")

    mensaje = mensaje.replace(" ", "")   # en Vernam se trabaja sin espacios
    total_letras = len(mensaje)

    # Validación de la clave (|K| = |M|; si es más larga se usan las primeras letras)
    while True:
        clave = input(f"> Ingrese la clave de al menos {total_letras} letras (Enter para generarla aleatoria): ").lower()

        if clave == "":
            clave = generar_clave(total_letras)
            print(f"  Clave generada: {clave}")
            break

        es_valida = True
        for caracter in clave:
            if caracter not in A:
                es_valida = False
                break

        if es_valida and len(clave) >= total_letras:
            clave = clave[:total_letras]
            break
        else:
            print(f"\n![Error]: La clave debe tener solo letras minúsculas (a-z) y al menos {total_letras} letras.\n")

    # Ejecución con los datos validados
    print("\n--- Cálculo del cifrado (fórmula C = M xor K) ---")
    criptograma = cifrar(mensaje, clave, mostrar_detalle=True)

    print("\n--- Cálculo del descifrado (fórmula M = C xor K) ---")
    mensaje_descifrado = descifrar(criptograma, clave, mostrar_detalle=True)

    print("\n------------- Resultados -------------\n")
    print("--> Clave utilizada:          ", clave)
    print("--> Mensaje original:         ", mensaje)
    print("--> Criptograma (bits):       ", " ".join(criptograma))
    print("--> Criptograma (decimal):    ", " ".join(str(int(c, 2)) for c in criptograma))
    print("--> Mensaje descifrado:       ", mensaje_descifrado)
    print("\n--------------------------------------\n")