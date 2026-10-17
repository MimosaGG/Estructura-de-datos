def evaluar_posfija(expresion):
    pila = []
   
    tokens = expresion.split()
    
    for token in tokens:
        
        if token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()):
            pila.append(float(token))
        else:
            
            if len(pila) < 2:
                raise ValueError("Expresión posfija mal formada.")
            
            b = pila.pop()
            a = pila.pop()
            
            if token == '+':
                pila.append(a + b)
            elif token == '-':
                pila.append(a - b)
            elif token == '*':
                pila.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Error: División por cero.")
                pila.append(a / b)
            elif token == '^':
                pila.append(a ** b)
            else:
                raise ValueError(f"Operador desconocido: {token}")
                
    if len(pila) != 1:
        raise ValueError("Expresión posfija mal formada.")
        
    return pila[0]


expresion_ejemplo = "5 4 5 + 4 + +"
resultado = evaluar_posfija(expresion_ejemplo)
print(f"El resultado de la expresión posfija '{expresion_ejemplo}' es: {resultado}")
