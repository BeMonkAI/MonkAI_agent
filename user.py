class User:
    """
      Class that represents a user.
    """
    def __init__(self, name, email=None, telephone=None, id=None):
        """
        Initializes a new instance of the User class.

        
        """
    
        self.name = name
        """
        name of the user.

        """
        self.email = email
        """
        e-mail of the user.

        """
        self.telephone = telephone
        """
        telephone number of the user. 
        """
        self.id = id

    def validacao(self):
        """
        Checks if the user has at least an email or a phone number.

        Returns:
            bool: True if the user has at least an email or a phone number, otherwise False.
        """
        return bool(self.email or self.telephone)

# Exemplo de uso
if __name__ == "__main__":
    """
    Usage example. Checks if users are valid.

    Creates three instances of the User class with different combinations of attributes and prints the validation result for each user.
    """
    user1 = User(name="Johan", email="joao@example.com")
    user2 = User(name="Maria", telephone="123456789")
    user3 = User(name="Pedro")

    print(user1.validacao())  # True
    print(user2.validacao())  # True
    print(user3.validacao())  # False