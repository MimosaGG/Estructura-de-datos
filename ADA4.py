import hashlib
import random
import tkinter as tk
from tkinter import messagebox


class BusquedasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos de Búsqueda en Python — Cualquier Tipo de Lista")
        self.root.geometry("1280x780")
        self.root.minsize(750, 660)

        # Paleta de colores: Morado y Rosado
        self.bg_principal = "#241438"      # Morado oscuro de fondo
        self.bg_tarjeta = "#341D52"        # Morado medio para contenedores
        self.bg_input = "#47296E"          # Morado más claro para entradas/consola
        self.morado_acento = "#7B2CBF"     # Morado vibrante
        self.rosado_principal = "#FF4D8D"  # Rosado intenso
        self.rosado_suave = "#FF85B3"      # Rosado pastel
        self.texto_claro = "#FFF5FA"       # Blanco rosado
        self.texto_muted = "#E2C6E9"       # Lavanda claro

        self.root.configure(bg=self.bg_principal)

        self.descripciones = {
            "Secuencial": (
                "Búsqueda Secuencial (o Lineal): Revisa los elementos uno por uno desde el inicio "
                "hasta encontrar el valor buscado o terminar la lista. Funciona con números o textos "
                "sin importar si la lista está ordenada."
            ),
            "Binaria": (
                "Búsqueda Binaria: Trabaja sobre una lista ordenada (numérica o alfabética) y en cada "
                "iteración compara el elemento central para descartar la mitad donde no puede estar el dato."
            ),
            "Hash": (
                "Búsqueda Hash: Usa una función hash para calcular el cubo/índice correspondiente a partir "
                "del valor buscado (numérico o texto) y revisa los elementos almacenados ahí."
            ),
        }

        self.metodo_var = tk.StringVar(value="Secuencial")
        self._construir_interfaz()
        self._actualizar_descripcion()

    def _construir_interfaz(self):
        # Encabezado
        header = tk.Frame(self.root, bg=self.bg_principal, padx=20, pady=12)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Métodos de Búsqueda con Paso a Paso",
            font=("Segoe UI", 19, "bold"),
            bg=self.bg_principal,
            fg=self.rosado_suave,
        ).pack()

        tk.Label(
            header,
            text="Compatible con enteros (int), decimales (float/double) y textos o nombres (str)",
            font=("Segoe UI", 10),
            bg=self.bg_principal,
            fg=self.texto_muted,
        ).pack(pady=(2, 0))

        main_frame = tk.Frame(self.root, bg=self.bg_principal, padx=20, pady=4)
        main_frame.pack(fill="both", expand=True)

        # 1. Menú de métodos
        card_menu = tk.Frame(
            main_frame,
            bg=self.bg_tarjeta,
            highlightbackground=self.rosado_principal,
            highlightthickness=1,
            padx=14,
            pady=10,
        )
        card_menu.pack(fill="x", pady=(0, 10))

        tk.Label(
            card_menu,
            text="1. Selecciona el método:",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_tarjeta,
            fg=self.rosado_suave,
        ).pack(anchor="w", pady=(0, 6))

        botones_frame = tk.Frame(card_menu, bg=self.bg_tarjeta)
        botones_frame.pack(fill="x")

        self.botones_metodo = {}
        for metodo in ["Secuencial", "Binaria", "Hash"]:
            btn = tk.Radiobutton(
                botones_frame,
                text=metodo,
                variable=self.metodo_var,
                value=metodo,
                command=self._actualizar_descripcion,
                indicatoron=0,
                font=("Segoe UI", 10, "bold"),
                bg=self.bg_input,
                fg=self.texto_claro,
                selectcolor=self.rosado_principal,
                activebackground=self.morado_acento,
                activeforeground=self.texto_claro,
                relief="flat",
                padx=16,
                pady=7,
                cursor="hand2",
            )
            btn.pack(side="left", padx=(0, 10))
            self.botones_metodo[metodo] = btn

        # 2. Descripción del método
        card_desc = tk.Frame(
            main_frame,
            bg=self.bg_tarjeta,
            highlightbackground=self.morado_acento,
            highlightthickness=1,
            padx=14,
            pady=10,
        )
        card_desc.pack(fill="x", pady=(0, 10))

        self.lbl_desc_titulo = tk.Label(
            card_desc,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_tarjeta,
            fg=self.rosado_principal,
        )
        self.lbl_desc_titulo.pack(anchor="w", pady=(0, 3))

        self.lbl_descripcion = tk.Label(
            card_desc,
            text="",
            font=("Segoe UI", 10),
            bg=self.bg_tarjeta,
            fg=self.texto_claro,
            justify="left",
            wraplength=740,
        )
        self.lbl_descripcion.pack(anchor="w")

        # 3. Datos y ejecución
        card_datos = tk.Frame(
            main_frame,
            bg=self.bg_tarjeta,
            highlightbackground=self.rosado_principal,
            highlightthickness=1,
            padx=14,
            pady=10,
        )
        card_datos.pack(fill="x", pady=(0, 10))

        fila_lista = tk.Frame(card_datos, bg=self.bg_tarjeta)
        fila_lista.pack(fill="x", pady=(0, 6))

        tk.Label(
            fila_lista,
            text="Lista de elementos (separados por coma):",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_tarjeta,
            fg=self.texto_claro,
        ).pack(side="left")

        botones_ejemplo = tk.Frame(fila_lista, bg=self.bg_tarjeta)
        botones_ejemplo.pack(side="right")

        tk.Button(
            botones_ejemplo,
            text="Ejemplo Nombres",
            command=self._ejemplo_nombres,
            font=("Segoe UI", 9, "bold"),
            bg=self.rosado_principal,
            fg="#FFFFFF",
            activebackground="#FF2A75",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=9,
            pady=3,
            cursor="hand2",
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            botones_ejemplo,
            text="Ejemplo Decimales",
            command=self._ejemplo_decimales,
            font=("Segoe UI", 9, "bold"),
            bg=self.morado_acento,
            fg=self.texto_claro,
            activebackground=self.rosado_principal,
            activeforeground=self.texto_claro,
            relief="flat",
            padx=9,
            pady=3,
            cursor="hand2",
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            botones_ejemplo,
            text="Ejemplo Enteros",
            command=self._ejemplo_enteros,
            font=("Segoe UI", 9, "bold"),
            bg=self.morado_acento,
            fg=self.texto_claro,
            activebackground=self.rosado_principal,
            activeforeground=self.texto_claro,
            relief="flat",
            padx=9,
            pady=3,
            cursor="hand2",
        ).pack(side="left")

        self.entry_lista = tk.Entry(
            card_datos,
            font=("Consolas", 11),
            bg=self.bg_input,
            fg=self.texto_claro,
            insertbackground=self.rosado_principal,
            relief="flat",
        )
        self.entry_lista.pack(fill="x", ipady=5, pady=(0, 8))
        self.entry_lista.insert(0, "Sofía, Mateo, Valentina, Lucas, Camila, Diego, Isabella")

        fila_buscar = tk.Frame(card_datos, bg=self.bg_tarjeta)
        fila_buscar.pack(fill="x")

        tk.Label(
            fila_buscar,
            text="Elemento a buscar:",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_tarjeta,
            fg=self.texto_claro,
        ).pack(side="left", padx=(0, 10))

        self.entry_objetivo = tk.Entry(
            fila_buscar,
            width=18,
            font=("Consolas", 11),
            bg=self.bg_input,
            fg=self.texto_claro,
            insertbackground=self.rosado_principal,
            relief="flat",
        )
        self.entry_objetivo.pack(side="left", ipady=4, padx=(0, 14))
        self.entry_objetivo.insert(0, "Diego")

        tk.Button(
            fila_buscar,
            text="Ejecutar y ver pasos",
            command=self._ejecutar_busqueda,
            font=("Segoe UI", 10, "bold"),
            bg=self.rosado_principal,
            fg="#FFFFFF",
            activebackground="#FF2A75",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=16,
            pady=5,
            cursor="hand2",
        ).pack(side="left")

        # 4. Consola en pantalla con iteraciones y scrollbar
        card_res = tk.Frame(
            main_frame,
            bg=self.bg_tarjeta,
            highlightbackground=self.morado_acento,
            highlightthickness=1,
            padx=14,
            pady=10,
        )
        card_res.pack(fill="both", expand=True, pady=(0, 10))

        tk.Label(
            card_res,
            text="Explicación iteración por iteración:",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_tarjeta,
            fg=self.rosado_suave,
        ).pack(anchor="w", pady=(0, 6))

        texto_frame = tk.Frame(card_res, bg=self.bg_input)
        texto_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(texto_frame)
        scrollbar.pack(side="right", fill="y")

        self.txt_resultado = tk.Text(
            texto_frame,
            font=("Consolas", 10),
            bg=self.bg_input,
            fg=self.texto_claro,
            relief="flat",
            padx=10,
            pady=8,
            wrap="word",
            yscrollcommand=scrollbar.set,
            state="disabled",
        )
        self.txt_resultado.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.txt_resultado.yview)

        self.txt_resultado.tag_config("titulo", foreground=self.rosado_suave, font=("Consolas", 10, "bold"))
        self.txt_resultado.tag_config("iteracion", foreground="#FFD1E6", font=("Consolas", 10, "bold"))
        self.txt_resultado.tag_config("exito", foreground="#FF85B3", font=("Consolas", 10, "bold"))

    def _actualizar_descripcion(self):
        metodo = self.metodo_var.get()
        self.lbl_desc_titulo.config(text=f"¿Qué hace la búsqueda {metodo}?")
        self.lbl_descripcion.config(text=self.descripciones[metodo])

        for nombre, btn in self.botones_metodo.items():
            if nombre == metodo:
                btn.config(bg=self.rosado_principal, fg="#FFFFFF")
            else:
                btn.config(bg=self.bg_input, fg=self.texto_claro)

    def _ejemplo_nombres(self):
        nombres = ["Sofía", "Mateo", "Valentina", "Lucas", "Camila", "Diego", "Isabella", "Emiliano"]
        random.shuffle(nombres)
        self.entry_lista.delete(0, tk.END)
        self.entry_lista.insert(0, ", ".join(nombres))
        self.entry_objetivo.delete(0, tk.END)
        self.entry_objetivo.insert(0, "Diego")

    def _ejemplo_decimales(self):
        decimales = [round(random.uniform(1.0, 99.9), 2) for _ in range(8)]
        self.entry_lista.delete(0, tk.END)
        self.entry_lista.insert(0, ", ".join(map(str, decimales)))
        self.entry_objetivo.delete(0, tk.END)
        self.entry_objetivo.insert(0, str(random.choice(decimales)))

    def _ejemplo_enteros(self):
        enteros = [random.randint(1, 99) for _ in range(8)]
        self.entry_lista.delete(0, tk.END)
        self.entry_lista.insert(0, ", ".join(map(str, enteros)))
        self.entry_objetivo.delete(0, tk.END)
        self.entry_objetivo.insert(0, str(random.choice(enteros)))

    def _limpiar_texto(self, texto):
        # Elimina espacios extra, saltos de línea o caracteres de espacio invisibles
        return " ".join(texto.replace("\u00a0", " ").split())

    def _parsear_token(self, token):
        limpio = self._limpiar_texto(token)
        try:
            return int(limpio)
        except ValueError:
            try:
                return float(limpio)
            except ValueError:
                return limpio

    def _obtener_datos(self):
        texto_lista = self._limpiar_texto(self.entry_lista.get())
        texto_obj = self._limpiar_texto(self.entry_objetivo.get())

        if not texto_lista or not texto_obj:
            raise ValueError("Completa tanto la lista de elementos como el elemento a buscar.")

        partes = [self._limpiar_texto(p) for p in texto_lista.split(",") if self._limpiar_texto(p) != ""]
        if not partes:
            raise ValueError("La lista está vacía.")

        elementos_parseados = [self._parsear_token(p) for p in partes]
        tipos = {type(x) for x in elementos_parseados}

        if tipos == {int}:
            lista = elementos_parseados
            try:
                objetivo = int(texto_obj)
            except ValueError:
                objetivo = texto_obj
        elif tipos.issubset({int, float}):
            lista = [float(x) for x in elementos_parseados]
            try:
                objetivo = float(texto_obj)
            except ValueError:
                objetivo = texto_obj
        else:
            lista = [str(x) for x in elementos_parseados]
            objetivo = texto_obj

        tipo_nombre = type(lista[0]).__name__
        return lista, objetivo, tipo_nombre

    def _son_iguales(self, a, b):
        if isinstance(a, str) and isinstance(b, str):
            return self._limpiar_texto(a).casefold() == self._limpiar_texto(b).casefold()
        return a == b

    def _clave_orden(self, valor):
        if isinstance(valor, str):
            return self._limpiar_texto(valor).casefold()
        return valor

    def _clave_hash(self, valor, capacidad):
        if isinstance(valor, int):
            return valor % capacidad, f"{valor} % {capacidad}"
        if isinstance(valor, float):
            if valor.is_integer():
                num = int(valor)
                return num % capacidad, f"int({valor}) % {capacidad}"
            digest = hashlib.sha256(str(valor).encode("utf-8")).hexdigest()
            num = int(digest[:12], 16)
            return num % capacidad, f"hash({valor!r}) % {capacidad}"

        normalizado = self._limpiar_texto(str(valor)).casefold()
        digest = hashlib.sha256(normalizado.encode("utf-8")).hexdigest()
        num = int(digest[:12], 16)
        return num % capacidad, f"hash({normalizado!r}) % {capacidad}"

    # --- Algoritmos con explicación por iteración ---
    def paso_secuencial(self, lista, objetivo, tipo_nombre):
        pasos = [
            ("titulo", f"=== BÚSQUEDA SECUENCIAL ({tipo_nombre}) | Objetivo: {objetivo!r} ===\n"),
            ("normal", f"Lista inicial: {lista}\n\n"),
        ]
        for idx, valor in enumerate(lista):
            pasos.append(("iteracion", f"Iteración {idx + 1}: "))
            pasos.append(("normal", f"Se revisa índice {idx} ({valor!r}) vs objetivo ({objetivo!r}). "))
            if self._son_iguales(valor, objetivo):
                pasos.append(("exito", f"¡Coincidencia! Se encontró {valor!r} en el índice {idx}.\n"))
                return pasos
            pasos.append(("normal", "No coincide, se avanza al siguiente elemento.\n"))

        pasos.append(("normal", f"\nConclusión: Se revisaron los {len(lista)} elementos y {objetivo!r} no está en la lista.\n"))
        return pasos

    def paso_binaria(self, lista, objetivo, tipo_nombre):
        ordenada = sorted(lista, key=self._clave_orden)
        izq, der = 0, len(ordenada) - 1
        iteracion = 0
        clave_obj = self._clave_orden(objetivo)

        pasos = [
            ("titulo", f"=== BÚSQUEDA BINARIA ({tipo_nombre}) | Objetivo: {objetivo!r} ===\n"),
            ("normal", f"Lista ordenada requerida: {ordenada}\n\n"),
        ]

        while izq <= der:
            iteracion += 1
            medio = (izq + der) // 2
            val_medio = ordenada[medio]
            clave_medio = self._clave_orden(val_medio)
            sublista = ordenada[izq : der + 1]

            pasos.append(("iteracion", f"Iteración {iteracion}: "))
            pasos.append(
                (
                    "normal",
                    f"Rango índices [{izq}..{der}] -> {sublista}. "
                    f"Centro en índice {medio} ({val_medio!r}).\n",
                )
            )

            if self._son_iguales(val_medio, objetivo):
                pasos.append(
                    (
                        "exito",
                        f"   -> ¡Encontrado! {val_medio!r} coincide con {objetivo!r} en el índice {medio} de la lista ordenada.\n",
                    )
                )
                return pasos
            if clave_medio < clave_obj:
                pasos.append(
                    (
                        "normal",
                        f"   -> Como {val_medio!r} va antes que {objetivo!r}, se descarta la mitad izquierda (izq = {medio + 1}).\n",
                    )
                )
                izq = medio + 1
            else:
                pasos.append(
                    (
                        "normal",
                        f"   -> Como {val_medio!r} va después que {objetivo!r}, se descarta la mitad derecha (der = {medio - 1}).\n",
                    )
                )
                der = medio - 1

        pasos.append(("normal", f"\nConclusión: Rango vacío tras {iteracion} iteración(es). {objetivo!r} no está en la lista.\n"))
        return pasos

    def paso_hash(self, lista, objetivo, tipo_nombre):
        capacidad = max(7, len(lista) * 2)
        tabla = [[] for _ in range(capacidad)]

        pasos = [
            ("titulo", f"=== BÚSQUEDA HASH ({tipo_nombre}) | Objetivo: {objetivo!r} ===\n"),
            ("normal", f"Lista original: {lista} | Capacidad de tabla: {capacidad}\n"),
            ("normal", "Construcción de la tabla hash:\n"),
        ]

        for i, valor in enumerate(lista):
            clave, expr = self._clave_hash(valor, capacidad)
            tabla[clave].append((valor, i))
            pasos.append(("normal", f"  - {valor!r} (índice orig. {i}) -> {expr} = cubo [{clave}]\n"))

        cubo_objetivo, expr_obj = self._clave_hash(objetivo, capacidad)
        pasos.append(("\niteracion", "\nIteración 1 (Cálculo de dirección): "))
        pasos.append(
            (
                "normal",
                f"Para {objetivo!r}: {expr_obj} = cubo [{cubo_objetivo}]. Contenido: {tabla[cubo_objetivo]}\n",
            )
        )

        if not tabla[cubo_objetivo]:
            pasos.append(("normal", f"Conclusión: El cubo [{cubo_objetivo}] está vacío; {objetivo!r} no existe en la tabla.\n"))
            return pasos

        for idx_interno, (val_guardado, idx_orig) in enumerate(tabla[cubo_objetivo], start=1):
            pasos.append(("iteracion", f"Iteración {idx_interno + 1} (Revisión en cubo [{cubo_objetivo}]): "))
            pasos.append(("normal", f"Se compara {val_guardado!r} (índice orig. {idx_orig}) con {objetivo!r}. "))
            if self._son_iguales(val_guardado, objetivo):
                pasos.append(("exito", f"¡Encontrado! Coincide con {val_guardado!r} (índice original {idx_orig}).\n"))
                return pasos
            pasos.append(("normal", "No coincide, se revisa el siguiente elemento en el cubo.\n"))

        pasos.append(("normal", f"\nConclusión: Se revisó todo el cubo [{cubo_objetivo}] y {objetivo!r} no se encontró.\n"))
        return pasos

    def _ejecutar_busqueda(self):
        try:
            lista, objetivo, tipo_nombre = self._obtener_datos()
        except ValueError as e:
            messagebox.showwarning("Datos inválidos", f"Revisa los datos ingresados.\nDetalle: {e}")
            return

        metodo = self.metodo_var.get()
        if metodo == "Secuencial":
            pasos = self.paso_secuencial(lista, objetivo, tipo_nombre)
        elif metodo == "Binaria":
            pasos = self.paso_binaria(lista, objetivo, tipo_nombre)
        else:
            pasos = self.paso_hash(lista, objetivo, tipo_nombre)

        self.txt_resultado.config(state="normal")
        self.txt_resultado.delete("1.0", tk.END)
        for tag, texto in pasos:
            if tag == "normal":
                self.txt_resultado.insert(tk.END, texto)
            else:
                self.txt_resultado.insert(tk.END, texto, tag)
        self.txt_resultado.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = BusquedasApp(root)
    root.mainloop()