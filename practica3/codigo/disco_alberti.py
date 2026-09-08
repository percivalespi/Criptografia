# Práctica 3: Algoritmo de Cifrado - Disco de Alberti
"""
    Integrantes
    - Espinoza Matamoros Percival Ulises
    - García Cortés Adolfo de Jesus
    - Lugo Manzano Rodrigo
    - Montiel Juárez Oscar Iván

    Fecha: 8 de septiembre del 2026
"""

# Definición del conjunto de caracteres (universo)
# Representa el anillo FIJO (exterior) del disco de Alberti
A = "abcdefghijklmnopqrstuvwxyz"


def obtener_anillo_movil(desplazamiento):
    """
    Genera el anillo MÓVIL (interior) del disco, rotado según
    el desplazamiento actual. Simula "girar" físicamente el disco.
    """
    return A[desplazamiento:] + A[:desplazamiento]


# Función de cifrado
def cifrar(mensaje, letra_alineacion, periodo, paso, mostrar_detalle=False):
    """
    Cifra un mensaje simulando el disco de Alberti.

    Parámetros:
        mensaje (str): Texto en minúsculas y sin acentos, puede contener espacios.
        letra_alineacion (str): Letra del anillo fijo con la que se alinea
                                 la 'a' del anillo móvil al inicio.
        periodo (int): Cada cuántas letras cifradas se gira el disco.
        paso (int): Cuántas posiciones avanza el disco al girar.
        mostrar_detalle (bool): Si es True, imprime la operación letra por letra.

    Retorna:
        str: Mensaje cifrado, manteniendo los espacios.
    """
    mensaje_cifrado = ""
    desplazamiento = A.index(letra_alineacion)
    contador = 0

    for caracter in mensaje:
        if caracter in A:
            anillo_movil = obtener_anillo_movil(desplazamiento)
            indice = A.index(caracter)
            letra_cifrada = anillo_movil[indice]

            if mostrar_detalle:
                print(f"'{caracter}' (fijo pos {indice:2d}) -> disco alineado en '{A[desplazamiento]}' -> '{letra_cifrada}'")

            mensaje_cifrado += letra_cifrada
            contador += 1

            # Girar el disco cada 'periodo' letras cifradas
            if contador % periodo == 0:
                desplazamiento = (desplazamiento + paso) % len(A)
        else:
            # Los espacios se mantienen y NO giran el disco
            mensaje_cifrado += caracter

    return mensaje_cifrado


# Función de descifrado
def descifrar(mensaje_cifrado, letra_alineacion, periodo, paso, mostrar_detalle=False):
    """
    Descifra un mensaje cifrado con el disco de Alberti.
    Debe usar la misma letra de alineación, periodo y paso que en el cifrado.
    """
    mensaje_descifrado = ""
    desplazamiento = A.index(letra_alineacion)
    contador = 0

    for caracter in mensaje_cifrado:
        if caracter in A:
            anillo_movil = obtener_anillo_movil(desplazamiento)
            indice = anillo_movil.index(caracter)
            letra_original = A[indice]

            if mostrar_detalle:
                print(f"'{caracter}' (móvil alineado en '{A[desplazamiento]}') -> pos {indice:2d} -> '{letra_original}'")

            mensaje_descifrado += letra_original
            contador += 1

            if contador % periodo == 0:
                desplazamiento = (desplazamiento + paso) % len(A)
        else:
            mensaje_descifrado += caracter

    return mensaje_descifrado


if __name__ == "__main__":
    print("\n <><><><><><> Algoritmo de Cifrado - Disco de Alberti <><><><><><>\n")

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

    # Validación de la letra de alineación inicial del disco
    while True:
        letra_alineacion = input("> Ingrese la letra con la que inicia alineado el disco (a-z): ").lower()
        if letra_alineacion in A:
            break
        else:
            print("\n![Error]: Debe ingresar una sola letra minúscula (a-z).\n")

    # Validación del periodo de giro (cada cuántas letras gira el disco)
    while True:
        try:
            periodo = int(input("> Ingrese cada cuántas letras gira el disco (ej. 3): "))
            if periodo > 0:
                break
            else:
                print("\n![Error]: El periodo debe ser un número entero mayor a 0.\n")
        except ValueError:
            print("\n![Error]: Debe ingresar un número entero válido.\n")

    # Validación del paso de giro (cuántas posiciones avanza el disco)
    while True:
        try:
            paso = int(input("> Ingrese cuántas posiciones avanza el disco al girar (1 al 25): "))
            if 1 <= paso <= 25:
                break
            else:
                print("\n![Error]: El paso debe estar en el rango de 1 a 25.\n")
        except ValueError:
            print("\n![Error]: Debe ingresar un número entero válido.\n")

    # Ejecución con los datos validados
    print("\n--- Cálculo del cifrado (letra fija -> disco móvil) ---")
    mensaje_cifrado = cifrar(mensaje, letra_alineacion, periodo, paso, mostrar_detalle=True)

    print("\n--- Cálculo del descifrado (disco móvil -> letra fija) ---")
    mensaje_descifrado = descifrar(mensaje_cifrado, letra_alineacion, periodo, paso, mostrar_detalle=True)

    print("\n------------- Resultados -------------\n")
    print("--> Letra de alineación inicial: ", letra_alineacion)
    print("--> Periodo de giro:              ", periodo)
    print("--> Paso de giro:                 ", paso)
    print("--> Mensaje original:             ", mensaje)
    print("--> Mensaje cifrado:              ", mensaje_cifrado)
    print("--> Mensaje descifrado:           ", mensaje_descifrado)
    print("\n--------------------------------------\n")
