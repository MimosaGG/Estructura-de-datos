class MemoriaDinamica():
    def __init__(self):
        self.Canasta = []
    
    def añadirFruta(self,agregar):
        self.Canasta.append(agregar)
        print(self.Canasta)
    
    def RemoverFruta(self,fruta):
        remover = self.Canasta.pop(0)
        remover = self.Canasta.pop(1)
        print(self.Canasta)

verduleria = MemoriaDinamica()

verduleria.añadirFruta("manzana")
verduleria.añadirFruta("banana")
verduleria.añadirFruta("mango")
verduleria.añadirFruta("uvas")
print("Canasta actual.")
verduleria.RemoverFruta("manzana")

print("Añadiendo una fruta nueva a la canasta.")
verduleria.añadirFruta("sandia")
