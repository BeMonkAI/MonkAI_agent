class Persona:
    """
    Clase que representa una persona con las propiedades de nombre, edad y sexo.
    """

    def __init__(self, nombre: str, edad: int, sexo: str):
        """
        Inicializa una nueva instancia de la clase Persona.

        :param nombre: Nombre de la persona.
        :param edad: Edad de la persona.
        :param sexo: Sexo de la persona.
        """
        self.nombre = nombre
        self.edad = edad
        self.sexo = sexo

    def __str__(self):
        """
        Devuelve una representación en cadena de la persona.
        """
        return f'Nombre: {self.nombre}, Edad: {self.edad}, Sexo: {self.sexo}'