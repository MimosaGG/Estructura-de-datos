def burbuja(numeros):
    intercambio = True
    while intercambio:
        for i in range(len(numeros) - 1):
            if numeros[i] > numeros[i + 1]:
                numeros[i], numeros[i + 1] = numeros[i + 1], numeros[i]
                intercambio = False
                
numerolista = [2,3,8,5,4]
burbuja(numerolista)
print(numerolista)