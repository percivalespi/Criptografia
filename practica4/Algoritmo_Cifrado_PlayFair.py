# Práctica 4: Algoritmo de Cifrado Playfair
"""
    Integrantes
    - Espinoza Matamoros Percival Ulises
    - García Cortés Adolfo de Jesus
    - Lugo Manzano Rodrigo
    - Montiel Juárez Oscar Iván 
"""

# Universo "abecedario" sin la letra 'ñ' (25 letras)
A = "abcdefghijklmnopqrstuvwxyz"

# Playfair usa una matriz de 5x5 (25 letras), por eso la 'j' se sustituye por la 'i'
A_PLAYFAIR = "abcdefghiklmnopqrstuvwxyz"


def generar_matriz(clave):
    
   # Construye la matriz 5x5 (como cadena de 25 letras):
   # primero las letras de la clave sin repetir y después el resto del alfabeto.

    clave = clave.replace("j", "i")
    matriz = ""
    for caracter in clave + A_PLAYFAIR:
        if caracter in A_PLAYFAIR and caracter not in matriz:
            matriz += caracter
    return matriz


def mostrar_matriz(matriz):
    #Imprime la matriz de 5x5 
    for i in range(5):
        print("   ", " ".join(matriz[i * 5:(i + 1) * 5]))


def preparar_digrafos(mensaje):
    
    #Quita espacios, cambia 'j' por 'i' y separa el mensaje en pares de letras.
    #- Si un par tiene dos letras iguales se inserta una 'x' entre ellas.
    #- Si queda una letra sola al final se completa con 'x'.
    
    texto = mensaje.replace(" ", "").replace("j", "i")
    pares = []
    i = 0
    while i < len(texto):
        a = texto[i]
        if i + 1 < len(texto) and texto[i + 1] != a:
            b = texto[i + 1]
            i += 2
        else:
            b = "x" if a != "x" else "q"   # relleno (si la letra ya es 'x' se usa 'q')
            i += 1
        pares.append(a + b)
    return pares


def transformar_par(par, matriz, direccion):
    
    #Aplica las reglas de Playfair a un par de letras.
    #direccion = 1  -> cifrar
    #direccion = -1 -> descifrar
    
    f1, c1 = divmod(matriz.index(par[0]), 5)
    f2, c2 = divmod(matriz.index(par[1]), 5)

    if f1 == f2:
        # Misma fila: se toma la letra a la derecha (cifrar) o a la izquierda (descifrar)
        n1 = matriz[f1 * 5 + (c1 + direccion) % 5]
        n2 = matriz[f2 * 5 + (c2 + direccion) % 5]
    elif c1 == c2:
        # Misma columna: se toma la letra de abajo (cifrar) o de arriba (descifrar)
        n1 = matriz[((f1 + direccion) % 5) * 5 + c1]
        n2 = matriz[((f2 + direccion) % 5) * 5 + c2]
    else:
        # Rectángulo: se intercambian las columnas
        n1 = matriz[f1 * 5 + c2]
        n2 = matriz[f2 * 5 + c1]

    return n1 + n2


# Función de cifrado
def cifrar(mensaje, clave, mostrar_detalle=False):
    matriz = generar_matriz(clave)
    mensaje_cifrado = ""

    for par in preparar_digrafos(mensaje):
        cifrado = transformar_par(par, matriz, 1)
        if mostrar_detalle:
            print(f"'{par}' -> '{cifrado}'")
        mensaje_cifrado += cifrado

    return mensaje_cifrado


# Función de descifrado
def descifrar(mensaje_cifrado, clave, mostrar_detalle=False):
    matriz = generar_matriz(clave)
    mensaje_descifrado = ""

    for i in range(0, len(mensaje_cifrado), 2):
        par = mensaje_cifrado[i:i + 2]
        original = transformar_par(par, matriz, -1)
        if mostrar_detalle:
            print(f"'{par}' -> '{original}'")
        mensaje_descifrado += original

    return mensaje_descifrado


if __name__ == "__main__":
    print("\n Algoritmo de Cifrado Playfair \n")

    # Validación del mensaje (solo letras minúsculas y espacios)
    while True:
        mensaje = input("> Ingrese el mensaje a cifrar: ").lower()

        es_valido = True
        hay_letras = False
        for caracter in mensaje:
            if caracter in A:
                hay_letras = True
            elif caracter != " ":
                es_valido = False
                break

        if es_valido and hay_letras:
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

    # Mostrar la matriz generada
    print("\n--- Matriz Playfair 5x5 (i y j comparten celda) ---")
    mostrar_matriz(generar_matriz(clave))

    # Ejecución con los datos validados
    print("\n--- Cálculo del cifrado (par -> par cifrado) ---")
    mensaje_cifrado = cifrar(mensaje, clave, mostrar_detalle=True)

    print("\n--- Cálculo del descifrado (par cifrado -> par) ---")
    mensaje_descifrado = descifrar(mensaje_cifrado, clave, mostrar_detalle=True)

    print("\n------------- Resultados -------------\n")
    print("--> Clave utilizada:          ", clave)
    print("--> Mensaje original:         ", mensaje)
    print("--> Mensaje cifrado:          ", mensaje_cifrado)
    print("--> Mensaje descifrado:       ", mensaje_descifrado)
    print("\n--------------------------------------\n")