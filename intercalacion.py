def intercalacion(lista1, lista2):
    resultado = []
    i = 0
    j = 0

    while i < len(lista1) and j < len(lista2):
        if lista1[i] < lista2[j]:
            resultado.append(lista1[i])
            i += 1
        else:
            resultado.append(lista2[j])
            j += 1

    resultado.extend(lista1[i:])
    resultado.extend(lista2[j:])

    return resultado


lista1 = [2, 6, 10, 14]
lista2 = [1, 3, 8, 12]

print("Primera lista:", lista1)
print("Segunda lista:", lista2)

resultado = intercalacion(lista1, lista2)

print("Lista intercalada:", resultado)
