import random

class Lista():
    def __init__(self):
        
        self.meses = ["Enero","Febrero","marzo","abril","mayo","junio","julio",
                      "agosto","septiembre","octubre","noviembre","diciembre"]
        
        self.departamentos = ["Deportes","Ropa","jugueteria"]
        
        self.matriz = [[random.randint(27,1500)  for _ in range(3)] for _ in range (12)]
    
    def mostrar_tabla(self):
        
        print(f"{'Mes':<12} | " + " | ".join(f"{dep:<12}" for dep in self.departamentos))
        print("-" * 55)
        for i, mes in enumerate(self.meses):
            fila = " | ".join(f"{val:<12}" for val in self.matriz[i])
            print(f"{mes:<12} | {fila}")
        print("-" * 55)
    
    def insertar_venta(self, mes_identificador, dep_identificador, valor):
       
        if 0 <= mes_identificador < 12 and 0 <= dep_identificador < 3:
            self.matriz[mes_identificador][dep_identificador] = valor
            print(f"Venta actualizada: {self.meses[mes_identificador]} - {self.departamentos[dep_identificador]} = {valor}")
        else:
            print("Índice de mes o departamento fuera de rango.")

    def buscar_venta(self, valor):
       
        encontrado = False
        for i in range(12):
            for j in range(3):
                if self.matriz[i][j] == valor:
                    print(f"El valor {valor} está en el mes de {self.meses[i]}, departamento {self.departamentos[j]}.")
                    encontrado = True
        if not encontrado:
            print(f"El valor {valor} no se encuentra registrado en la matriz.")

    def eliminar_venta(self, mes_idx, dep_idx):
        
        if 0 <= mes_idx < 12 and 0 <= dep_idx < 3:
            anterior = self.matriz[mes_idx][dep_idx]
            self.matriz[mes_idx][dep_idx] = 0
            print(f"Eliminado la venta de {self.meses[mes_idx]} en {self.departamentos[dep_idx]} (valor anterior: {anterior}).")
        else:
            print("No se encuentra en el rango papu")


sistema = Lista()
sistema.mostrar_tabla()

print("\nBúsqueda")
sistema.buscar_venta(504) 

print("\ninsertar")
sistema.insertar_venta(0,1,480)

print("\nEliminacion")
sistema.eliminar_venta(0, 1)
