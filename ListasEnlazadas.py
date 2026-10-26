class Nodo:
    def __init__(self, info):
        self.info = info
        self.liga = None

class ListaSimple:
    def __init__(self):
        self.p = None

    def crea_inicio(self):
        primer_info = input("Ingrese el valor de INFORMACIÓN para el primer nodo: ")
        self.p = Nodo(primer_info)
        self.p.liga = None

        res = input("¿Desea ingresar más nodos a la lista? (Sí/No): ").strip().lower()

        while res in ["si", "sí", "s"]:
            nuevo_info = input("Ingrese el valor de INFORMACIÓN para el nuevo nodo: ")
            q = Nodo(nuevo_info)

            q.liga = self.p
            self.p = q

            res = input("¿Desea ingresar más nodos a la lista? (Sí/No): ").strip().lower()
            
        print("Lista creada exitosamente al inicio.")

    def insertar_inicio(self, valor):
        nuevo = Nodo(valor)
        nuevo.liga = self.p
        self.p = nuevo
        print(f"¡Dato '{valor}' insertado correctamente al inicio!")

    def recorrer_lista(self):
        actual = self.p
        print("Estructura de la lista: ", end="")
        while actual is not None:
            print(f"[{actual.info}] -> ", end="")
            actual = actual.liga
        print("NIL")

    def recorrer_desde(self, nodo_inicio, nombre_camino="Lista"):
        actual = nodo_inicio
        print(f"Estructura ({nombre_camino}): ", end="")
        while actual is not None:
            print(f"[{actual.info}] -> ", end="")
            actual = actual.liga
        print("NIL")

    def buscar(self, valor):
        actual = self.p
        posicion = 1
        while actual is not None:
            if actual.info == valor:
                return True, posicion
            actual = actual.liga
            posicion += 1
        return False, -1

    def eliminar(self, valor):
        actual = self.p
        anterior = None

        while actual is not None:
            if actual.info == valor:
                if anterior is None:
                    self.p = actual.liga
                else:
                    anterior.liga = actual.liga
                print(f"¡Dato '{valor}' eliminado correctamente!")
                return True
            
            anterior = actual
            actual = actual.liga

        print(f"El dato '{valor}' no se encontró en la lista.")
        return False

if __name__ == "__main__":
    lista = ListaSimple()
    lista.crea_inicio()
    lista.recorrer_lista() 

    print("\n--- PRUEBA DE INSERCIÓN ---")
    valor_a_insertar = input("Ingrese un valor para insertar al inicio: ")
    lista.insertar_inicio(valor_a_insertar)
    lista.recorrer_lista()

    print("\n--- PRUEBA DE BÚSQUEDA ---")
    valor_a_buscar = input("Ingrese el valor que desea buscar: ")
    encontrado, pos = lista.buscar(valor_a_buscar)
    if encontrado:
        print(f"¡Dato encontrado! Está en la posición (desde el inicio actual): {pos}")
    else:
        print("El dato no existe en la lista.")

    print("\n--- PRUEBA DE ELIMINACIÓN ---")
    valor_a_eliminar = input("Ingrese el valor que desea eliminar: ")
    lista.eliminar(valor_a_eliminar)
    
    print("\nLista después de la operación de eliminación:")
    lista.recorrer_lista()

    print("\n--- DEMOSTRACIÓN: DOS NODOS APUNTANDO AL MISMO NODO ---")
    nodo_comun = Nodo("Comun_Z")
    
    nodo_x = Nodo("Nodo_X")
    nodo_y = Nodo("Nodo_Y")

    nodo_x.liga = nodo_comun
    nodo_y.liga = nodo_comun

    lista_x = ListaSimple()
    lista_x.p = nodo_x
    lista_x.recorrer_desde(lista_x.p, "Camino X")

    lista_y = ListaSimple()
    lista_y.p = nodo_y
    lista_y.recorrer_desde(lista_y.p, "Camino Y")

    print(f"\n¿Ambos nodos apuntan físicamente al mismo objeto en memoria? {nodo_x.liga is nodo_y.liga}")
