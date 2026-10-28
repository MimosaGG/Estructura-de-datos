
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.sig = None         


class Postre:
    

    def __init__(self, nombre):
        self.nombre = nombre
        self.cabeza = None       

    def ingredientes(self):
        lista, p = [], self.cabeza
        while p:
            lista.append(p.dato)
            p = p.sig
        return lista

    def tiene(self, ingrediente):
        p = self.cabeza
        while p:
            if clave(p.dato) == clave(ingrediente):
                return True
            p = p.sig
        return False

    def agregar(self, ingrediente):
       
        if self.tiene(ingrediente):
            return False
        nuevo = Nodo(ingrediente)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            p = self.cabeza
            while p.sig:
                p = p.sig
            p.sig = nuevo
        return True

    def quitar(self, ingrediente):
       
        ant, p = None, self.cabeza
        while p:
            if clave(p.dato) == clave(ingrediente):
                if ant is None:
                    self.cabeza = p.sig
                else:
                    ant.sig = p.sig
                return True
            ant, p = p, p.sig
        return False


def clave(texto):
    
    return " ".join(texto.split()).lower()


def limpiar(texto):
    return " ".join(texto.split())



def buscar(postres, nombre):

    k = clave(nombre)
    ini, fin = 0, len(postres) - 1
    while ini <= fin:
        mid = (ini + fin) // 2
        km = clave(postres[mid].nombre)
        if km == k:
            return True, mid
        if km < k:
            ini = mid + 1
        else:
            fin = mid - 1
    return False, ini



def imprimir_ingredientes(postres, nombre):                       
    if not postres:
        return "El arreglo POSTRES está vacío."
    if not clave(nombre):
        return "Error: el nombre del postre no puede estar vacío."
    ok, pos = buscar(postres, nombre)
    if not ok:
        return f"Error: el postre '{limpiar(nombre)}' no existe."
    ings = postres[pos].ingredientes()
    if not ings:
        return f"'{postres[pos].nombre}' no tiene ingredientes (lista vacía)."
    return f"Ingredientes de '{postres[pos].nombre}':\n" + \
           "\n".join(f"  - {i}" for i in ings)


def insertar_ingredientes(postres, nombre, nuevos):               
    ok, pos = buscar(postres, nombre)
    if not ok:
        return f"Error: el postre '{limpiar(nombre)}' no existe."
    nuevos = [limpiar(i) for i in nuevos if clave(i)]
    if not nuevos:
        return "Error: no se indicó ningún ingrediente."
    agregados, repetidos = [], []
    for ing in nuevos:
        (agregados if postres[pos].agregar(ing) else repetidos).append(ing)
    msg = ""
    if agregados:
        msg += f"Agregados a '{postres[pos].nombre}': {', '.join(agregados)}.\n"
    if repetidos:
        msg += f"Ya existían (no se agregaron): {', '.join(repetidos)}."
    return msg.strip()


def eliminar_ingrediente(postres, nombre, ingrediente):           
    ok, pos = buscar(postres, nombre)
    if not ok:
        return f"Error: el postre '{limpiar(nombre)}' no existe."
    if postres[pos].cabeza is None:
        return f"Error: '{postres[pos].nombre}' no tiene ingredientes."
    if not clave(ingrediente):
        return "Error: el ingrediente no puede estar vacío."
    if postres[pos].quitar(ingrediente):
        return f"Ingrediente '{limpiar(ingrediente)}' eliminado de '{postres[pos].nombre}'."
    return f"Error: '{limpiar(ingrediente)}' no es ingrediente de '{postres[pos].nombre}'."


def alta_postre(postres, nombre, ingredientes):                   
    nombre = limpiar(nombre)
    if not nombre:
        return "Error: el nombre del postre no puede estar vacío."
    ings = [limpiar(i) for i in ingredientes if clave(i)]
    if not ings:
        return "Error: el postre debe tener al menos un ingrediente."
    ok, pos = buscar(postres, nombre)
    if ok:
        return f"Error: el postre '{postres[pos].nombre}' ya existe."
    nuevo = Postre(nombre)
    for ing in ings:
        nuevo.agregar(ing)               
    postres.insert(pos, nuevo)           
    return f"Alta de '{nombre}' con {len(nuevo.ingredientes())} ingrediente(s)."


def baja_postre(postres, nombre):                                 
    if not postres:
        return "Error: el arreglo POSTRES está vacío."
    ok, pos = buscar(postres, nombre)
    if not ok:
        return f"Error: el postre '{limpiar(nombre)}' no existe."
    nombre_real = postres[pos].nombre
    del postres[pos]                    
    return f"Baja de '{nombre_real}' (con todos sus ingredientes)."



def eliminar_repetidos(postres):

    postres.sort(key=lambda p: clave(p.nombre))
    unicos, post_elim = [], 0
    for p in postres:
        if unicos and clave(unicos[-1].nombre) == clave(p.nombre):
            for ing in p.ingredientes():
                unicos[-1].agregar(ing)  
            post_elim += 1
        else:
            unicos.append(p)
    postres[:] = unicos


    ing_elim = 0
    for p in postres:
        actual = p.cabeza
        while actual:
            ant, q = actual, actual.sig
            while q:
                if clave(q.dato) == clave(actual.dato):
                    ant.sig = q.sig      
                    ing_elim += 1
                else:
                    ant = q
                q = q.sig
            actual = actual.sig
    return post_elim, ing_elim



def mostrar_todo(postres):
    if not postres:
        return "POSTRES está vacío."
    filas = []
    for i, p in enumerate(postres):
        ings = " -> ".join(p.ingredientes() + ["NIL"])
        filas.append(f"[{i}] {p.nombre} -> {ings}")
    return "\n".join(filas)


def cargar_ejemplo_con_repetidos(postres):
    """Carga datos 'crudos' (sin validar) para probar el ejercicio 2."""
    datos = {
        "Flan": ["huevo", "leche", "azúcar", "leche", "vainilla"],
        "Gelatina": ["grenetina", "agua", "azúcar"],
        "flan": ["caramelo", "Huevo"],
        "Pastel": ["harina", "huevo", "harina", "mantequilla"],
        "Gelatina ": ["fruta"],
        "Arroz con leche": ["arroz", "leche", "canela", "arroz"],
    }
    postres.clear()
    for nombre, ings in datos.items():
        p = Postre(nombre)
        for ing in ings:                 
            nuevo = Nodo(ing)
            if p.cabeza is None:
                p.cabeza = nuevo
            else:
                q = p.cabeza
                while q.sig:
                    q = q.sig
                q.sig = nuevo
        postres.append(p)               


def pedir_lista(texto):
    return [x for x in input(texto).split(",")]



MENU = """
===== POSTRES =====
 1. Imprimir ingredientes de un postre
 2. Insertar ingredientes a un postre
 3. Eliminar un ingrediente de un postre
 4. Alta de un postre (con todos sus ingredientes)
 5. Baja de un postre
 6. Mostrar toda la estructura
 7. Eliminar elementos repetidos (ejercicio 2)
 8. Cargar datos de ejemplo CON repetidos (para probar el 7)
 0. Salir"""


def main():
    postres = []
    while True:
        print(MENU)
        op = input("Opción: ").strip()
        if op == "0":
            break
        elif op == "1":
            print(imprimir_ingredientes(postres, input("Postre: ")))
        elif op == "2":
            n = input("Postre: ")
            print(insertar_ingredientes(postres, n, pedir_lista("Ingredientes (separados por coma): ")))
        elif op == "3":
            print(eliminar_ingrediente(postres, input("Postre: "), input("Ingrediente a eliminar: ")))
        elif op == "4":
            n = input("Nombre del nuevo postre: ")
            print(alta_postre(postres, n, pedir_lista("Ingredientes (separados por coma): ")))
        elif op == "5":
            print(baja_postre(postres, input("Postre a dar de baja: ")))
        elif op == "6":
            print(mostrar_todo(postres))
        elif op == "7":
            if not postres:
                print("POSTRES está vacío.")
            else:
                p, i = eliminar_repetidos(postres)
                print(f"Eliminados: {p} postre(s) repetido(s) y {i} ingrediente(s) repetido(s).")
        elif op == "8":
            cargar_ejemplo_con_repetidos(postres)
            print("Datos cargados:\n" + mostrar_todo(postres))
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
