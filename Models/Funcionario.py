# Models/Funcionario.py
"""
Modelo da entidade Funcionário.
Representa um funcionário do restaurante que atende os clientes.
"""

class Funcionario:
    """
    Classe que modela um Funcionário do sistema.
    
    Atributos:
        _id_funcionario: Identificador único do funcionário (chave primária)
        _cpf: CPF do funcionário
        _nome: Nome completo do funcionário
    """
    
    def __init__(self, id_funcionario, cpf, nome):
        """Inicializa um novo funcionário com seus dados."""
        self._id_funcionario = id_funcionario
        self._cpf = cpf
        self._nome = nome

    # ===== GETTERS (Métodos para obter valores) =====
    def get_id_funcionario(self):
        """Retorna o ID único do funcionário."""
        return self._id_funcionario

    def get_cpf(self):
        """Retorna o CPF do funcionário."""
        return self._cpf

    def get_nome(self):
        """Retorna o nome do funcionário."""
        return self._nome

    # ===== SETTERS (Métodos para atribuir/modificar valores) =====
    def set_id_funcionario(self, id_funcionario):
        """Define um novo ID para o funcionário."""
        self._id_funcionario = id_funcionario

    def set_cpf(self, cpf):
        """Define um novo CPF para o funcionário."""
        self._cpf = cpf

    def set_nome(self, nome):
        """Define um novo nome para o funcionário."""
        self._nome = nome