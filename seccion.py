def seccion(numeros):
    for i in range(len(numeros)):
        lowest_valor_index = i
        for j in range(i + 1, len(numeros)):
            if numeros[j] < numeros[lowest_valor_index]:
                lowest_valor_index = j
        numeros[i], numeros[lowest_valor_index] = numeros[lowest_valor_index], numeros[i]

listanumeros = [2,3,46,7,32,83,31] 
print("Lista aleatoria" + str(listanumeros))
seccion(listanumeros) 
print("Lista ordenadas" + str(listanumeros))      