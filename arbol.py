"""
ÁRBOLES BINARIOS DE BÚSQUEDA  -  Estructuras de Datos
=====================================================
Implementa la clase Nodo y la clase Arbol con todos los métodos de la
presentación "Unidad VII. Árboles", más una interfaz gráfica (tkinter) para
ver el árbol, insertar nodos donde quieras y eliminar nodos.

Menú de la presentación (todos implementados):
 [1] Insertar elemento              [10] Recorrer por niveles (amplitud)
 [2] Mostrar árbol acostado         [11] Altura del árbol
 [3] Graficar árbol completo        [12] Cantidad de hojas
 [4] Buscar un elemento             [13] Cantidad de nodos
 [5] Recorrido PreOrden             [14] (extra) ¿Está equilibrado?
 [6] Recorrido InOrden              [15] ¿Es completo?
 [7] Recorrido PostOrden            [16] ¿Es lleno?
 [8] Eliminar (PREDECESOR)          [17] Eliminar el árbol
 [9] Eliminar (SUCESOR)             + esVacio, regresaRaiz, buscaMenor, buscaMayor, podarArbol

Conceptos de la presentación también incluidos: nivel, altura, peso, orden,
grado, camino y su longitud, padre/hijo/hermano, nodo raíz/interior/hoja,
subárbol, árboles distintos/similares/equivalentes, completo, lleno,
degenerado, equilibrado AVL y perfectamente equilibrado.

Ejecutar:   python arbol_bst.py            (interfaz gráfica)
            python arbol_bst.py --consola  (menú de texto como en el PDF)
"""
import sys
from collections import deque

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    from tkinter import font as tkfont
except ImportError:          # permite usar la lógica sin entorno gráfico
    tk = ttk = messagebox = tkfont = None

sys.setrecursionlimit(20000)


# ============================================================
#                      CLASE NODO
# ============================================================
class Nodo:
    """Nodo de un árbol binario:   [ izquierdo | dato | derecho ]"""
    __slots__ = ("dato", "izquierdo", "derecho")

    def __init__(self, dato, izquierdo=None, derecho=None):
        self.dato = dato                  # valor entero que contiene el nodo
        self.izquierdo = izquierdo        # izquierdoPtr (None = NULL)
        self.derecho = derecho            # derechoPtr   (None = NULL)

    def es_hoja(self):
        return self.izquierdo is None and self.derecho is None

    def grado(self):
        """Grado de un nodo = número de hijos (0, 1 o 2)."""
        return (self.izquierdo is not None) + (self.derecho is not None)

    def hijos(self):
        return [h for h in (self.izquierdo, self.derecho) if h is not None]

    def __repr__(self):
        return f"Nodo({self.dato})"


def _si(b):
    return "SÍ" if b else "NO"


# ============================================================
#                      CLASE ÁRBOL
# ============================================================
class Arbol:
    """Árbol binario de búsqueda (raizPtr apunta al nodo raíz)."""

    ORDEN = 2     # Orden: número máximo de hijos por nodo (árbol binario)

    # ---------------- constructor / destructor ----------------
    def __init__(self, valores=None):
        """Constructor: inicializa la raíz con valor nulo."""
        self.raiz = None
        for v in (valores or []):
            self.insertar_nodo(v)

    def __del__(self):
        """Destructor: libera la memoria ocupada por los nodos (podarArbol)."""
        try:
            self.podar_arbol()
        except Exception:
            pass

    def es_vacio(self):
        """Verifica si la raíz del árbol apunta a vacío."""
        return self.raiz is None

    def regresa_raiz(self):
        """Regresa el nodo de la raíz del árbol."""
        return self.raiz

    # ---------------- [1] insertar ----------------
    def insertar_nodo(self, valor, traza=None):
        """
        Crea un nuevo nodo y lo inserta en el lugar correspondiente (recursivo).
        Si el valor ya existe no se inserta (devuelve False).
        'traza' (lista) recibe la prueba de escritorio de la recursión.
        """
        if self.existe(valor):
            if traza is not None:
                traza.append(f"El valor {valor} ya existe en el árbol: no se inserta.")
            return False
        if traza is not None:
            traza.append(f"Llamada en el menú principal: insertarNodo({valor}, raizPtr)")
        self.raiz = self._insertar(valor, self.raiz, traza, 1)
        return True

    def _insertar(self, valor, nodo, traza, iteracion):
        if nodo is None:
            if traza is not None:
                traza.append(f"Iteración {iteracion} de la recursión: nodoPtr = NULL → "
                             f"se crea el nuevo nodo con el dato {valor}.")
            return Nodo(valor)
        if valor < nodo.dato:
            if traza is not None:
                traza.append(f"Iteración {iteracion} de la recursión: nodoPtr = nodo con el dato "
                             f"{nodo.dato} (no es nulo). {valor} < {nodo.dato} → "
                             f"insertarNodo({valor}, nodoPtr→izquierdoPtr)")
            nodo.izquierdo = self._insertar(valor, nodo.izquierdo, traza, iteracion + 1)
        else:
            if traza is not None:
                traza.append(f"Iteración {iteracion} de la recursión: nodoPtr = nodo con el dato "
                             f"{nodo.dato} (no es nulo). {valor} > {nodo.dato} → "
                             f"insertarNodo({valor}, nodoPtr→derechoPtr)")
            nodo.derecho = self._insertar(valor, nodo.derecho, traza, iteracion + 1)
        return nodo

    def insertar_en(self, padre, lado, valor, exigir_bst=False):
        """
        Inserta un nodo EXACTAMENTE donde se pide: como hijo 'izq' o 'der' de
        'padre' (padre=None → como raíz de un árbol vacío).
        Con exigir_bst=True se rechaza si rompe la propiedad de búsqueda.
        Devuelve (ok, mensaje).
        """
        if self.existe(valor):
            return False, f"El valor {valor} ya existe en el árbol."
        if padre is None:
            if self.raiz is not None:
                return False, "El árbol ya tiene raíz."
            self.raiz = Nodo(valor)
            return True, f"{valor} insertado como raíz."
        atributo = "izquierdo" if lado == "izq" else "derecho"
        if getattr(padre, atributo) is not None:
            return False, f"El hijo {'izquierdo' if lado == 'izq' else 'derecho'} de {padre.dato} ya está ocupado."
        nuevo = Nodo(valor)
        setattr(padre, atributo, nuevo)
        if exigir_bst and self.nodos_que_violan():
            setattr(padre, atributo, None)
            return False, (f"{valor} como hijo {'izquierdo' if lado == 'izq' else 'derecho'} de "
                           f"{padre.dato} rompería la propiedad del árbol de búsqueda "
                           f"(izquierda menores, derecha mayores).")
        return True, (f"{valor} insertado como hijo {'izquierdo' if lado == 'izq' else 'derecho'} "
                      f"de {padre.dato}.")

    # ---------------- [4] búsqueda ----------------
    def busqueda(self, x, traza=None):
        """Busca x de forma recursiva en el campo dato de los nodos (True/False)."""
        if traza is not None:
            traza.append(f"Llamada en el menú principal: búsqueda({x}, raizPtr)")
        return self._busqueda(x, self.raiz, traza)

    def _busqueda(self, x, nodo, traza):
        if nodo is None:
            if traza is not None:
                traza.append("nodoPtr == NULL → return False")
            return False
        if x < nodo.dato:
            if traza is not None:
                traza.append(f"x ({x}) < nodoPtr→dato ({nodo.dato})? Sí → "
                             f"return búsqueda(x, nodoPtr→izquierdoPtr)")
            return self._busqueda(x, nodo.izquierdo, traza)
        if x > nodo.dato:
            if traza is not None:
                traza.append(f"x ({x}) < nodoPtr→dato ({nodo.dato})? No.  "
                             f"x ({x}) > nodoPtr→dato ({nodo.dato})? Sí → "
                             f"return búsqueda(x, nodoPtr→derechoPtr)")
            return self._busqueda(x, nodo.derecho, traza)
        if traza is not None:
            traza.append(f"x ({x}) no es menor ni mayor que nodoPtr→dato ({nodo.dato}) → return True")
        return True

    def ruta_busqueda(self, x):
        """Nodos visitados por la búsqueda binaria de x (para resaltarlos)."""
        ruta, n = [], self.raiz
        while n is not None:
            ruta.append(n)
            if x == n.dato:
                break
            n = n.izquierdo if x < n.dato else n.derecho
        return ruta

    def buscar_nodo(self, x):
        """Devuelve el nodo con dato x (búsqueda binaria; si el árbol no está
        ordenado, cae a una búsqueda completa) o None."""
        n = self.raiz
        while n is not None:
            if x == n.dato:
                return n
            n = n.izquierdo if x < n.dato else n.derecho
        return self._buscar_general(x)

    def _buscar_general(self, x):
        pila = [self.raiz] if self.raiz else []
        while pila:
            n = pila.pop()
            if n.dato == x:
                return n
            pila.extend(n.hijos())
        return None

    def existe(self, x):
        return self._buscar_general(x) is not None

    def busca_menor(self, nodo=None):
        """Regresa el nodo con el dato menor (del árbol o del subárbol dado)."""
        n = nodo if nodo is not None else self.raiz
        while n is not None and n.izquierdo is not None:
            n = n.izquierdo
        return n

    def busca_mayor(self, nodo=None):
        """Regresa el nodo con el dato mayor (del árbol o del subárbol dado)."""
        n = nodo if nodo is not None else self.raiz
        while n is not None and n.derecho is not None:
            n = n.derecho
        return n

    # ---------------- recorridos [5][6][7][10] ----------------
    def _recorrer(self, tipo, nodo, salida):
        if nodo is None:
            return
        if tipo == "pre":
            salida.append(nodo)
        self._recorrer(tipo, nodo.izquierdo, salida)
        if tipo == "in":
            salida.append(nodo)
        self._recorrer(tipo, nodo.derecho, salida)
        if tipo == "post":
            salida.append(nodo)

    def recorrido_nodos(self, tipo):
        """tipo: 'pre', 'in', 'post' o 'amplitud' → lista de NODOS en ese orden."""
        if tipo == "amplitud":
            return [n for nivel in self._niveles() for n in nivel]
        salida = []
        self._recorrer(tipo, self.raiz, salida)
        return salida

    def pre_orden(self):      # (raíz, izquierdo, derecho)
        return [n.dato for n in self.recorrido_nodos("pre")]

    def in_orden(self):       # (izquierdo, raíz, derecho) → ascendente
        return [n.dato for n in self.recorrido_nodos("in")]

    def post_orden(self):     # (izquierdo, derecho, raíz)
        return [n.dato for n in self.recorrido_nodos("post")]

    def _niveles(self):
        niveles, actual = [], ([self.raiz] if self.raiz else [])
        while actual:
            niveles.append(actual)
            actual = [h for n in actual for h in n.hijos()]
        return niveles

    def amplitud(self):
        """Recorrido por niveles (de arriba abajo, de izquierda a derecha)."""
        return [n.dato for n in self.recorrido_nodos("amplitud")]

    def amplitud_por_niveles(self):
        return [[n.dato for n in nivel] for nivel in self._niveles()]

    def traza_recorrido(self, tipo):
        """
        Prueba de escritorio del recorrido (como las láminas de la presentación):
        nodos pendientes y secuencia que se va generando.
        """
        nombres = {"pre": "PreOrden (raíz, izquierdo, derecho)",
                   "in": "InOrden (izquierdo, raíz, derecho)",
                   "post": "PostOrden (izquierdo, derecho, raíz)"}
        if tipo == "amplitud":
            return self._traza_amplitud()
        lineas = [f"Prueba de escritorio - recorrido {nombres[tipo]}"]
        pend, seq = [], []

        def procesa(n):
            seq.append(n.dato)
            lineas.append(f"   ✔ Procesa {n.dato}      Secuencia: {' – '.join(map(str, seq))}")

        def rec(n):
            if n is None:
                tope = f"nodo pendiente {pend[-1]}" if pend else "el main"
                lineas.append(f"   nodoPtr == NULL → regresa a {tope}")
                return
            pend.append(n.dato)
            lineas.append(f"→ Entra a {n.dato}      Pendientes: {pend}")
            if tipo == "pre":
                procesa(n)
            rec(n.izquierdo)
            if tipo == "in":
                procesa(n)
            rec(n.derecho)
            if tipo == "post":
                procesa(n)
            pend.pop()

        rec(self.raiz)
        lineas.append("TERMINA, ya no hay pendientes.")
        lineas.append(f"Secuencia final: {' – '.join(map(str, seq))}")
        return lineas

    def _traza_amplitud(self):
        lineas = ["Prueba de escritorio - recorrido por niveles (amplitud) con una cola"]
        if self.raiz is None:
            return lineas + ["El árbol está vacío."]
        cola, seq = deque([self.raiz]), []
        while cola:
            lineas.append(f"Cola: {[n.dato for n in cola]}")
            n = cola.popleft()
            seq.append(n.dato)
            hijos = n.hijos()
            lineas.append(f"   Sale {n.dato} → se procesa; entran a la cola: "
                          f"{[h.dato for h in hijos] or 'ningún hijo'}")
            cola.extend(hijos)
        lineas.append(f"Secuencia final: {' – '.join(map(str, seq))}")
        return lineas

    # ---------------- [11][12][13] altura, hojas, nodos ----------------
    def altura(self, nodo=None):
        """Altura = número máximo de niveles (árbol vacío = 0, solo raíz = 1)."""
        return self._altura(nodo if nodo is not None else self.raiz)

    def _altura(self, n):
        return 0 if n is None else 1 + max(self._altura(n.izquierdo), self._altura(n.derecho))

    def contar_hojas(self, nodo=None):
        return self._hojas(nodo if nodo is not None else self.raiz)

    def _hojas(self, n):
        if n is None:
            return 0
        if n.es_hoja():
            return 1
        return self._hojas(n.izquierdo) + self._hojas(n.derecho)

    def contar_nodos(self, nodo=None):
        """Peso del árbol = número de nodos."""
        return self._cuenta(nodo if nodo is not None else self.raiz)

    def _cuenta(self, n):
        return 0 if n is None else 1 + self._cuenta(n.izquierdo) + self._cuenta(n.derecho)

    def contar_interiores(self):
        """Nodos interiores (ramas): no son la raíz y tienen al menos un hijo."""
        return sum(1 for n in self.recorrido_nodos("pre") if n is not self.raiz and not n.es_hoja())

    def traza_altura(self):
        lineas = ["Prueba de escritorio - altura (cada nodo = 1 + max(altura izq, altura der))"]
        def rec(n):
            if n is None:
                return 0
            hl, hr = rec(n.izquierdo), rec(n.derecho)
            h = 1 + max(hl, hr)
            lineas.append(f"   altura({n.dato}) = 1 + max({hl}, {hr}) = {h}")
            return h
        h = rec(self.raiz)
        lineas.append(f"Altura del árbol = {h}")
        return lineas

    def traza_hojas(self):
        lineas = ["Prueba de escritorio - contarHojas (NULL → 0, hoja → 1, otro → izq + der)"]
        def rec(n):
            if n is None:
                return 0
            if n.es_hoja():
                lineas.append(f"   contarHojas({n.dato}) → es hoja → 1")
                return 1
            a, b = rec(n.izquierdo), rec(n.derecho)
            lineas.append(f"   contarHojas({n.dato}) = {a} + {b} = {a + b}")
            return a + b
        lineas.append(f"Cantidad de hojas = {rec(self.raiz)}")
        return lineas

    # ---------------- [8][9] eliminar ----------------
    def _ubicar(self, x):
        """Devuelve (padre, nodo) del dato x o (None, None)."""
        padre, n = None, self.raiz
        while n is not None:
            if x == n.dato:
                return padre, n
            padre, n = n, (n.izquierdo if x < n.dato else n.derecho)
        pila = [(self.raiz, None)] if self.raiz else []
        while pila:                       # árbol no ordenado: búsqueda completa
            n, padre = pila.pop()
            if n.dato == x:
                return padre, n
            pila.extend((h, n) for h in n.hijos())
        return None, None

    def _padre_de(self, nodo):
        pila = [(self.raiz, None)] if self.raiz else []
        while pila:
            n, padre = pila.pop()
            if n is nodo:
                return padre
            pila.extend((h, n) for h in n.hijos())
        return None

    def _enlazar(self, padre, viejo, nuevo):
        if padre is None:
            self.raiz = nuevo
        elif padre.izquierdo is viejo:
            padre.izquierdo = nuevo
        else:
            padre.derecho = nuevo

    def eliminar_predecesor(self, x, traza=None):
        """Elimina el nodo con dato x; con dos hijos lo sustituye por el
        PREDECESOR en inOrden (mayor del subárbol izquierdo)."""
        return self._eliminar_valor(x, "predecesor", traza)

    def eliminar_sucesor(self, x, traza=None):
        """Elimina el nodo con dato x; con dos hijos lo sustituye por el
        SUCESOR en inOrden (menor del subárbol derecho)."""
        return self._eliminar_valor(x, "sucesor", traza)

    def _eliminar_valor(self, x, modo, traza):
        padre, nodo = self._ubicar(x)
        if nodo is None:
            if traza is not None:
                traza.append(f"El valor {x} no está en el árbol: no se elimina nada.")
            return False
        return self.eliminar_nodo(nodo, modo, traza, padre)

    def eliminar_nodo(self, nodo, modo="predecesor", traza=None, padre="?"):
        """Elimina un nodo concreto (por referencia). Casos de la presentación:
        sin hijos / con un subárbol hijo / con dos subárboles hijo."""
        if padre == "?":
            padre = self._padre_de(nodo)
        log = traza if traza is not None else []
        if nodo.es_hoja():
            log.append(f"Caso 1 - nodo sin hijos (hoja): se pone a NULL el apuntador de su "
                       f"padre y se elimina el {nodo.dato}.")
            self._enlazar(padre, nodo, None)
        elif nodo.izquierdo is None or nodo.derecho is None:
            hijo = nodo.izquierdo or nodo.derecho
            log.append(f"Caso 2 - nodo con un subárbol hijo: el subárbol de {hijo.dato} pasa a "
                       f"ser subárbol del padre y se elimina el {nodo.dato}.")
            self._enlazar(padre, nodo, hijo)
        else:
            ino = self.in_orden()
            log.append(f"Caso 3 - nodo con dos subárboles hijo. InOrden: {' – '.join(map(str, ino))}")
            if modo == "predecesor":
                p, cand = nodo, nodo.izquierdo
                while cand.derecho is not None:
                    p, cand = cand, cand.derecho
                log.append(f"   Predecesor = mayor del subárbol izquierdo = {cand.dato}. "
                           f"Se reemplaza el valor {nodo.dato} por {cand.dato} y se borra el nodo del predecesor.")
                nodo.dato = cand.dato
                self._enlazar(p, cand, cand.izquierdo)
            else:
                p, cand = nodo, nodo.derecho
                while cand.izquierdo is not None:
                    p, cand = cand, cand.izquierdo
                log.append(f"   Sucesor = menor del subárbol derecho = {cand.dato}. "
                           f"Se reemplaza el valor {nodo.dato} por {cand.dato} y se borra el nodo del sucesor.")
                nodo.dato = cand.dato
                self._enlazar(p, cand, cand.derecho)
        return True

    # ---------------- [17] eliminar el árbol ----------------
    def podar_arbol(self, traza=None):
        """Libera (recursivamente, en postorden) todos los nodos del árbol."""
        self.raiz = self._podar(self.raiz, traza, [])

    def _podar(self, nodo, traza, pendientes):
        if nodo is None:
            return None
        pendientes.append(nodo.dato)
        if traza is not None:
            traza.append(f"Pendientes: {pendientes}")
        nodo.izquierdo = self._podar(nodo.izquierdo, traza, pendientes)
        nodo.derecho = self._podar(nodo.derecho, traza, pendientes)
        if traza is not None:
            traza.append(f"   Pendiente {nodo.dato}. Elimina nodo")
        pendientes.pop()
        return None

    eliminar_arbol = podar_arbol

    # ---------------- [2][3] mostrar y graficar ----------------
    def muestra_acostado(self):
        """Árbol en horizontal con la raíz a la izquierda (derecha arriba)."""
        lineas = []

        def rec(n, nivel):
            if n is None:
                return
            rec(n.derecho, nivel + 1)
            lineas.append("      " * nivel + str(n.dato))
            rec(n.izquierdo, nivel + 1)
        rec(self.raiz, 0)
        return "\n".join(lineas) if lineas else "(árbol vacío)"

    def graficar_texto(self):
        """Árbol dibujado en texto, con la raíz arriba."""
        if self.raiz is None:
            return "(árbol vacío)"
        pos, cont = {}, [0]

        def rec(n, prof):
            if n is None:
                return
            rec(n.izquierdo, prof + 1)
            pos[n] = (cont[0], prof)
            cont[0] += 1
            rec(n.derecho, prof + 1)
        rec(self.raiz, 0)
        ancho = max(len(str(n.dato)) for n in pos) + 2
        filas = 2 * self.altura() - 1
        grid = [[" "] * (cont[0] * ancho) for _ in range(filas)]
        centro = {n: i * ancho + ancho // 2 for n, (i, _) in pos.items()}

        for n, (i, d) in pos.items():
            txt = str(n.dato)
            ini = centro[n] - len(txt) // 2
            for k, ch in enumerate(txt):
                grid[2 * d][ini + k] = ch
            pc, fila = centro[n], 2 * d + 1
            izq, der = n.izquierdo, n.derecho
            if izq or der:
                a = centro[izq] if izq else pc
                b = centro[der] if der else pc
                for col in range(a, b + 1):
                    grid[fila][col] = "─"
                grid[fila][pc] = "┴" if (izq and der) else ("┘" if izq else "└")
                if izq:
                    grid[fila][a] = "┌"
                if der:
                    grid[fila][b] = "┐"
        return "\n".join("".join(f).rstrip() for f in grid)

    # ---------------- propiedades del árbol ----------------
    def grado_arbol(self):
        """Grado del árbol = máximo grado de todos sus nodos."""
        return max((n.grado() for n in self.recorrido_nodos("pre")), default=0)

    def es_completo(self):
        """Completo: todos los niveles llenos salvo el último, cuyas hojas están
        lo más a la izquierda posible."""
        if self.raiz is None:
            return True
        cola, hueco = deque([self.raiz]), False
        while cola:
            n = cola.popleft()
            for h in (n.izquierdo, n.derecho):
                if h is None:
                    hueco = True
                else:
                    if hueco:
                        return False
                    cola.append(h)
        return True

    def es_lleno(self):
        """Lleno: todos los nodos tienen cero o dos hijos."""
        return all(n.grado() in (0, 2) for n in self.recorrido_nodos("pre"))

    def es_degenerado(self):
        """Degenerado: un solo nodo hoja y cada nodo no hoja tiene un solo hijo
        (equivale a una lista enlazada)."""
        if self.raiz is None:
            return False
        nodos = self.recorrido_nodos("pre")
        return all(n.grado() <= 1 for n in nodos) and self._hojas(self.raiz) == 1

    def es_avl(self):
        """AVL: en todo nodo la diferencia de alturas de sus subárboles es ≤ 1."""
        def rec(n):
            if n is None:
                return 0
            a, b = rec(n.izquierdo), rec(n.derecho)
            if a == -1 or b == -1 or abs(a - b) > 1:
                return -1
            return 1 + max(a, b)
        return rec(self.raiz) != -1

    def es_perfectamente_equilibrado(self):
        """En todo nodo, el nº de nodos de los subárboles izq. y der. difiere ≤ 1."""
        def rec(n):
            if n is None:
                return 0
            a, b = rec(n.izquierdo), rec(n.derecho)
            if a == -1 or b == -1 or abs(a - b) > 1:
                return -1
            return 1 + a + b
        return rec(self.raiz) != -1

    def nodos_que_violan(self):
        """Nodos que rompen la propiedad de árbol de búsqueda (lista vacía = válido)."""
        malos = []

        def rec(n, minimo, maximo):
            if n is None:
                return
            if (minimo is not None and n.dato <= minimo) or (maximo is not None and n.dato >= maximo):
                malos.append(n)
            rec(n.izquierdo, minimo, n.dato if maximo is None else min(maximo, n.dato))
            rec(n.derecho, n.dato if minimo is None else max(minimo, n.dato), maximo)
        rec(self.raiz, None, None)
        return malos

    def es_bst(self):
        return not self.nodos_que_violan()

    # ---------------- conceptos de un nodo ----------------
    def _camino_donde(self, pred):
        pila = [(self.raiz, [self.raiz])] if self.raiz else []
        while pila:
            n, cam = pila.pop()
            if pred(n):
                return cam
            for h in reversed(n.hijos()):
                pila.append((h, cam + [h]))
        return []

    def camino_a(self, valor):
        """Camino (secuencia de nodos) desde la raíz hasta el dato 'valor'."""
        return self._camino_donde(lambda n: n.dato == valor)

    def informacion_nodo(self, nodo):
        cam = self._camino_donde(lambda n: n is nodo)
        padre = cam[-2] if len(cam) > 1 else None
        hermano = None
        if padre:
            hermano = padre.derecho if padre.izquierdo is nodo else padre.izquierdo
        if padre is None:
            tipo = "Raíz" + (" (y también hoja)" if nodo.es_hoja() else "")
        elif nodo.es_hoja():
            tipo = "Hoja"
        else:
            tipo = "Interior (rama)"
        fe = self._altura(nodo.izquierdo) - self._altura(nodo.derecho)
        return [
            f"Nodo {nodo.dato}",
            f"   Tipo: {tipo}",
            f"   Nivel: {len(cam)}  (la raíz es el nivel 1)",
            f"   Grado (número de hijos): {nodo.grado()}",
            f"   Padre: {padre.dato if padre else 'ninguno (es la raíz)'}",
            f"   Hermano: {hermano.dato if hermano else 'ninguno'}",
            f"   Hijo izquierdo: {nodo.izquierdo.dato if nodo.izquierdo else 'NULL'}   "
            f"Hijo derecho: {nodo.derecho.dato if nodo.derecho else 'NULL'}",
            f"   Camino desde la raíz: {' → '.join(str(n.dato) for n in cam)}",
            f"   Longitud del camino: {len(cam)} nodos ({len(cam) - 1} aristas)",
            f"   Subárbol: {self._cuenta(nodo)} nodos, altura {self._altura(nodo)}, "
            f"{self._hojas(nodo)} hoja(s)",
            f"   Factor de equilibrio (alt. izq − alt. der): {fe}",
        ]

    def subarbol(self, valor):
        """Devuelve una COPIA del subárbol cuyo nodo raíz tiene el dato 'valor'."""
        n = self.buscar_nodo(valor)
        if n is None:
            return None

        def copia(x):
            return None if x is None else Nodo(x.dato, copia(x.izquierdo), copia(x.derecho))
        nuevo = Arbol()
        nuevo.raiz = copia(n)
        return nuevo

    # ---------------- comparación de árboles ----------------
    @staticmethod
    def _misma_estructura(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        return (Arbol._misma_estructura(a.izquierdo, b.izquierdo)
                and Arbol._misma_estructura(a.derecho, b.derecho))

    @staticmethod
    def _misma_info(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        return (a.dato == b.dato and Arbol._misma_info(a.izquierdo, b.izquierdo)
                and Arbol._misma_info(a.derecho, b.derecho))

    def comparar(self, otro):
        """'distintos' (estructura diferente), 'similares' (misma estructura,
        distinta información) o 'equivalentes' (misma estructura e información)."""
        if not Arbol._misma_estructura(self.raiz, otro.raiz):
            return "distintos", "Sus estructuras son diferentes."
        if Arbol._misma_info(self.raiz, otro.raiz):
            return "equivalentes", "Son similares y además sus nodos contienen la misma información."
        return "similares", "Sus estructuras son idénticas, pero la información de los nodos difiere."

    # ---------------- informe completo ----------------
    def informe(self):
        if self.raiz is None:
            return ["El árbol está vacío (raizPtr = NULL).", "Altura: 0 niveles · Peso: 0 nodos"]
        mal = self.nodos_que_violan()
        return [
            f"Raíz: {self.raiz.dato}",
            f"Peso (número de nodos): {self.contar_nodos()}",
            f"Altura (niveles): {self.altura()}",
            f"Orden: {self.ORDEN} (árbol binario)   Grado del árbol: {self.grado_arbol()}",
            f"Hojas: {self.contar_hojas()}   Nodos interiores (ramas): {self.contar_interiores()}",
            f"Menor: {self.busca_menor().dato}   Mayor: {self.busca_mayor().dato}",
            f"¿Árbol binario de búsqueda válido? {_si(not mal)}"
            + ("" if not mal else f"   (violan el orden: {', '.join(str(n.dato) for n in mal)})"),
            f"¿Completo? {_si(self.es_completo())}   ¿Lleno? {_si(self.es_lleno())}   "
            f"¿Degenerado (lista enlazada)? {_si(self.es_degenerado())}",
            f"¿Equilibrado AVL? {_si(self.es_avl())}   "
            f"¿Perfectamente equilibrado? {_si(self.es_perfectamente_equilibrado())}",
            f"PreOrden:  {' – '.join(map(str, self.pre_orden()))}",
            f"InOrden:   {' – '.join(map(str, self.in_orden()))}",
            f"PostOrden: {' – '.join(map(str, self.post_orden()))}",
            f"Amplitud:  {' – '.join(map(str, self.amplitud()))}",
        ]

    # Alias con los nombres de la presentación (estilo C++)
    esVacio = es_vacio
    regresaRaiz = regresa_raiz
    insertarNodo = insertar_nodo
    muestraAcostado = muestra_acostado
    preOrden = pre_orden
    inOrden = in_orden
    postOrden = post_orden
    eliminarPredecesor = eliminar_predecesor
    eliminarSucesor = eliminar_sucesor
    buscaMenor = busca_menor
    buscaMayor = busca_mayor
    contarHojas = contar_hojas
    podarArbol = podar_arbol


# ============================================================
#                  EJEMPLOS DE LA PRESENTACIÓN
# ============================================================
EJEMPLOS = {
    "PDF: 8, 3, 1, 20, 5, 10, 7, 4": [8, 3, 1, 20, 5, 10, 7, 4],
    "PDF: 9, 2, 1, 16, 6, 11, 8, 4": [9, 2, 1, 16, 6, 11, 8, 4],
    "PDF recorridos: 8, 3, 14, 1, 6, 10, 4, 7, 13": [8, 3, 14, 1, 6, 10, 4, 7, 13],
    "PDF actividad: 12, 9, 25, 7, 10, 15, 30, 35": [12, 9, 25, 7, 10, 15, 30, 35],
    "PDF InOrden: 27, 13, 42, 6, 17, 33, 48": [27, 13, 42, 6, 17, 33, 48],
    "PDF AVL / perfecto: 15, 12, 20, 10, 13, 18, 22": [15, 12, 20, 10, 13, 18, 22],
    "Degenerado (lista): 1, 2, 3, 4, 5": [1, 2, 3, 4, 5],
    "Vacío": [],
}


def parsear_lista(texto):
    """'8, 3 1;20' → [8, 3, 1, 20]. Lanza ValueError si hay algo no entero."""
    partes = texto.replace(";", " ").replace(",", " ").split()
    return [int(p) for p in partes]


# ============================================================
#                   DISEÑO DEL DIBUJO (GUI)
# ============================================================
def calcular_layout(raiz):
    """
    Posiciones para dibujar: cada nodo queda centrado sobre sus dos hijos y
    cada hijo vacío ocupa una 'posición libre' (así nada se encima).
    Devuelve (pos, libres):  pos[nodo] = (x, nivel);
    libres = [(padre, 'izq'|'der'|'raiz', x, nivel)]
    """
    pos, libres, cont = {}, [], [0]

    def rec(n, prof, padre, lado):
        if n is None:
            x = cont[0]
            cont[0] += 1
            libres.append((padre, lado, x, prof))
            return x
        xl = rec(n.izquierdo, prof + 1, n, "izq")
        xr = rec(n.derecho, prof + 1, n, "der")
        x = (xl + xr) / 2
        pos[n] = (x, prof)
        return x

    rec(raiz, 0, None, "raiz")
    return pos, libres


# ============================================================
#                      INTERFAZ GRÁFICA
# ============================================================
TEMAS = {
    "claro": dict(
        bg="#f1f4fb", panel="#ffffff", panel2="#eceffa", text="#1f2937", muted="#6b7280",
        accent="#6366f1", accent_dark="#4f46e5", accent_text="#ffffff", border="#dde3f0",
        hdr="#4f46e5", hdr_txt="#ffffff", hdr_sub="#c7d2fe",
        canvas="#fbfcff", band="#f2f5fd", edge="#9aa5bd", ghost="#c3cbe0",
        raiz="#c7d2fe", raiz_b="#4f46e5", interior="#bae6fd", interior_b="#0284c7",
        hoja="#bbf7d0", hoja_b="#16a34a", sombra="#e3e8f4", sel="#f59e0b",
        ok="#16a34a", bad="#dc2626", warn="#d97706", log_bg="#fbfcff",
        r_nuevo="#86efac", r_visitado="#fde68a", r_actual="#fdba74", r_hallado="#6ee7b7",
        r_error="#fca5a5", r_hoja="#fbcfe8"),
    "oscuro": dict(
        bg="#0f172a", panel="#1e293b", panel2="#334155", text="#e5e7eb", muted="#94a3b8",
        accent="#818cf8", accent_dark="#6366f1", accent_text="#0f172a", border="#334155",
        hdr="#312e81", hdr_txt="#ffffff", hdr_sub="#a5b4fc",
        canvas="#111827", band="#151f33", edge="#64748b", ghost="#475569",
        raiz="#3730a3", raiz_b="#a5b4fc", interior="#0c4a6e", interior_b="#38bdf8",
        hoja="#14532d", hoja_b="#4ade80", sombra="#0a0f1c", sel="#fbbf24",
        ok="#4ade80", bad="#f87171", warn="#fbbf24", log_bg="#0b1220",
        r_nuevo="#166534", r_visitado="#854d0e", r_actual="#c2410c", r_hallado="#15803d",
        r_error="#991b1b", r_hoja="#9d174d"),
}


class Tooltip:
    """Globito de ayuda que aparece al pasar el ratón sobre un widget."""

    def __init__(self, widget, texto):
        self.widget, self.texto, self.ventana = widget, texto, None
        widget.bind("<Enter>", self.mostrar, add="+")
        widget.bind("<Leave>", self.ocultar, add="+")

    def mostrar(self, _ev=None):
        if self.ventana is not None:
            return
        self.ventana = tk.Toplevel(self.widget)
        self.ventana.wm_overrideredirect(True)
        x = self.widget.winfo_rootx() + 16
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        self.ventana.wm_geometry(f"+{x}+{y}")
        tk.Label(self.ventana, text=self.texto, bg="#1f2937", fg="#ffffff", padx=9, pady=5,
                 font=("TkDefaultFont", 9), justify="left", wraplength=280).pack()

    def ocultar(self, _ev=None):
        if self.ventana is not None:
            self.ventana.destroy()
            self.ventana = None


class App(tk.Tk if tk else object):
    TIPOS = {"PreOrden": "pre", "InOrden": "in", "PostOrden": "post", "Amplitud": "amplitud"}
    AYUDA = (
        "🌳  Así se usa\n\n"
        "➕  Escribe un número arriba y pulsa «Insertar»: el árbol lo coloca en su lugar.\n\n"
        "👆  Haz clic en un nodo para seleccionarlo; clic derecho abre su menú.\n\n"
        "✨  Los círculos punteados (+) son posiciones libres: haz clic en uno para poner "
        "ahí un nodo, donde tú quieras.\n\n"
        "🗑  Para eliminar, selecciona el nodo o escribe su valor y pulsa «Eliminar».\n\n"
        "🔄  En «Recorridos» verás cómo se recorre el árbol, nodo por nodo.\n\n"
        "🔎  Con el control de zoom haces el dibujo más grande o más pequeño.\n\n"
        "⌨  Atajos: Enter = insertar · Supr = eliminar el nodo seleccionado · Esc = quitar resaltado.")

    def __init__(self):
        super().__init__()
        self.title("🌳 Árboles Binarios de Búsqueda")
        self.geometry("1380x880")
        self.minsize(1120, 720)
        self.fam = self._elegir_fuente(("Segoe UI", "SF Pro Text", "Helvetica Neue", "Ubuntu", "Noto Sans",
                                        "DejaVu Sans", "Helvetica"))
        self.mono = self._elegir_fuente(("Cascadia Mono", "Consolas", "Menlo", "DejaVu Sans Mono", "Courier New"))
        self.tema = "claro"
        self.p = TEMAS[self.tema]
        self.arbol = Arbol()
        self.seleccionado = None
        self.resaltados = {}          # Nodo -> clave de color ('nuevo', 'visitado', ...)
        self._anim, self._tkw, self._toast_id = [], [], None
        self.style = ttk.Style(self)
        self._construir_ui()
        self.aplicar_tema("claro")
        self.bind("<Delete>", self._tecla_supr)
        self.bind("<Escape>", lambda e: self.quitar_resaltado())
        self.cargar_ejemplo(next(iter(EJEMPLOS)))
        self.toast("¡Bienvenido! Pulsa ❓ Ayuda si quieres un recorrido rápido 🌱", "info", 4500)

    # ------------------------------------------------ apariencia
    def _elegir_fuente(self, opciones):
        try:
            disponibles = set(tkfont.families())
            for f in opciones:
                if f in disponibles:
                    return f
        except Exception:
            pass
        return opciones[-1]

    def _reg(self, widget, **opciones):
        """Registra un widget tk (no ttk) para recolorearlo al cambiar de tema."""
        self._tkw.append((widget, opciones))
        return widget

    def aplicar_tema(self, nombre):
        self.tema, self.p = nombre, TEMAS[nombre]
        P, F, s = self.p, self.fam, self.style
        try:
            s.theme_use("clam")
        except Exception:
            pass
        self.configure(bg=P["bg"])
        s.configure(".", background=P["panel"], foreground=P["text"], font=(F, 10),
                    bordercolor=P["border"], lightcolor=P["panel"], darkcolor=P["panel"],
                    troughcolor=P["panel2"], focuscolor=P["panel"], relief="flat")
        s.configure("TFrame", background=P["bg"])
        s.configure("Card.TFrame", background=P["panel"])
        s.configure("TLabel", background=P["panel"], foreground=P["text"])
        s.configure("Sec.TLabel", background=P["panel"], foreground=P["accent"], font=(F, 9, "bold"))
        s.configure("Muted.TLabel", background=P["panel"], foreground=P["muted"], font=(F, 9))
        s.configure("Sel.TLabel", background=P["panel2"], foreground=P["text"], font=(F, 11, "bold"),
                    padding=(10, 8))
        s.configure("TButton", background=P["panel2"], foreground=P["text"], padding=(12, 7),
                    borderwidth=0, font=(F, 10))
        s.map("TButton", background=[("pressed", P["border"]), ("active", P["border"])])
        s.configure("Accent.TButton", background=P["accent"], foreground=P["accent_text"],
                    font=(F, 10, "bold"))
        s.map("Accent.TButton", background=[("pressed", P["accent_dark"]), ("active", P["accent_dark"])])
        s.configure("Danger.TButton", background=P["bad"], foreground="#ffffff", font=(F, 10, "bold"))
        s.map("Danger.TButton", background=[("active", "#b91c1c")])
        s.configure("Head.TButton", background=P["accent"], foreground="#ffffff", padding=(10, 5))
        s.map("Head.TButton", background=[("active", P["accent_dark"])])
        s.configure("TEntry", fieldbackground=P["canvas"], foreground=P["text"], insertcolor=P["text"],
                    bordercolor=P["border"], padding=6)
        s.configure("TCombobox", fieldbackground=P["canvas"], foreground=P["text"], background=P["panel2"],
                    arrowcolor=P["text"], bordercolor=P["border"], padding=5)
        s.map("TCombobox", fieldbackground=[("readonly", P["canvas"])], foreground=[("readonly", P["text"])])
        s.configure("TSpinbox", fieldbackground=P["canvas"], foreground=P["text"], arrowcolor=P["text"],
                    background=P["panel2"], bordercolor=P["border"], padding=4)
        s.configure("TNotebook", background=P["bg"], borderwidth=0, tabmargins=(0, 0, 0, 0))
        s.configure("TNotebook.Tab", background=P["panel2"], foreground=P["muted"], padding=(11, 7),
                    font=(F, 10, "bold"), borderwidth=0)
        s.map("TNotebook.Tab", background=[("selected", P["panel"])], foreground=[("selected", P["accent"])])
        for w in ("TCheckbutton", "TRadiobutton"):
            s.configure(w, background=P["panel"], foreground=P["text"], indicatorcolor=P["canvas"])
            s.map(w, background=[("active", P["panel"])], indicatorcolor=[("selected", P["accent"])])
        s.configure("TSeparator", background=P["border"])
        s.configure("Horizontal.TScale", background=P["panel"], troughcolor=P["panel2"])
        for sb in ("Vertical.TScrollbar", "Horizontal.TScrollbar"):
            s.configure(sb, background=P["panel2"], troughcolor=P["bg"], arrowcolor=P["muted"],
                        bordercolor=P["bg"], relief="flat")
        self.option_add("*TCombobox*Listbox.background", P["panel"])
        self.option_add("*TCombobox*Listbox.foreground", P["text"])
        self.option_add("*TCombobox*Listbox.selectBackground", P["accent"])
        self.option_add("*TCombobox*Listbox.selectForeground", P["accent_text"])

        for w, opciones in self._tkw:
            try:
                w.configure(**{k: P[v] for k, v in opciones.items()})
            except Exception:
                pass
        t = self.txt
        t.tag_configure("titulo", foreground=P["accent"], font=(self.mono, 10, "bold"))
        t.tag_configure("ok", foreground=P["ok"])
        t.tag_configure("aviso", foreground=P["warn"])
        t.tag_configure("normal", foreground=P["text"])
        self.btn_tema.config(text="☀️ Claro" if nombre == "oscuro" else "🌙 Oscuro")
        if hasattr(self, "arbol") and hasattr(self, "var_zoom"):
            self.dibujar()

    def alternar_tema(self):
        self.aplicar_tema("oscuro" if self.tema == "claro" else "claro")

    def toast(self, mensaje, tipo="info", ms=2800):
        """Aviso amable que aparece unos segundos sobre el dibujo (sin ventanas emergentes)."""
        P = self.p
        color = {"info": P["accent"], "ok": P["ok"], "aviso": P["warn"], "error": P["bad"]}[tipo]
        self.lbl_toast.config(text=f"   {mensaje}   ", bg=color,
                              fg="#1f2937" if tipo == "aviso" and self.tema == "claro" else "#ffffff")
        self.lbl_toast.place(relx=0.5, rely=0.97, anchor="s")
        self.lbl_toast.lift()
        if self._toast_id is not None:
            try:
                self.after_cancel(self._toast_id)
            except Exception:
                pass
        self._toast_id = self.after(ms, self.lbl_toast.place_forget)

    def ayuda(self):
        messagebox.showinfo("Ayuda", self.AYUDA)

    # ------------------------------------------------ construcción
    def _boton(self, padre, texto, comando, estilo="TButton", tip=None):
        b = ttk.Button(padre, text=texto, command=comando, style=estilo)
        b.pack(fill="x", pady=3)
        if tip:
            Tooltip(b, tip)
        return b

    def _seccion(self, padre, titulo, primero=False):
        ttk.Label(padre, text=titulo.upper(), style="Sec.TLabel").pack(anchor="w", pady=(0 if primero else 14, 4))

    def _construir_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ----- encabezado
        hdr = self._reg(tk.Frame(self), bg="hdr")
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.columnconfigure(0, weight=1)
        caja = self._reg(tk.Frame(hdr), bg="hdr")
        caja.grid(row=0, column=0, sticky="w", padx=18, pady=10)
        self._reg(tk.Label(caja, text="🌳  Árboles Binarios de Búsqueda", font=(self.fam, 17, "bold")),
                  bg="hdr", fg="hdr_txt").pack(anchor="w")
        self._reg(tk.Label(caja, text="Estructuras de Datos · juega con el árbol: inserta, busca, elimina y recorre",
                           font=(self.fam, 10)), bg="hdr", fg="hdr_sub").pack(anchor="w")
        botones = self._reg(tk.Frame(hdr), bg="hdr")
        botones.grid(row=0, column=1, padx=16)
        self.btn_tema = ttk.Button(botones, text="🌙 Oscuro", style="Head.TButton", command=self.alternar_tema)
        self.btn_tema.pack(side="left", padx=4)
        Tooltip(self.btn_tema, "Cambia entre tema claro y oscuro")
        b = ttk.Button(botones, text="❓ Ayuda", style="Head.TButton", command=self.ayuda)
        b.pack(side="left", padx=4)

        cuerpo = ttk.Frame(self)
        cuerpo.grid(row=1, column=0, sticky="nsew", padx=14, pady=12)
        cuerpo.columnconfigure(0, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        # ----- columna izquierda
        izq = ttk.Frame(cuerpo)
        izq.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        izq.columnconfigure(0, weight=1)
        izq.rowconfigure(1, weight=3)
        izq.rowconfigure(4, weight=2)

        barra = ttk.Frame(izq, style="Card.TFrame", padding=(12, 10))
        barra.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(barra, text="Valor", style="Sec.TLabel").pack(side="left", padx=(0, 8))
        self.var_valor = tk.StringVar()
        self.entrada = ttk.Entry(barra, textvariable=self.var_valor, width=9, justify="center",
                                 font=(self.fam, 13, "bold"))
        self.entrada.pack(side="left", padx=(0, 10))
        self.entrada.bind("<Return>", lambda e: self.insertar())
        for texto, cmd, estilo, tip in (
                ("➕ Insertar", self.insertar, "Accent.TButton", "Lo coloca donde le toca en el árbol de búsqueda [1]"),
                ("🔍 Buscar", self.buscar, "TButton", "Busca el valor y muestra el camino paso a paso [4]"),
                ("🗑 Eliminar", lambda: self.eliminar_valor(self.var_modo.get()), "Danger.TButton",
                 "Elimina el valor escrito [8][9] (reemplazo configurable en la pestaña Editar)")):
            bt = ttk.Button(barra, text=texto, command=cmd, style=estilo)
            bt.pack(side="left", padx=3)
            Tooltip(bt, tip)
        self.var_zoom = tk.DoubleVar(value=1.0)
        ttk.Scale(barra, from_=0.6, to=1.5, variable=self.var_zoom, length=110,
                  command=lambda v: self.dibujar()).pack(side="right", padx=(4, 0))
        ttk.Label(barra, text="🔎 Zoom", style="Muted.TLabel").pack(side="right", padx=(10, 4))

        marco = ttk.Frame(izq, style="Card.TFrame", padding=2)
        marco.grid(row=1, column=0, sticky="nsew")
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        self.canvas = self._reg(tk.Canvas(marco, highlightthickness=0), bg="canvas")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        sx = ttk.Scrollbar(marco, orient="horizontal", command=self.canvas.xview)
        sy = ttk.Scrollbar(marco, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=sx.set, yscrollcommand=sy.set)
        sx.grid(row=1, column=0, sticky="ew")
        sy.grid(row=0, column=1, sticky="ns")
        self.lbl_toast = tk.Label(marco, font=(self.fam, 11, "bold"), pady=7)

        estado = ttk.Frame(izq, style="Card.TFrame", padding=(12, 8))
        estado.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        estado.columnconfigure(0, weight=1)
        self.lbl_stats = self._reg(tk.Label(estado, anchor="w", font=(self.fam, 10, "bold")),
                                   bg="panel", fg="text")
        self.lbl_stats.grid(row=0, column=0, sticky="w")
        self.lbl_badge = tk.Label(estado, font=(self.fam, 10, "bold"), padx=10, pady=3)
        self.lbl_badge.grid(row=0, column=1, sticky="e")
        leyenda = self._reg(tk.Frame(estado), bg="panel")
        leyenda.grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))
        for texto, clave in (("●  Raíz", "raiz_b"), ("●  Interior", "interior_b"), ("●  Hoja", "hoja_b"),
                             ("◎  Seleccionado", "sel"), ("○  Posición libre", "muted")):
            self._reg(tk.Label(leyenda, text=texto, font=(self.fam, 9)), bg="panel", fg=clave).pack(
                side="left", padx=(0, 14))

        self.lbl_seq = self._reg(tk.Label(izq, anchor="w", font=(self.mono, 11, "bold")), bg="bg", fg="warn")
        self.lbl_seq.grid(row=3, column=0, sticky="ew", pady=(6, 2))

        tarjeta = ttk.Frame(izq, style="Card.TFrame", padding=10)
        tarjeta.grid(row=4, column=0, sticky="nsew")
        tarjeta.rowconfigure(1, weight=1)
        tarjeta.columnconfigure(0, weight=1)
        ttk.Label(tarjeta, text="📜  BITÁCORA Y PRUEBAS DE ESCRITORIO", style="Sec.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 6))
        ttk.Button(tarjeta, text="Limpiar", command=self.limpiar_log).grid(row=0, column=1, sticky="e", pady=(0, 6))
        self.txt = self._reg(tk.Text(tarjeta, height=11, font=(self.mono, 10), state="disabled", wrap="none",
                                     relief="flat", padx=10, pady=8), bg="log_bg", fg="text",
                             insertbackground="text")
        self.txt.grid(row=1, column=0, columnspan=2, sticky="nsew")
        ly = ttk.Scrollbar(tarjeta, orient="vertical", command=self.txt.yview)
        lx = ttk.Scrollbar(tarjeta, orient="horizontal", command=self.txt.xview)
        self.txt.configure(yscrollcommand=ly.set, xscrollcommand=lx.set)
        ly.grid(row=1, column=2, sticky="ns")
        lx.grid(row=2, column=0, columnspan=2, sticky="ew")

        # ----- columna derecha
        der = ttk.Frame(cuerpo)
        der.grid(row=0, column=1, sticky="ns")
        nb = ttk.Notebook(der, width=380)
        nb.pack(fill="both", expand=True)
        for nombre, constructor in (("✏️ Editar", self._tab_editar), ("🔄 Recorridos", self._tab_recorridos),
                                    ("📊 Propiedades", self._tab_propiedades), ("🧰 Más", self._tab_mas)):
            f = ttk.Frame(nb, style="Card.TFrame", padding=14)
            nb.add(f, text=nombre)
            constructor(f)
        self.menu_ctx = tk.Menu(self, tearoff=0)

    def _tab_editar(self, f):
        self._seccion(f, "Nodo seleccionado", primero=True)
        self.lbl_sel = ttk.Label(f, text="Haz clic en un nodo del dibujo 👆", style="Sel.TLabel", wraplength=330)
        self.lbl_sel.pack(fill="x")
        self.var_modo = tk.StringVar(value="predecesor")
        ttk.Label(f, text="Si el nodo tiene dos hijos, se reemplaza con:", style="Muted.TLabel").pack(
            anchor="w", pady=(10, 2))
        fr = ttk.Frame(f, style="Card.TFrame")
        fr.pack(anchor="w")
        ttk.Radiobutton(fr, text="Predecesor", variable=self.var_modo, value="predecesor").pack(side="left", padx=(0, 12))
        ttk.Radiobutton(fr, text="Sucesor", variable=self.var_modo, value="sucesor").pack(side="left")
        self._boton(f, "🗑  Eliminar nodo seleccionado", self.eliminar_seleccionado, "Danger.TButton")
        self._boton(f, "ℹ️  Ver información del nodo", self.info_seleccionado,
                    tip="Nivel, grado, padre, hermano, camino desde la raíz…")
        self._seccion(f, "Poner un nodo donde quieras")
        ttk.Label(f, text="Haz clic en un círculo punteado (+) del dibujo, o selecciona un nodo y usa "
                          "estos botones con el valor de arriba.", style="Muted.TLabel", wraplength=330,
                  justify="left").pack(anchor="w", pady=(0, 4))
        self._boton(f, "⬅  Como hijo izquierdo del seleccionado", lambda: self.insertar_hijo("izq"))
        self._boton(f, "➡  Como hijo derecho del seleccionado", lambda: self.insertar_hijo("der"))
        self._seccion(f, "Eliminar por valor (caja de arriba)")
        self._boton(f, "[8]  Reemplazar por el PREDECESOR", lambda: self.eliminar_valor("predecesor"))
        self._boton(f, "[9]  Reemplazar por el SUCESOR", lambda: self.eliminar_valor("sucesor"))
        self._seccion(f, "Opciones")
        self.var_libre = tk.BooleanVar(value=True)
        ttk.Checkbutton(f, text="Permitir posiciones fuera del orden de búsqueda",
                        variable=self.var_libre).pack(anchor="w", pady=2)
        self.var_traza = tk.BooleanVar(value=True)
        ttk.Checkbutton(f, text="Mostrar prueba de escritorio al insertar",
                        variable=self.var_traza).pack(anchor="w", pady=2)
        self.var_libres = tk.BooleanVar(value=True)
        ttk.Checkbutton(f, text="Mostrar posiciones libres (+)", variable=self.var_libres,
                        command=self.dibujar).pack(anchor="w", pady=2)

    def _tab_recorridos(self, f):
        self._seccion(f, "Elige un recorrido", primero=True)
        self.var_rec = tk.StringVar(value="PreOrden")
        ttk.Combobox(f, textvariable=self.var_rec, state="readonly", values=list(self.TIPOS)).pack(fill="x")
        self.var_animar = tk.BooleanVar(value=True)
        ttk.Checkbutton(f, text="Animar nodo por nodo", variable=self.var_animar).pack(anchor="w", pady=(8, 2))
        fr = ttk.Frame(f, style="Card.TFrame")
        fr.pack(fill="x", pady=(0, 6))
        ttk.Label(fr, text="Velocidad (ms entre nodos)", style="Muted.TLabel").pack(side="left")
        self.var_vel = tk.IntVar(value=600)
        ttk.Spinbox(fr, from_=100, to=3000, increment=100, width=6, textvariable=self.var_vel).pack(side="right")
        self._boton(f, "▶  Recorrer", self.recorrer, "Accent.TButton")
        self._boton(f, "🧮  Prueba de escritorio del recorrido", self.traza_recorrido)
        self._seccion(f, "Atajos")
        self._boton(f, "[5]  PreOrden  (raíz, izq., der.)", lambda: self.recorrer_rapido("PreOrden"))
        self._boton(f, "[6]  InOrden  (izq., raíz, der.)", lambda: self.recorrer_rapido("InOrden"))
        self._boton(f, "[7]  PostOrden  (izq., der., raíz)", lambda: self.recorrer_rapido("PostOrden"))
        self._boton(f, "[10]  Por niveles (amplitud)", lambda: self.recorrer_rapido("Amplitud"))
        self._boton(f, "✨  Quitar resaltado", self.quitar_resaltado)

    def _tab_propiedades(self, f):
        self._seccion(f, "Medidas", primero=True)
        self._boton(f, "[11]  Altura del árbol", self.m_altura)
        self._boton(f, "[12]  Cantidad de hojas", self.m_hojas)
        self._boton(f, "[13]  Cantidad de nodos (peso)", self.m_nodos)
        self._boton(f, "Menor y mayor (buscaMenor / buscaMayor)", self.m_minmax)
        self._seccion(f, "¿Qué tipo de árbol es?")
        self._boton(f, "[14]  ¿Equilibrado? (AVL / perfecto)", self.m_equilibrado)
        self._boton(f, "[15]  ¿Es completo?", self.m_completo)
        self._boton(f, "[16]  ¿Es lleno?", self.m_lleno)
        self._boton(f, "¿Es degenerado? (lista enlazada)", self.m_degenerado)
        self._boton(f, "¿Es de búsqueda válido?", self.m_bst)
        self._seccion(f, "Resumen")
        self._boton(f, "esVacio() / regresaRaiz()", self.m_vacio)
        self._boton(f, "📋  Informe completo del árbol", self.m_informe, "Accent.TButton")

    def _tab_mas(self, f):
        self._seccion(f, "Ejemplos de la presentación", primero=True)
        self.var_ej = tk.StringVar(value=next(iter(EJEMPLOS)))
        ttk.Combobox(f, textvariable=self.var_ej, state="readonly", values=list(EJEMPLOS)).pack(fill="x")
        self._boton(f, "📂  Cargar ejemplo", lambda: self.cargar_ejemplo(self.var_ej.get()), "Accent.TButton")
        self._seccion(f, "Construir con tu propia lista")
        self.var_lista = tk.StringVar(value="8, 3, 1, 20, 5, 10, 7, 4")
        ttk.Entry(f, textvariable=self.var_lista).pack(fill="x")
        self._boton(f, "🌱  Construir árbol nuevo", self.construir_lista)
        self._boton(f, "➕  Agregar la lista al árbol actual", lambda: self.construir_lista(reemplazar=False))
        self._seccion(f, "Ver el árbol en texto")
        self._boton(f, "[2]  Árbol acostado", self.m_acostado)
        self._boton(f, "[3]  Árbol graficado en texto", self.m_graficar)
        self._boton(f, "🧮  Prueba de escritorio: altura", lambda: self.log("Altura", self.arbol.traza_altura()))
        self._boton(f, "🧮  Prueba de escritorio: contarHojas", lambda: self.log("Hojas", self.arbol.traza_hojas()))
        self._seccion(f, "Comparar con otro árbol B")
        self.var_listab = tk.StringVar(value="8, 3, 1, 20, 5, 10, 7, 4")
        ttk.Entry(f, textvariable=self.var_listab).pack(fill="x")
        self._boton(f, "⚖️  ¿Distintos, similares o equivalentes?", self.comparar)
        self._seccion(f, "Empezar de cero")
        self._boton(f, "[17]  Eliminar el árbol completo", self.m_podar, "Danger.TButton")

    # ------------------------------------------------ utilidades
    def log(self, titulo, lineas=None):
        t = self.txt
        t.configure(state="normal")
        t.insert("end", f"▶ {titulo}\n", "titulo")
        if isinstance(lineas, str):
            lineas = lineas.split("\n")
        for ln in (lineas or []):
            etiqueta = "aviso" if ln.lstrip().startswith("⚠") else ("ok" if "✔" in ln else "normal")
            t.insert("end", f"{ln}\n", etiqueta)
        t.insert("end", "\n", "normal")
        t.see("end")
        t.configure(state="disabled")

    def limpiar_log(self):
        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.configure(state="disabled")

    def _valor(self):
        try:
            return int(self.var_valor.get().strip())
        except ValueError:
            self.toast("Escribe un número entero en la caja «Valor» (por ejemplo 15) 🔢", "error")
            self.entrada.focus_set()
            return None

    def pedir_entero(self, titulo, mensaje):
        """Diálogo amable para pedir un número entero. Devuelve int o None."""
        P = self.p
        top = tk.Toplevel(self)
        top.title(titulo)
        top.configure(bg=P["panel"])
        top.transient(self)
        top.resizable(False, False)
        resultado = [None]
        tk.Label(top, text=mensaje, bg=P["panel"], fg=P["text"], font=(self.fam, 11),
                 wraplength=300, justify="center").pack(padx=26, pady=(20, 8))
        var = tk.StringVar()
        e = ttk.Entry(top, textvariable=var, justify="center", width=10, font=(self.fam, 14, "bold"))
        e.pack(pady=4)
        aviso = tk.Label(top, text="", bg=P["panel"], fg=P["bad"], font=(self.fam, 9))
        aviso.pack()

        def aceptar(_ev=None):
            try:
                resultado[0] = int(var.get().strip())
                top.destroy()
            except ValueError:
                aviso.config(text="Escribe un número entero 🔢")
        fila = tk.Frame(top, bg=P["panel"])
        fila.pack(pady=(6, 18))
        ttk.Button(fila, text="Cancelar", command=top.destroy).pack(side="left", padx=6)
        ttk.Button(fila, text="Aceptar", style="Accent.TButton", command=aceptar).pack(side="left", padx=6)
        top.bind("<Return>", aceptar)
        top.bind("<Escape>", lambda ev: top.destroy())
        top.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - top.winfo_width()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - top.winfo_height()) // 3
        top.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        e.focus_set()
        top.grab_set()
        self.wait_window(top)
        return resultado[0]

    def _tecla_supr(self, _ev=None):
        if "entry" in str(self.focus_get()).lower() or "spinbox" in str(self.focus_get()).lower():
            return
        if self.seleccionado is not None:
            self.eliminar_seleccionado()

    def cancelar_animacion(self):
        for i in self._anim:
            try:
                self.after_cancel(i)
            except Exception:
                pass
        self._anim = []

    def quitar_resaltado(self):
        self.cancelar_animacion()
        self.resaltados = {}
        self.lbl_seq.config(text="")
        self.dibujar()

    # ------------------------------------------------ dibujo
    def _rol(self, n):
        if n is self.arbol.raiz:
            return "raiz"
        return "hoja" if n.es_hoja() else "interior"

    def dibujar(self):
        P, c = self.p, self.canvas
        c.delete("all")
        z = float(self.var_zoom.get())
        DX, DY, R, M = int(62 * z), int(82 * z), int(23 * z), 92
        fuente_nodo = (self.fam, max(8, int(12 * z)), "bold")
        pos, libres = calcular_layout(self.arbol.raiz)
        mostrar = self.var_libres.get()

        def X(u):
            return M + u * DX + DX / 2

        def Y(d):
            return 56 + d * DY

        pos_libre = {(p, l): (x, d) for p, l, x, d in libres}
        niveles = max([d for _, d in pos.values()] + [d for *_, d in libres] + [0])
        ancho = M + (len(pos) + 1) * DX + 60
        c.configure(scrollregion=(0, 0, max(ancho, 640), Y(niveles) + DY))
        W = max(ancho, 640, c.winfo_width() or 0)

        if pos:                                    # franjas por nivel
            for d in range(max(dd for _, dd in pos.values()) + 1):
                if d % 2 == 0:
                    c.create_rectangle(0, Y(d) - DY / 2, W, Y(d) + DY / 2, fill=P["band"], outline="")
                c.create_text(14, Y(d), text=f"Nivel {d + 1}", anchor="w", fill=P["muted"],
                              font=(self.fam, 9))

        for n, (x, d) in pos.items():              # aristas
            for lado, hijo in (("izq", n.izquierdo), ("der", n.derecho)):
                if hijo is not None:
                    hx, hd = pos[hijo]
                    activa = n in self.resaltados and hijo in self.resaltados
                    c.create_line(X(x), Y(d), X(hx), Y(hd), width=3 if activa else 2, capstyle="round",
                                  fill=P["accent"] if activa else P["edge"])
                elif mostrar:
                    lx, ld = pos_libre[(n, lado)]
                    c.create_line(X(x), Y(d), X(lx), Y(ld), dash=(2, 4), fill=P["ghost"])

        if mostrar:                                # posiciones libres (clicables)
            for k, (padre, lado, x, d) in enumerate(libres):
                tag = f"libre{k}"
                r = int((10 if padre is not None else 17) * z)
                c.create_oval(X(x) - r, Y(d) - r, X(x) + r, Y(d) + r, outline=P["ghost"], dash=(3, 3),
                              width=2, fill=P["canvas"], tags=(tag,))
                c.create_text(X(x), Y(d), text="+", fill=P["muted"], font=(self.fam, max(9, int(12 * z)), "bold"),
                              tags=(tag,))
                c.tag_bind(tag, "<Button-1>", lambda e, p=padre, l=lado: self.click_libre(p, l))
                c.tag_bind(tag, "<Enter>", lambda e: c.configure(cursor="hand2"))
                c.tag_bind(tag, "<Leave>", lambda e: c.configure(cursor=""))

        for n, (x, d) in pos.items():              # nodos
            tag = f"nodo{id(n)}"
            rol = self._rol(n)
            clave = self.resaltados.get(n)
            relleno = P["r_" + clave] if clave else P[rol]
            borde = P[rol + "_b"]
            cx, cy = X(x), Y(d)
            c.create_oval(cx - R + 2, cy - R + 4, cx + R + 2, cy + R + 4, fill=P["sombra"], outline="",
                          tags=(tag,))
            if n is self.seleccionado:
                c.create_oval(cx - R - 6, cy - R - 6, cx + R + 6, cy + R + 6, outline=P["sel"], width=3,
                              tags=(tag,))
            c.create_oval(cx - R, cy - R, cx + R, cy + R, fill=relleno, outline=borde, width=3, tags=(tag,))
            c.create_text(cx, cy, text=str(n.dato), font=fuente_nodo, fill=P["text"], tags=(tag,))
            c.tag_bind(tag, "<Button-1>", lambda e, n=n: self.click_nodo(n))
            for boton in ("<Button-3>", "<Button-2>"):
                c.tag_bind(tag, boton, lambda e, n=n: self.menu_nodo(e, n))
            c.tag_bind(tag, "<Enter>", lambda e: c.configure(cursor="hand2"))
            c.tag_bind(tag, "<Leave>", lambda e: c.configure(cursor=""))

        if self.arbol.es_vacio():                  # mensaje de bienvenida
            c.create_text(max(W / 2, 330), 190, justify="center", fill=P["muted"], font=(self.fam, 13),
                          width=420,
                          text="Tu árbol está vacío ✨\n\nHaz clic en el círculo + para poner la raíz,\n"
                               "o escribe un número arriba y pulsa «Insertar».")

        a = self.arbol
        malos = a.nodos_que_violan()
        self.lbl_stats.config(text=f"🌿 {a.contar_nodos()} nodos     📏 Altura {a.altura()}     "
                                   f"🍃 {a.contar_hojas()} hojas")
        if a.es_vacio():
            self.lbl_badge.config(text="  Árbol vacío  ", bg=P["panel2"], fg=P["muted"])
        elif not malos:
            self.lbl_badge.config(text="  ✔ Árbol de búsqueda válido  ", bg=P["ok"], fg="#ffffff")
        else:
            self.lbl_badge.config(text="  ⚠ No es de búsqueda: " + ", ".join(str(m.dato) for m in malos) + "  ",
                                  bg=P["bad"], fg="#ffffff")
        self.actualizar_seleccion()

    def actualizar_seleccion(self):
        n = self.seleccionado
        cam = self.arbol._camino_donde(lambda x: x is n) if n is not None else []
        if not cam:
            self.seleccionado = None
            self.lbl_sel.config(text="Haz clic en un nodo del dibujo 👆")
            return
        tipo = {"raiz": "Raíz", "hoja": "Hoja", "interior": "Interior"}[self._rol(n)]
        self.lbl_sel.config(text=f"Nodo {n.dato}   ·   {tipo}   ·   nivel {len(cam)}")

    # ------------------------------------------------ interacción con el dibujo
    def click_nodo(self, nodo):
        self.seleccionado = nodo
        self.dibujar()

    def menu_nodo(self, ev, nodo):
        self.seleccionado = nodo
        self.dibujar()
        m = self.menu_ctx
        m.delete(0, "end")
        m.add_command(label=f"Nodo {nodo.dato}", state="disabled")
        m.add_separator()
        m.add_command(label="⬅  Insertar hijo izquierdo…", command=lambda: self.click_libre(nodo, "izq"))
        m.add_command(label="➡  Insertar hijo derecho…", command=lambda: self.click_libre(nodo, "der"))
        m.add_separator()
        m.add_command(label="🗑  Eliminar (predecesor)", command=lambda: self._eliminar_ref(nodo, "predecesor"))
        m.add_command(label="🗑  Eliminar (sucesor)", command=lambda: self._eliminar_ref(nodo, "sucesor"))
        m.add_separator()
        m.add_command(label="ℹ️  Información del nodo", command=self.info_seleccionado)
        m.add_command(label="🌿  Ver subárbol (texto)", command=lambda: self._ver_subarbol(nodo))
        m.tk_popup(ev.x_root, ev.y_root)

    def click_libre(self, padre, lado):
        if padre is not None:
            ocupado = padre.izquierdo if lado == "izq" else padre.derecho
            if ocupado is not None:
                self.toast("Ese lugar ya está ocupado 🙂", "aviso")
                return
            donde = f"hijo {'izquierdo' if lado == 'izq' else 'derecho'} del {padre.dato}"
        else:
            donde = "raíz del árbol"
        v = self.pedir_entero("Nuevo nodo", f"¿Qué número quieres poner como {donde}?")
        if v is None:
            return
        self._colocar(padre, lado, v)

    def _colocar(self, padre, lado, v):
        ok, msg = self.arbol.insertar_en(padre, lado, v, exigir_bst=not self.var_libre.get())
        self.log("Insertar en la posición elegida", [msg])
        if not ok:
            self.toast(msg, "aviso", 4200)
        else:
            self.resaltados = {self.arbol.buscar_nodo(v): "nuevo"}
            if self.arbol.es_bst():
                self.toast(f"¡Listo! El {v} quedó donde lo pusiste 🌱", "ok")
            else:
                self.toast(f"Colocado, pero el árbol ya no es de búsqueda ⚠ (mira la barra de estado)", "aviso", 4200)
            self.var_valor.set("")
        self.dibujar()

    def _ver_subarbol(self, nodo):
        sub = self.arbol.subarbol(nodo.dato)
        if sub is None:
            return
        self.log(f"Subárbol con raíz {nodo.dato}",
                 sub.graficar_texto().split("\n") + [""] + sub.informe()[:5])

    # ------------------------------------------------ edición
    def insertar(self):
        v = self._valor()
        if v is None:
            return
        traza = []
        ok = self.arbol.insertar_nodo(v, traza)
        if ok:
            self.log(f"[1] Insertar {v}", traza if self.var_traza.get() else [f"✔ {v} insertado."])
            self.resaltados = {self.arbol.buscar_nodo(v): "nuevo"}
            self.toast(f"¡Listo! El {v} se agregó al árbol 🌱", "ok")
        else:
            self.resaltados = {self.arbol.buscar_nodo(v): "hallado"}
            self.toast(f"El {v} ya está en el árbol 🙂 (no se repiten valores)", "aviso")
        self.dibujar()
        self.var_valor.set("")
        self.entrada.focus_set()

    def insertar_hijo(self, lado):
        if self.seleccionado is None:
            self.toast("Primero haz clic en el nodo que será el padre 👆", "aviso")
            return
        v = self._valor()
        if v is None:
            return
        self._colocar(self.seleccionado, lado, v)

    def buscar(self):
        v = self._valor()
        if v is None:
            return
        traza = []
        hallado = self.arbol.busqueda(v, traza)
        ruta = self.arbol.ruta_busqueda(v)
        self.resaltados = {n: "visitado" for n in ruta}
        if hallado:
            self.resaltados[ruta[-1]] = "hallado"
            self.toast(f"¡Lo encontré! El {v} está en el árbol 🎯", "ok")
        elif self.arbol.existe(v):
            self.resaltados[self.arbol.buscar_nodo(v)] = "error"
            traza.append(f"⚠ El árbol NO está ordenado: la búsqueda binaria no lo encontró, pero el "
                         f"{v} sí está (búsqueda completa).")
            self.toast(f"El {v} está, pero el árbol no está ordenado ⚠", "aviso", 4200)
        else:
            self.toast(f"No encontré el {v} en el árbol 🔍", "aviso")
        self.log(f"[4] Buscar {v}  →  {'ENCONTRADO' if hallado else 'NO encontrado'}", traza)
        self.dibujar()

    def eliminar_valor(self, modo):
        v = self._valor()
        if v is None:
            return
        traza = []
        ok = self.arbol.eliminar_predecesor(v, traza) if modo == "predecesor" else self.arbol.eliminar_sucesor(v, traza)
        self.log(f"[{8 if modo == 'predecesor' else 9}] Eliminar {v} ({modo})", traza)
        if ok:
            self.toast(f"Eliminé el {v} 🗑", "ok")
        else:
            self.toast(f"El {v} no está en el árbol, no hay nada que eliminar 🔍", "aviso")
        self.resaltados = {}
        self.dibujar()
        self.var_valor.set("")

    def eliminar_seleccionado(self):
        if self.seleccionado is None:
            self.toast("Primero haz clic en el nodo que quieres eliminar 👆", "aviso")
            return
        self._eliminar_ref(self.seleccionado, self.var_modo.get())

    def _eliminar_ref(self, nodo, modo):
        traza = []
        valor = nodo.dato
        self.arbol.eliminar_nodo(nodo, modo, traza)
        self.log(f"Eliminar nodo seleccionado {valor} ({modo})", traza)
        self.toast(f"Eliminé el nodo {valor} 🗑", "ok")
        self.seleccionado = None
        self.resaltados = {}
        self.dibujar()

    def info_seleccionado(self):
        if self.seleccionado is None:
            self.toast("Haz clic en un nodo para ver su información 👆", "aviso")
            return
        self.log("Información del nodo", self.arbol.informacion_nodo(self.seleccionado))

    # ------------------------------------------------ recorridos
    def recorrer(self):
        nombre = self.var_rec.get()
        nodos = self.arbol.recorrido_nodos(self.TIPOS[nombre])
        if not nodos:
            self.toast("El árbol está vacío: agrega algunos nodos primero 🌱", "aviso")
            return
        self.log(f"Recorrido {nombre}", [" – ".join(str(n.dato) for n in nodos)])
        self.cancelar_animacion()
        self.resaltados = {}
        if not self.var_animar.get():
            self.resaltados = {n: "visitado" for n in nodos}
            self.lbl_seq.config(text=f"{nombre}:  " + " – ".join(str(n.dato) for n in nodos))
            self.dibujar()
            return
        seq = []

        def paso(i):
            if i > 0:
                self.resaltados[nodos[i - 1]] = "visitado"
            if i < len(nodos):
                self.resaltados[nodos[i]] = "actual"
                seq.append(nodos[i].dato)
                self.lbl_seq.config(text=f"{nombre}:  " + " – ".join(map(str, seq)))
                self.dibujar()
                self._anim.append(self.after(max(50, int(self.var_vel.get())), lambda: paso(i + 1)))
            else:
                self.dibujar()
        paso(0)

    def recorrer_rapido(self, nombre):
        self.var_rec.set(nombre)
        self.recorrer()

    def traza_recorrido(self):
        self.log(f"Prueba de escritorio {self.var_rec.get()}",
                 self.arbol.traza_recorrido(self.TIPOS[self.var_rec.get()]))

    # ------------------------------------------------ propiedades
    def m_altura(self):
        self.log("[11] Altura del árbol", self.arbol.traza_altura())
        self.toast(f"La altura es {self.arbol.altura()} 📏", "info")

    def m_hojas(self):
        a = self.arbol
        self.resaltados = {n: "hoja" for n in a.recorrido_nodos("pre") if n.es_hoja()}
        self.log("[12] Cantidad de hojas", a.traza_hojas())
        self.toast(f"Hay {a.contar_hojas()} hojas 🍃 (resaltadas en rosa)", "info")
        self.dibujar()

    def m_nodos(self):
        n = self.arbol.contar_nodos()
        self.log("[13] Cantidad de nodos (peso)", [f"El árbol tiene {n} nodo(s)."])
        self.toast(f"El árbol tiene {n} nodo(s) 🌿", "info")

    def m_equilibrado(self):
        a = self.arbol
        self.log("[14] Equilibrio", [
            f"¿Equilibrado AVL (diferencia de alturas ≤ 1 en todo nodo)? {_si(a.es_avl())}",
            f"¿Perfectamente equilibrado (diferencia de nº de nodos ≤ 1 en todo nodo)? "
            f"{_si(a.es_perfectamente_equilibrado())}"])
        self.toast(f"AVL: {_si(a.es_avl())}  ·  Perfecto: {_si(a.es_perfectamente_equilibrado())} ⚖️", "info")

    def m_completo(self):
        r = self.arbol.es_completo()
        self.log("[15] ¿Es completo?", [f"Árbol binario completo: {_si(r)}"])
        self.toast(f"¿Completo? {_si(r)}", "ok" if r else "info")

    def m_lleno(self):
        r = self.arbol.es_lleno()
        self.log("[16] ¿Es lleno?", [f"Árbol binario lleno (todo nodo con 0 o 2 hijos): {_si(r)}"])
        self.toast(f"¿Lleno? {_si(r)}", "ok" if r else "info")

    def m_degenerado(self):
        r = self.arbol.es_degenerado()
        self.log("¿Es degenerado?", [f"Árbol degenerado (equivale a una lista enlazada): {_si(r)}"])
        self.toast(f"¿Degenerado? {_si(r)}", "info")

    def m_bst(self):
        malos = self.arbol.nodos_que_violan()
        self.resaltados = {n: "error" for n in malos}
        self.log("¿Árbol binario de búsqueda?",
                 [_si(not malos) + ("" if not malos else
                  f" - nodos que rompen el orden: {', '.join(str(n.dato) for n in malos)}")])
        self.toast("¡Es un árbol de búsqueda válido! ✔" if not malos else
                   "No es de búsqueda: los nodos en rojo rompen el orden ⚠", "ok" if not malos else "aviso")
        self.dibujar()

    def m_minmax(self):
        a = self.arbol
        if a.es_vacio():
            self.toast("El árbol está vacío 🌱", "aviso")
            return
        mn, mx = a.busca_menor(), a.busca_mayor()
        self.resaltados = {mn: "hallado", mx: "error"}
        self.log("buscaMenor / buscaMayor", [f"Menor (nodo más a la izquierda): {mn.dato}",
                                             f"Mayor (nodo más a la derecha): {mx.dato}"])
        self.toast(f"Menor: {mn.dato} (verde)  ·  Mayor: {mx.dato} (rojo)", "info")
        self.dibujar()

    def m_vacio(self):
        a = self.arbol
        self.log("esVacio() / regresaRaiz()", [f"esVacio() = {a.es_vacio()}", f"regresaRaiz() = {a.regresa_raiz()}"])

    def m_informe(self):
        self.log("Informe completo del árbol", self.arbol.informe())

    def m_acostado(self):
        self.log("[2] Árbol acostado (raíz a la izquierda)", self.arbol.muestra_acostado())

    def m_graficar(self):
        self.log("[3] Árbol graficado en texto", self.arbol.graficar_texto())

    def m_podar(self):
        if self.arbol.es_vacio():
            self.toast("El árbol ya está vacío 🌱", "aviso")
            return
        if not messagebox.askyesno("Eliminar el árbol", "¿Seguro que quieres eliminar todos los nodos del árbol?"):
            return
        traza = []
        self.arbol.podar_arbol(traza)
        self.log("[17] Eliminar el árbol (podarArbol)", traza + ["raizPtr = NULL"])
        self.toast("Árbol eliminado. ¡A empezar de nuevo! 🌱", "ok")
        self.seleccionado = None
        self.resaltados = {}
        self.dibujar()

    # ------------------------------------------------ carga y comparación
    def cargar_ejemplo(self, nombre):
        valores = EJEMPLOS[nombre]
        self.arbol = Arbol(valores)
        self.seleccionado = None
        self.resaltados = {}
        self.cancelar_animacion()
        self.lbl_seq.config(text="")
        self.log(f"Ejemplo cargado: {nombre}", [f"Orden de inserción: {valores}"] if valores else ["Árbol vacío"])
        self.dibujar()

    def construir_lista(self, reemplazar=True):
        try:
            valores = parsear_lista(self.var_lista.get())
        except ValueError:
            self.toast("Escribe enteros separados por comas o espacios, por ejemplo: 8, 3, 10 🔢", "error", 4000)
            return
        if reemplazar:
            self.arbol = Arbol()
        repetidos = [v for v in valores if not self.arbol.insertar_nodo(v)]
        self.seleccionado = None
        self.resaltados = {}
        self.log("Árbol construido", [f"Valores: {valores}"] +
                 ([f"⚠ Repetidos ignorados: {repetidos}"] if repetidos else []))
        self.toast("¡Árbol listo! 🌳" + (f" (se ignoraron {len(repetidos)} repetidos)" if repetidos else ""), "ok")
        self.dibujar()

    def comparar(self):
        try:
            valores = parsear_lista(self.var_listab.get())
        except ValueError:
            self.toast("Escribe enteros separados por comas o espacios 🔢", "error", 4000)
            return
        b = Arbol(valores)
        veredicto, razon = self.arbol.comparar(b)
        self.log(f"Comparación con el árbol B {valores}",
                 [f"Árbol A y árbol B son {veredicto.upper()}: {razon}", "", "Árbol A:"]
                 + self.arbol.graficar_texto().split("\n") + ["", "Árbol B:"] + b.graficar_texto().split("\n"))
        self.toast(f"Los árboles son {veredicto} ⚖️", "info")


# ============================================================
#              MENÚ DE CONSOLA (igual al de la presentación)
# ============================================================
def menu_consola():
    a = Arbol()
    menu = """
 ===== ÁRBOL BINARIO DE BÚSQUEDA =====
 [1] Insertar elemento
 [2] Mostrar árbol completo acostado con la raíz a la izquierda
 [3] Graficar árbol completo
 [4] Buscar un elemento en el árbol
 [5] Recorrer el árbol en PreOrden
 [6] Recorrer el árbol en InOrden
 [7] Recorrer el árbol en PostOrden
 [8] Eliminar un nodo del árbol PREDECESOR
 [9] Eliminar un nodo del árbol SUCESOR
 [10] Recorrer el árbol por niveles (Amplitud)
 [11] Altura del árbol
 [12] Cantidad de hojas del árbol
 [13] Cantidad de nodos del árbol
 [14] Revisa si está equilibrado (AVL / perfecto)
 [15] Revisa si es un árbol binario completo
 [16] Revisa si es un árbol binario lleno
 [17] Eliminar el árbol
 [18] Informe completo           [19] Cargar ejemplo
 [20] Insertar en una posición elegida (padre y lado)
 [21] Información de un nodo     [22] Menor y mayor
 [0] Salir"""

    def entero(msg):
        try:
            return int(input(msg))
        except ValueError:
            print("Dato inválido: escribe un entero.")
            return None

    while True:
        print(menu)
        op = input("Opción: ").strip()
        if op == "0":
            break
        elif op == "1":
            v = entero("Valor: ")
            if v is not None:
                t = []
                a.insertar_nodo(v, t)
                print("\n".join(t))
        elif op == "2":
            print(a.muestra_acostado())
        elif op == "3":
            print(a.graficar_texto())
        elif op == "4":
            v = entero("Valor a buscar: ")
            if v is not None:
                t = []
                r = a.busqueda(v, t)
                print("\n".join(t))
                print("ENCONTRADO" if r else "NO encontrado")
        elif op in ("5", "6", "7", "10"):
            tipo = {"5": "pre", "6": "in", "7": "post", "10": "amplitud"}[op]
            print(" – ".join(str(n.dato) for n in a.recorrido_nodos(tipo)) or "(árbol vacío)")
        elif op in ("8", "9"):
            v = entero("Valor a eliminar: ")
            if v is not None:
                t = []
                (a.eliminar_predecesor if op == "8" else a.eliminar_sucesor)(v, t)
                print("\n".join(t))
        elif op == "11":
            print("Altura:", a.altura())
        elif op == "12":
            print("Hojas:", a.contar_hojas())
        elif op == "13":
            print("Nodos:", a.contar_nodos())
        elif op == "14":
            print(f"AVL: {_si(a.es_avl())}   Perfectamente equilibrado: {_si(a.es_perfectamente_equilibrado())}")
        elif op == "15":
            print("Completo:", _si(a.es_completo()))
        elif op == "16":
            print("Lleno:", _si(a.es_lleno()))
        elif op == "17":
            t = []
            a.podar_arbol(t)
            print("\n".join(t) or "El árbol ya estaba vacío.")
        elif op == "18":
            print("\n".join(a.informe()))
        elif op == "19":
            for i, k in enumerate(EJEMPLOS, 1):
                print(f" {i}. {k}")
            i = entero("Número de ejemplo: ")
            if i is not None and 1 <= i <= len(EJEMPLOS):
                a = Arbol(list(EJEMPLOS.values())[i - 1])
                print(a.graficar_texto())
        elif op == "20":
            if a.es_vacio():
                v = entero("Valor de la raíz: ")
                if v is not None:
                    print(a.insertar_en(None, "raiz", v)[1])
            else:
                p, v = entero("Valor del nodo padre: "), entero("Valor nuevo: ")
                lado = input("Lado (izq/der): ").strip().lower()
                nodo = a.buscar_nodo(p) if p is not None else None
                if nodo is None or v is None or lado not in ("izq", "der"):
                    print("Datos inválidos o padre inexistente.")
                else:
                    print(a.insertar_en(nodo, lado, v)[1])
                    if not a.es_bst():
                        print("⚠ El árbol dejó de ser de búsqueda.")
        elif op == "21":
            v = entero("Valor del nodo: ")
            n = a.buscar_nodo(v) if v is not None else None
            print("\n".join(a.informacion_nodo(n)) if n else "Ese valor no está en el árbol.")
        elif op == "22":
            if a.es_vacio():
                print("El árbol está vacío.")
            else:
                print(f"Menor: {a.busca_menor().dato}   Mayor: {a.busca_mayor().dato}")
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    if "--consola" in sys.argv or tk is None:
        if tk is None and "--consola" not in sys.argv:
            print("tkinter no está disponible: se usa el menú de consola.")
        menu_consola()
    else:
        App().mainloop()
