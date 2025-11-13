# Models/Cliente.py
"""
Modelo da entidade Cliente.
Representa um cliente do restaurante com seus dados pessoais.
"""

class Cliente:
    """
    Classe que modela um Cliente do sistema.
    
    Atributos:
        _id_cliente: Identificador único do cliente (chave primária)
        _cpf: CPF do cliente
        _nome: Nome completo do cliente
        _telefone: Telefone de contato
    """
    
    def __init__(self, id_cliente, cpf, nome, telefone):
        """Inicializa um novo cliente com seus dados."""
        self._id_cliente = id_cliente
        self._cpf = cpf
        self._nome = nome
        self._telefone = telefone

    # ===== GETTERS (Métodos para obter valores) =====
    def get_id_cliente(self):
        """Retorna o ID único do cliente."""
        return self._id_cliente

    def get_cpf(self):
        """Retorna o CPF do cliente."""
        return self._cpf

    def get_nome(self):
        """Retorna o nome do cliente."""
        return self._nome

    def get_telefone(self):
        """Retorna o telefone do cliente."""
        return self._telefone

    # ===== SETTERS (Métodos para atribuir/modificar valores) =====
    def set_id_cliente(self, id_cliente):
        """Define um novo ID para o cliente."""
        self._id_cliente = id_cliente

    def set_cpf(self, cpf):
        """Define um novo CPF para o cliente."""
        self._cpf = cpf

    def set_nome(self, nome):
        """Define um novo nome para o cliente."""
        self._nome = nome

    def set_telefone(self, telefone):
        """Define um novo telefone para o cliente."""
        self._telefone = telefone