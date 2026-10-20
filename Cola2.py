class Cola:
    def __init__(self):
        self.items = []

    def es_vacia(self):
        return len(self.items) == 0

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.es_vacia():
            return self.items.pop(0)
        return None

def simular_sistema_seguros():
    colas_servicios = {}
    contadores_turnos = {}

    print("=== Sistema de Colas - Compañía de Seguros ===")
    print("Comandos:")
    print("  C<num> -> Registrar llegada de cliente (Ej: C1 para servicio 1)")
    print("  A<num> -> Atender siguiente cliente (Ej: A1 para servicio 1)")
    print("  SALIR  -> Salir del programa\n")

    while True:
        entrada = input("Ingrese comando: ").strip()
        
        if entrada.upper() == "SALIR":
            print("Saliendo del sistema...")
            break
            
        if len(entrada) < 2:
            print("Formato inválido. Use la letra del comando seguida del número (Ej: C1, A2).")
            continue
            
        comando = entrada[0].upper()
        parte_servicio = entrada[1:].strip()
        
        if not parte_servicio.isdigit():
            print("Error: El servicio especificado debe ser un número entero.")
            continue
            
        servicio = int(parte_servicio)
        
       
        if servicio not in colas_servicios:
            colas_servicios[servicio] = Cola()
            contadores_turnos[servicio] = 0
            
        if comando == 'C':
         
            contadores_turnos[servicio] += 1
            num_atencion = contadores_turnos[servicio]
            colas_servicios[servicio].encolar(num_atencion)
            print(f"-> [Llegada] Cliente asignado al Servicio {servicio}. Su número de atención es: {num_atencion}")
            
        elif comando == 'A':
            # Atender a un cliente de la cola elegida
            if colas_servicios[servicio].es_vacia():
                print(f"-> [Atención] No hay clientes en espera para el servicio {servicio}.")
            else:
                cliente_llamado = colas_servicios[servicio].desencolar()
                print(f"-> [ATENCIÓN] Llamando al cliente número: {cliente_llamado} (Servicio {servicio})")
        else:
            print("Error: Comando no reconocido. Use 'C' para llegada o 'A' para atención.")

# Ejecutar la simulación
if __name__ == "__main__":
    simular_sistema_seguros()