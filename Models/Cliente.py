# Models/Cliente.py
class Cliente:
    def __init__(self, id_cliente, cpf, nome, telefone):
        self._id_cliente = id_cliente
        self._cpf = cpf
        self._nome = nome
        self._telefone = telefone

    # Getters
    def get_id_cliente(self):
        return self._id_cliente

    def get_cpf(self):
        return self._cpf

    def get_nome(self):
        return self._nome

    def get_telefone(self):
        return self._telefone

    # Setters
    def set_id_cliente(self, id_cliente):
        self._id_cliente = id_cliente

    def set_cpf(self, cpf):
        self._cpf = cpf

    def set_nome(self, nome):
        self._nome = nome

    def set_telefone(self, telefone):
        self._telefone = telefone