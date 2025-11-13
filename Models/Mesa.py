# Models/Mesa.py
"""
Modelo da entidade Mesa.
Representa uma mesa do restaurante com suas informações.
Status possíveis: 'livre' (disponível), 'ocupada' (com cliente), 'reservada' (pré-agendada).
"""

class Mesa:
    """
    Classe que modela uma Mesa do sistema.
    
    Atributos:
        _id_mesa: Identificador único da mesa (chave primária)
        _status: Situação atual da mesa (livre, ocupada ou reservada)
        _capacidade: Número máximo de assentos da mesa
    """
    
    def __init__(self, id_mesa, status, capacidade):
        """Inicializa uma nova mesa com seus dados."""
        self._id_mesa = id_mesa
        self._status = status
        self._capacidade = capacidade

    # ===== GETTERS (Métodos para obter valores) =====
    def get_id_mesa(self):
        """Retorna o ID único da mesa."""
        return self._id_mesa

    def get_status(self):
        """Retorna o status atual da mesa (livre/ocupada/reservada)."""
        return self._status

    def get_capacidade(self):
        """Retorna a capacidade (número de assentos) da mesa."""
        return self._capacidade

    # ===== SETTERS (Métodos para atribuir/modificar valores) =====
    def set_id_mesa(self, id_mesa):
        """Define um novo ID para a mesa."""
        self._id_mesa = id_mesa

    def set_status(self, status):
        """
        Define um novo status para a mesa.
        Valores válidos: 'livre', 'ocupada', 'reservada'
        Lança ValueError se o status for inválido.
        """
        if status not in ['livre', 'ocupada', 'reservada']:
            raise ValueError("Status inválido")
        self._status = status

    def set_capacidade(self, capacidade):
        """Define uma nova capacidade (número de assentos) para a mesa."""
        self._capacidade = capacidade