def pedirnumero(lista):
    for numeros in lista:
        print(numeros,end=" ")
    num = int(input("ingresa un numero de la lista:"))
    return num

def busquedasecuencial(lista,num):
    for i in range(0,len(lista)):
        if num == lista[i]:
            return True
    return False
lista = [1,2,3,4,5]
while True:
    num = pedirnumero(lista)
    encontrado=busquedasecuencial(lista,num)
    if encontrado == True:
        print("Colocaste un numero de la lista, felicidades.")
        break
    else:
        print("Intetalo de nuevo:")