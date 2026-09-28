def calcular_auditoria_legal(nivel_complejidad, contratos_base):

    if nivel_complejidad == 0:
        return contratos_base + 1
    

    elif nivel_complejidad > 0 and contratos_base == 0:
        return calcular_auditoria_legal(nivel_complejidad - 1, 1)

    else:
        return calcular_auditoria_legal(
            nivel_complejidad - 1, 
            calcular_auditoria_legal(nivel_complejidad, contratos_base - 1)
        )


nivel_filial = 2
num_contratos = 400

factor_riesgo = calcular_auditoria_legal(nivel_filial, num_contratos)
print(f"Factor de riesgo/complejidad calculado para la filial (Nivel {nivel_filial}, {num_contratos} contratos): {factor_riesgo}")
