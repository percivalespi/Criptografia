#  Práctica 2: Algoritmo de Cifrado Vigenère (Español) con clave numérica
"""
    Integrantes
    - Espinoza Matamoros Percival Ulises
    - García Cortés Adolfo de Jesus
    - Lugo Manzano Rodrigo
    - Montiel Juárez Oscar Iván

    Fecha: 1 de septiembre del 2026
"""

#  Definición del conjunto de caracteres (universo) para el español
#  Sin ñ, solo letras minúsculas sin acentos
A = "abcdefghijklmnopqrstuvwxyz"

# Función de cifrado (con clave numérica)
def cifrar(mensaje, k):
    """
    Cifra un mensaje usando el algoritmo de Vigenère con una clave numérica fija.
    Equivale a un cifrado César con corrimiento k.

    Parámetros:
        mensaje (str): Texto en minúsculas y sin acentos, que puede contener espacios.
        k (int): Número de corrimiento (0-25).

    Retorna:
        str: Mensaje cifrado, manteniendo los espacios.
    """
    mensaje_cifrado = ""

    for caracter in mensaje:
        if caracter in A:
            indice = A.index(caracter)
            # Aplicando la fórmula: C = (P + k) mod N
            nuevo_indice = (indice + k) % len(A)
            mensaje_cifrado += A[nuevo_indice]
        else:
            # Los espacios se mantienen igual
            mensaje_cifrado += caracter
    return mensaje_cifrado

# Función de descifrado (con clave numérica)
def descifrar(mensaje_cifrado, k):
    """
    Descifra un mensaje cifrado con Vigenère usando clave numérica fija.

    Parámetros:
        mensaje_cifrado (str): Texto cifrado en minúsculas y sin acentos.
        k (int): Mismo número de corrimiento usado para cifrar.

    Retorna:
        str: Mensaje original descifrado.
    """
    mensaje_descifrado = ""

    for caracter in mensaje_cifrado:
        if caracter in A:
            indice = A.index(caracter)
            # Aplicando la fórmula: P = (C - k) mod N
            nuevo_indice = (indice - k) % len(A)
            mensaje_descifrado += A[nuevo_indice]
        else:
            mensaje_descifrado += caracter
    return mensaje_descifrado


if __name__ == "__main__":
    print("\n <><><><><><> Algoritmo de Cifrado Vigenère (Clave Numérica) <><><><><><>\n")
    
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

    # Validación de la clave numérica (0 al 25)
    while True:
        try:
            k = int(input("> Ingrese el número de corrimiento (0 al 25): "))
            if 0 <= k <= 25:
                break
            else:
                print("\n![Error]: El corrimiento debe estar en el rango de 0 a 25.\n")
        except ValueError:
            print("\n![Error]: Debe ingresar un número entero válido.\n")

    # Ejecución con los datos validados
    mensaje_cifrado = cifrar(mensaje, k)
    mensaje_descifrado = descifrar(mensaje_cifrado, k)

    print("\n------------- Resultados -------------\n")
    print("--> Corrimiento utilizado:   ", k)
    print("--> Mensaje original:         ", mensaje)
    print("--> Mensaje cifrado:          ", mensaje_cifrado)
    print("--> Mensaje descifrado:       ", mensaje_descifrado)
    print("\n--------------------------------------\n")