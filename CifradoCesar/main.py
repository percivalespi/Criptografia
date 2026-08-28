#  Práctica 1: Algoritmo de Cifrado César
"""
    Integrantes
    - Espinoza Matamoros Percival Ulises
    - García Cortés Adolfo de Jesus
    - Lugo Manzano Rodrigo
    - Montiel Juárez Oscar Iván
"""

#  Definición del conjunto de caracteres (universo)
A = "abcdefghijklmnopqrstuvwxyz"

# Función de cifrado
def cifrar(mensaje, k):
    mensaje_cifrado = ""

    # Recorriendo cada caracter del mensaje
    for caracter in mensaje:
        # Verificación si el caracter pertence al universo
        if caracter in A:
            indice = A.index(caracter)
            # Aplicando la fórmula: C_k = ((x + k) mod N)
            # Donde N es el tamaño del universo
            nuevo_indice = (indice + k) % len(A)
            mensaje_cifrado += A[nuevo_indice]      
        else:
            # En caso de ser el carater de espacio se mantiene igual
            mensaje_cifrado += caracter
    return mensaje_cifrado

# Función de descifrado
def descifrar(mensaje_cifrado, k):
    mensaje_descifrado = ""
    # Recorriendo cada caracter del mensaje
    for caracter in mensaje_cifrado:
        # Verificación si el caracter pertence al universo
        if caracter in A:
            indice = A.index(caracter)
            # Aplicando la fórmula: D_k = ((x - k) mod N)
            # Donde N es el tamaño del universo
            nuevo_indice = (indice - k) % len(A)
            mensaje_descifrado += A[nuevo_indice]
        else:
            mensaje_descifrado += caracter
            
    return mensaje_descifrado


if __name__ == "__main__":
    print("\n <><><><><><> Algoritmo de Cifrado César <><><><><><>\n")
    
    # Validación del mensaje (Solo letras minúsculas y espacios)
    while True:
        mensaje = input("> Ingrese el mensaje a cifrar: ").lower()

        # Revisando que la cadena solo contenga letras minúsculas y espacios        
        es_valido = True
        for caracter in mensaje:
            if caracter not in A and caracter != " ":
                es_valido = False
                break
                
        if es_valido and len(mensaje) > 0:
            break
        else:
            print("\n![Error]: Ingrese únicamente letras minúsculas (a-z) y espacios. No se permiten números ni símbolos.\n")

    # Validación de la llave (0 al 25)
    while True:
        try:
            k = int(input("> Ingrese la llave de cifrado (0 al 25): "))
            if 0 <= k <= 25:
                break
            else:
                print("\n![Error]: La llave debe estar en el rango de 0 a 25.\n")
        except ValueError:
            print("\n![Error]: Debe ingresar un número entero válido.\n")

    # Ejecución con los datos validados
    mensaje_cifrado = cifrar(mensaje, k)
    mensaje_descifrado = descifrar(mensaje_cifrado, k)

    print("\n------------- Resultados -------------\n")
    print("--> Llave utilizada:   ", k)
    print("--> Mensaje original:  ", mensaje)
    print("--> Mensaje cifrado:   ", mensaje_cifrado)
    print("--> Mensaje descifrado:", mensaje_descifrado)
    print("\n--------------------------------------\n")