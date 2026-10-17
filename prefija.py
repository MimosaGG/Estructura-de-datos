def evaluar_prefija(expresion):
    pila = []
   
    tokens = expresion.split()
    
   
    for token in reversed(tokens):
       
        if token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()):
            pila.append(float(token))
        else:
            
            if len(pila) < 2:
                raise ValueError("Expresión mal formada.")
            

            a = pila.pop()
            b = pila.pop()
            
            if token == '+':
                pila.append(a + b)
            elif token == '-':
                pila.append(a - b)
            elif token == '*':
                pila.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("División por cero.")
                pila.append(a / b)
            elif token == '^':
                pila.append(a ** b)
            else:
                raise ValueError(f"Operador desconocido: {token}")
                
    if len(pila) != 1:
        raise ValueError("Expresión mal formada.")
        
    return pila[0]


expresion_ejemplo = "- + 5 * + 1 2 4 3"
resultado = evaluar_prefija(expresion_ejemplo)
print(f"El resultado de la expresión prefija '{expresion_ejemplo}' es: {resultado}")
