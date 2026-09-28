def generar_fibonacci(n):

    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    
    secuencia = [0, 1]
    
    while len(secuencia) < n:
        
        siguiente = secuencia[-1] + secuencia[-2]
        secuencia.append(siguiente)
        
    return secuencia


print(generar_fibonacci(10))
