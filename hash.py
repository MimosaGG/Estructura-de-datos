class persona: 
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
    
    def __eq__(self, other):
        return self.nombre == other.nombre and self.edad == other.edad
    
    def __hash__(self):
        return hash((self.nombre, self.edad))

persona1 = persona("juan",20)
persona2 = persona("Emiliano",19)

print(persona1 == persona2)

print(hash(persona1))
print(hash(persona2))