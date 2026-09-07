import random
import statistics


numeros = [random.randint(100, 500) for _ in range(50)]


media = statistics.mean(numeros)

try:
    moda = statistics.mode(numeros)
except statistics.StatisticsError:
    
    moda = statistics.multimode(numeros)

varianza = statistics.variance(numeros)
desv_est = statistics.stdev(numeros)


print(f"Números generados: {numeros}")
print(f"Media: {media:.2f}")
print(f"Moda: {moda}")
print(f"Varianza (muestral): {varianza:.2f}")
print(f"Desviación estándar (muestral): {desv_est:.2f}")
