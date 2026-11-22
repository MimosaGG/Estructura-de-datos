import os


def escribir_corridas(nombre, corridas):
    with open(nombre, "w") as archivo:
        for corrida in corridas:
            archivo.write(" ".join(map(str, corrida)) + "\n")


def leer_corridas(nombre):
    if not os.path.exists(nombre):
        return []

    with open(nombre, "r") as archivo:
        return [
            list(map(int, linea.split()))
            for linea in archivo
            if linea.strip()
        ]


def intercalar_corridas(izquierda, derecha):
    resultado = []
    i = 0
    j = 0

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

    return resultado


def mezcla_equilibrada(numeros):
    archivo_a = "A.txt"
    archivo_b = "B.txt"
    archivo_c = "C.txt"
    archivo_d = "D.txt"

    # Distribuir los numeros en corridas iniciales
    corridas_a = []
    corridas_b = []

    for i, numero in enumerate(numeros):
        if i % 2 == 0:
            corridas_a.append([numero])
        else:
            corridas_b.append([numero])

    escribir_corridas(archivo_a, corridas_a)
    escribir_corridas(archivo_b, corridas_b)

    pasada = 1

    while True:
        entrada_a = leer_corridas(archivo_a)
        entrada_b = leer_corridas(archivo_b)

        salida_c = []
        salida_d = []

        if not entrada_a and not entrada_b:
            break

        # Mezclar las corridas por parejas
        cantidad = max(len(entrada_a), len(entrada_b))

        for i in range(cantidad):
            izquierda = entrada_a[i] if i < len(entrada_a) else []
            derecha = entrada_b[i] if i < len(entrada_b) else []

            mezcla = intercalar_corridas(izquierda, derecha)

            if i % 2 == 0:
                salida_c.append(mezcla)
            else:
                salida_d.append(mezcla)

        escribir_corridas(archivo_c, salida_c)
        escribir_corridas(archivo_d, salida_d)

        # Contar las corridas resultantes
        total = len(salida_c) + len(salida_d)

        if total == 1:
            break

        # Intercambiar archivos de entrada y salida
        archivo_a, archivo_c = archivo_c, archivo_a
        archivo_b, archivo_d = archivo_d, archivo_b

        pasada += 1

    # Recuperar la unica corrida ordenada
    resultado = leer_corridas(archivo_c)

    if not resultado:
        resultado = leer_corridas(archivo_d)

    return resultado[0] if resultado else []


numeros = [8, 3, 6, 1, 9, 2, 7, 4]

print("Lista original:", numeros)

resultado = mezcla_equilibrada(numeros)

print("Lista ordenada:", resultado)
