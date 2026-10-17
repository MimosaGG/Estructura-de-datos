class Pila:
    def __init__(self):
        self.elementos = []

    def esta_vacia(self):
        return len(self.elementos) == 0

    def apilar(self, item):
        self.elementos.append(item)

    def desapilar(self):
        if self.esta_vacia():
            return None
        return self.elementos.pop()

    def cima(self):
        if self.esta_vacia():
            return None
        return self.elementos[-1]


class NavegadorWeb:
    def __init__(self):
        self.historial_atras = Pila()
        self.historial_adelante = Pila()
        self.pagina_actual = None

    def visitar_pagina(self, url):
        """Visita una nueva página web."""
        if self.pagina_actual:
            self.historial_atras.apilar(self.pagina_actual)
        
        self.pagina_actual = url
        self.historial_adelante = Pila()
        print(f"-> Navegando a: {url}")

    def atras(self):
        """Simula el botón 'Atrás' del navegador."""
        if self.historial_atras.esta_vacia():
            print("-> No hay páginas anteriores en el historial.")
            return
        self.historial_adelante.apilar(self.pagina_actual)
        self.pagina_actual = self.historial_atras.desapilar()
        print(f"-> Retrocediendo a: {self.pagina_actual}")

    def adelante(self):
        
        if self.historial_adelante.esta_vacia():
            print("-> No hay páginas siguientes en el historial.")
            return
        self.historial_atras.apilar(self.pagina_actual)
        
        self.pagina_actual = self.historial_adelante.desapilar()
        print(f"-> Avanzando a: {self.pagina_actual}")

    def mostrar_estado(self):
        print(f"   [Página Actual]: {self.pagina_actual}")



navegador = NavegadorWeb()

navegador.visitar_pagina("google.com")
navegador.visitar_pagina("github.com")
navegador.visitar_pagina("stackoverflow.com")

navegador.mostrar_estado()

print("Acciones de Navegación")
navegador.atras()      
navegador.atras()      
navegador.adelante()   
navegador.visitar_pagina("python.org") 
navegador.mostrar_estado()
