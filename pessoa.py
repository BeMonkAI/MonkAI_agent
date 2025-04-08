class Pessoa:
    """
    Classe que representa uma pessoa.

    Atributos:
        nome (str): Nome da pessoa.
        idade (int): Idade da pessoa.
        sexo (str): Sexo da pessoa.
    """
    
    def __init__(self, nome, idade, sexo):
        """
        Construtor da classe Pessoa.

        Args:
            nome (str): Nome da pessoa.
            idade (int): Idade da pessoa.
            sexo (str): Sexo da pessoa.
        """
        self.nome = nome
        self.idade = idade
        self.sexo = sexo

    def __str__(self):
        """
        Método para retornar uma representação em string do objeto.

        Returns:
            str: Representação em string do objeto Pessoa.
        """
        return f'Pessoa(nome={self.nome}, idade={self.idade}, sexo={self.sexo})'
