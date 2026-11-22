def mezclar(lista, inicio, medio, fin):
    izquierda = lista[inicio:medio]
    derecha = lista[medio:fin]

    i = 0
    j = 0
    k = inicio

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            lista[k] = izquierda[i]
            i += 1
        else:
            lista[k] = derecha[j]
            j += 1
        k += 1

    while i < len(izquierda):
        lista[k] = izquierda[i]
        i += 1
        k += 1

    while j < len(derecha):
        lista[k] = derecha[j]
        j += 1
        k += 1


def mezcla_directa(lista):
    tamaño = 1
    n = len(lista)

    while tamaño < n:
        inicio = 0

        while inicio < n:
            medio = min(inicio + tamaño, n)
            fin = min(inicio + 2 * tamaño, n)

            if medio < fin:
                mezclar(lista, inicio, medio, fin)

            inicio += 2 * tamaño

        tamaño *= 2

    return lista


numeros = [8, 3, 6, 1, 9, 2, 7, 4]

print("Lista original:", numeros)

resultado = mezcla_directa(numeros)

print("Lista ordenada:", resultado)
