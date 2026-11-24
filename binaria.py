def pedirNumero(lista):
    for numero in lista:
        print(numero,end=" ")
    num = int(input("\nPorfavor de ingresar un numero de la lista: "))
    return num

def busquedaBinaria(lista,num):
    tam = len(lista)
    cont = 0
    inf = 0
    sup = tam
    while inf <= sup and cont<tam:
        mitad =int((inf+sup)/2)
        if lista[mitad] == num:
            return True
        elif lista[mitad]>num:
            sup =mitad
            mitad =int((inf+sup)/2)
        elif lista[mitad]<num:
            inf = mitad
            mitad =int((inf+sup)/2)
        cont =+ 1
    return False       
        
lista = [1,2,3,4,5,6,7,8,9,10]
while True:
    num = pedirNumero(lista)        
    encontrado = busquedaBinaria(lista,num)
    if encontrado == True:
        print("El numero ingresado fue encontrado")
        decision = input("Desea continuar? (Y/N): ").upper
        if decision == "Y":
            continue
        elif decision == "N":
            print("Nos vemos.")
            break
    else:
        print("El numero no esta en la lista")