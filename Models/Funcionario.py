# Models/Funcionario.py
class Funcionario:
    def __init__(self, id_funcionario, cpf, nome):
        self._id_funcionario = id_funcionario
        self._cpf = cpf
        self._nome = nome

    # Getters
    def get_id_funcionario(self):
        return self._id_funcionario

    def get_cpf(self):
        return self._cpf

    def get_nome(self):
        return self._nome

    # Setters
    def set_id_funcionario(self, id_funcionario):
        self._id_funcionario = id_funcionario

    def set_cpf(self, cpf):
        self._cpf = cpf

    def set_nome(self, nome):
        self._nome = nome