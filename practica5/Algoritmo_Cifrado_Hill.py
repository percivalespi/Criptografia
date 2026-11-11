# Práctica 5: Algoritmo de Cifrado Hill (matriz clave 2x2 o 3x3)
"""
    Integrantes
    - Espinoza Matamoros Percival Ulises
    - García Cortés Adolfo de Jesus
    - Lugo Manzano Rodrigo
    - Montiel Juárez Oscar Iván
"""

from math import gcd

# Definición del alfabeto (su universo)
A = "abcdefghijklmnopqrstuvwxyz"
N = len(A)



#Para leer la clave
def leer_clave(entrada):
    
    # Convierte la clave escrita por el usuario en una lista de números (0-25).
    # Acepta una palabra (como 'dcdf') o números separados por espacio (como '3 2 3 5').
    ## De igual forma no regresamos nada si no lo podemos descifrar el mensaje
    
    partes = entrada.split()

    if len(partes) == 1 and all(c in A for c in partes[0]):
        numeros = [A.index(c) for c in partes[0]]      # clave en letras
    else:
        try:
            numeros = [int(p) % N for p in partes]      # clave en números
        except ValueError:
            return None

    return numeros if len(numeros) in (4, 9) else None


def matriz_desde_clave(numeros):
    
    # Convierte la lista de números en matriz, llenando por filas.
    # 4 valores -> 2x2, 9 valores -> 3x3. Ej: [3, 2, 3, 5] -> [[3, 2], [3, 5]]
    
    n = 2 if len(numeros) == 4 else 3
    return [numeros[i * n:(i + 1) * n] for i in range(n)]


def determinante(K):
    # Determinante de una matriz 2x2 o 3x3. Se asume que K es cuadrada y de tamaño 2 o 3.
    if len(K) == 2:
        return K[0][0] * K[1][1] - K[0][1] * K[1][0]
    a, b, c = K[0]
    d, e, f = K[1]
    g, h, i = K[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def adjunta(K):
    # Matriz adjunta 
    n = len(K)
    if n == 2:
        return [[K[1][1], -K[0][1]], [-K[1][0], K[0][0]]]

    adj = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            # Menor: matriz 2x2 que queda al quitar la fila i y la columna j
            menor = [[K[r][c] for c in range(3) if c != j] for r in range(3) if r != i]
            cofactor = ((-1) ** (i + j)) * determinante(menor)
            adj[j][i] = cofactor
    return adj


def matriz_inversa(K):
    # K^-1 = (det K)^-1 * adj(K) mod 26 
    det_inv = pow(determinante(K) % N, -1, N)
    adj = adjunta(K)
    n = len(K)
    return [[(det_inv * adj[i][j]) % N for j in range(n)] for i in range(n)]


def aplicar_matriz(texto, K, mostrar_detalle=False, etiqueta="P"):
    
    # Multiplica cada bloque (vector columna) por la matriz K mod 26.
    # Se usa para cifrar (con K) y para descifrar (con K^-1).
    
    n = len(K)
    resultado = ""

    for i in range(0, len(texto), n):
        bloque = texto[i:i + n]
        x = [A.index(c) for c in bloque]
        y = [sum(K[f][c] * x[c] for c in range(n)) % N for f in range(n)]
        letras = "".join(A[v] for v in y)

        if mostrar_detalle:
            print(f"'{bloque}' ({etiqueta}={x}) -> {y} -> '{letras}'")

        resultado += letras

    return resultado


# Función de cifrado
def cifrar(mensaje, K, mostrar_detalle=False):
    n = len(K)
    # Quitamos espacios y rellenamos con 'x' hasta completar el último bloque
    texto = mensaje.replace(" ", "")
    while len(texto) % n != 0:
        texto += "x"

    # Fórmula: C = K * P mod 26
    return aplicar_matriz(texto, K, mostrar_detalle, "P")


# Función de descifrado
def descifrar(mensaje_cifrado, K, mostrar_detalle=False):
    # Fórmula: P = K^-1 * C mod 26
    return aplicar_matriz(mensaje_cifrado, matriz_inversa(K), mostrar_detalle, "C")


if __name__ == "__main__":
    print("\n  Algoritmo de Cifrado Hill \n")

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

    # Validación de la clave: palabra o números, 4 valores (2x2) o 9 valores (3x3)
    while True:
        clave = input("> Ingrese la clave (palabra o números separados por espacio; 4 para 2x2, 9 para 3x3): ").lower()

        numeros = leer_clave(clave)
        if numeros is None:
            print("\n![Error]: Ingrese una palabra de 4 o 9 letras (a-z) o 4 o 9 números enteros separados por espacio.\n")
            continue

        K = matriz_desde_clave(numeros)
        det = determinante(K) % N

        # La matriz es invertible mod 26 solo si minimo comun Divisor común mas grande(det, 26) = 1
        if gcd(det, N) == 1:
            break
        else:
            print(f"\n![Error]: El determinante ({det}) no es coprimo con 26, la matriz no tiene inversa.\n")

    K_inv = matriz_inversa(K)

    # Ejecución con los datos validados
    print("\n--- Cálculo del cifrado (C = K * P mod 26) ---")
    mensaje_cifrado = cifrar(mensaje, K, mostrar_detalle=True)

    print("\n--- Cálculo del descifrado (P = K^-1 * C mod 26) ---")
    mensaje_descifrado = descifrar(mensaje_cifrado, K, mostrar_detalle=True)

    print("\n------------- Resultados -------------\n")
    print("--> Clave utilizada:          ", clave)
    print("--> Matriz clave K:           ", K)
    print("--> Determinante (mod 26):    ", det)
    print("--> Matriz inversa K^-1:      ", K_inv)
    print("--> Mensaje original:         ", mensaje)
    print("--> Mensaje cifrado:          ", mensaje_cifrado)
    print("--> Mensaje descifrado:       ", mensaje_descifrado)
    print("\n--------------------------------------\n")