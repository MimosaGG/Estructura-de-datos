import random
import sys
import time

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import font as tkfont
except ImportError:
    tk = ttk = tkfont = None

LIMITE_PASO_A_PASO = 30
MAX_BARRAS = 60
LIMITE_DATOS = 100000


def nuevas_stats():
    return {"comparaciones": 0, "movimientos": 0}


def shell_sort(datos, trazar=None):
    a, st = list(datos), nuevas_stats()
    n = len(a)
    salto = n // 2
    while salto > 0:
        for i in range(salto, n):
            temp, j = a[i], i
            while j >= salto:
                st["comparaciones"] += 1
                if a[j - salto] > temp:
                    a[j] = a[j - salto]
                    st["movimientos"] += 1
                    j -= salto
                else:
                    break
            a[j] = temp
        if trazar:
            trazar(f"Salto = {salto}: se ordenan por inserción los elementos que están a "
                   f"{salto} {'posición' if salto == 1 else 'posiciones'} de distancia  →  {a}",
                   a[:], None)
        salto //= 2
    return a, st


def quick_sort(datos, trazar=None):
    a, st = list(datos), nuevas_stats()

    def ordenar(lo, hi):
        while lo < hi:
            pivote = a[(lo + hi) // 2]
            lt, i, gt = lo, lo, hi
            while i <= gt:
                st["comparaciones"] += 1
                if a[i] < pivote:
                    a[lt], a[i] = a[i], a[lt]
                    st["movimientos"] += 1
                    lt += 1
                    i += 1
                elif a[i] > pivote:
                    a[i], a[gt] = a[gt], a[i]
                    st["movimientos"] += 1
                    gt -= 1
                else:
                    i += 1
            if trazar:
                trazar(f"Pivote = {pivote}:  menores {a[lo:lt]} | iguales {a[lt:gt + 1]} | "
                       f"mayores {a[gt + 1:hi + 1]}  →  lista: {a}", a[:], (lt, gt))
            if lt - lo < hi - gt:
                ordenar(lo, lt - 1)
                lo = gt + 1
            else:
                ordenar(gt + 1, hi)
                hi = lt - 1

    ordenar(0, len(a) - 1)
    return a, st


def heap_sort(datos, trazar=None):
    a, st = list(datos), nuevas_stats()
    n = len(a)

    def hundir(i, tam):
        while True:
            izq, der, mayor = 2 * i + 1, 2 * i + 2, i
            if izq < tam:
                st["comparaciones"] += 1
                if a[izq] > a[mayor]:
                    mayor = izq
            if der < tam:
                st["comparaciones"] += 1
                if a[der] > a[mayor]:
                    mayor = der
            if mayor == i:
                return
            a[i], a[mayor] = a[mayor], a[i]
            st["movimientos"] += 1
            i = mayor

    for i in range(n // 2 - 1, -1, -1):
        hundir(i, n)
    if trazar:
        trazar(f"Montículo máximo construido (el mayor, {a[0] if a else '-'}, queda en la raíz)  →  {a}",
               a[:], (0, 0) if a else None)
    for fin in range(n - 1, 0, -1):
        a[0], a[fin] = a[fin], a[0]
        st["movimientos"] += 1
        hundir(0, fin)
        if trazar:
            trazar(f"Se coloca {a[fin]} en su lugar definitivo:  montículo {a[:fin]} | ordenado {a[fin:]}",
                   a[:], (fin, n - 1))
    return a, st


def radix_sort(datos, trazar=None):
    st = nuevas_stats()
    negativos = [-x for x in datos if x < 0]
    positivos = [x for x in datos if x >= 0]

    def lsd(valores, etiqueta, estado):
        if not valores:
            return []
        maximo, exp, nombres = max(valores), 1, ["unidades", "decenas", "centenas", "millares"]
        paso = 0
        while maximo // exp > 0:
            cubetas = [[] for _ in range(10)]
            for v in valores:
                cubetas[(v // exp) % 10].append(v)
                st["movimientos"] += 1
            valores = [v for c in cubetas for v in c]
            if trazar:
                nombre = nombres[paso] if paso < len(nombres) else f"10^{paso}"
                usadas = "  ".join(f"[{d}]:{c}" for d, c in enumerate(cubetas) if c)
                trazar(f"{etiqueta}Dígito de las {nombre}:  {usadas}  →  {valores}", estado(valores), None)
            exp *= 10
            paso += 1
        return valores

    if negativos and trazar:
        trazar("Se separan los negativos (se ordenarán por valor absoluto) de los no negativos  →  "
               f"{[-x for x in negativos]} | {positivos}", [-x for x in negativos] + positivos, None)
    neg_abs = lsd(negativos, "(negativos, en valor absoluto) ", lambda v: [-x for x in v] + positivos)
    neg_ord = [-x for x in reversed(neg_abs)]
    if negativos and trazar:
        trazar(f"Los negativos quedaron ordenados por valor absoluto; se invierte su orden  →  {neg_ord}",
               neg_ord + positivos, (0, len(neg_ord) - 1))
    pos_ord = lsd(positivos, "(no negativos) " if negativos else "", lambda v: neg_ord + v)
    return neg_ord + pos_ord, st


METODOS = {
    "1": dict(
        nombre="ShellSort", funcion=shell_sort,
        consiste=(
            "Es una mejora del ordenamiento por inserción. En lugar de comparar solo elementos vecinos,\n"
            "  empieza comparando elementos separados por un 'salto' grande (n/2) y ordena esas\n"
            "  sublistas; luego reduce el salto a la mitad (n/4, n/8, ...) hasta llegar a 1. Así los\n"
            "  números mueven distancias largas desde el principio y, cuando el salto es 1, la lista\n"
            "  ya está casi ordenada y la inserción termina muy rápido."),
        porque=(
            "Es muy sencillo de programar, no usa recursión ni memoria extra (ordena 'en sitio') y\n"
            "  es mucho más rápido que inserción o burbuja con listas medianas. Es buena opción cuando\n"
            "  se quiere algo simple y eficiente sin complicarse."),
        complejidad="Mejor: O(n log n) · Promedio: ≈ O(n^1.3 – n^1.5) según los saltos · Peor: O(n²) · No estable",
        mejora=(
            "• Con mejores secuencias de saltos (Knuth: 1, 4, 13, 40… o Ciura) el mismo ShellSort baja a\n"
            "    ≈ O(n^1.3).\n"
            "  • Para listas grandes (miles de elementos) Quicksort, Heapsort o Timsort son mejores porque\n"
            "    garantizan o logran O(n log n)."),
    ),
    "2": dict(
        nombre="Quicksort", funcion=quick_sort,
        consiste=(
            "Usa 'divide y vencerás'. Se elige un pivote (aquí el elemento central) y se reparte la\n"
            "  lista en tres zonas: menores que el pivote, iguales y mayores. El pivote queda en su lugar\n"
            "  definitivo. Después se repite exactamente lo mismo con la zona de los menores y con la de\n"
            "  los mayores, hasta que las zonas tengan 0 o 1 elemento."),
        porque=(
            "Es en la práctica el más rápido de los métodos por comparación: O(n log n) en promedio,\n"
            "  ordena en sitio (poca memoria) y aprovecha muy bien la memoria caché. Por eso es la base\n"
            "  de muchas funciones de ordenamiento de librerías."),
        complejidad="Mejor y promedio: O(n log n) · Peor: O(n²) (pivotes muy malos) · En sitio · No estable",
        mejora=(
            "• Elegir el pivote como mediana de tres o al azar, y usar inserción en sublistas pequeñas\n"
            "    (≤ 16 elementos).\n"
            "  • Introsort: Quicksort que cambia a Heapsort si la recursión se vuelve muy profunda;\n"
            "    así el peor caso también es O(n log n).\n"
            "  • Si necesitas que sea ESTABLE (no cambiar el orden de iguales): Mergesort o Timsort."),
    ),
    "3": dict(
        nombre="Heapsort", funcion=heap_sort,
        consiste=(
            "Usa una estructura llamada montículo (heap) máximo, un árbol binario almacenado en la propia\n"
            "  lista donde cada padre es mayor que sus hijos. Primero se convierte la lista en montículo;\n"
            "  luego se intercambia la raíz (el mayor) con el último elemento, ese queda ya ordenado al\n"
            "  final, se reacomoda el montículo restante y se repite."),
        porque=(
            "Garantiza O(n log n) SIEMPRE (no tiene mal caso como Quicksort), ordena en sitio con memoria\n"
            "  extra O(1) y no usa recursión. Es ideal cuando se necesita un tiempo predecible o poca\n"
            "  memoria; además el montículo es la base de las colas de prioridad."),
        complejidad="Mejor, promedio y peor: O(n log n) · En sitio · No estable",
        mejora=(
            "• En la práctica Quicksort/Introsort suele ser ≈ 2 veces más rápido (mejor uso de la caché).\n"
            "  • Si se necesita estabilidad: Mergesort o Timsort.\n"
            "  • Con datos ya casi ordenados Heapsort no lo aprovecha; Insertion sort o Timsort sí."),
    ),
    "4": dict(
        nombre="Radix Sort", funcion=radix_sort,
        consiste=(
            "No compara los números entre sí. Los ordena dígito por dígito, empezando por el menos\n"
            "  significativo (unidades): reparte los números en 10 cubetas (0 a 9) según ese dígito y\n"
            "  los junta en orden; repite con las decenas, centenas, etc. Después del dígito más grande\n"
            "  la lista queda ordenada. Es estable en cada pasada."),
        porque=(
            "Con números enteros de pocos dígitos es de tiempo lineal, O(d·n), y supera a los métodos\n"
            "  basados en comparaciones (cuyo mínimo es O(n log n)). Es ideal para muchos enteros, claves\n"
            "  o códigos de longitud parecida."),
        complejidad="O(d·(n + b)) con d = número de dígitos y b = base (10) · Memoria extra O(n + b) · Estable",
        mejora=(
            "• Si los valores están en un rango pequeño, Counting Sort directo (O(n + rango)) es aún más\n"
            "    simple y rápido.\n"
            "  • Usar una base mayor (256 o 65536) reduce el número de pasadas.\n"
            "  • Si los números tienen MUCHOS dígitos (d grande) o hay decimales/texto mezclado,\n"
            "    Quicksort o Timsort resultan mejores."),
    ),
}


def fmt(x):
    return str(x)


def recomendar(datos, clave):
    n = len(datos)
    lineas = []
    ya_ordenada = all(datos[i] <= datos[i + 1] for i in range(n - 1))
    desordenados = sum(1 for i in range(n - 1) if datos[i] > datos[i + 1])
    rango = (max(datos) - min(datos) + 1) if n else 0
    digitos = len(str(max(abs(x) for x in datos))) if n else 0

    if n <= 1:
        lineas.append("Con 0 o 1 número no hay nada que ordenar: cualquier método sirve.")
    elif ya_ordenada:
        lineas.append("Tus números YA estaban ordenados: Insertion Sort o Timsort lo detectan y terminan en "
                      "una sola pasada, O(n).")
    elif n <= 16:
        lineas.append(f"Con solo {n} números lo más práctico es Insertion Sort: es el más simple y, con tan "
                      "pocos datos, el más rápido. Los métodos avanzados solo pagan la pena con listas grandes.")
    elif n > 1 and desordenados <= n * 0.1:
        lineas.append("Tus datos están CASI ordenados: Insertion Sort o Timsort los aprovechan y se acercan a O(n).")
    elif rango <= 2 * n:
        lineas.append(f"Tus valores están en un rango pequeño ({rango} posibles) para {n} datos: Counting Sort "
                      f"(O(n + {rango})) sería el más rápido.")
    elif clave == "4" and digitos > 8:
        lineas.append(f"Tus números tienen hasta {digitos} dígitos: Radix necesita una pasada por dígito; "
                      "Quicksort o Timsort serían mejores.")
    elif clave in ("1", "3"):
        lineas.append("Para listas grandes de números generales, Quicksort (o Introsort/Timsort, que es lo que "
                      "usa sorted() de Python) sería la mejor opción.")
    elif clave == "2":
        lineas.append("Quicksort ya es una excelente opción para datos generales. Solo lo superaría Timsort si "
                      "necesitaras estabilidad, o Radix si fueran enteros con pocos dígitos.")
    else:
        lineas.append(f"Radix es muy buena opción aquí: enteros de {digitos} dígito(s). Solo Counting Sort o una "
                      "base mayor lo mejorarían.")
    return lineas


def medir_los_cuatro(datos):
    repeticiones = max(1, 20000 // max(len(datos), 1))
    filas = []
    for m in METODOS.values():
        _, st = m["funcion"](datos)
        t0 = time.perf_counter()
        for _ in range(repeticiones):
            m["funcion"](datos)
        ms = (time.perf_counter() - t0) / repeticiones * 1000
        filas.append((m["nombre"], st["comparaciones"], st["movimientos"], ms))
    t0 = time.perf_counter()
    for _ in range(repeticiones):
        sorted(datos)
    filas.append(("sorted() de Python (Timsort)", "-", "-", (time.perf_counter() - t0) / repeticiones * 1000))
    return filas


def parsear_numeros(texto):
    datos = []
    for p in texto.replace(",", " ").replace(";", " ").split():
        try:
            datos.append(int(p))
        except ValueError:
            raise ValueError(p)
    return datos


COL = dict(
    bg="#08060d", panel="#120e1c", panel2="#1b1530", caja="#0d0a16", borde="#3b2a63",
    morado="#8b5cf6", morado_osc="#6d28d9", lila="#c4b5fd", magenta="#e879f9",
    texto="#ede9fe", suave="#9d8fc4", error="#f472b6",
)


def limpiar_parrafos(texto):
    items = []
    for ln in texto.split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        if ln.startswith("•") or not items:
            items.append(ln)
        else:
            items[-1] += " " + ln
    return items


class App(tk.Tk if tk else object):
    def __init__(self):
        super().__init__()
        self.title("Métodos de Ordenamiento")
        self.geometry("1320x860")
        self.minsize(1120, 740)
        self.configure(bg=COL["bg"])
        self.fam = self._fuente(("Segoe UI", "SF Pro Text", "Helvetica Neue", "Ubuntu", "Noto Sans",
                                 "DejaVu Sans", "Helvetica"))
        self.mono = self._fuente(("Cascadia Mono", "Consolas", "Menlo", "DejaVu Sans Mono", "Courier New"))
        self.metodo = tk.StringVar(value="1")
        self.var_n = tk.StringVar()
        self.var_pasos = tk.BooleanVar(value=True)
        self.var_vel = tk.IntVar(value=700)
        self.pasos, self.k, self._reproduciendo = [], 0, None
        self._estilos()
        self._construir()
        self.mostrar_explicacion("1")
        self.dibujar()
        self.mensaje("Escribe tus números (o pulsa 🎲 Aleatorios), elige un método y pulsa ORDENAR.", "info")

    def _fuente(self, opciones):
        try:
            disponibles = set(tkfont.families())
            for f in opciones:
                if f in disponibles:
                    return f
        except Exception:
            pass
        return opciones[-1]

    def _estilos(self):
        C, F = COL, self.fam
        s = ttk.Style(self)
        try:
            s.theme_use("clam")
        except Exception:
            pass
        s.configure(".", background=C["panel"], foreground=C["texto"], font=(F, 10), bordercolor=C["borde"],
                    lightcolor=C["panel"], darkcolor=C["panel"], troughcolor=C["panel2"],
                    focuscolor=C["panel"], relief="flat")
        s.configure("TFrame", background=C["bg"])
        s.configure("Card.TFrame", background=C["panel"])
        s.configure("TLabel", background=C["panel"], foreground=C["texto"])
        s.configure("Sec.TLabel", background=C["panel"], foreground=C["magenta"], font=(F, 9, "bold"))
        s.configure("Muted.TLabel", background=C["panel"], foreground=C["suave"], font=(F, 9))
        s.configure("TButton", background=C["panel2"], foreground=C["texto"], padding=(12, 8), borderwidth=0,
                    font=(F, 10, "bold"))
        s.map("TButton", background=[("pressed", C["borde"]), ("active", C["borde"])])
        s.configure("Accent.TButton", background=C["morado"], foreground="#ffffff", padding=(12, 11),
                    font=(F, 12, "bold"))
        s.map("Accent.TButton", background=[("pressed", C["morado_osc"]), ("active", C["morado_osc"])])
        s.configure("Salir.TButton", background=C["bg"], foreground=C["lila"], padding=(12, 8),
                    bordercolor=C["morado"], borderwidth=1)
        s.map("Salir.TButton", background=[("active", C["morado_osc"])], foreground=[("active", "#ffffff")])
        s.configure("Ctl.TButton", background=C["panel2"], foreground=C["lila"], padding=(10, 6))
        s.map("Ctl.TButton", background=[("active", C["morado_osc"])], foreground=[("active", "#ffffff")])
        s.configure("Metodo.Toolbutton", background=C["panel2"], foreground=C["texto"], padding=(14, 10),
                    anchor="w", font=(F, 11, "bold"), borderwidth=0, relief="flat")
        s.map("Metodo.Toolbutton", background=[("selected", C["morado"]), ("active", C["borde"])],
              foreground=[("selected", "#ffffff")])
        s.configure("TCheckbutton", background=C["panel"], foreground=C["texto"], indicatorcolor=C["caja"])
        s.map("TCheckbutton", background=[("active", C["panel"])], indicatorcolor=[("selected", C["morado"])])
        s.configure("TEntry", fieldbackground=C["caja"], foreground=C["texto"], insertcolor=C["lila"],
                    bordercolor=C["borde"], lightcolor=C["borde"], darkcolor=C["borde"], padding=7)
        s.configure("TNotebook", background=C["bg"], borderwidth=0, tabmargins=(0, 0, 0, 0))
        s.configure("TNotebook.Tab", background=C["panel2"], foreground=C["suave"], padding=(16, 8),
                    font=(F, 10, "bold"), borderwidth=0)
        s.map("TNotebook.Tab", background=[("selected", C["panel"])], foreground=[("selected", C["lila"])])
        s.configure("Horizontal.TScale", background=C["panel"], troughcolor=C["panel2"])
        for sb in ("Vertical.TScrollbar", "Horizontal.TScrollbar"):
            s.configure(sb, background=C["panel2"], troughcolor=C["bg"], arrowcolor=C["lila"],
                        bordercolor=C["bg"], relief="flat")
        s.configure("Treeview", background=C["caja"], fieldbackground=C["caja"], foreground=C["texto"],
                    rowheight=32, borderwidth=0, font=(F, 10))
        s.configure("Treeview.Heading", background=C["morado_osc"], foreground="#ffffff", relief="flat",
                    font=(F, 10, "bold"), padding=(8, 7))
        s.map("Treeview", background=[("selected", C["morado"])])

    def _texto(self, padre, **kw):
        C = COL
        t = tk.Text(padre, bg=C["caja"], fg=C["texto"], insertbackground=C["lila"], selectbackground=C["morado"],
                    relief="flat", highlightthickness=1, highlightbackground=C["borde"],
                    highlightcolor=C["morado"], padx=12, pady=10, **kw)
        return t

    def _construir(self):
        C, F = COL, self.fam
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        hdr = tk.Frame(self, bg=C["morado_osc"])
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.columnconfigure(0, weight=1)
        caja = tk.Frame(hdr, bg=C["morado_osc"])
        caja.grid(row=0, column=0, sticky="w", padx=20, pady=12)
        tk.Label(caja, text="MÉTODOS DE ORDENAMIENTO", bg=C["morado_osc"], fg="#ffffff",
                 font=(F, 18, "bold")).pack(anchor="w")
        tk.Label(caja, text="ShellSort  ·  Quicksort  ·  Heapsort  ·  Radix", bg=C["morado_osc"],
                 fg=C["lila"], font=(F, 10)).pack(anchor="w")

        cuerpo = ttk.Frame(self)
        cuerpo.grid(row=1, column=0, sticky="nsew", padx=14, pady=14)
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        izq = ttk.Frame(cuerpo, style="Card.TFrame", padding=16)
        izq.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        ttk.Label(izq, text="1 · ELIGE EL MÉTODO", style="Sec.TLabel").pack(anchor="w", pady=(0, 6))
        for clave, m in METODOS.items():
            ttk.Radiobutton(izq, text=f"{clave}   ·   {m['nombre']}", variable=self.metodo, value=clave,
                            style="Metodo.Toolbutton", command=lambda k=clave: self.cambio_metodo(k)
                            ).pack(fill="x", pady=2)
        ttk.Label(izq, text="2 · CANTIDAD DE NÚMEROS", style="Sec.TLabel").pack(anchor="w", pady=(16, 4))
        self.entrada_n = ttk.Entry(izq, textvariable=self.var_n, width=10, font=(F, 12, "bold"))
        self.entrada_n.pack(fill="x")
        ttk.Label(izq, text="(si lo dejas vacío se cuenta solo)", style="Muted.TLabel").pack(anchor="w")
        ttk.Label(izq, text="3 · ESCRIBE LOS NÚMEROS", style="Sec.TLabel").pack(anchor="w", pady=(14, 4))
        self.entrada_nums = self._texto(izq, height=4, width=30, wrap="word", font=(self.mono, 11))
        self.entrada_nums.pack(fill="x")
        ttk.Label(izq, text="Enteros separados por espacios o comas. Aceptan negativos.",
                  style="Muted.TLabel", wraplength=290, justify="left").pack(anchor="w", pady=(2, 8))
        fila = ttk.Frame(izq, style="Card.TFrame")
        fila.pack(fill="x")
        fila.columnconfigure((0, 1), weight=1)
        ttk.Button(fila, text="🎲  Aleatorios", command=self.aleatorios).grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(fila, text="🧹  Limpiar", command=self.limpiar).grid(row=0, column=1, sticky="ew", padx=(4, 0))
        ttk.Checkbutton(izq, text=f"Mostrar paso a paso (hasta {MAX_BARRAS} números)",
                        variable=self.var_pasos).pack(anchor="w", pady=(12, 10))
        ttk.Button(izq, text="▶   O R D E N A R", style="Accent.TButton", command=self.ordenar).pack(fill="x")
        ttk.Button(izq, text="⚖   Comparar los 4 métodos", command=self.comparar).pack(fill="x", pady=(8, 0))
        self.lbl_msg = tk.Label(izq, text="", bg=C["panel"], fg=C["suave"], font=(F, 10), wraplength=290,
                                justify="left", anchor="w")
        self.lbl_msg.pack(fill="x", pady=(14, 8))
        ttk.Button(izq, text="Salir", style="Salir.TButton", command=self.destroy).pack(side="bottom", fill="x")

        der = ttk.Frame(cuerpo)
        der.grid(row=0, column=1, sticky="nsew")
        der.columnconfigure(0, weight=1)
        der.rowconfigure(1, weight=3)
        der.rowconfigure(4, weight=2)

        self.lbl_paso = tk.Label(der, text="", bg=C["bg"], fg=C["lila"], font=(F, 11, "bold"), anchor="w",
                                 justify="left", wraplength=900)
        self.lbl_paso.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        marco = ttk.Frame(der, style="Card.TFrame", padding=2)
        marco.grid(row=1, column=0, sticky="nsew")
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(marco, bg=C["caja"], highlightthickness=0, height=280)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", lambda e: self.dibujar())

        ctl = ttk.Frame(der, style="Card.TFrame", padding=(10, 8))
        ctl.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        for texto, cmd in (("⏮  Inicio", self.ir_inicio), ("◀  Anterior", self.anterior)):
            ttk.Button(ctl, text=texto, style="Ctl.TButton", command=cmd).pack(side="left", padx=3)
        self.btn_play = ttk.Button(ctl, text="▶  Reproducir", style="Ctl.TButton", command=self.reproducir)
        self.btn_play.pack(side="left", padx=3)
        for texto, cmd in (("Siguiente  ▶", self.siguiente), ("Final  ⏭", self.ir_final)):
            ttk.Button(ctl, text=texto, style="Ctl.TButton", command=cmd).pack(side="left", padx=3)
        ttk.Scale(ctl, from_=1500, to=100, variable=self.var_vel, length=130).pack(side="right", padx=(6, 2))
        ttk.Label(ctl, text="⏱ Velocidad", style="Muted.TLabel").pack(side="right", padx=(10, 2))

        self.txt_res = self._texto(der, height=4, wrap="word", font=(self.mono, 10))
        self.txt_res.grid(row=3, column=0, sticky="ew", pady=(8, 8))
        self.txt_res.tag_configure("rotulo", foreground=C["magenta"], font=(self.mono, 10, "bold"))
        self.txt_res.tag_configure("dato", foreground=C["texto"])
        self.txt_res.configure(state="disabled")

        nb = ttk.Notebook(der)
        nb.grid(row=4, column=0, sticky="nsew")
        self.nb = nb
        tab1 = ttk.Frame(nb, style="Card.TFrame", padding=8)
        tab2 = ttk.Frame(nb, style="Card.TFrame", padding=8)
        tab3 = ttk.Frame(nb, style="Card.TFrame", padding=8)
        nb.add(tab1, text="📖  Explicación")
        nb.add(tab2, text="🧾  Procedimiento")
        nb.add(tab3, text="⚖  Comparación")
        for tab in (tab1, tab2, tab3):
            tab.rowconfigure(0, weight=1)
            tab.columnconfigure(0, weight=1)

        self.txt_exp = self._texto(tab1, wrap="word", font=(F, 11), state="disabled")
        self.txt_exp.grid(row=0, column=0, sticky="nsew")
        sb1 = ttk.Scrollbar(tab1, orient="vertical", command=self.txt_exp.yview)
        sb1.grid(row=0, column=1, sticky="ns")
        self.txt_exp.configure(yscrollcommand=sb1.set)
        self.txt_exp.tag_configure("titulo", foreground=C["lila"], font=(F, 15, "bold"), spacing3=6)
        self.txt_exp.tag_configure("rotulo", foreground=C["magenta"], font=(F, 10, "bold"), spacing1=10, spacing3=2)
        self.txt_exp.tag_configure("cuerpo", foreground=C["texto"], spacing3=3)
        self.txt_exp.tag_configure("suave", foreground=C["suave"])

        self.txt_proc = self._texto(tab2, wrap="word", font=(self.mono, 10), state="disabled")
        self.txt_proc.grid(row=0, column=0, sticky="nsew")
        sb2 = ttk.Scrollbar(tab2, orient="vertical", command=self.txt_proc.yview)
        sb2.grid(row=0, column=1, sticky="ns")
        self.txt_proc.configure(yscrollcommand=sb2.set)
        self.txt_proc.tag_configure("actual", background=C["morado_osc"], foreground="#ffffff")
        self.txt_proc.tag_configure("normal", foreground=C["texto"])

        self.tabla = ttk.Treeview(tab3, columns=("metodo", "comp", "mov", "tiempo"), show="headings", height=6)
        for col, texto, ancho, ancla in (("metodo", "Método", 260, "w"), ("comp", "Comparaciones", 130, "center"),
                                         ("mov", "Movimientos", 120, "center"), ("tiempo", "Tiempo (ms)", 120, "center")):
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, anchor=ancla)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        self.tabla.tag_configure("ganador", background=C["morado_osc"], foreground="#ffffff")
        self.lbl_comp = tk.Label(tab3, text="Pulsa «Comparar los 4 métodos» para ver quién gana con tus datos.",
                                 bg=C["panel"], fg=C["suave"], font=(F, 10), anchor="w", justify="left",
                                 wraplength=800)
        self.lbl_comp.grid(row=1, column=0, sticky="ew", pady=(8, 0))

        self.bind("<Return>", self._enter)

    def _enter(self, ev):
        if ev.widget is not self.entrada_nums:
            self.ordenar()

    def mensaje(self, texto, tipo="info"):
        color = {"info": COL["suave"], "ok": COL["lila"], "error": COL["error"]}[tipo]
        self.lbl_msg.config(text=texto, fg=color)

    def _escribir(self, widget, fn):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        fn(widget)
        widget.configure(state="disabled")

    def mostrar_explicacion(self, clave, datos=None):
        m = METODOS[clave]

        def llenar(t):
            t.insert("end", f"{m['nombre']}\n", "titulo")
            for rotulo, texto in (("¿EN QUÉ CONSISTE?", m["consiste"]), ("¿POR QUÉ SE USA ESTE MÉTODO?", m["porque"])):
                t.insert("end", rotulo + "\n", "rotulo")
                for p in limpiar_parrafos(texto):
                    t.insert("end", p + "\n", "cuerpo")
            t.insert("end", "COMPLEJIDAD\n", "rotulo")
            t.insert("end", m["complejidad"] + "\n", "cuerpo")
            t.insert("end", "¿SE PODRÍA MEJORAR CON OTRO MÉTODO? ¿CUÁL?\n", "rotulo")
            for p in limpiar_parrafos(m["mejora"]):
                t.insert("end", p + "\n", "cuerpo")
            if datos is not None:
                t.insert("end", "PARA TUS DATOS\n", "rotulo")
                for ln in recomendar(datos, clave):
                    t.insert("end", "→ " + ln + "\n", "cuerpo")
        self._escribir(self.txt_exp, llenar)

    def cambio_metodo(self, clave):
        self.mostrar_explicacion(clave)
        self.nb.select(0)
        self.mensaje(f"Método elegido: {METODOS[clave]['nombre']}. Pulsa ORDENAR.", "info")

    def leer_datos(self):
        txt = self.entrada_nums.get("1.0", "end").strip()
        if not txt:
            self.mensaje("✖ Escribe los números a ordenar (o pulsa 🎲 Aleatorios).", "error")
            self.entrada_nums.focus_set()
            return None
        try:
            datos = parsear_numeros(txt)
        except ValueError as e:
            self.mensaje(f"✖ «{e}» no es un número entero. Solo se aceptan enteros (sin letras ni decimales).", "error")
            return None
        if len(datos) > LIMITE_DATOS:
            self.mensaje(f"✖ Máximo {LIMITE_DATOS} números.", "error")
            return None
        cantidad = self.var_n.get().strip()
        if cantidad:
            try:
                n = int(cantidad)
                if n < 1:
                    raise ValueError
            except ValueError:
                self.mensaje("✖ La cantidad debe ser un entero positivo.", "error")
                self.entrada_n.focus_set()
                return None
            if n != len(datos):
                self.mensaje(f"✖ Dijiste {n} números pero escribiste {len(datos)}. "
                             "Corrige la cantidad o los números.", "error")
                return None
        else:
            self.var_n.set(str(len(datos)))
        return datos

    def aleatorios(self):
        try:
            n = int(self.var_n.get().strip())
            if not 1 <= n <= LIMITE_DATOS:
                raise ValueError
        except ValueError:
            n = 12
            self.var_n.set("12")
        tope = 99 if n <= 40 else 999
        datos = [random.randint(1, tope) for _ in range(n)]
        self.entrada_nums.delete("1.0", "end")
        self.entrada_nums.insert("1.0", ", ".join(map(str, datos)))
        self.mensaje(f"Se generaron {n} números al azar. Pulsa ORDENAR.", "ok")

    def limpiar(self):
        self.detener()
        self.var_n.set("")
        self.entrada_nums.delete("1.0", "end")
        self.pasos, self.k = [], 0
        self._escribir(self.txt_res, lambda t: None)
        self._escribir(self.txt_proc, lambda t: None)
        self.mostrar_explicacion(self.metodo.get())
        self.lbl_paso.config(text="")
        self.dibujar()
        self.mensaje("Todo limpio. Escribe nuevos números para empezar.", "info")

    def ordenar(self):
        datos = self.leer_datos()
        if datos is None:
            return
        self.detener()
        clave = self.metodo.get()
        m = METODOS[clave]
        trazas = []
        visual = self.var_pasos.get() and len(datos) <= MAX_BARRAS
        ordenada, st = m["funcion"](datos, (lambda msg, estado, marca: trazas.append((msg, estado, marca)))
                                    if visual else None)
        assert ordenada == sorted(datos)
        self.pasos = [("Lista original", list(datos), None)] + trazas + [("✔ Lista ORDENADA", ordenada, "todo")]
        self.k = 0
        if self.var_pasos.get() and len(datos) > MAX_BARRAS:
            self.mensaje(f"Son {len(datos)} números: demasiados para dibujar paso a paso (máx. {MAX_BARRAS}). "
                         "Se muestra el resultado final.", "info")
            self.pasos = [self.pasos[0], self.pasos[-1]]
            self.k = 1
        elif not self.var_pasos.get():
            self.k = len(self.pasos) - 1
            self.mensaje(f"¡Listo! Ordenado con {m['nombre']}.", "ok")
        else:
            self.mensaje(f"¡Listo! Ordenado con {m['nombre']}. Usa los botones para ver cada paso.", "ok")

        def res(t):
            t.insert("end", "Original: ", "rotulo")
            t.insert("end", self._lista(datos) + "\n", "dato")
            t.insert("end", "Ordenada: ", "rotulo")
            t.insert("end", self._lista(ordenada) + "\n", "dato")
            t.insert("end", "Comparaciones: ", "rotulo")
            t.insert("end", f"{st['comparaciones']}" + ("  (Radix no compara números entre sí)" if clave == "4" else "")
                     + "     ", "dato")
            t.insert("end", "Movimientos: ", "rotulo")
            t.insert("end", f"{st['movimientos']}\n", "dato")
        self._escribir(self.txt_res, res)
        self.mostrar_explicacion(clave, datos)

        def proc(t):
            for i, (msg, _, _) in enumerate(self.pasos):
                t.insert("end", f"{i}. {msg}\n" if i else f"{msg}  →  {self._lista(datos)}\n", "normal")
        self._escribir(self.txt_proc, proc)
        self.refrescar()

    @staticmethod
    def _lista(lista, maximo=40):
        if len(lista) <= maximo:
            return str(lista)
        return f"{lista[:20]} ... {lista[-10:]}   ({len(lista)} números)"

    def comparar(self):
        datos = self.leer_datos()
        if datos is None:
            return
        filas = medir_los_cuatro(datos)
        for it in self.tabla.get_children():
            self.tabla.delete(it)
        ganador = min(filas[:4], key=lambda f: f[3])[0]
        for nombre, c, mv, ms in filas:
            self.tabla.insert("", "end", values=(nombre, c, mv, f"{ms:.4f}"),
                              tags=("ganador",) if nombre == ganador else ())
        nota = f"Más rápido de los 4 con tus datos: {ganador}."
        if len(datos) < 200:
            nota += "  Con tan pocos números las diferencias son mínimas; prueba con cientos o miles (🎲 Aleatorios)."
        nota += "\n→ " + recomendar(datos, "2")[0]
        self.lbl_comp.config(text=nota, fg=COL["lila"])
        self.nb.select(2)
        self.mensaje(f"Comparación lista con {len(datos)} números.", "ok")

    def dibujar(self):
        C, c = COL, self.canvas
        c.delete("all")
        W = max(c.winfo_width() or 0, 500)
        H = max(c.winfo_height() or 0, 240)
        if not self.pasos:
            c.create_text(W / 2, H / 2, fill=C["suave"], font=(self.fam, 14), justify="center",
                          text="Aquí verás tus números como barras moradas.\n\n"
                               "Escribe una lista, elige un método y pulsa ORDENAR.")
            return
        _, estado, marca = self.pasos[self.k]
        n = len(estado)
        if n > MAX_BARRAS:
            c.create_text(W / 2, H / 2, fill=C["lila"], font=(self.fam, 14), justify="center",
                          text=f"Son {n} números: son demasiados para dibujarlos como barras.\n"
                               "Mira el resultado ordenado debajo.")
            return
        pad = 26
        vmax, vmin = max(max(estado), 0), min(min(estado), 0)
        rango = (vmax - vmin) or 1
        top, bottom = pad + 14, H - pad
        zona = bottom - top
        base = bottom - (0 - vmin) / rango * zona
        ancho = (W - 2 * pad) / n
        bw = ancho * 0.74
        for i, v in enumerate(estado):
            x = pad + i * ancho + (ancho - bw) / 2
            y = bottom - (v - vmin) / rango * zona
            if marca == "todo":
                color = C["lila"]
            elif marca and marca[0] <= i <= marca[1]:
                color = C["magenta"]
            else:
                color = C["morado"]
            y1, y2 = min(y, base), max(y, base)
            if y2 - y1 < 3:
                y2 = y1 + 3
            c.create_rectangle(x, y1, x + bw, y2, fill=color, outline="")
            if n <= 25:
                if v >= 0:
                    c.create_text(x + bw / 2, y1 - 3, text=str(v), fill=C["texto"], anchor="s",
                                  font=(self.fam, 9 if n > 18 else 10, "bold"))
                else:
                    c.create_text(x + bw / 2, y2 + 3, text=str(v), fill=C["texto"], anchor="n",
                                  font=(self.fam, 9 if n > 18 else 10, "bold"))
        c.create_line(pad - 6, base, W - pad + 6, base, fill=C["borde"])

    def refrescar(self):
        msg = self.pasos[self.k][0] if self.pasos else ""
        total = len(self.pasos) - 1
        self.lbl_paso.config(text=("Paso %d de %d  —  " % (self.k, total) if total > 0 else "") + msg[:260])
        self.dibujar()
        t = self.txt_proc
        t.tag_remove("actual", "1.0", "end")
        if self.pasos:
            t.tag_add("actual", f"{self.k + 1}.0", f"{self.k + 1}.end")
            t.see(f"{self.k + 1}.0")
        if self._reproduciendo is None:
            self.btn_play.config(text="▶  Reproducir")

    def siguiente(self):
        self.detener()
        if self.pasos and self.k < len(self.pasos) - 1:
            self.k += 1
            self.refrescar()

    def anterior(self):
        self.detener()
        if self.pasos and self.k > 0:
            self.k -= 1
            self.refrescar()

    def ir_inicio(self):
        self.detener()
        if self.pasos:
            self.k = 0
            self.refrescar()

    def ir_final(self):
        self.detener()
        if self.pasos:
            self.k = len(self.pasos) - 1
            self.refrescar()

    def detener(self):
        if self._reproduciendo is not None:
            try:
                self.after_cancel(self._reproduciendo)
            except Exception:
                pass
            self._reproduciendo = None
            self.btn_play.config(text="▶  Reproducir")

    def reproducir(self):
        if self._reproduciendo is not None:
            self.detener()
            return
        if not self.pasos:
            self.mensaje("Primero pulsa ORDENAR para generar los pasos.", "error")
            return
        if self.k >= len(self.pasos) - 1:
            self.k = 0
        self.btn_play.config(text="⏸  Pausa")
        self._tick()

    def _tick(self):
        self.refrescar()
        if self.k < len(self.pasos) - 1:
            self.k += 1
            self._reproduciendo = self.after(max(80, int(self.var_vel.get())), self._tick)
        else:
            self._reproduciendo = None
            self.refrescar()


def pedir(texto):
    try:
        return input(texto).strip()
    except EOFError:
        print("\n(fin de la entrada)")
        raise SystemExit


def mostrar(lista, max_items=40):
    if len(lista) <= max_items:
        return str(lista)
    return f"{lista[:20]} ... {lista[-10:]}   ({len(lista)} números en total)"


def leer_datos_consola():
    while True:
        txt = pedir("\nCantidad de números a ordenar (o 'c' para cancelar): ")
        if txt.lower() == "c":
            return None
        try:
            n = int(txt)
            if not 1 <= n <= LIMITE_DATOS:
                raise ValueError
            break
        except ValueError:
            print(f"  ✖ Escribe un entero entre 1 y {LIMITE_DATOS}.")
    while True:
        txt = pedir(f"Escribe los {n} números (enteros) separados por espacios o comas.\n"
                    f"   Escribe 'r' para generar {n} números al azar, o 'c' para cancelar:\n> ")
        if txt.lower() == "c":
            return None
        if txt.lower() == "r":
            datos = [random.randint(-99, 999) for _ in range(n)]
            print(f"  Números generados: {mostrar(datos)}")
            return datos
        try:
            datos = parsear_numeros(txt)
        except ValueError:
            print("  ✖ Solo se aceptan números enteros (sin letras ni decimales). Inténtalo otra vez.")
            continue
        if len(datos) != n:
            print(f"  ✖ Dijiste {n} números pero escribiste {len(datos)}. Inténtalo otra vez.")
            continue
        return datos


def ejecutar_consola(clave):
    m = METODOS[clave]
    print(f"\n{'=' * 64}\n  {m['nombre'].upper()}\n{'=' * 64}")
    print(f"¿EN QUÉ CONSISTE?\n  {m['consiste']}")
    datos = leer_datos_consola()
    if datos is None:
        print("Operación cancelada.")
        return
    ver_pasos = False
    if len(datos) <= LIMITE_PASO_A_PASO:
        ver_pasos = pedir("¿Quieres ver el procedimiento paso a paso? (s/n): ").lower().startswith("s")
    else:
        print(f"(Con más de {LIMITE_PASO_A_PASO} números no se muestran los pasos para no llenar la pantalla.)")
    traza = []
    ordenada, st = m["funcion"](datos, (lambda msg, estado=None, marca=None: traza.append(msg)) if ver_pasos else None)
    print(f"\nLista original: {mostrar(datos)}")
    if ver_pasos:
        print("\nPROCEDIMIENTO:")
        for i, p in enumerate(traza, 1):
            print(f"  {i:>2}. {p}")
    print(f"\n✔ Lista ORDENADA ({m['nombre']}): {mostrar(ordenada)}")
    assert ordenada == sorted(datos)
    print(f"  Comparaciones: {st['comparaciones']}   Movimientos: {st['movimientos']}"
          + ("   (Radix no compara números entre sí)" if clave == "4" else ""))
    print(f"  Complejidad: {m['complejidad']}")
    print(f"\n¿POR QUÉ SE USA ESTE MÉTODO?\n  {m['porque']}")
    print(f"\n¿SE PODRÍA MEJORAR CON OTRO MÉTODO? ¿CUÁL?\n  {m['mejora']}")
    print("\n  → Para TUS datos:")
    for ln in recomendar(datos, clave):
        print(f"    {ln}")


def comparar_consola():
    print(f"\n{'=' * 64}\n  COMPARAR LOS CUATRO MÉTODOS CON LOS MISMOS DATOS\n{'=' * 64}")
    datos = leer_datos_consola()
    if datos is None:
        print("Operación cancelada.")
        return
    filas = medir_los_cuatro(datos)
    print(f"\nDatos ({len(datos)}): {mostrar(datos)}\nResultado ordenado: {mostrar(sorted(datos))}\n")
    print(f"  {'Método':<30}{'Comparaciones':>15}{'Movimientos':>14}{'Tiempo (ms)':>14}")
    print("  " + "-" * 73)
    for nombre, c, mv, ms in filas:
        print(f"  {nombre:<30}{str(c):>15}{str(mv):>14}{ms:>14.4f}")
    print(f"\n  Más rápido de los 4 con estos datos: {min(filas[:4], key=lambda f: f[3])[0]}")
    print("\n  → Sugerencia para tus datos:")
    for ln in recomendar(datos, "2"):
        print(f"    {ln}")


def explicaciones_consola():
    for m in METODOS.values():
        print(f"\n{'=' * 64}\n  {m['nombre'].upper()}\n{'=' * 64}")
        print(f"¿EN QUÉ CONSISTE?\n  {m['consiste']}")
        print(f"\n¿POR QUÉ SE USA?\n  {m['porque']}")
        print(f"\nCOMPLEJIDAD\n  {m['complejidad']}")
        print(f"\n¿SE PUEDE MEJORAR?\n  {m['mejora']}")


MENU = """
╔══════════════════════════════════════════════╗
║        MÉTODOS DE ORDENAMIENTO               ║
╠══════════════════════════════════════════════╣
║  1. ShellSort                                ║
║  2. Quicksort                                ║
║  3. Heapsort                                 ║
║  4. Radix                                    ║
║  5. Comparar los cuatro con los mismos datos ║
║  6. Ver la explicación de todos los métodos  ║
║  0. Salir                                    ║
╚══════════════════════════════════════════════╝"""


def menu_consola():
    while True:
        print(MENU)
        op = pedir("Elige una opción: ")
        if op == "0":
            print("¡Hasta luego!")
            break
        elif op in METODOS:
            ejecutar_consola(op)
        elif op == "5":
            comparar_consola()
        elif op == "6":
            explicaciones_consola()
        else:
            print("  ✖ Opción no válida. Elige un número del menú.")
        pedir("\nPresiona Enter para volver al menú...")


if __name__ == "__main__":
    if "--consola" in sys.argv or tk is None:
        if tk is None and "--consola" not in sys.argv:
            print("tkinter no está disponible en este equipo: se usa el menú de consola.")
        menu_consola()
    else:
        App().mainloop()