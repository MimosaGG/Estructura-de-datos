class Cola:
    def __init__(self):
        self.items = []
    
    def es_vacia(self):
        return len(self.items) == 0
    
    def encolar(self,item):
        self.items.append(item)
    
    def desencolar(self):
        if not self.es_vacia():
            return self.items.pop(0)
        return None

def llamada(cola_a, cola_b):
    cola_resultado = Cola()
    aux_a  = Cola()
    aux_b = Cola()
    while not cola_a.es_vacia() and not cola_b.es_vacia():
        val_a = cola_a.desencolar()
        val_b = cola_b.desencolar()

        suma = val_a + val_b
        cola_resultado.encolar(suma)
            
        aux_a.encolar(val_a)
        aux_b.encolar(val_b)
        
    while not aux_a.es_vacia():
        cola_a.encolar(aux_a.desencolar())
    while not aux_b.es_vacia():
        cola_b.encolar(aux_b.desencolar())
        
    return cola_resultado

cola_1 = Cola()
for i in [3,4,5,6,7,3,2]:
    cola_1.encolar(i)

cola_2 = Cola()
for i in [6,7,8,4,2,5,9]:
    cola_2.encolar(i)

cola_resultado = llamada(cola_1, cola_2)

print("Elementos resultados Cola:")
while not cola_resultado.es_vacia():
    print(cola_resultado.desencolar())
