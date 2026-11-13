def inseccion(numeros):
    for i in range(len(numeros)):
        item_a_ingresar = numeros[i]
        
        j = i -1
        
        while j >= 0 and numeros[j] > item_a_ingresar:
            numeros [j + 1] = numeros[i]    
            j-=1 
        numeros [j+1] = item_a_ingresar

listanumerosaleatorios = [12,4,232,56,76,23,23]
print("Lista aletoria" + str(listanumerosaleatorios))
inseccion(listanumerosaleatorios) 
print("Numeros ordenada" + str(listanumerosaleatorios))      