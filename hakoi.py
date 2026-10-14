import time

n = 5
src = 'A'
des = 'B'
aux = 'C'

contador_movimientos = 0

def mover_discos(n, src, des, aux):
    global contador_movimientos
    if n == 1:
        contador_movimientos += 1
        print(f"[{contador_movimientos}] Mover disco 1 de {src} a {des}")
        return
    
    mover_discos(n - 1, src, aux, des)
    
    contador_movimientos += 1
    print(f"[{contador_movimientos}] Mover disco {n} de {src} a {des}")
    
    mover_discos(n - 1, aux, des, src)


inicio = time.time()
mover_discos(n, src, des, aux)
fin = time.time()


print(f"Total de movimientos realizados: {contador_movimientos}")

print(f"Tiempo de ejecución: {fin - inicio:.6f} segundos")
